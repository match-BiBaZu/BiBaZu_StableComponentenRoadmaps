# Kl1i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Kl1i_0001 | 46.96% | 4696 | High | 17.3823 | Kl1i_0003 |
| 1 | Kl1i_0006 | 45.51% | 4551 | High | 17.3813 | Kl1i_0003 |
| 2 | Kl1i_0003 | 3.81% | 381 | High | 1.0369 | Kl1i_0001 |
| 3 | Kl1i_0002 | 3.26% | 326 | High | 1.0357 | Kl1i_0001 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kl1i_roadmap.graphml](Kl1i_roadmap.graphml), [Kl1i_roadmap.json](Kl1i_roadmap.json), [Kl1i_roadmap.png](Kl1i_roadmap.png), [Kl1i_roadmap.svg](Kl1i_roadmap.svg), [Kl1i_roadmap.yaml](Kl1i_roadmap.yaml)
