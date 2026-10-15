# Kk2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Kk2i_0018 | 20.23% | 2023 |
| 1 | Kk2i_0017 | 8.33% | 833 |
| 2 | Kk2i_0003 | 7.73% | 773 |
| 3 | Kk2i_0004 | 6.61% | 661 |
| 4 | Kk2i_0024 | 3.21% | 321 |
| 5 | Kk2i_0026 | 3.15% | 315 |
| 6 | Kk2i_0025 | 2.85% | 285 |
| 7 | Kk2i_0015 | 2.53% | 253 |
| 8 | Kk2i_0021 | 2.53% | 253 |
| 9 | Kk2i_0016 | 2.46% | 246 |
| 10 | Kk2i_0029 | 2.42% | 242 |
| 11 | Kk2i_0030 | 2.42% | 242 |
| 12 | Kk2i_0020 | 2.36% | 236 |
| 13 | Kk2i_0028 | 2.36% | 236 |
| 14 | Kk2i_0022 | 2.33% | 233 |
| 15 | Kk2i_0019 | 2.23% | 223 |
| 16 | Kk2i_0005 | 2.1% | 210 |
| 17 | Kk2i_0006 | 2.09% | 209 |
| 18 | Kk2i_0008 | 1.84% | 184 |
| 19 | Kk2i_0010 | 1.65% | 165 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kk2i_roadmap.graphml](Kk2i_roadmap.graphml), [Kk2i_roadmap.json](Kk2i_roadmap.json), [Kk2i_roadmap.png](Kk2i_roadmap.png), [Kk2i_roadmap.svg](Kk2i_roadmap.svg), [Kk2i_roadmap.yaml](Kk2i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **129/380** ordered group pairs; all candidate routes reach **380/380**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
