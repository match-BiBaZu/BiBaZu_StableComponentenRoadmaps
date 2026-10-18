from copy import deepcopy
from dataclasses import replace
import json
import pytest

from bibazu_stable_roadmaps.inputs import load_source, select_poses
from bibazu_stable_roadmaps.roadmap import build_roadmap
from bibazu_stable_roadmaps.individual_groups import individualize
from bibazu_stable_roadmaps.generate import generate_one, GenerationConfig


def grouped(source_folder, counts=(27,20,5,4)):
    path=source_folder/'poses.json'
    original=json.loads(path.read_text(encoding='utf-8'))
    for row,count in zip(original['poses'],counts):
        row.update(count=count,frequency_percent=float(count))
    (source_folder/'original_observations.json').write_text(json.dumps(original),encoding='utf-8')
    value=deepcopy(original)
    rare=value['poses'].pop()
    for row in value['poses']:row['group_members']=[row['id']]
    value['poses'][0]['group_members'].append(rare['id'])
    value['poses'][0]['count']+=rare['count'];value['poses'][0]['frequency_percent']+=rare['frequency_percent']
    path.write_text(json.dumps(value),encoding='utf-8')
    registry_path=source_folder/'pose_registry.json'
    registry=json.loads(registry_path.read_text(encoding='utf-8'))
    registry['entries']=[e for e in registry['entries'] if e['id'] in {p['id'] for p in value['poses']}]
    registry_path.write_text(json.dumps(registry),encoding='utf-8')
    return load_source(path)


def test_individual_frequency_order_ties_cutoff_and_no_internal_actions(source_folder):
    source=grouped(source_folder,(20,27,5,4))
    numbered,_=select_poses(source,0,True)
    built=build_roadmap(source,numbered)
    for node in built.document['nodes']:
        node['group_members']=next(p['group_members'] for p in json.loads(source.path.read_text())['poses'] if p['id']==node['source_pose_ids'][0])
    result=individualize(source,built,5)
    nodes=result.document['nodes']
    assert [n['source_pose_ids'][0] for n in nodes]==['Test1_0009','Test1_0007','Test1_0003']
    assert [n['observed_frequency_percent'] for n in nodes]==[27,20,5]
    assert result.document['consumer_export']['version']==3
    assert not any(s['retained'] for s in result.document['member_states'] if s['member_id']=='Test1_0010')
    assert all(t['source']!=t['target'] and not t['is_composite'] and len(t['commands'])==1 for t in result.document['group_transfers'])
    assert all(w['source_member_id']!='Test1_0010' and w['target_member_id']!='Test1_0010'
        for t in result.document['group_transfers'] for w in t['witnesses'])


@pytest.mark.parametrize('use_registry',[False,True])
def test_empty_individual_groups_replace_stale_outputs(source_folder,tmp_path,use_registry):
    source=grouped(source_folder,(4,3,2,3))
    input_path=source.path.with_name('pose_registry.json') if use_registry else source.path
    root=tmp_path/'output'
    status,result=generate_one(input_path,GenerationConfig(str(root),minimum_frequency_percent=1,
        outputs=('json','yaml'),estimate_capture_intervals=False))
    assert status=='completed'
    assert (root/'Test1/Test1_roadmap.json').exists()
    status,result=generate_one(input_path,GenerationConfig(str(root),minimum_frequency_percent=5,
        outputs=('json','yaml'),estimate_capture_intervals=False))
    manifest=json.loads((root/'Test1/manifest.json').read_text())
    assert manifest['status']=='no_eligible_poses'
    assert manifest['pose_count']==0
    assert not (root/'Test1/Test1_roadmap.json').exists()
    assert not (root/'Test1/Test1_roadmap.yaml').exists()
    assert (root/'Test1/no_eligible_poses.json').exists()


def test_tied_individual_frequencies_use_source_id_order(source_folder):
    source=grouped(source_folder,(20,20,5,4))
    built=build_roadmap(source,select_poses(source,0,True)[0])
    rows=json.loads(source.path.read_text())['poses']
    for node in built.document['nodes']:
        node['group_members']=next(p['group_members'] for p in rows if p['id']==node['source_pose_ids'][0])
    result=individualize(source,built,5)
    assert [n['source_pose_ids'][0] for n in result.document['nodes']]==['Test1_0007','Test1_0009','Test1_0003']
