# Df1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Df1a_0004 | 29.75% | 2975 | Resistant | 9.1844 | Df1a_0001 |
| 1 | Df1a_0007 | 27.15% | 2715 | Resistant | 9.1876 | Df1a_0010 |
| 2 | Df1a_0010 | 22.4% | 2240 | Resistant | 6.1817 | Df1a_0007 |
| 3 | Df1a_0001 | 20.3% | 2030 | Resistant | 6.1833 | Df1a_0004 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Df1a_roadmap.graphml](Df1a_roadmap.graphml), [Df1a_roadmap.json](Df1a_roadmap.json), [Df1a_roadmap.png](Df1a_roadmap.png), [Df1a_roadmap.svg](Df1a_roadmap.svg), [Df1a_roadmap.yaml](Df1a_roadmap.yaml)
