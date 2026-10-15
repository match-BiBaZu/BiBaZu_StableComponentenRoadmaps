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

Nodes use the chosen representative orientations. Direct connections remain geometric action candidates.

<!-- COMPOSITE CONNECTIVITY -->

## Composite orientation candidates

Existing connections reach 6/30 ordered pairs. With 3 composite bridges, candidate routes reach 30/30 pairs.

Representatives and direct edges are unchanged. Dashed purple bridges are geometry-only candidates: contact, settling, actuator feasibility and reliability remain unverified. Transient orientations are not pose catalogue entries. Calibrate a full transfer pressure profile before execution.

JSON/YAML contain ordered commands, preferred routes and separate directed connectivity reports.

## Member-conditioned transfers

20 known-member actions connect groups. 649 total member transfer candidates include sampled downhill capture intervals and composite fallbacks. Routes preserve possible member orientations, including explicit intra-group repositioning. The group overview alone is not a proof that two member-conditioned actions can be chained.

All retained source members have candidate paths to every retained group: **True**. Runtime use requires a calibrated profile with explicitly declared source-member coverage; old profiles receive no automatic group-wide coverage.

<!-- CONSUMER EXPORT -->

Control applications read finished calibration choices, ordered commands, preview segments and execution routes from `consumer_export` in JSON/YAML. They do not construct routes. Execution requires assigned pressure profiles and explicit source-member coverage; geometry-only evidence does not grant either.
