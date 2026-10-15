# Qk4a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Qk4a_0021 | 6.39% | 639 |
| 1 | Qk4a_0019 | 6.29% | 629 |
| 2 | Qk4a_0004 | 5.92% | 592 |
| 3 | Qk4a_0014 | 5.79% | 579 |
| 4 | Qk4a_0010 | 5.71% | 571 |
| 5 | Qk4a_0006 | 5.7% | 570 |
| 6 | Qk4a_0024 | 5.68% | 568 |
| 7 | Qk4a_0007 | 5.25% | 525 |
| 8 | Qk4a_0001 | 4.03% | 403 |
| 9 | Qk4a_0017 | 3.82% | 382 |
| 10 | Qk4a_0016 | 3.65% | 365 |
| 11 | Qk4a_0002 | 3.63% | 363 |
| 12 | Qk4a_0018 | 3.59% | 359 |
| 13 | Qk4a_0020 | 3.58% | 358 |
| 14 | Qk4a_0003 | 3.52% | 352 |
| 15 | Qk4a_0013 | 3.48% | 348 |
| 16 | Qk4a_0025 | 3.44% | 344 |
| 17 | Qk4a_0022 | 3.4% | 340 |
| 18 | Qk4a_0015 | 3.24% | 324 |
| 19 | Qk4a_0009 | 3.08% | 308 |
| 20 | Qk4a_0005 | 2.85% | 285 |
| 21 | Qk4a_0023 | 2.82% | 282 |
| 22 | Qk4a_0011 | 2.56% | 256 |
| 23 | Qk4a_0012 | 2.53% | 253 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Qk4a_roadmap.graphml](Qk4a_roadmap.graphml), [Qk4a_roadmap.json](Qk4a_roadmap.json), [Qk4a_roadmap.png](Qk4a_roadmap.png), [Qk4a_roadmap.svg](Qk4a_roadmap.svg), [Qk4a_roadmap.yaml](Qk4a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **552/552** ordered group pairs; all candidate routes reach **552/552**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
