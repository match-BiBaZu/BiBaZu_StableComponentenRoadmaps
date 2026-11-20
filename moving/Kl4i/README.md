# Kl4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Kl4i_0032 | 17.59% | 1759 | Fragile | 0.0674 | Kl4i_0028 (within group) |
| 1 | Kl4i_0081 | 16.15% | 1615 | Fragile | 0.0668 | Kl4i_0078 (within group) |
| 2 | Kl4i_0028 | 16.01% | 1601 | Fragile | 0.0657 | Kl4i_0032 (within group) |
| 3 | Kl4i_0078 | 15.72% | 1572 | Fragile | 0.0663 | Kl4i_0081 (within group) |
| 4 | Kl4i_0075 | 6.35% | 635 | Fragile | 0.0328 | Kl4i_0078 (within group) |
| 5 | Kl4i_0024 | 5.39% | 539 | Fragile | 0.0340 | Kl4i_0032 (within group) |
| 6 | Kl4i_0083 | 5.3% | 530 | Fragile | 0.0329 | Kl4i_0081 (within group) |
| 7 | Kl4i_0036 | 5.11% | 511 | Fragile | 0.0327 | Kl4i_0032 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kl4i_roadmap.graphml](Kl4i_roadmap.graphml), [Kl4i_roadmap.json](Kl4i_roadmap.json), [Kl4i_roadmap.png](Kl4i_roadmap.png), [Kl4i_roadmap.svg](Kl4i_roadmap.svg), [Kl4i_roadmap.yaml](Kl4i_roadmap.yaml)
