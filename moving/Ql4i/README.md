# Ql4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Ql4i_0013 | 12.95% | 1295 | High | 5.6524 | Ql4i_0020 |
| 1 | Ql4i_0012 | 12.89% | 1289 | High | 5.6499 | Ql4i_0021 |
| 2 | Ql4i_0021 | 12.88% | 1288 | High | 5.6480 | Ql4i_0012 |
| 3 | Ql4i_0020 | 12.22% | 1222 | High | 5.6460 | Ql4i_0013 |
| 4 | Ql4i_0007 | 11.21% | 1121 | High | 5.3636 | Ql4i_0012 |
| 5 | Ql4i_0008 | 11.09% | 1109 | High | 5.3648 | Ql4i_0013 |
| 6 | Ql4i_0005 | 10.69% | 1069 | High | 5.3686 | Ql4i_0020 |
| 7 | Ql4i_0004 | 10.29% | 1029 | High | 5.3655 | Ql4i_0012 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Ql4i_roadmap.graphml](Ql4i_roadmap.graphml), [Ql4i_roadmap.json](Ql4i_roadmap.json), [Ql4i_roadmap.png](Ql4i_roadmap.png), [Ql4i_roadmap.svg](Ql4i_roadmap.svg), [Ql4i_roadmap.yaml](Ql4i_roadmap.yaml)
