# Rf1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rf1a_0009 | 21.18% | 2118 | Resistant | 9.4014 | Rf1a_0008 |
| 1 | Rf1a_0017 | 20.17% | 2017 | Resistant | 9.4095 | Rf1a_0020 |
| 2 | Rf1a_0004 | 9.87% | 987 | Resistant | 7.0698 | Rf1a_0009 |
| 3 | Rf1a_0016 | 9.29% | 929 | Resistant | 7.0712 | Rf1a_0017 |
| 4 | Rf1a_0022 | 7.42% | 742 | Resistant | 0.6931 | Rf1a_0023 |
| 5 | Rf1a_0023 | 5.54% | 554 | Resistant | 0.6909 | Rf1a_0022 |
| 6 | Rf1a_0018 | 4.13% | 413 | Resistant | 0.9340 | Rf1a_0014 |
| 7 | Rf1a_0021 | 4.06% | 406 | Resistant | 0.8626 | Rf1a_0023 |
| 8 | Rf1a_0001 | 3.42% | 342 | Resistant | 0.9447 | Rf1a_0002 (within group) |
| 9 | Rf1a_0020 | 2.86% | 286 | Resistant | 0.9878 | Rf1a_0017 |
| 10 | Rf1a_0005 | 2.81% | 281 | Resistant | 0.8625 | Rf1a_0022 |
| 11 | Rf1a_0008 | 2.64% | 264 | Resistant | 0.9863 | Rf1a_0009 |
| 12 | Rf1a_0003 | 1.83% | 183 | Marginal | 0.3260 | Rf1a_0001 |
| 13 | Rf1a_0012 | 1.5% | 150 | Marginal | 0.3268 | Rf1a_0018 |
| 14 | Rf1a_0013 | 1.45% | 145 | Marginal | 0.3258 | Rf1a_0014 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rf1a_roadmap.graphml](Rf1a_roadmap.graphml), [Rf1a_roadmap.json](Rf1a_roadmap.json), [Rf1a_roadmap.png](Rf1a_roadmap.png), [Rf1a_roadmap.svg](Rf1a_roadmap.svg), [Rf1a_roadmap.yaml](Rf1a_roadmap.yaml)
