"""Compile exact-source actions and finished routes to accepted target groups.

No source-member interchangeability is assumed. An uncertain intermediate
group cannot supply an exact departure pose without a new observation.
"""
from copy import deepcopy
import heapq

from .group_transfers import cartesian, command_name, identity


def compile_pose_to_group(document):
    """Replace group-shared choices with source-specific witness choices."""
    result = deepcopy(document)
    if document.get('planning_semantics') == 'pose_to_group':
        return result
    groups = {g['group_id']: g for g in result['pose_groups']}
    nodes = {n['source_pose_ids'][0]: n for n in result['nodes']}
    transfers = []
    for original in document['group_transfers']:
        if original.get('is_composite'):
            continue
        by_source = {}
        for witness in original['witnesses']:
            if (witness['source_member_id'] in nodes and witness['target_member_id'] in nodes
                    and not witness.get('is_composite') and len(witness['commands']) == 1):
                by_source.setdefault(witness['source_member_id'], []).append(witness)
        for member, witnesses in sorted(by_source.items()):
            source = nodes[member]
            target = groups[original['target']]
            if source['group_key'] == target['group_key']:
                continue
            witnesses.sort(key=lambda w: (bool(w.get('settling_segments')),
                w.get('endpoint_error_deg') or 0, w['target_member_id'], identity(w)))
            chosen = witnesses[0]
            commands = chosen['commands']
            record = dict(original,
                edge_id='pose-group:' + identity([source['pose_key'], target['group_key'], original['edge_id']]),
                prior_group_transfer_id=original['edge_id'], source_pose_specific=True,
                source=source['node_id'], target=target['pose_ids'][0],
                source_group_id=source['group_id'], target_group_id=target['group_id'],
                applicable_source_pose_ids=[source['node_id']], accepted_target_pose_ids=target['pose_ids'],
                source_member_ids=[member], witnesses=witnesses, commands=commands,
                possible_target_member_ids=sorted({w['target_member_id'] for w in witnesses}),
                preview_source_member_id=member, preview_target_member_id=chosen['target_member_id'],
                preview_segments=[dict(c, segment_kind='command') for c in commands]
                    + [dict(s, segment_kind='settling') for s in chosen.get('settling_segments', [])],
                display_name=command_name(commands), cartesian_preferred=cartesian(commands),
                settling_required=bool(chosen.get('settling_segments')), is_composite=False,
                actuation_count=1, total_absolute_angle_deg=abs(commands[0]['signed_angle_deg']),
                planning_assumption='pose_to_group: exact source pose; any qualifying target member',
                profile_requirements=dict(assigned_profile=True, explicit_source_group_calibration=True,
                    required_source_pose_ids=[source['node_id']]))
            record['preference_cost'] = [int(not record['cartesian_preferred']), 1,
                record['total_absolute_angle_deg'], int(record['settling_required'])]
            transfers.append(record)
    transfers.sort(key=lambda r: (*r['preference_cost'], r['edge_id']))
    routes = preferred_routes(result['nodes'], groups, transfers)
    choices = list(transfers)
    execution = []
    by_id = {r['edge_id']: r for r in transfers}
    for route in routes:
        legs = [by_id[key] for key in route['component_edge_ids']]
        if len(legs) > 1:
            macro = dict(legs[0], **{k: route[k] for k in ('edge_id', 'target', 'target_group_id',
                'target_group_key', 'accepted_target_pose_ids', 'preference_cost')})
            macro.update(transition_kind='group_route', component_edge_ids=route['component_edge_ids'],
                commands=[c for leg in legs for c in leg['commands']],
                preview_segments=[dict(s, leg_index=i) for i, leg in enumerate(legs) for s in leg['preview_segments']],
                witnesses=[], possible_target_member_ids=legs[-1]['possible_target_member_ids'],
                target_group_member_ids=legs[-1]['target_group_member_ids'],
                preview_target_member_id=legs[-1]['preview_target_member_id'],
                actuation_count=len(legs), total_absolute_angle_deg=sum(l['total_absolute_angle_deg'] for l in legs),
                display_name=' → '.join(l['display_name'] for l in legs),
                settling_required=any(l['settling_required'] for l in legs),
                cartesian_preferred=all(l['cartesian_preferred'] for l in legs))
            choices.append(macro)
    for choice in choices:
        legs = [by_id[k] for k in choice.get('component_edge_ids', [])] or [choice]
        execution.append(dict(route_id=choice['edge_id'] + ':profile', source=choice['source'], target=choice['target'],
            source_group_key=choice['source_group_key'], target_group_key=choice['target_group_key'],
            source_pose_specific=True, group_semantics=True,
            applicable_source_pose_ids=choice['applicable_source_pose_ids'], accepted_target_pose_ids=choice['accepted_target_pose_ids'],
            profile_edge_ids=[choice['edge_id']], steps=[step(choice)],
            priority=choice['preference_cost'] + [0], tie_breaker=choice['edge_id'], evidence_status='geometry_only'))
        if len(legs) > 1:
            execution.append(dict(execution[-1], route_id=choice['edge_id'] + ':profiles',
                profile_edge_ids=[l['edge_id'] for l in legs], steps=[step(l) for l in legs],
                priority=choice['preference_cost'] + [1]))
    result.update(planning_semantics='pose_to_group', group_transfers=[], group_routes=[],
        pose_group_transfers=transfers, pose_group_routes=routes)
    section = dict(document['consumer_export'], planning_semantics='pose_to_group',
        calibration_choices=choices, execution_routes=execution,
        route_policy='exported_only; exact observed source pose; assigned profile and source-group calibration required')
    result['consumer_export'] = section
    pairs = {(r['source'], r['target_group_id']) for r in routes}
    direct = {(r['source'], r['target_group_id']) for r in transfers}
    all_pairs = {(n['node_id'], g) for n in result['nodes'] for g in groups if g != n['group_id']}
    result['connectivity']['pose_to_group'] = dict(total_pair_count=len(all_pairs),
        direct_pair_count=len(direct), reachable_pair_count=len(pairs),
        unreachable_pairs=[list(p) for p in sorted(all_pairs - pairs)],
        same_group_target_satisfied=True,
        intermediate_policy='Continue only when the accepted arrival group contains one qualifying pose; otherwise observe the exact pose again.')
    result['connectivity']['groups']['planning_assumption'] = 'Group projection only; exact source applicability is mandatory. See pose_to_group.'
    result['connectivity']['groups']['transfer_count'] = len(transfers)
    result['connectivity']['poses'] = dict(
        same_group_no_motion_pairs=[[a['node_id'], b['node_id']] for a in result['nodes'] for b in result['nodes']
            if a['node_id'] != b['node_id'] and a['group_key'] == b['group_key']],
        motion_reachable_pair_count=sum((a['node_id'], b['group_id']) in pairs
            for a in result['nodes'] for b in result['nodes'] if a['group_key'] != b['group_key']),
        unreachable_pairs=[[a['node_id'], b['node_id']] for a in result['nodes'] for b in result['nodes']
            if a['group_key'] != b['group_key'] and (a['node_id'], b['group_id']) not in pairs])
    return result


def step(choice):
    return dict(edge_id=choice['edge_id'], source=choice['source'], target=choice['target'],
        required_source_group_key=choice['source_group_key'],
        required_source_pose_ids=choice['applicable_source_pose_ids'],
        possible_target_pose_ids=choice['accepted_target_pose_ids'])


def preferred_routes(nodes, groups, transfers):
    """Rank finished paths, never exchanging members of an intermediate group."""
    adjacency = {}
    for transfer in transfers:
        adjacency.setdefault(transfer['source'], []).append(transfer)
    output = []
    for node in sorted(nodes, key=lambda n: n['node_id']):
        source = node['node_id']
        queue = [((0, 0, 0., 0, ()), 0, source)]
        visited = set()
        reached = set()
        while queue:
            cost, kind, current = heapq.heappop(queue)
            if kind == 1:
                group_id = current
                group = groups[group_id]
                anchor = group['pose_ids'][0]
                if group_id != node['group_id'] and group_id not in reached:
                    reached.add(group_id)
                    output.append(dict(edge_id='pose-group-route:' + identity([node['pose_key'], group['group_key'], cost[-1]]),
                        source=source, target=anchor, target_group_id=group_id,
                        target_group_key=group['group_key'], accepted_target_pose_ids=group['pose_ids'],
                        component_edge_ids=list(cost[-1]), preference_cost=list(cost[:4])))
                if len(group['pose_ids']) == 1:
                    heapq.heappush(queue, (cost, 0, anchor))
                continue
            if current in visited:
                continue
            visited.add(current)
            for leg in adjacency.get(current, []):
                values = tuple(a + b for a, b in zip(cost[:4], leg['preference_cost']))
                next_cost = values + (cost[-1] + (leg['edge_id'],),)
                heapq.heappush(queue, (next_cost, 1, leg['target_group_id']))
    return sorted(output, key=lambda r: (r['source'], r['target_group_id']))
