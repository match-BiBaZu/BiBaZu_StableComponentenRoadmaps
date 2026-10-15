import copy
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as R

from bibazu_stable_roadmaps.connectivity import augment_roadmap, composite_transfer, connectivity, preferred_routes


@pytest.mark.parametrize('target', [R.identity(), R.from_euler('x', 180, degrees=True),
                                    R.from_euler('y', 90, degrees=True), R.from_euler('z', -180, degrees=True),
                                    R.from_euler('xyz', [27, -36, 148], degrees=True)])
@pytest.mark.parametrize('sign', [1, -1])
def test_composite_commands_reconstruct_endpoint_in_chute_order(target, sign):
    source = R.from_euler('xyz', [12, 38, -92], degrees=True)
    record = composite_transfer(0, 1, sign*source.as_quat(), sign*target.as_quat(), R.from_quat([[0, 0, 0, 1]]))
    current = source
    for command in record['commands']:
        axis = np.array([0., command['axis'] == 'y', command['axis'] == 'z'])
        current = R.from_rotvec(np.deg2rad(command['signed_angle_deg'])*axis)*current
        assert np.rad2deg((current.inv()*R.from_quat(command['end_quaternion_xyzw'])).magnitude()) < 1e-6
    assert np.rad2deg((current.inv()*target).magnitude()) < 1e-6
    assert record['endpoint_error_deg'] < 1e-6
    assert record['edge_id'] == composite_transfer(0, 1, source.as_quat(), target.as_quat(), R.from_quat([[0, 0, 0, 1]]))['edge_id']


def test_identity_and_singularities_have_no_fabricated_motion():
    symmetries = R.from_quat([[0, 0, 0, 1]])
    transfer = composite_transfer(0, 1, [0, 0, 0, 1], [0, 0, 0, -1], symmetries)
    assert transfer['commands'] == []
    for axis in ('y', 'z'):
        transfer = composite_transfer(0, 1, [0, 0, 0, 1], R.from_euler(axis, 180, degrees=True).as_quat(), symmetries)
        assert transfer['actuation_count'] == 1


@pytest.mark.parametrize('part,nodes,edges,reachable,bridges', [('Qk1a', 6, 8, 6, 3), ('Dl1a', 5, 2, 2, 4)])
def test_published_workpieces_preserve_representatives_and_edges(part, nodes, edges, reachable, bridges):
    base = Path(__file__).resolve().parents[2]/'Dashas_drop_sim/experiments/grouped_pose_study/report'/part
    if not base.is_dir():
        pytest.skip('Optional published workspace fixtures')
    document = json.loads((base/f'{part}_roadmap.json').read_text())
    catalogue = json.loads((base/'representatives.json').read_text())
    before = copy.deepcopy(document)
    symmetries = R.from_quat(catalogue['recognition']['symmetry_quaternions_xyzw'])
    augment_roadmap(document, symmetries)
    assert document['nodes'] == before['nodes'] and len(document['nodes']) == nodes
    assert document['edges'] == before['edges'] and len(document['edges']) == edges
    assert document['connectivity']['direct']['reachable_pair_count'] == reachable
    assert document['connectivity']['with_candidates']['reachable_pair_count'] == nodes*(nodes-1)
    assert len(document['composite_transfers']) == bridges
    assert len(document['routes']) == nodes*(nodes-1)
    assert all(c['endpoint_error_deg'] < 1e-6 for c in document['composite_transfers'])
    again = copy.deepcopy(document)
    augment_roadmap(again, symmetries)
    assert document == again


def test_routes_prefer_existing_edges_and_support_long_directed_chains():
    edges = [dict(source=i, target=i+1, edge_id=f'a{i}', actuation_count=1, signed_angle_deg=90) for i in range(6)]
    bridge = dict(source=0, target=6, edge_id='composite:a', transition_kind='composite_candidate',
                  actuation_count=1, total_absolute_angle_deg=1)
    parallel = dict(edges[0], edge_id='z0', signed_angle_deg=100)
    routes = preferred_routes(range(7), edges + [bridge, parallel])
    route = next(r for r in routes if (r['source'], r['target']) == (0, 6))
    assert route['component_edge_ids'] == [f'a{i}' for i in range(6)]
    assert not any(r['source'] == 6 for r in routes)
    assert connectivity(range(7), edges)['reachable_pair_count'] == 21
    assert connectivity([], [])['total_pair_count'] == 0


def test_directed_component_cycle_and_single_node():
    nodes = [dict(node_id=i, representative_quaternion_xyzw=R.from_euler('x', i*23, degrees=True).as_quat().tolist()) for i in range(4)]
    document = dict(nodes=nodes, edges=[dict(source=0, target=1, edge_id='a', signed_angle_deg=23)])
    augment_roadmap(document, R.from_quat([[0, 0, 0, 1]]))
    assert document['connectivity']['with_candidates']['strongly_connected']
    single = dict(nodes=nodes[:1], edges=[])
    augment_roadmap(single, R.from_quat([[0, 0, 0, 1]]))
    assert single['composite_transfers'] == [] and single['routes'] == []
