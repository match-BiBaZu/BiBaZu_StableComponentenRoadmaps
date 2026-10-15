# Rl1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Minimum frequency: **0%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Rl1a_0006 | 24.62% | 2462 |
| 1 | Rl1a_0012 | 22.34% | 2234 |
| 2 | Rl1a_0007 | 22.21% | 2221 |
| 3 | Rl1a_0011 | 21.56% | 2156 |
| 4 | Rl1a_0005 | 2.59% | 259 |
| 5 | Rl1a_0001 | 1.67% | 167 |
| 6 | Rl1a_0013 | 1.5% | 150 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl1a_roadmap.graphml](Rl1a_roadmap.graphml), [Rl1a_roadmap.json](Rl1a_roadmap.json), [Rl1a_roadmap.png](Rl1a_roadmap.png), [Rl1a_roadmap.svg](Rl1a_roadmap.svg), [Rl1a_roadmap.yaml](Rl1a_roadmap.yaml)

[Group membership](membership.csv), [all groups](source/groups.json), [member stability curves](source/group_stability.csv), [barrier evidence](source/grouping_geometry.json).

Nodes use the chosen representative orientations. Direct connections remain geometric action candidates.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.
