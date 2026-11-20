# Rl2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rl2i_0004 | 26.79% | 2679 | Resistant | 4.8819 | Rl2i_0007 |
| 1 | Rl2i_0007 | 26.49% | 2649 | Resistant | 4.8817 | Rl2i_0004 |
| 2 | Rl2i_0008 | 21.3% | 2130 | Resistant | 4.5561 | Rl2i_0004 |
| 3 | Rl2i_0005 | 20.32% | 2032 | Resistant | 4.5522 | Rl2i_0007 |
| 4 | Rl2i_0002 | 1.12% | 112 | Resistant | 0.8701 | Rl2i_0007 |
| 5 | Rl2i_0003 | 1.02% | 102 | Resistant | 0.8712 | Rl2i_0008 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl2i_roadmap.graphml](Rl2i_roadmap.graphml), [Rl2i_roadmap.json](Rl2i_roadmap.json), [Rl2i_roadmap.png](Rl2i_roadmap.png), [Rl2i_roadmap.svg](Rl2i_roadmap.svg), [Rl2i_roadmap.yaml](Rl2i_roadmap.yaml)
