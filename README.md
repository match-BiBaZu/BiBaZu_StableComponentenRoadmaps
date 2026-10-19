# BiBaZu grouped roadmaps: source poses to destination groups

Individual observed poses are numbered from 0 by descending frequency. Groups are labelled **A, B, …, Z, AA, …** in row order. The diagrams use rows and columns, with horizontal, vertical and 45° arrow segments. Each arrow starts on a **pose border** and ends on a **destination-group border**; attachment positions vary to separate the lines. Physical rotation commands remain written on the arrows.

## Filtering and planning

All active components use **exact source pose → destination group** transitions. Each action is witnessed from its stated source pose and accepts any qualifying member of the target group. An action from another source-group member is not inherited. A target in the current group is already satisfied and requires no actuation.

The cutoff is **1%** for the original group total and each individual pose. Percentages retain the completed-trial denominator. Below-cutoff members do not supply active transfer witnesses; groups without qualifying members are omitted.

Routes use retained single-axis actions and continue automatically only through singleton arrival groups. A multi-member arrival requires another exact pose observation before a further source-specific action. Candidates rank Cartesian commands first, followed by actuation count, commanded angle, settling requirements and stable IDs. No composite bridges are generated. Missing connectivity is reported explicitly.

All candidates remain `geometry_only`. Execution requires assigned pressure profiles and explicit source qualification. Group-only recognition cannot identify an exact source member in a multi-member group.

## Exports and control integration

Each active component supplies JSON, YAML, GraphML, PNG, SVG and numeric pose sheets, together with original source snapshots, a manifest and exact-byte checksums. Consumer export v3 contains source applicability, accepted target sets, real command witnesses, previews, calibration choices and finished execution routes. The control GUIs read these exports and do not generate routes.

Changed JSON hashes require **explicit reimport**. Previous exports are retained in `history/`; former group-wide choices require fresh exact-source qualification. Numeric pose numbers never grant applicability by matching an older export. Display letters remain separate from stable group identities.

## Application

Start `StableComponentRoadmapsGUI.cmd`, or run `uv run bibazu-stable-roadmaps`. Grouped generation defaults to pose-to-group planning. For offline generation:

```json
{"settings":{"output_root":"OUTPUT_DIRECTORY","minimum_frequency_percent":1,"renumber_by_frequency":true,"include_members":true,"include_composites":false,"estimate_capture_intervals":false,"planning_semantics":"pose_to_group","outputs":["json","yaml","graphml","roadmap_png","roadmap_svg","poses_png","poses_svg"]},"sources":["SOURCE_DIRECTORY/Dk1i/poses.json"]}
```

Source inputs require matching mesh geometry, original observations and grouping evidence. The application bundles its MIT geometry primitives; see [ENGINE_PROVENANCE.json](ENGINE_PROVENANCE.json), [ENGINE_LICENSE](ENGINE_LICENSE), and [LICENSE](LICENSE). Non-grouped inputs retain their ordinary pose-to-pose exports.

## Catalogue

38 existing generated entries were processed: **37 active roadmaps** and **Kf4i with no eligible poses at 1%**. Kf1i's pre-existing no-observation entry remains unchanged. Source simulation/grouping statistics remain in [grouped_study.json](grouped_study.json); current graph statistics are in [connectivity_audit.json](connectivity_audit.json), [consumer_export_audit.json](consumer_export_audit.json) and [index.json](index.json).

| Workpiece | Individual poses | Displayed groups | Reachable pose → group pairs | Status |
|---|---:|---:|---:|---|
| [Df1a](Df1a/README.md) | 4 | 4 | 12/12 | complete |
| [Df2i](Df2i/README.md) | 6 | 6 | 30/30 | complete |
| [Df4a](Df4a/README.md) | 12 | 12 | 132/132 | complete |
| [Dk1i](Dk1i/README.md) | 8 | 6 | 40/40 | complete |
| [Dk2a](Dk2a/README.md) | 14 | 12 | 154/154 | complete |
| [Dk4i](Dk4i/README.md) | 24 | 18 | 408/408 | complete |
| [Dl1a](Dl1a/README.md) | 7 | 4 | 21/21 | complete |
| [Dl2i](Dl2i/README.md) | 9 | 6 | 45/45 | complete |
| [Dl4a](Dl4a/README.md) | 8 | 6 | 32/40 | complete |
| [Kf2a](Kf2a/README.md) | 3 | 3 | 2/6 | complete |
| [Kf4i](Kf4i/README.md) | 0 | 0 | 0/0 | no_eligible_poses |
| [Kk1a](Kk1a/README.md) | 2 | 2 | 2/2 | complete |
| [Kk2i](Kk2i/README.md) | 20 | 20 | 116/380 | complete |
| [Kk4a](Kk4a/README.md) | 4 | 4 | 2/12 | complete |
| [Kl1i](Kl1i/README.md) | 2 | 2 | 2/2 | complete |
| [Kl2a](Kl2a/README.md) | 17 | 16 | 103/255 | complete |
| [Kl4i](Kl4i/README.md) | 30 | 30 | 677/870 | complete |
| [Qf1i](Qf1i/README.md) | 4 | 4 | 12/12 | complete |
| [Qf2a](Qf2a/README.md) | 10 | 10 | 90/90 | complete |
| [Qf4i](Qf4i/README.md) | 16 | 16 | 240/240 | complete |
| [Qk1a](Qk1a/README.md) | 10 | 6 | 50/50 | complete |
| [Qk2i](Qk2i/README.md) | 13 | 13 | 144/156 | complete |
| [Qk4a](Qk4a/README.md) | 24 | 24 | 552/552 | complete |
| [Ql1i](Ql1i/README.md) | 5 | 5 | 20/20 | complete |
| [Ql2a](Ql2a/README.md) | 8 | 8 | 56/56 | complete |
| [Ql4i](Ql4i/README.md) | 12 | 12 | 132/132 | complete |
| [Rf1a](Rf1a/README.md) | 16 | 15 | 209/224 | complete |
| [Rf2i](Rf2i/README.md) | 8 | 8 | 56/56 | complete |
| [Rf3a](Rf3a/README.md) | 9 | 9 | 72/72 | complete |
| [Rf4i](Rf4i/README.md) | 16 | 16 | 240/240 | complete |
| [Rk1a](Rk1a/README.md) | 30 | 24 | 690/690 | complete |
| [Rk2i](Rk2i/README.md) | 12 | 12 | 132/132 | complete |
| [Rk3a](Rk3a/README.md) | 13 | 11 | 130/130 | complete |
| [Rk4i](Rk4i/README.md) | 24 | 24 | 552/552 | complete |
| [Rl1a](Rl1a/README.md) | 6 | 6 | 30/30 | complete |
| [Rl2i](Rl2i/README.md) | 6 | 6 | 30/30 | complete |
| [Rl3a](Rl3a/README.md) | 10 | 9 | 80/80 | complete |
| [Rl4i](Rl4i/README.md) | 8 | 8 | 56/56 | complete |

Dk1i was regenerated on 2026-10-19 from a fresh **1,000-drop** grouped run with the latest main profile (500 mm, belt 100 ± 3 mm/s, damping ratio 0.19) and latest stable main pose anchors. Pose 0 is **Dk1i_0002** at 18.8%. Exact-source pose-to-group reachability is **40/40**. Changed exports require explicit reimport and calibration review.
