from copy import deepcopy

from bibazu_stable_roadmaps.pose_to_group import compile_pose_to_group
from bibazu_stable_roadmaps.member_transfers import command


def document():
    groups = [dict(group_id=i, group_key=f'g{i}', pose_ids=ids,
        planning_member_ids=[f'p{n}' for n in ids]) for i, ids in enumerate(([0,1], [2], [3,4]))]
    nodes = [dict(node_id=n, pose_key=f'pose:{n}', source_pose_ids=[f'p{n}'],
        group_id=g['group_id'], group_key=g['group_key']) for g in groups for n in g['pose_ids']]
    records = []
    for source, target, angle in [(0,1,90), (1,2,180), (2,2,90), (3,1,90)]:
        node = next(n for n in nodes if n['node_id'] == source)
        target_member = groups[target]['planning_member_ids'][0]
        cmd = command([0,0,0,1], 'x', angle)
        records.append(dict(edge_id=f't{source}-{target}', source=node['group_id'], target=target,
            source_group_key=node['group_key'], target_group_key=f'g{target}',
            target_group_member_ids=groups[target]['planning_member_ids'],
            witnesses=[dict(source_member_id=f'p{source}', target_member_id=target_member,
                commands=[cmd], settling_segments=[], endpoint_error_deg=0)]))
    return dict(nodes=nodes, pose_groups=groups, group_transfers=records, group_routes=[],
        connectivity=dict(groups={}), consumer_export=dict(version=3))


def test_actions_use_exact_source_and_any_target_member():
    original = document()
    before = deepcopy(original)
    result = compile_pose_to_group(original)
    assert original == before
    actions = result['pose_group_transfers']
    assert {(a['source'],a['target_group_id']) for a in actions} == {(0,1),(2,2),(3,1),(1,2)}
    assert all(a['applicable_source_pose_ids'] == [a['source']] for a in actions)
    assert next(a for a in actions if a['source'] == 1)['accepted_target_pose_ids'] == [3,4]
    assert not any(a['source'] == 4 for a in actions)
    assert all(all(w['source_member_id'] == f"p{a['source']}" for w in a['witnesses']) for a in actions)
    assert not result['group_transfers'] and not result['group_routes']
    assert compile_pose_to_group(result) == result


def test_routes_never_change_an_uncertain_arrival_into_a_departure_pose():
    result = compile_pose_to_group(document())
    routes = {(r['source'],r['target_group_id']):r for r in result['pose_group_routes']}
    assert len(routes[0,2]['component_edge_ids']) == 2  # singleton intermediate pose 2
    assert (1,1) not in routes  # group 2 may contain pose 4, which has no outgoing action
    assert [1,1] in result['connectivity']['pose_to_group']['unreachable_pairs']
    assert all(not c['is_composite'] for c in result['consumer_export']['calibration_choices'])


def test_cartesian_route_wins_over_shorter_non_cartesian_action():
    source = document()
    alternative = deepcopy(source['group_transfers'][0])
    alternative.update(edge_id='short', target=2, target_group_key='g2')
    alternative['witnesses'][0].update(target_member_id='p3', commands=[command([0,0,0,1],'z',45)])
    source['group_transfers'].append(alternative)
    result = compile_pose_to_group(source)
    route = next(r for r in result['pose_group_routes'] if r['source'] == 0 and r['target_group_id'] == 2)
    assert len(route['component_edge_ids']) == 2
    assert route['preference_cost'][0] == 0
    source['group_transfers'].reverse()
    assert compile_pose_to_group(source)['pose_group_routes'] == result['pose_group_routes']


def test_generation_can_select_pose_to_group_semantics(source_folder, tmp_path):
    from test_individual_groups import grouped
    from bibazu_stable_roadmaps.generate import GenerationConfig, generate_one
    import json
    source = grouped(source_folder)
    root = tmp_path/'output'
    status, _ = generate_one(source.path, GenerationConfig(str(root), minimum_frequency_percent=1,
        outputs=('json','yaml','graphml'), estimate_capture_intervals=False, planning_semantics='pose_to_group'))
    assert status == 'completed'
    exported = json.loads((root/'Test1/Test1_roadmap.json').read_text(encoding='utf-8'))
    assert exported['consumer_export']['planning_semantics'] == 'pose_to_group'
    assert all(t['applicable_source_pose_ids'] == [t['source']] for t in exported['pose_group_transfers'])
    assert not exported['group_transfers'] and not exported['group_routes']
    import networkx as nx
    graph = nx.read_graphml(root/'Test1/Test1_roadmap.graphml')
    assert graph.number_of_edges() == len(exported['pose_group_transfers'])
    assert all(graph.nodes[b]['node_kind'] == 'accepted_target_group' for a,b in graph.edges())
