# Ql1i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Ql1i_0003 | 47.19% | 4719 | Resistant | 18.8474 | Ql1i_0002 |
| 1 | Ql1i_0002 | 46.54% | 4654 | Resistant | 18.8499 | Ql1i_0003 |
| 2 | Ql1i_0005 | 2.34% | 234 | Resistant | 0.9824 | Ql1i_0002 |
| 3 | Ql1i_0004 | 1.81% | 181 | Resistant | 0.9829 | Ql1i_0003 |
| 4 | Ql1i_0001 | 1.23% | 123 | Resistant | 0.7801 | Ql1i_0003 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Ql1i_roadmap.graphml](Ql1i_roadmap.graphml), [Ql1i_roadmap.json](Ql1i_roadmap.json), [Ql1i_roadmap.png](Ql1i_roadmap.png), [Ql1i_roadmap.svg](Ql1i_roadmap.svg), [Ql1i_roadmap.yaml](Ql1i_roadmap.yaml)
