# Kl2a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Kl2a_0019 | 24.03% | 2403 | Marginal | 0.1790 | Kl2a_0016 |
| 1 | Kl2a_0022 | 20.39% | 2039 | Marginal | 0.1792 | Kl2a_0025 |
| 2 | Kl2a_0043 | 7.5% | 750 | Marginal | 0.2755 | Kl2a_0038 |
| 3 | Kl2a_0038 | 6.59% | 659 | Marginal | 0.2774 | Kl2a_0043 |
| 4 | Kl2a_0045 | 3.55% | 355 | Fragile | 0.0432 | Kl2a_0012 (within group) |
| 5 | Kl2a_0035 | 3.51% | 351 | Fragile | 0.0434 | Kl2a_0025 (within group) |
| 6 | Kl2a_0050 | 3.42% | 342 | Fragile | 0.0299 | Kl2a_0012 (within group) |
| 7 | Kl2a_0033 | 3.27% | 327 | Fragile | 0.0308 | Kl2a_0022 |
| 8 | Kl2a_0025 | 3.14% | 314 | Fragile | 0.0167 | Kl2a_0022 |
| 9 | Kl2a_0016 | 3.12% | 312 | Fragile | 0.0167 | Kl2a_0019 |
| 10 | Kl2a_0040 | 3.05% | 305 | Fragile | 0.0594 | Kl2a_0050 (within group) |
| 11 | Kl2a_0028 | 2.8% | 280 | Fragile | 0.0213 | Kl2a_0025 (within group) |
| 12 | Kl2a_0012 | 2.49% | 249 | Fragile | 0.0205 | Kl2a_0016 (within group) |
| 13 | Kl2a_0009 | 2.46% | 246 | Fragile | 0.0780 | Kl2a_0038 |
| 14 | Kl2a_0029 | 1.88% | 188 | Fragile | 0.0767 | Kl2a_0038 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kl2a_roadmap.graphml](Kl2a_roadmap.graphml), [Kl2a_roadmap.json](Kl2a_roadmap.json), [Kl2a_roadmap.png](Kl2a_roadmap.png), [Kl2a_roadmap.svg](Kl2a_roadmap.svg), [Kl2a_roadmap.yaml](Kl2a_roadmap.yaml)
