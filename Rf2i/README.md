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

Nodes use the chosen representative orientations. Direct connections remain geometric action candidates.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.
