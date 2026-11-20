# Dl2i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Dl2i_0007 | 20.28% | 2028 | Resistant | 0.6309 | Dl2i_0008 (within group) |
| 1 | Dl2i_0012 | 19.83% | 1983 | Resistant | 0.6279 | Dl2i_0011 (within group) |
| 2 | Dl2i_0003 | 19.18% | 1918 | Marginal | 0.3600 | Dl2i_0004 (within group) |
| 3 | Dl2i_0004 | 18.33% | 1833 | Marginal | 0.3587 | Dl2i_0003 (within group) |
| 4 | Dl2i_0011 | 9.47% | 947 | Marginal | 0.2327 | Dl2i_0012 (within group) |
| 5 | Dl2i_0008 | 8.96% | 896 | Marginal | 0.2328 | Dl2i_0007 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dl2i_roadmap.graphml](Dl2i_roadmap.graphml), [Dl2i_roadmap.json](Dl2i_roadmap.json), [Dl2i_roadmap.png](Dl2i_roadmap.png), [Dl2i_roadmap.svg](Dl2i_roadmap.svg), [Dl2i_roadmap.yaml](Dl2i_roadmap.yaml)
