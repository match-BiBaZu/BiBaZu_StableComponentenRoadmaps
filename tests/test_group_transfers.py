from copy import deepcopy
from types import SimpleNamespace

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as R
import trimesh

from bibazu_stable_roadmaps.consumer_export import attach_consumer_export
from bibazu_stable_roadmaps.group_transfers import (
    augment_groups, endpoint_errors, preferred_group_routes,
)


def action(key, source, target, *, cardinal=True, angle=90, composite=False):
    return dict(edge_id=key, source=source, target=target, cartesian_preferred=cardinal,
                is_composite=composite, actuation_count=1, total_absolute_angle_deg=angle,
                settling_required=False)


def test_different_intermediate_members_compose_without_extra_motion():
    edges = [dict(action('ab', 0, 1), source_member_ids=['a'], possible_target_member_ids=['b1']),
             dict(action('bc', 1, 2), source_member_ids=['b2'], possible_target_member_ids=['c'])]
    route = next(r for r in preferred_group_routes([0, 1, 2], edges) if r['source'] == 0 and r['target'] == 2)
    assert route['component_edge_ids'] == ['ab', 'bc']


def test_entirely_cartesian_route_wins_over_shorter_arbitrary_and_composite():
    edges = [action('a',0,1),action('b',1,2),action('c',2,3),
             action('short',0,3,cardinal=False,angle=20),
             action('composite',0,3,cardinal=False,composite=True)]
    route = next(r for r in preferred_group_routes(range(4), edges) if r['source']==0 and r['target']==3)
    assert route['component_edge_ids']==['a','b','c']
    assert not any(r['source']==3 and r['target']==0 for r in preferred_group_routes(range(4),edges))


def test_parallel_actions_and_disconnected_inputs_are_deterministic():
    edges=[action('z',0,1),action('a',0,1)]
    assert preferred_group_routes([0,1,2],edges)==preferred_group_routes([2,1,0],edges[::-1])
    assert preferred_group_routes([0,1,2],edges)[0]['component_edge_ids']==['a']
    assert not any(r['target']==2 for r in preferred_group_routes([0,1,2],edges))


def test_endpoint_symmetry_signs_and_continuous_axis_reversal():
    sym=R.from_rotvec([[0,0,0],[np.pi,0,0]])
    end=R.from_rotvec([[np.pi,0,0]])
    assert endpoint_errors(end,R.identity(),sym)[0] < 1e-6
    assert endpoint_errors(end,R.identity(),sym,[0,0,1])[0] < 1e-6
    assert endpoint_errors(R.from_quat(-end.as_quat()),R.identity(),sym)[0] < 1e-6


def fixture():
    states=[dict(member_id=key,group_id=group,retained=True,observed_count=1,
                 quaternion_xyzw=R.from_euler('x',angle,degrees=True).as_quat().tolist())
            for key,group,angle in [('a',0,0),('b',1,90),('c',1,180)]]
    nodes=[dict(node_id=group,kind='robust',source_pose_ids=[key],
                representative_quaternion_xyzw=states[index]['quaternion_xyzw'])
           for group,key,index in [(0,'a',0),(1,'b',1)]]
    document=dict(nodes=nodes,edges=[],alpha_deg=45,beta_deg=0,member_states=states,
                  member_transfers=[],member_routes=[],connectivity={})
    return SimpleNamespace(workpiece='Test'),SimpleNamespace(document=document,mesh=trimesh.creation.box())


def test_fresh_group_generation_exports_union_routes_and_retains_rare_members(source_folder, tmp_path):
    import json
    import yaml
    from bibazu_stable_roadmaps.generate import GenerationConfig, generate_one

    path = source_folder / 'poses.json'
    original = json.loads(path.read_text(encoding='utf-8'))
    (source_folder/'original_observations.json').write_text(json.dumps(original),encoding='utf-8')
    grouped = deepcopy(original)
    rare = grouped['poses'].pop()
    for row in grouped['poses']:
        row['group_members'] = [row['id']]
    grouped['poses'][0]['group_members'].append(rare['id'])
    path.write_text(json.dumps(grouped),encoding='utf-8')
    status,result = generate_one(path,GenerationConfig(str(tmp_path/'output'),
        outputs=('json','yaml','graphml'),estimate_capture_intervals=False))
    assert status == 'completed'
    from pathlib import Path
    folder = Path(result['folder'])
    document = json.loads((folder/'Test1_roadmap.json').read_text(encoding='utf-8'))
    handover = yaml.safe_load((folder/'Test1_roadmap.yaml').read_text(encoding='utf-8'))
    assert document['consumer_export']['version']==2
    assert next(s for s in document['member_states'] if s['member_id']==rare['id'])['retained']
    assert document['connectivity']['groups']['cartesian']['strongly_connected']
    assert all(not t['is_composite'] for t in document['group_transfers'])
    assert document['group_routes']==handover['group_routes']
    assert 'Ordered group reachability:' in (folder/'README.md').read_text(encoding='utf-8')


def test_exact_commands_all_axes_witness_dedup_and_immutable_nodes(monkeypatch):
    import bibazu_stable_roadmaps.group_transfers as module
    monkeypatch.setattr(module,'_symmetry',lambda source:(R.from_quat([[0,0,0,1]]),None,'C1'))
    source,built=fixture();original=deepcopy(built.document['nodes'])
    augment_groups(source,built,include_fallback=False)
    assert built.document['nodes']==original and built.document['edges']==[]
    transfers=built.document['group_transfers']
    assert any(t['commands'][0]['axis']=='x' and t['commands'][0]['signed_angle_deg']==90 for t in transfers)
    assert all(abs(t['commands'][0]['signed_angle_deg']) in (90,180) for t in transfers)
    assert len({t['edge_id'] for t in transfers})==len(transfers)
    first=[(t['edge_id'],t['source_group_key']) for t in transfers]
    for s in built.document['member_states']:
        s['quaternion_xyzw']=(-np.asarray(s['quaternion_xyzw'])).tolist()
    augment_groups(source,built,include_fallback=False)
    assert [(t['edge_id'],t['source_group_key']) for t in built.document['group_transfers']]==first
    attach_consumer_export(built.document)
    section=built.document['consumer_export']
    assert section['version']==2
    assert all(r['group_semantics'] for r in section['execution_routes'])
    assert all('required_source_group_key' in step for r in section['execution_routes'] for step in r['steps'])
    before=deepcopy(section);attach_consumer_export(built.document)
    assert before==built.document['consumer_export']


@pytest.mark.parametrize('error,accepted',[(.999,True),(1.001,False)])
def test_observed_endpoint_tolerance_is_not_command_rounding(error,accepted):
    target=R.from_euler('z',90+error,degrees=True)
    exact=R.from_quat([R.from_euler('z',90,degrees=True).as_quat()])
    measured=endpoint_errors(exact,target,R.from_quat([[0,0,0,1]]))[0]
    assert (measured <= 1) == accepted
    assert measured == pytest.approx(error)


def test_excluded_competing_destination_does_not_remove_group_candidate(monkeypatch):
    import bibazu_stable_roadmaps.group_transfers as module
    monkeypatch.setattr(module,'_symmetry',lambda source:(R.from_quat([[0,0,0,1]]),None,'C1'))
    source,built=fixture()
    built.document['member_states'].append(dict(built.document['member_states'][1],
        member_id='excluded',group_id=None,retained=False))
    augment_groups(source,built,include_fallback=False)
    assert any(not outcome['retained'] for t in built.document['group_transfers']
               for w in t['witnesses'] for outcome in w.get('possible_outcomes',[]))
    assert all(t['source'] is not None and t['target'] is not None for t in built.document['group_transfers'])


def test_composite_fallback_connects_remaining_group_gaps(monkeypatch):
    import bibazu_stable_roadmaps.group_transfers as module
    monkeypatch.setattr(module,'_symmetry',lambda source:(R.from_quat([[0,0,0,1]]),None,'C1'))
    class NoSettling:
        def __init__(self,*args): pass
        def downhill(self,endpoints,*args):
            return np.zeros(len(endpoints),dtype=bool),np.zeros((len(endpoints),3)),endpoints
    monkeypatch.setattr(module,'SeatedEnergy',NoSettling)
    source,built=fixture()
    built.document['member_states']=built.document['member_states'][:2]
    built.document['member_states'][1]['quaternion_xyzw']=R.from_euler('xyz',[13,27,41],degrees=True).as_quat().tolist()
    augment_groups(source,built)
    assert built.document['connectivity']['groups']['all_candidates']['reachable_pair_count']==2
    assert all(t['is_composite'] for t in built.document['group_transfers'])
    assert all(w['endpoint_error_deg']<1e-6 for t in built.document['group_transfers'] for w in t['witnesses'])
