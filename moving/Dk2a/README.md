# Dk2a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Dk2a_0008 | 20.71% | 2071 | Resistant | 2.9794 | Dk2a_0012 |
| 1 | Dk2a_0006 | 19.99% | 1999 | Resistant | 2.9753 | Dk2a_0012 |
| 2 | Dk2a_0016 | 8.96% | 896 | Marginal | 0.4585 | Dk2a_0015 (within group) |
| 3 | Dk2a_0015 | 8.56% | 856 | Marginal | 0.4589 | Dk2a_0016 (within group) |
| 4 | Dk2a_0003 | 6.24% | 624 | Resistant | 1.8447 | Dk2a_0008 |
| 5 | Dk2a_0017 | 6.09% | 609 | Resistant | 1.8424 | Dk2a_0008 |
| 6 | Dk2a_0018 | 5.54% | 554 | Resistant | 1.8462 | Dk2a_0006 |
| 7 | Dk2a_0009 | 5.26% | 526 | Resistant | 1.8429 | Dk2a_0006 |
| 8 | Dk2a_0012 | 4.23% | 423 | Marginal | 0.1385 | Dk2a_0014 (within group) |
| 9 | Dk2a_0007 | 3.05% | 305 | Resistant | 0.5158 | Dk2a_0004 |
| 10 | Dk2a_0014 | 2.96% | 296 | Marginal | 0.1392 | Dk2a_0012 (within group) |
| 11 | Dk2a_0005 | 2.91% | 291 | Resistant | 0.5169 | Dk2a_0011 |
| 12 | Dk2a_0001 | 2.63% | 263 | Marginal | 0.4202 | Dk2a_0002 (within group) |
| 13 | Dk2a_0013 | 2.22% | 222 | Marginal | 0.4240 | Dk2a_0011 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dk2a_roadmap.graphml](Dk2a_roadmap.graphml), [Dk2a_roadmap.json](Dk2a_roadmap.json), [Dk2a_roadmap.png](Dk2a_roadmap.png), [Dk2a_roadmap.svg](Dk2a_roadmap.svg), [Dk2a_roadmap.yaml](Dk2a_roadmap.yaml)
