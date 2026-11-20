# Kk2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Kk2i_0047 | 10.03% | 1003 | Fragile | 0.0474 | Kk2i_0050 (within group) |
| 1 | Kk2i_0053 | 9.78% | 978 | Fragile | 0.0470 | Kk2i_0050 (within group) |
| 2 | Kk2i_0050 | 9.2% | 920 | Fragile | 0.0656 | Kk2i_0047 (within group) |
| 3 | Kk2i_0044 | 7.51% | 751 | Fragile | 0.0333 | Kk2i_0050 (within group) |
| 4 | Kk2i_0057 | 7.07% | 707 | Fragile | 0.0333 | Kk2i_0053 (within group) |
| 5 | Kk2i_0035 | 4.97% | 497 | Resistant | 0.5476 | Kk2i_0044 |
| 6 | Kk2i_0015 | 4.95% | 495 | Resistant | 0.5451 | Kk2i_0024 |
| 7 | Kk2i_0030 | 2.65% | 265 | Fragile | 0.0100 | Kk2i_0033 (within group) |
| 8 | Kk2i_0032 | 2.12% | 212 | Fragile | 0.0132 | Kk2i_0016 (within group) |
| 9 | Kk2i_0025 | 1.94% | 194 | Fragile | 0.0244 | Kk2i_0014 (within group) |
| 10 | Kk2i_0014 | 1.85% | 185 | Fragile | 0.0238 | Kk2i_0025 (within group) |
| 11 | Kk2i_0017 | 1.81% | 181 | Resistant | 0.8011 | Kk2i_0008 |
| 12 | Kk2i_0037 | 1.75% | 175 | Resistant | 0.8056 | Kk2i_0062 |
| 13 | Kk2i_0016 | 1.73% | 173 | Fragile | 0.0351 | Kk2i_0014 (within group) |
| 14 | Kk2i_0041 | 1.72% | 172 | Fragile | 0.0199 | Kk2i_0044 (within group) |
| 15 | Kk2i_0036 | 1.71% | 171 | Fragile | 0.0365 | Kk2i_0040 (within group) |
| 16 | Kk2i_0040 | 1.61% | 161 | Fragile | 0.0235 | Kk2i_0036 (within group) |
| 17 | Kk2i_0013 | 1.44% | 144 | Fragile | 0.0138 | Kk2i_0025 (within group) |
| 18 | Kk2i_0042 | 1.42% | 142 | Fragile | 0.0131 | Kk2i_0040 (within group) |
| 19 | Kk2i_0033 | 1.26% | 126 | Fragile | 0.0218 | Kk2i_0036 (within group) |
| 20 | Kk2i_0046 | 1.26% | 126 | Fragile | 0.0077 | Kk2i_0036 (within group) |
| 21 | Kk2i_0060 | 1.16% | 116 | Fragile | 0.0216 | Kk2i_0057 (within group) |
| 22 | Kk2i_0011 | 1.15% | 115 | Fragile | 0.0076 | Kk2i_0013 (within group) |
| 23 | Kk2i_0009 | 1.05% | 105 | Fragile | 0.0026 | Kk2i_0011 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kk2i_roadmap.graphml](Kk2i_roadmap.graphml), [Kk2i_roadmap.json](Kk2i_roadmap.json), [Kk2i_roadmap.png](Kk2i_roadmap.png), [Kk2i_roadmap.svg](Kk2i_roadmap.svg), [Kk2i_roadmap.yaml](Kk2i_roadmap.yaml)
