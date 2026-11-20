# Dl4a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Dl4a_0006 | 15.79% | 1579 | High | 1.0269 | Dl4a_0004 (within group) |
| 1 | Dl4a_0021 | 15.74% | 1574 | High | 1.0263 | Dl4a_0022 (within group) |
| 2 | Dl4a_0011 | 15.53% | 1553 | High | 1.0276 | Dl4a_0010 (within group) |
| 3 | Dl4a_0003 | 15.52% | 1552 | High | 1.0224 | Dl4a_0005 (within group) |
| 4 | Dl4a_0023 | 8.26% | 826 | Medium | 0.3885 | Dl4a_0020 (within group) |
| 5 | Dl4a_0012 | 8.16% | 816 | Medium | 0.3952 | Dl4a_0009 (within group) |
| 6 | Dl4a_0009 | 8.14% | 814 | Medium | 0.3896 | Dl4a_0012 (within group) |
| 7 | Dl4a_0020 | 7.8% | 780 | Medium | 0.3929 | Dl4a_0023 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dl4a_roadmap.graphml](Dl4a_roadmap.graphml), [Dl4a_roadmap.json](Dl4a_roadmap.json), [Dl4a_roadmap.png](Dl4a_roadmap.png), [Dl4a_roadmap.svg](Dl4a_roadmap.svg), [Dl4a_roadmap.yaml](Dl4a_roadmap.yaml)
