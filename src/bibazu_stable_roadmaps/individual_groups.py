"""Individual observations with group-wide actions; no internal motion or bridges."""
from copy import deepcopy
from dataclasses import replace
import json

from scipy.spatial.transform import Rotation

from .consumer_export import build_group_consumer_export
from .group_transfers import augment_groups, identity
from .inputs import ObservedPose, read_json
from .member_transfers import load_members
from .roadmap import build_roadmap


def individualize(source, built, cutoff, progress=lambda message: None):
    """Filter witnesses before generating actions, preserving historical group keys."""
    document = built.document
    observations = read_json(source.path.with_name('original_observations.json'))
    rows = {str(p['id']): p for p in observations['poses']}
    denominator = observations.get('completed_trials') or sum(p['count'] for p in rows.values())
    states = deepcopy(document.get('member_states') or load_members(source, document))
    previous_keys = document.get('group_keys', {})
    original_nodes = deepcopy(document['nodes'])
    groups = []
    eligible = set()
    for node in original_nodes:
        number = node['node_id']
        members = [s for s in states if s['group_id'] == number and s['retained']]
        key = previous_keys.get(str(number)) or f'{source.workpiece}:group:{number}:' + identity([
            (s['member_id'], [round(float(v), 12)+0.0 for v in
                Rotation.from_quat(s['quaternion_xyzw']).as_quat(canonical=True)])
            for s in sorted(members, key=lambda s:s['member_id'])])
        passing = [s['member_id'] for s in members
                   if 100*rows[s['member_id']]['count']/denominator >= cutoff]
        if node['observed_frequency_percent'] + 1e-12 < cutoff or not passing:
            continue
        eligible.update(passing)
        groups.append(dict(group_id=number, group_key=key,
            observed_count=node['observed_count'], observed_frequency_percent=node['observed_frequency_percent'],
            original_member_ids=sorted(s['member_id'] for s in members), planning_member_ids=sorted(passing)))
    ordered = sorted(eligible, key=lambda k:(-rows[k]['count'], k))
    pose_ids = {k:i for i,k in enumerate(ordered)}
    group_for_member = {k:g for g in groups for k in g['planning_member_ids']}
    for group in groups:
        group['pose_ids'] = sorted(pose_ids[k] for k in group['planning_member_ids'])
    for state in states:
        state['retained'] = state['member_id'] in eligible
        state['observed_frequency_percent'] = 100*rows[state['member_id']]['count']/denominator
    document['member_states'] = states
    # These are inputs to group aggregation only. Excluded outcomes remain in the
    # witness records, but never supply an active endpoint or a composite bridge.
    document['composite_transfers'] = []
    document['member_transfers'] = [t for t in document.get('member_transfers', [])
        if t.get('transfer_model') != 'composite_fallback' and len(t.get('commands',[])) == 1
        and set(t['source_member_ids']).issubset(eligible)]
    augment_groups(source, built, include_fallback=False, progress=progress,
        group_key_overrides={str(g['group_id']):g['group_key'] for g in groups})
    if not ordered:
        document.update(nodes=[], edges=[], pose_groups=[], pose_to_group={}, group_transfers=[], group_routes=[])
        document['member_transfers'] = []
        document.pop('member_routes', None)
        document['consumer_export'] = consumer_export(document)
        built.numbered=[]
        built.contacts={}
        return built
    poses = tuple(ObservedPose(k, tuple(rows[k]['quaternion_xyzw']), rows[k]['count'],
        100*rows[k]['count']/denominator, i) for i,k in enumerate(ordered))
    individual = build_roadmap(replace(source, poses=poses), [(p,i) for i,p in enumerate(poses)], progress)
    for node in individual.document['nodes']:
        member = node['source_pose_ids'][0]
        group = group_for_member[member]
        node.update(group_id=group['group_id'], group_key=group['group_key'],
                    pose_key=f'{source.workpiece}:pose:{member}')
    edges = []
    for edge in individual.document['edges']:
        a,b = ordered[edge['source']], ordered[edge['target']]
        if group_for_member[a]['group_id'] == group_for_member[b]['group_id']:
            continue
        edge['edge_id'] = f'pose:{a}->{b}:{edge["actuation"]}'
        edges.append(edge)
    individual.document.update({k:document[k] for k in
        ('group_keys','group_transfers','group_routes','connectivity','member_states')})
    individual.document.update(edges=edges, pose_groups=groups,
        pose_to_group={str(pose_ids[k]):group_for_member[k]['group_key'] for k in ordered},
        member_transfers=[], member_routes=[],
        filtering=dict(minimum_frequency_percent=cutoff, denominator=denominator,
                       excluded_members=sorted(set(rows)-eligible), composite_fallbacks=False),
        catalogue_id_namespace='individual_observation_frequency',
        part_name=source.workpiece)
    group_stats=document['connectivity']['groups']
    unreachable={tuple(p) for p in group_stats['all_candidates']['unreachable_pairs']}
    same=[];motion=[];missing=[]
    for a in individual.document['nodes']:
        for b in individual.document['nodes']:
            if a['node_id'] == b['node_id']: continue
            pair=[a['node_id'],b['node_id']]
            if a['group_key'] == b['group_key']: same.append(pair)
            elif (a['group_id'],b['group_id']) in unreachable: missing.append(pair)
            else: motion.append(pair)
    individual.document['connectivity']=dict(groups=group_stats,poses=dict(
        same_group_no_motion_pairs=same,motion_reachable_pair_count=len(motion),unreachable_pairs=missing))
    for key in ('generation','classical_metadata'):
        if key in document: individual.document[key] = document[key]
    individual.document['consumer_export'] = consumer_export(individual.document)
    return individual


def consumer_export(document):
    """Version 3 explicitly binds individual numbers to group-scoped choices."""
    temporary = deepcopy(document)
    temporary['consumer_export'] = dict(calibration_choices=[], execution_routes=[])
    section = build_group_consumer_export(temporary)
    groups = {g['group_id']:g for g in document['pose_groups']}
    def endpoints(record):
        a,b = record['source'],record['target']
        record.update(source_group_id=a,target_group_id=b,
            source_group_key=groups[a]['group_key'],target_group_key=groups[b]['group_key'],
            applicable_source_pose_ids=groups[a]['pose_ids'],accepted_target_pose_ids=groups[b]['pose_ids'],
            source=groups[a]['pose_ids'][0],target=groups[b]['pose_ids'][0])
        return record
    for record in section['calibration_choices']:
        endpoints(record)
    for route in section['execution_routes']:
        endpoints(route)
        for step in route['steps']:
            endpoints(step)
    section.update(version=3, group_keys=document['pose_to_group'], pose_groups=document['pose_groups'],
        same_group_target_satisfied=True, composite_fallbacks=False, legacy_execution_routes=[])
    return section
