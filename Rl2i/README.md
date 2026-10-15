# Rl2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rl2i_0007 | 27.18% | 2718 |
| 1 | Rl2i_0001 | 24.5% | 2450 |
| 2 | Rl2i_0006 | 22.65% | 2265 |
| 3 | Rl2i_0002 | 21.57% | 2157 |
| 4 | Rl2i_0005 | 1.71% | 171 |
| 5 | Rl2i_0008 | 1.62% | 162 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl2i_roadmap.graphml](Rl2i_roadmap.graphml), [Rl2i_roadmap.json](Rl2i_roadmap.json), [Rl2i_roadmap.png](Rl2i_roadmap.png), [Rl2i_roadmap.svg](Rl2i_roadmap.svg), [Rl2i_roadmap.yaml](Rl2i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **30/30** ordered group pairs; all candidate routes reach **30/30**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
