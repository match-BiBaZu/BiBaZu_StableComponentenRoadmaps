# Dk1i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Dk1i_0003 | 17% | 1700 | Marginal | 0.3922 | Dk1i_0005 (within group) |
| 1 | Dk1i_0005 | 16.34% | 1634 | Marginal | 0.3933 | Dk1i_0003 (within group) |
| 2 | Dk1i_0002 | 16.3% | 1630 | Marginal | 0.3920 | Dk1i_0004 (within group) |
| 3 | Dk1i_0004 | 16.07% | 1607 | Marginal | 0.3853 | Dk1i_0002 (within group) |
| 4 | Dk1i_0007 | 11.74% | 1174 | Resistant | 2.4274 | Dk1i_0005 |
| 5 | Dk1i_0006 | 10.89% | 1089 | Resistant | 2.4283 | Dk1i_0003 |
| 6 | Dk1i_0001 | 6.02% | 602 | Resistant | 1.9098 | Dk1i_0005 |
| 7 | Dk1i_0008 | 5.14% | 514 | Resistant | 1.9046 | Dk1i_0003 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dk1i_roadmap.graphml](Dk1i_roadmap.graphml), [Dk1i_roadmap.json](Dk1i_roadmap.json), [Dk1i_roadmap.png](Dk1i_roadmap.png), [Dk1i_roadmap.svg](Dk1i_roadmap.svg), [Dk1i_roadmap.yaml](Dk1i_roadmap.yaml)
