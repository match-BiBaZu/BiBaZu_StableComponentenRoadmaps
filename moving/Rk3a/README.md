# Rk3a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rk3a_0021 | 17.25% | 1725 | Resistant | 5.3725 | Rk3a_0017 |
| 1 | Rk3a_0017 | 16.38% | 1638 | Resistant | 5.3694 | Rk3a_0021 |
| 2 | Rk3a_0014 | 11.98% | 1198 | Resistant | 1.8486 | Rk3a_0012 |
| 3 | Rk3a_0006 | 11.14% | 1114 | Resistant | 1.8483 | Rk3a_0010 |
| 4 | Rk3a_0005 | 8.2% | 820 | Resistant | 1.8213 | Rk3a_0012 |
| 5 | Rk3a_0004 | 8.17% | 817 | Resistant | 1.8213 | Rk3a_0012 |
| 6 | Rk3a_0016 | 7.4% | 740 | Resistant | 1.8206 | Rk3a_0010 |
| 7 | Rk3a_0015 | 7.34% | 734 | Resistant | 1.8216 | Rk3a_0010 |
| 8 | Rk3a_0019 | 2.64% | 264 | Resistant | 1.2522 | Rk3a_0021 |
| 9 | Rk3a_0018 | 2.62% | 262 | Resistant | 1.2508 | Rk3a_0017 |
| 10 | Rk3a_0011 | 1.87% | 187 | Fragile | 0.0965 | Rk3a_0014 (within group) |
| 11 | Rk3a_0010 | 1.24% | 124 | Fragile | 0.0978 | Rk3a_0006 |
| 12 | Rk3a_0012 | 1.22% | 122 | Fragile | 0.0979 | Rk3a_0014 |
| 13 | Rk3a_0009 | 1% | 100 | Fragile | 0.0963 | Rk3a_0006 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk3a_roadmap.graphml](Rk3a_roadmap.graphml), [Rk3a_roadmap.json](Rk3a_roadmap.json), [Rk3a_roadmap.png](Rk3a_roadmap.png), [Rk3a_roadmap.svg](Rk3a_roadmap.svg), [Rk3a_roadmap.yaml](Rk3a_roadmap.yaml)
