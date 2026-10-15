# Rf2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rf2i_0006 | 15.92% | 1592 |
| 1 | Rf2i_0005 | 15.54% | 1554 |
| 2 | Rf2i_0003 | 15.17% | 1517 |
| 3 | Rf2i_0004 | 13.91% | 1391 |
| 4 | Rf2i_0009 | 10.61% | 1061 |
| 5 | Rf2i_0001 | 9.14% | 914 |
| 6 | Rf2i_0010 | 8.87% | 887 |
| 7 | Rf2i_0002 | 8.81% | 881 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rf2i_roadmap.graphml](Rf2i_roadmap.graphml), [Rf2i_roadmap.json](Rf2i_roadmap.json), [Rf2i_roadmap.png](Rf2i_roadmap.png), [Rf2i_roadmap.svg](Rf2i_roadmap.svg), [Rf2i_roadmap.yaml](Rf2i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **56/56** ordered group pairs; all candidate routes reach **56/56**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
