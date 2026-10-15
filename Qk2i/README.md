# Qk2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Qk2i_0004 | 11.88% | 1188 |
| 1 | Qk2i_0012 | 11.47% | 1147 |
| 2 | Qk2i_0011 | 11.45% | 1145 |
| 3 | Qk2i_0006 | 11.13% | 1113 |
| 4 | Qk2i_0003 | 7.12% | 712 |
| 5 | Qk2i_0015 | 7.05% | 705 |
| 6 | Qk2i_0005 | 6.72% | 672 |
| 7 | Qk2i_0009 | 6.67% | 667 |
| 8 | Qk2i_0002 | 6.44% | 644 |
| 9 | Qk2i_0001 | 6.43% | 643 |
| 10 | Qk2i_0010 | 6.22% | 622 |
| 11 | Qk2i_0014 | 5.75% | 575 |
| 12 | Qk2i_0013 | 1.25% | 125 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Qk2i_roadmap.graphml](Qk2i_roadmap.graphml), [Qk2i_roadmap.json](Qk2i_roadmap.json), [Qk2i_roadmap.png](Qk2i_roadmap.png), [Qk2i_roadmap.svg](Qk2i_roadmap.svg), [Qk2i_roadmap.yaml](Qk2i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **144/156** ordered group pairs; all candidate routes reach **156/156**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
