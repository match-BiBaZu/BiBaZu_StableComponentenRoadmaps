# Dl1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Dl1a_0007 | 47.24% | 4724 |
| 1 | Dl1a_0006 | 46.28% | 4628 |
| 2 | Dl1a_0013 | 3.32% | 332 |
| 3 | Dl1a_0003 | 1.55% | 155 |
| 4 | Dl1a_0002 | 1.13% | 113 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dl1a_roadmap.graphml](Dl1a_roadmap.graphml), [Dl1a_roadmap.json](Dl1a_roadmap.json), [Dl1a_roadmap.png](Dl1a_roadmap.png), [Dl1a_roadmap.svg](Dl1a_roadmap.svg), [Dl1a_roadmap.yaml](Dl1a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.


## Whole-group reorientations

Cartesian-only routes reach **20/20** ordered group pairs; all candidate routes reach **20/20**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
