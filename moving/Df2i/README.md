# Df2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Df2i_0004 | 19.12% | 1912 | Resistant | 7.7883 | Df2i_0002 |
| 1 | Df2i_0005 | 19.01% | 1901 | Resistant | 7.7850 | Df2i_0001 |
| 2 | Df2i_0002 | 17.75% | 1775 | Resistant | 7.7835 | Df2i_0004 |
| 3 | Df2i_0001 | 17.19% | 1719 | Resistant | 7.7854 | Df2i_0005 |
| 4 | Df2i_0008 | 14.13% | 1413 | Resistant | 9.1103 | Df2i_0007 |
| 5 | Df2i_0007 | 12.67% | 1267 | Resistant | 9.1094 | Df2i_0008 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Df2i_roadmap.graphml](Df2i_roadmap.graphml), [Df2i_roadmap.json](Df2i_roadmap.json), [Df2i_roadmap.png](Df2i_roadmap.png), [Df2i_roadmap.svg](Df2i_roadmap.svg), [Df2i_roadmap.yaml](Df2i_roadmap.yaml)
