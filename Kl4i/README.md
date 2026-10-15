# Kl4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Kl4i_0008 | 11.17% | 1117 |
| 1 | Kl4i_0028 | 8.51% | 851 |
| 2 | Kl4i_0030 | 7.46% | 746 |
| 3 | Kl4i_0010 | 4.2% | 420 |
| 4 | Kl4i_0023 | 3.88% | 388 |
| 5 | Kl4i_0024 | 3.73% | 373 |
| 6 | Kl4i_0012 | 3.72% | 372 |
| 7 | Kl4i_0020 | 3.69% | 369 |
| 8 | Kl4i_0036 | 3.48% | 348 |
| 9 | Kl4i_0034 | 3.47% | 347 |
| 10 | Kl4i_0032 | 3.31% | 331 |
| 11 | Kl4i_0038 | 3.27% | 327 |
| 12 | Kl4i_0014 | 3.25% | 325 |
| 13 | Kl4i_0027 | 3.16% | 316 |
| 14 | Kl4i_0017 | 3.05% | 305 |
| 15 | Kl4i_0001 | 2.6% | 260 |
| 16 | Kl4i_0018 | 2.23% | 223 |
| 17 | Kl4i_0002 | 2.04% | 204 |
| 18 | Kl4i_0021 | 1.55% | 155 |
| 19 | Kl4i_0003 | 1.52% | 152 |
| 20 | Kl4i_0007 | 1.45% | 145 |
| 21 | Kl4i_0005 | 1.4% | 140 |
| 22 | Kl4i_0004 | 1.31% | 131 |
| 23 | Kl4i_0029 | 1.27% | 127 |
| 24 | Kl4i_0009 | 1.24% | 124 |
| 25 | Kl4i_0019 | 1.23% | 123 |
| 26 | Kl4i_0006 | 1.18% | 118 |
| 27 | Kl4i_0011 | 1.13% | 113 |
| 28 | Kl4i_0031 | 1.09% | 109 |
| 29 | Kl4i_0026 | 1.03% | 103 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kl4i_roadmap.graphml](Kl4i_roadmap.graphml), [Kl4i_roadmap.json](Kl4i_roadmap.json), [Kl4i_roadmap.png](Kl4i_roadmap.png), [Kl4i_roadmap.svg](Kl4i_roadmap.svg), [Kl4i_roadmap.yaml](Kl4i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **704/870** ordered group pairs; all candidate routes reach **870/870**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
