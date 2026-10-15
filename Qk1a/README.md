# Qk1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Qk1a_0007 | 23.17% | 2317 |
| 1 | Qk1a_0008 | 21.87% | 2187 |
| 2 | Qk1a_0012 | 14.3% | 1430 |
| 3 | Qk1a_0009 | 13.72% | 1372 |
| 4 | Qk1a_0004 | 13.7% | 1370 |
| 5 | Qk1a_0006 | 12.8% | 1280 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Qk1a_roadmap.graphml](Qk1a_roadmap.graphml), [Qk1a_roadmap.json](Qk1a_roadmap.json), [Qk1a_roadmap.png](Qk1a_roadmap.png), [Qk1a_roadmap.svg](Qk1a_roadmap.svg), [Qk1a_roadmap.yaml](Qk1a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.


## Whole-group reorientations

Cartesian-only routes reach **30/30** ordered group pairs; all candidate routes reach **30/30**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
