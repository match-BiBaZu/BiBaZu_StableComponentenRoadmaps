# Rk2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rk2i_0008 | 17.33% | 1733 | Resistant | 5.0646 | Rk2i_0004 |
| 1 | Rk2i_0004 | 16.25% | 1625 | Resistant | 5.0627 | Rk2i_0008 |
| 2 | Rk2i_0007 | 16.08% | 1608 | Resistant | 4.9870 | Rk2i_0008 |
| 3 | Rk2i_0002 | 15.2% | 1520 | Resistant | 4.9856 | Rk2i_0008 |
| 4 | Rk2i_0005 | 6.37% | 637 | Resistant | 2.1421 | Rk2i_0008 |
| 5 | Rk2i_0006 | 6.16% | 616 | Resistant | 2.1401 | Rk2i_0007 |
| 6 | Rk2i_0010 | 5.98% | 598 | Resistant | 2.1401 | Rk2i_0004 |
| 7 | Rk2i_0009 | 5.96% | 596 | Resistant | 2.1418 | Rk2i_0002 |
| 8 | Rk2i_0011 | 2.85% | 285 | Resistant | 1.1905 | Rk2i_0004 |
| 9 | Rk2i_0003 | 2.75% | 275 | Resistant | 1.1916 | Rk2i_0008 |
| 10 | Rk2i_0012 | 2.55% | 255 | Resistant | 1.1906 | Rk2i_0008 |
| 11 | Rk2i_0001 | 2.49% | 249 | Resistant | 1.1877 | Rk2i_0011 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rk2i_roadmap.graphml](Rk2i_roadmap.graphml), [Rk2i_roadmap.json](Rk2i_roadmap.json), [Rk2i_roadmap.png](Rk2i_roadmap.png), [Rk2i_roadmap.svg](Rk2i_roadmap.svg), [Rk2i_roadmap.yaml](Rk2i_roadmap.yaml)
