# Rf4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rf4i_0008 | 10.61% | 1061 |
| 1 | Rf4i_0005 | 10.52% | 1052 |
| 2 | Rf4i_0015 | 8.16% | 816 |
| 3 | Rf4i_0003 | 7.76% | 776 |
| 4 | Rf4i_0006 | 6.16% | 616 |
| 5 | Rf4i_0010 | 5.71% | 571 |
| 6 | Rf4i_0016 | 5.57% | 557 |
| 7 | Rf4i_0011 | 5.53% | 553 |
| 8 | Rf4i_0002 | 5.44% | 544 |
| 9 | Rf4i_0013 | 5.44% | 544 |
| 10 | Rf4i_0009 | 5.01% | 501 |
| 11 | Rf4i_0004 | 4.96% | 496 |
| 12 | Rf4i_0020 | 4.69% | 469 |
| 13 | Rf4i_0012 | 4.66% | 466 |
| 14 | Rf4i_0014 | 4.47% | 447 |
| 15 | Rf4i_0001 | 3.96% | 396 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rf4i_roadmap.graphml](Rf4i_roadmap.graphml), [Rf4i_roadmap.json](Rf4i_roadmap.json), [Rf4i_roadmap.png](Rf4i_roadmap.png), [Rf4i_roadmap.svg](Rf4i_roadmap.svg), [Rf4i_roadmap.yaml](Rf4i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **240/240** ordered group pairs; all candidate routes reach **240/240**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
