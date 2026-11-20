# Qf1i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Qf1i_0002 | 26.49% | 2649 | High | 13.0970 | Qf1i_0006 |
| 1 | Qf1i_0005 | 25.91% | 2591 | High | 12.9804 | Qf1i_0002 |
| 2 | Qf1i_0006 | 24.98% | 2498 | High | 13.0960 | Qf1i_0002 |
| 3 | Qf1i_0001 | 22.34% | 2234 | High | 12.9778 | Qf1i_0002 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Qf1i_roadmap.graphml](Qf1i_roadmap.graphml), [Qf1i_roadmap.json](Qf1i_roadmap.json), [Qf1i_roadmap.png](Qf1i_roadmap.png), [Qf1i_roadmap.svg](Qf1i_roadmap.svg), [Qf1i_roadmap.yaml](Qf1i_roadmap.yaml)
