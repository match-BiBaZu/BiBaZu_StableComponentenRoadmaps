# Kf2a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Kf2a_0045 | 24.12% | 2412 | Resistant | 1.8081 | Kf2a_0040 |
| 1 | Kf2a_0001 | 8.21% | 821 | Resistant | 1.6577 | Kf2a_0052 |
| 2 | Kf2a_0013 | 3.42% | 342 | Fragile | 0.0242 | Kf2a_0018 (within group) |
| 3 | Kf2a_0043 | 3.3% | 330 | Fragile | 0.0285 | Kf2a_0038 (within group) |
| 4 | Kf2a_0047 | 3.11% | 311 | Fragile | 0.0241 | Kf2a_0043 (within group) |
| 5 | Kf2a_0015 | 2.8% | 280 | Fragile | 0.0283 | Kf2a_0018 (within group) |
| 6 | Kf2a_0011 | 2.48% | 248 | Fragile | 0.0211 | Kf2a_0013 (within group) |
| 7 | Kf2a_0010 | 2.07% | 207 | Fragile | 0.0196 | Kf2a_0015 (within group) |
| 8 | Kf2a_0049 | 2.07% | 207 | Fragile | 0.0213 | Kf2a_0043 (within group) |
| 9 | Kf2a_0009 | 1.89% | 189 | Fragile | 0.0196 | Kf2a_0013 (within group) |
| 10 | Kf2a_0051 | 1.67% | 167 | Fragile | 0.0199 | Kf2a_0049 (within group) |
| 11 | Kf2a_0012 | 1.6% | 160 | Fragile | 0.0206 | Kf2a_0011 (within group) |
| 12 | Kf2a_0020 | 1.59% | 159 | Fragile | 0.0326 | Kf2a_0017 (within group) |
| 13 | Kf2a_0050 | 1.56% | 156 | Fragile | 0.0197 | Kf2a_0049 (within group) |
| 14 | Kf2a_0014 | 1.53% | 153 | Fragile | 0.0234 | Kf2a_0012 (within group) |
| 15 | Kf2a_0048 | 1.44% | 144 | Fragile | 0.0199 | Kf2a_0050 (within group) |
| 16 | Kf2a_0017 | 1.43% | 143 | Fragile | 0.0266 | Kf2a_0014 (within group) |
| 17 | Kf2a_0042 | 1.42% | 142 | Fragile | 0.0262 | Kf2a_0048 (within group) |
| 18 | Kf2a_0046 | 1.35% | 135 | Fragile | 0.0224 | Kf2a_0048 (within group) |
| 19 | Kf2a_0038 | 1.32% | 132 | Fragile | 0.0912 | Kf2a_0043 (within group) |
| 20 | Kf2a_0030 | 1.27% | 127 | Resistant | 0.7255 | Kf2a_0040 |
| 21 | Kf2a_0036 | 1.26% | 126 | Fragile | 0.0330 | Kf2a_0046 (within group) |
| 22 | Kf2a_0026 | 1.24% | 124 | Fragile | 0.0609 | Kf2a_0023 (within group) |
| 23 | Kf2a_0018 | 1.22% | 122 | Fragile | 0.0918 | Kf2a_0015 (within group) |
| 24 | Kf2a_0005 | 1.21% | 121 | Fragile | 0.0735 | Kf2a_0001 |
| 25 | Kf2a_0023 | 1.21% | 121 | Fragile | 0.0501 | Kf2a_0017 (within group) |
| 26 | Kf2a_0022 | 1.19% | 119 | Fragile | 0.0393 | Kf2a_0020 (within group) |
| 27 | Kf2a_0028 | 1.15% | 115 | Fragile | 0.0761 | Kf2a_0018 (within group) |
| 28 | Kf2a_0034 | 1.09% | 109 | Fragile | 0.0410 | Kf2a_0038 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kf2a_roadmap.graphml](Kf2a_roadmap.graphml), [Kf2a_roadmap.json](Kf2a_roadmap.json), [Kf2a_roadmap.png](Kf2a_roadmap.png), [Kf2a_roadmap.svg](Kf2a_roadmap.svg), [Kf2a_roadmap.yaml](Kf2a_roadmap.yaml)
