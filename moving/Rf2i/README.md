# Rf2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rf2i_0008 | 18.5% | 1850 | Resistant | 9.9708 | Rf2i_0003 |
| 1 | Rf2i_0009 | 17.91% | 1791 | Resistant | 10.1338 | Rf2i_0003 |
| 2 | Rf2i_0002 | 16.49% | 1649 | Resistant | 9.9691 | Rf2i_0009 |
| 3 | Rf2i_0003 | 15.41% | 1541 | Resistant | 10.1341 | Rf2i_0009 |
| 4 | Rf2i_0013 | 8.53% | 853 | Resistant | 4.8243 | Rf2i_0008 |
| 5 | Rf2i_0004 | 7.95% | 795 | Resistant | 4.3890 | Rf2i_0007 |
| 6 | Rf2i_0014 | 7.17% | 717 | Resistant | 4.3902 | Rf2i_0012 |
| 7 | Rf2i_0001 | 7.15% | 715 | Resistant | 4.8257 | Rf2i_0002 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rf2i_roadmap.graphml](Rf2i_roadmap.graphml), [Rf2i_roadmap.json](Rf2i_roadmap.json), [Rf2i_roadmap.png](Rf2i_roadmap.png), [Rf2i_roadmap.svg](Rf2i_roadmap.svg), [Rf2i_roadmap.yaml](Rf2i_roadmap.yaml)
