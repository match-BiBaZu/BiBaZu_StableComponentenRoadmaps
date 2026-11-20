# Ql2a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Ql2a_0008 | 23.94% | 2394 | Resistant | 5.6308 | Ql2a_0002 |
| 1 | Ql2a_0003 | 23.67% | 2367 | Resistant | 5.6345 | Ql2a_0009 |
| 2 | Ql2a_0009 | 22.76% | 2276 | Resistant | 4.3492 | Ql2a_0002 |
| 3 | Ql2a_0002 | 22.64% | 2264 | Resistant | 4.3505 | Ql2a_0009 |
| 4 | Ql2a_0001 | 1.26% | 126 | Resistant | 0.9261 | Ql2a_0003 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Ql2a_roadmap.graphml](Ql2a_roadmap.graphml), [Ql2a_roadmap.json](Ql2a_roadmap.json), [Ql2a_roadmap.png](Ql2a_roadmap.png), [Ql2a_roadmap.svg](Ql2a_roadmap.svg), [Ql2a_roadmap.yaml](Ql2a_roadmap.yaml)
