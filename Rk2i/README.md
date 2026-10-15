# Rk2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rk2i_0009 | 13.42% | 1342 |
| 1 | Rk2i_0010 | 12.98% | 1298 |
| 2 | Rk2i_0003 | 12.97% | 1297 |
| 3 | Rk2i_0006 | 12.55% | 1255 |
| 4 | Rk2i_0002 | 8.18% | 818 |
| 5 | Rk2i_0008 | 7.51% | 751 |
| 6 | Rk2i_0005 | 7.08% | 708 |
| 7 | Rk2i_0007 | 7.07% | 707 |
| 8 | Rk2i_0001 | 4.74% | 474 |
| 9 | Rk2i_0012 | 4.72% | 472 |
| 10 | Rk2i_0004 | 4.52% | 452 |
| 11 | Rk2i_0011 | 4.25% | 425 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk2i_roadmap.graphml](Rk2i_roadmap.graphml), [Rk2i_roadmap.json](Rk2i_roadmap.json), [Rk2i_roadmap.png](Rk2i_roadmap.png), [Rk2i_roadmap.svg](Rk2i_roadmap.svg), [Rk2i_roadmap.yaml](Rk2i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **132/132** ordered group pairs; all candidate routes reach **132/132**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
