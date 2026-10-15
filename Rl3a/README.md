# Rl3a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rl3a_0013 | 25.07% | 2507 |
| 1 | Rl3a_0011 | 23.5% | 2350 |
| 2 | Rl3a_0009 | 21.72% | 2172 |
| 3 | Rl3a_0002 | 17.46% | 1746 |
| 4 | Rl3a_0006 | 2.6% | 260 |
| 5 | Rl3a_0016 | 2.29% | 229 |
| 6 | Rl3a_0007 | 1.97% | 197 |
| 7 | Rl3a_0014 | 1.54% | 154 |
| 8 | Rl3a_0010 | 1.13% | 113 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl3a_roadmap.graphml](Rl3a_roadmap.graphml), [Rl3a_roadmap.json](Rl3a_roadmap.json), [Rl3a_roadmap.png](Rl3a_roadmap.png), [Rl3a_roadmap.svg](Rl3a_roadmap.svg), [Rl3a_roadmap.yaml](Rl3a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Thumbnails retain the chosen representative orientations. Each group contains all its observed members.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.

## Whole-group reorientations

Cartesian-only routes reach **54/72** ordered group pairs; all candidate routes reach **72/72**.

A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. This interchangeability is the planning assumption; no extra motion is invented between those witnesses.

Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. Competing landing outcomes and sampled downhill evidence remain in the records.

The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. Execution requires an assigned pressure profile explicitly calibrated for the exported source group. Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.
