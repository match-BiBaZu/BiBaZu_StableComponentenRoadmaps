# Rk3a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rk3a_0014 | 13.49% | 1349 |
| 1 | Rk3a_0010 | 13.1% | 1310 |
| 2 | Rk3a_0012 | 12.67% | 1267 |
| 3 | Rk3a_0004 | 12.15% | 1215 |
| 4 | Rk3a_0003 | 10.35% | 1035 |
| 5 | Rk3a_0009 | 10.27% | 1027 |
| 6 | Rk3a_0002 | 8.99% | 899 |
| 7 | Rk3a_0008 | 8.49% | 849 |
| 8 | Rk3a_0011 | 4.26% | 426 |
| 9 | Rk3a_0013 | 4.09% | 409 |
| 10 | Rk3a_0001 | 1.33% | 133 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk3a_roadmap.graphml](Rk3a_roadmap.graphml), [Rk3a_roadmap.json](Rk3a_roadmap.json), [Rk3a_roadmap.png](Rk3a_roadmap.png), [Rk3a_roadmap.svg](Rk3a_roadmap.svg), [Rk3a_roadmap.yaml](Rk3a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **110/110** ordered group pairs; all candidate routes reach **110/110**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
