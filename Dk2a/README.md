# Dk2a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Dk2a_0006 | 16.94% | 1694 |
| 1 | Dk2a_0004 | 15.57% | 1557 |
| 2 | Dk2a_0016 | 12.96% | 1296 |
| 3 | Dk2a_0012 | 9.47% | 947 |
| 4 | Dk2a_0002 | 7.85% | 785 |
| 5 | Dk2a_0015 | 7.13% | 713 |
| 6 | Dk2a_0014 | 6.88% | 688 |
| 7 | Dk2a_0007 | 6.76% | 676 |
| 8 | Dk2a_0005 | 5.24% | 524 |
| 9 | Dk2a_0003 | 5.11% | 511 |
| 10 | Dk2a_0001 | 2.58% | 258 |
| 11 | Dk2a_0010 | 1.83% | 183 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dk2a_roadmap.graphml](Dk2a_roadmap.graphml), [Dk2a_roadmap.json](Dk2a_roadmap.json), [Dk2a_roadmap.png](Dk2a_roadmap.png), [Dk2a_roadmap.svg](Dk2a_roadmap.svg), [Dk2a_roadmap.yaml](Dk2a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **132/132** ordered group pairs; all candidate routes reach **132/132**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
