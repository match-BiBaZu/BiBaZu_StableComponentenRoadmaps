# Rl1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rl1a_0009 | 23.67% | 2367 | Resistant | 2.8712 | Rl1a_0011 |
| 1 | Rl1a_0008 | 23.12% | 2312 | Resistant | 2.8721 | Rl1a_0012 |
| 2 | Rl1a_0022 | 22.24% | 2224 | Resistant | 2.5034 | Rl1a_0011 (within group) |
| 3 | Rl1a_0023 | 21.76% | 2176 | Resistant | 2.5054 | Rl1a_0012 (within group) |
| 4 | Rl1a_0024 | 2.11% | 211 | Resistant | 0.8520 | Rl1a_0021 |
| 5 | Rl1a_0007 | 1.54% | 154 | Resistant | 0.8541 | Rl1a_0006 |
| 6 | Rl1a_0013 | 1.34% | 134 | Marginal | 0.2854 | Rl1a_0016 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl1a_roadmap.graphml](Rl1a_roadmap.graphml), [Rl1a_roadmap.json](Rl1a_roadmap.json), [Rl1a_roadmap.png](Rl1a_roadmap.png), [Rl1a_roadmap.svg](Rl1a_roadmap.svg), [Rl1a_roadmap.yaml](Rl1a_roadmap.yaml)
