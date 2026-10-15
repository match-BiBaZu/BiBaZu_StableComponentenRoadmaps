# Rk4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rk4i_0006 | 6.23% | 623 |
| 1 | Rk4i_0020 | 6.23% | 623 |
| 2 | Rk4i_0011 | 6.21% | 621 |
| 3 | Rk4i_0019 | 6.21% | 621 |
| 4 | Rk4i_0012 | 6.16% | 616 |
| 5 | Rk4i_0008 | 6.1% | 610 |
| 6 | Rk4i_0005 | 6.02% | 602 |
| 7 | Rk4i_0021 | 6.01% | 601 |
| 8 | Rk4i_0010 | 5.9% | 590 |
| 9 | Rk4i_0009 | 5.6% | 560 |
| 10 | Rk4i_0007 | 5.44% | 544 |
| 11 | Rk4i_0013 | 5.33% | 533 |
| 12 | Rk4i_0016 | 3.79% | 379 |
| 13 | Rk4i_0002 | 3.56% | 356 |
| 14 | Rk4i_0017 | 3.49% | 349 |
| 15 | Rk4i_0014 | 3.47% | 347 |
| 16 | Rk4i_0023 | 2.36% | 236 |
| 17 | Rk4i_0022 | 2.3% | 230 |
| 18 | Rk4i_0004 | 2.28% | 228 |
| 19 | Rk4i_0003 | 1.96% | 196 |
| 20 | Rk4i_0024 | 1.43% | 143 |
| 21 | Rk4i_0015 | 1.35% | 135 |
| 22 | Rk4i_0018 | 1.33% | 133 |
| 23 | Rk4i_0001 | 1.23% | 123 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk4i_roadmap.graphml](Rk4i_roadmap.graphml), [Rk4i_roadmap.json](Rk4i_roadmap.json), [Rk4i_roadmap.png](Rk4i_roadmap.png), [Rk4i_roadmap.svg](Rk4i_roadmap.svg), [Rk4i_roadmap.yaml](Rk4i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **552/552** ordered group pairs; all candidate routes reach **552/552**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
