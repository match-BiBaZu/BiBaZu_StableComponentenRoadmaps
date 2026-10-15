# Rk1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rk1a_0034 | 7.17% | 717 |
| 1 | Rk1a_0007 | 6.73% | 673 |
| 2 | Rk1a_0026 | 6.56% | 656 |
| 3 | Rk1a_0010 | 6.52% | 652 |
| 4 | Rk1a_0011 | 6.4% | 640 |
| 5 | Rk1a_0033 | 6.3% | 630 |
| 6 | Rk1a_0008 | 6.23% | 623 |
| 7 | Rk1a_0022 | 6.2% | 620 |
| 8 | Rk1a_0019 | 3.93% | 393 |
| 9 | Rk1a_0004 | 3.86% | 386 |
| 10 | Rk1a_0035 | 3.74% | 374 |
| 11 | Rk1a_0037 | 3.67% | 367 |
| 12 | Rk1a_0003 | 3.58% | 358 |
| 13 | Rk1a_0009 | 3.41% | 341 |
| 14 | Rk1a_0017 | 3.36% | 336 |
| 15 | Rk1a_0028 | 3.32% | 332 |
| 16 | Rk1a_0042 | 2.44% | 244 |
| 17 | Rk1a_0024 | 2.43% | 243 |
| 18 | Rk1a_0001 | 2.38% | 238 |
| 19 | Rk1a_0021 | 2.36% | 236 |
| 20 | Rk1a_0030 | 2.29% | 229 |
| 21 | Rk1a_0025 | 2.23% | 223 |
| 22 | Rk1a_0005 | 2.18% | 218 |
| 23 | Rk1a_0023 | 2.18% | 218 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk1a_roadmap.graphml](Rk1a_roadmap.graphml), [Rk1a_roadmap.json](Rk1a_roadmap.json), [Rk1a_roadmap.png](Rk1a_roadmap.png), [Rk1a_roadmap.svg](Rk1a_roadmap.svg), [Rk1a_roadmap.yaml](Rk1a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **552/552** ordered group pairs; all candidate routes reach **552/552**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
