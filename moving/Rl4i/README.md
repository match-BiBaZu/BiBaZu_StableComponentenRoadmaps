# Rl4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rl4i_0009 | 13.76% | 1376 | Resistant | 4.8203 | Rl4i_0018 |
| 1 | Rl4i_0008 | 13.37% | 1337 | Resistant | 4.8204 | Rl4i_0011 |
| 2 | Rl4i_0006 | 13.23% | 1323 | Resistant | 4.8209 | Rl4i_0018 |
| 3 | Rl4i_0005 | 12.69% | 1269 | Resistant | 4.8208 | Rl4i_0019 |
| 4 | Rl4i_0011 | 11.98% | 1198 | Resistant | 4.9973 | Rl4i_0019 |
| 5 | Rl4i_0018 | 11.21% | 1121 | Resistant | 4.9961 | Rl4i_0012 |
| 6 | Rl4i_0012 | 11.03% | 1103 | Resistant | 4.9930 | Rl4i_0018 |
| 7 | Rl4i_0019 | 10.31% | 1031 | Resistant | 4.9961 | Rl4i_0011 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl4i_roadmap.graphml](Rl4i_roadmap.graphml), [Rl4i_roadmap.json](Rl4i_roadmap.json), [Rl4i_roadmap.png](Rl4i_roadmap.png), [Rl4i_roadmap.svg](Rl4i_roadmap.svg), [Rl4i_roadmap.yaml](Rl4i_roadmap.yaml)
