"""Orientation-only bridge candidates; no contact or actuator feasibility claim."""
from __future__ import annotations

import hashlib
import heapq
import json
import warnings

import networkx as nx
import numpy as np
from scipy.spatial.transform import Rotation


def connectivity(nodes, edges):
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from((e['source'], e['target']) for e in edges)
    components = sorted((sorted(c) for c in nx.strongly_connected_components(graph)), key=lambda c: c[0])
    unreachable = [[a, b] for a in sorted(graph) for b in sorted(graph)
                   if a != b and not nx.has_path(graph, a, b)]
    total = len(graph) * (len(graph) - 1)
    return {'strongly_connected_components': components, 'unreachable_pairs': unreachable,
            'reachable_pair_count': total - len(unreachable), 'total_pair_count': total,
            'strongly_connected': bool(graph) and len(components) == 1}


def composite_transfer(source_id, target_id, source_quat, target_quat, symmetries):
    def canonical(quat):
        return Rotation.from_quat([float(v) + 0.0 for v in Rotation.from_quat(quat).as_quat(canonical=True)])
    source, target = canonical(source_quat), canonical(target_quat)
    candidates = []
    for symmetry_index, symmetry in enumerate(symmetries):
        symmetry = canonical(symmetry.as_quat())
        terminal = target * symmetry
        delta = terminal * source.inv()
        for sequence in ('yzy', 'zyz'):
            # At a singularity scipy chooses a valid solution with the last angle zero.
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', message='Gimbal lock detected.*')
                angles = delta.as_euler(sequence, degrees=True)
            commands, current = [], source
            for axis, angle in zip(sequence, angles):
                angle = float(angle)
                if abs(angle) <= 1e-10:
                    continue
                start = current.as_quat(canonical=True).tolist()
                vector = np.array([0., axis == 'y', axis == 'z'], dtype=float)
                current = Rotation.from_rotvec(np.deg2rad(angle) * vector) * current
                commands.append({'axis': axis, 'actuation': f'free_{axis}', 'signed_angle_deg': angle,
                                 'start_quaternion_xyzw': start,
                                 'end_quaternion_xyzw': current.as_quat(canonical=True).tolist()})
            error = float(np.rad2deg((current.inv() * terminal).magnitude()))
            if error > 1e-6:
                raise ValueError('Composite transfer fails its endpoint check')
            score = (len(commands), sum(abs(c['signed_angle_deg']) for c in commands), sequence, symmetry_index)
            candidates.append((score, commands, symmetry, terminal, error))
    score, commands, symmetry, terminal, error = min(candidates, key=lambda c: c[0])
    identity = {'source': source_id, 'target': target_id,
                'commands': [[c['axis'], round(c['signed_angle_deg'], 10)] for c in commands],
                'terminal_quaternion_xyzw': [round(float(v), 10) + 0.0 for v in terminal.as_quat(canonical=True)]}
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:16]
    return {'edge_id': f'composite:{source_id}->{target_id}:{digest}', 'source': source_id, 'target': target_id,
            'directed': True, 'transition_kind': 'composite_candidate', 'evidence_status': 'geometry_only',
            'experimental_status': 'untested', 'commands': commands, 'actuation_count': len(commands),
            'total_absolute_angle_deg': score[1], 'axis_sequence': score[2], 'symmetry_index': score[3],
            'terminal_symmetry_quaternion_xyzw': symmetry.as_quat(canonical=True).tolist(),
            'terminal_quaternion_xyzw': terminal.as_quat(canonical=True).tolist(), 'endpoint_error_deg': error,
            'transient_quaternions_xyzw': [c['end_quaternion_xyzw'] for c in commands[:-1]],
            'contact_feasibility_evaluated': False, 'settling_evaluated': False}


def preferred_routes(nodes, edges):
    """Lexicographic Dijkstra: existing-only first, then rotations and angle."""
    adjacency = {n: [] for n in nodes}
    for edge in edges:
        adjacency[edge['source']].append(edge)
    routes = []
    for start in sorted(nodes):
        queue = [((0, 0, 0., ()), start, (start,))]
        best = {}
        while queue:
            cost, pose, visited = heapq.heappop(queue)
            if pose in best:
                continue
            best[pose] = cost
            if pose != start:
                routes.append({'source': start, 'target': pose, 'component_edge_ids': list(cost[3]),
                               'via_pose_ids': list(visited[1:-1]), 'composite_transfer_count': cost[0],
                               'actuation_count': cost[1], 'total_absolute_angle_deg': cost[2],
                               'evidence_status': 'geometry_only' if cost[0] else 'direct_geometric_candidates'})
            for edge in adjacency[pose]:
                target = edge['target']
                if target in visited:
                    continue
                composite = edge.get('transition_kind') == 'composite_candidate'
                rotations = edge.get('actuation_count', 1)
                angle = edge.get('total_absolute_angle_deg', abs(edge.get('signed_angle_deg') or 0.))
                new = (cost[0] + int(composite), cost[1] + rotations, cost[2] + angle,
                       cost[3] + (edge['edge_id'],))
                heapq.heappush(queue, (new, target, visited + (target,)))
    return sorted(routes, key=lambda r: (r['source'], r['target']))


def augment_roadmap(document, symmetries):
    """Add separate candidates without modifying any node or direct edge."""
    nodes = {n['node_id']: n['representative_quaternion_xyzw'] for n in document['nodes']}
    direct = connectivity(nodes, document['edges'])
    components = direct['strongly_connected_components']
    transfers = []
    if len(components) > 1:
        for index, component in enumerate(components):
            following = components[(index + 1) % len(components)]
            # Existing cross-component edges already provide this cycle segment.
            if any(e['source'] in component and e['target'] in following for e in document['edges']):
                continue
            choices = [composite_transfer(a, b, nodes[a], nodes[b], symmetries)
                       for a in component for b in following]
            transfers.append(min(choices, key=lambda c: (c['actuation_count'], c['total_absolute_angle_deg'],
                                                       c['axis_sequence'], c['symmetry_index'], c['source'], c['target'])))
    all_edges = document['edges'] + transfers
    document.update(composite_transfers=transfers, routes=preferred_routes(nodes, all_edges),
                    connectivity={'direct': direct, 'with_candidates': connectivity(nodes, all_edges),
                                  'note': 'Orientation geometry only; physical feasibility and reliability are unverified.'})
    return document
