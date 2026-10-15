# Rl4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rl4i_0004 | 14.76% | 1476 |
| 1 | Rl4i_0001 | 14.24% | 1424 |
| 2 | Rl4i_0005 | 14.04% | 1404 |
| 3 | Rl4i_0002 | 13.62% | 1362 |
| 4 | Rl4i_0012 | 10.4% | 1040 |
| 5 | Rl4i_0014 | 10.37% | 1037 |
| 6 | Rl4i_0008 | 10.27% | 1027 |
| 7 | Rl4i_0007 | 9.81% | 981 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl4i_roadmap.graphml](Rl4i_roadmap.graphml), [Rl4i_roadmap.json](Rl4i_roadmap.json), [Rl4i_roadmap.png](Rl4i_roadmap.png), [Rl4i_roadmap.svg](Rl4i_roadmap.svg), [Rl4i_roadmap.yaml](Rl4i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **56/56** ordered group pairs; all candidate routes reach **56/56**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
