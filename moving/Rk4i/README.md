# Rk4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rk4i_0021 | 8.13% | 813 | High | 3.6253 | Rk4i_0012 |
| 1 | Rk4i_0010 | 7.99% | 799 | High | 3.6199 | Rk4i_0012 |
| 2 | Rk4i_0013 | 7.78% | 778 | High | 3.6231 | Rk4i_0007 |
| 3 | Rk4i_0008 | 7.67% | 767 | High | 3.6262 | Rk4i_0017 |
| 4 | Rk4i_0015 | 7.54% | 754 | High | 3.6251 | Rk4i_0009 |
| 5 | Rk4i_0023 | 7.39% | 739 | High | 3.6235 | Rk4i_0017 |
| 6 | Rk4i_0003 | 7.34% | 734 | High | 3.6259 | Rk4i_0007 |
| 7 | Rk4i_0005 | 7.24% | 724 | High | 3.6189 | Rk4i_0009 |
| 8 | Rk4i_0012 | 5.31% | 531 | High | 2.6701 | Rk4i_0021 |
| 9 | Rk4i_0017 | 5.05% | 505 | High | 2.6683 | Rk4i_0008 |
| 10 | Rk4i_0009 | 4.88% | 488 | High | 2.6681 | Rk4i_0015 |
| 11 | Rk4i_0007 | 4.8% | 480 | High | 2.6689 | Rk4i_0013 |
| 12 | Rk4i_0014 | 2.17% | 217 | High | 1.5377 | Rk4i_0013 |
| 13 | Rk4i_0004 | 2.14% | 214 | High | 1.5368 | Rk4i_0010 |
| 14 | Rk4i_0016 | 2.12% | 212 | High | 1.5373 | Rk4i_0021 |
| 15 | Rk4i_0019 | 2.05% | 205 | High | 1.5351 | Rk4i_0003 |
| 16 | Rk4i_0006 | 1.95% | 195 | High | 1.7744 | Rk4i_0008 |
| 17 | Rk4i_0020 | 1.94% | 194 | High | 1.7759 | Rk4i_0013 |
| 18 | Rk4i_0002 | 1.78% | 178 | High | 1.7745 | Rk4i_0010 |
| 19 | Rk4i_0022 | 1.7% | 170 | High | 1.7724 | Rk4i_0015 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk4i_roadmap.graphml](Rk4i_roadmap.graphml), [Rk4i_roadmap.json](Rk4i_roadmap.json), [Rk4i_roadmap.png](Rk4i_roadmap.png), [Rk4i_roadmap.svg](Rk4i_roadmap.svg), [Rk4i_roadmap.yaml](Rk4i_roadmap.yaml)
