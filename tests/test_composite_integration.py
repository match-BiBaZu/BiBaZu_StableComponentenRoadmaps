"""Real workpiece exports must agree across both independently launched consumers."""
import copy
import json
from pathlib import Path

import pytest
import yaml
from scipy.spatial.transform import Rotation

from bibazu_stable_roadmaps.connectivity import augment_roadmap
from bibazu_stable_roadmaps.consumer_export import attach_consumer_export
from bibazu_stable_roadmaps.roadmap import handover_dict


@pytest.mark.parametrize('part,total', [('Qk1a', 30), ('Dl1a', 20)])
def test_export_consumers_and_profile_only_runtime(part, total, tmp_path, monkeypatch):
    workspace = Path(__file__).resolve().parents[2]
    report = workspace/'Dashas_drop_sim/experiments/grouped_pose_study/report'/part
    consumer = workspace/'BiBaZu_Big_Boi/ReorientationControlGUI/src'
    pressure = workspace/'BiBaZu_Big_Boi/CSVSaver'
    if not all(p.is_dir() for p in (report, consumer, pressure)):
        pytest.skip('Optional workspace integration fixtures')
    monkeypatch.syspath_prepend(str(consumer))
    monkeypatch.syspath_prepend(str(pressure))
    from bibazu_reorientation.roadmap import load_pose_roadmap
    from bibazu_reorientation.config import TransitionResolver
    from bibazu_reorientation.models import PartDefinition, PoseDefinition, TransitionSpec
    from roadmap_transition_dialog import load_roadmap_document

    data = json.loads((report/f'{part}_roadmap.json').read_text())
    catalogue = json.loads((report/'representatives.json').read_text())
    original = copy.deepcopy(data)
    augment_roadmap(data, Rotation.from_quat(catalogue['recognition']['symmetry_quaternions_xyzw']))
    assert data['nodes'] == original['nodes'] and data['edges'] == original['edges']
    # The report's original relative mesh path refers to its publication checkout.
    data['source'] = str(workspace/'Dashas_drop_sim/src/dashas_drop_sim/assets/geometry/cad'/f'{part}.STL')
    attach_consumer_export(data)
    path = tmp_path/f'{part}_roadmap.json'
    path.write_text(json.dumps(data), encoding='utf-8')
    path.with_suffix('.yaml').write_text(yaml.safe_dump(handover_dict(data)), encoding='utf-8')
    roadmap = load_pose_roadmap(path)
    assert roadmap.transitions == load_pose_roadmap(path.with_suffix('.yaml')).transitions
    calibration = load_roadmap_document(path)
    poses = tuple(PoseDefinition(p.pose_id, str(p.pose_id), p.pose_id) for p in roadmap.robust_poses)
    # Parallel direct actions remain separate choices; explicitly choose one.
    selected = {}
    for edge in roadmap.profile_transitions:
        selected.setdefault((edge.from_pose, edge.to_pose), edge)
    legs = list(selected.values()) + list(roadmap.composite_transitions)
    specs = tuple(TransitionSpec(e.from_pose, e.to_pose, tmp_path/'explicit-profile.json', e.edge_id,
                                 transition_kind=e.transition_kind, evidence_status=e.evidence_status) for e in legs)
    definition = PartDefinition(2, part, tmp_path/'model.pt', poses, 0, specs, execution_routes=roadmap.execution_routes)
    checked = 0
    for a in poses:
        for b in poses:
            if a.id != b.id:
                assert TransitionResolver(definition).plan(a.id, b.id)
                assert calibration.route_options(a.id, b.id)
                checked += 1
    assert checked == total
    from dataclasses import replace
    unassigned = tuple(replace(e, pressure_profile=None) if e.evidence_status else e for e in specs)
    resolver = TransitionResolver(replace(definition, transitions=unassigned))
    unreachable = data['connectivity']['direct']['unreachable_pairs']
    for a,b in unreachable:
        with pytest.raises(ValueError, match='No path|No transition'):
            resolver.plan(a,b)
