# Rl3a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rl3a_0019 | 25.94% | 2594 | Resistant | 4.6870 | Rl3a_0020 |
| 1 | Rl3a_0016 | 24.77% | 2477 | Resistant | 4.6843 | Rl3a_0015 |
| 2 | Rl3a_0012 | 21.01% | 2101 | Resistant | 2.0613 | Rl3a_0010 |
| 3 | Rl3a_0004 | 19.1% | 1910 | Resistant | 2.0556 | Rl3a_0008 |
| 4 | Rl3a_0003 | 1.49% | 149 | Resistant | 0.7653 | Rl3a_0007 |
| 5 | Rl3a_0006 | 1.33% | 133 | Resistant | 0.7612 | Rl3a_0007 (within group) |
| 6 | Rl3a_0014 | 1.22% | 122 | Resistant | 0.7643 | Rl3a_0004 |
| 7 | Rl3a_0010 | 1.06% | 106 | Marginal | 0.1454 | Rl3a_0012 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rl3a_roadmap.graphml](Rl3a_roadmap.graphml), [Rl3a_roadmap.json](Rl3a_roadmap.json), [Rl3a_roadmap.png](Rl3a_roadmap.png), [Rl3a_roadmap.svg](Rl3a_roadmap.svg), [Rl3a_roadmap.yaml](Rl3a_roadmap.yaml)
