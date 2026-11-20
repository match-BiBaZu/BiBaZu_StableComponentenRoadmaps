# Rf3a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Rf3a_0014 | 17.63% | 1763 | High | 10.9703 | Rf3a_0005 |
| 1 | Rf3a_0001 | 16.88% | 1688 | High | 10.9728 | Rf3a_0005 |
| 2 | Rf3a_0004 | 15.78% | 1578 | High | 10.9694 | Rf3a_0008 |
| 3 | Rf3a_0016 | 15.49% | 1549 | High | 10.9699 | Rf3a_0008 |
| 4 | Rf3a_0005 | 14.01% | 1401 | High | 5.3147 | Rf3a_0013 |
| 5 | Rf3a_0008 | 11.93% | 1193 | High | 5.3168 | Rf3a_0012 |
| 6 | Rf3a_0015 | 4.18% | 418 | High | 4.6501 | Rf3a_0013 |
| 7 | Rf3a_0011 | 3.05% | 305 | High | 4.6489 | Rf3a_0012 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Rf3a_roadmap.graphml](Rf3a_roadmap.graphml), [Rf3a_roadmap.json](Rf3a_roadmap.json), [Rf3a_roadmap.png](Rf3a_roadmap.png), [Rf3a_roadmap.svg](Rf3a_roadmap.svg), [Rf3a_roadmap.yaml](Rf3a_roadmap.yaml)
