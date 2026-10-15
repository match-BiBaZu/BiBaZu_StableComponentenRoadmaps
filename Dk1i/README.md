# Dk1i

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Dk1i_0005 | 27.68% | 2768 |
| 1 | Dk1i_0002 | 26.91% | 2691 |
| 2 | Dk1i_0007 | 16.44% | 1644 |
| 3 | Dk1i_0006 | 14.39% | 1439 |
| 4 | Dk1i_0001 | 7.46% | 746 |
| 5 | Dk1i_0008 | 7.1% | 710 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dk1i_roadmap.graphml](Dk1i_roadmap.graphml), [Dk1i_roadmap.json](Dk1i_roadmap.json), [Dk1i_roadmap.png](Dk1i_roadmap.png), [Dk1i_roadmap.svg](Dk1i_roadmap.svg), [Dk1i_roadmap.yaml](Dk1i_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **30/30** ordered group pairs; all candidate routes reach **30/30**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
