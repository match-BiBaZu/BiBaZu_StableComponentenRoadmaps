# Dl1a

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Stability | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 4 | Dl1a_0002 | 1.71% | 171 | High | 0.9259 | Dl1a_0001 (within group) |
| 5 | Dl1a_0016 | 1.24% | 124 | High | 0.9277 | Dl1a_0015 (within group) |
| 0 | Dl1a_0006 | 25.04% | 2504 | Medium | 0.4726 | Dl1a_0005 (within group) |
| 1 | Dl1a_0007 | 24.75% | 2475 | Medium | 0.4756 | Dl1a_0004 (within group) |
| 2 | Dl1a_0005 | 22.77% | 2277 | Medium | 0.4752 | Dl1a_0006 (within group) |
| 3 | Dl1a_0004 | 22.37% | 2237 | Medium | 0.4738 | Dl1a_0007 (within group) |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. High: at least 0.5 mm; Medium: 0.1–below 0.5 mm; Low: below 0.1 mm. Ratings are published by DropSim after grouping. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dl1a_roadmap.graphml](Dl1a_roadmap.graphml), [Dl1a_roadmap.json](Dl1a_roadmap.json), [Dl1a_roadmap.png](Dl1a_roadmap.png), [Dl1a_roadmap.svg](Dl1a_roadmap.svg), [Dl1a_roadmap.yaml](Dl1a_roadmap.yaml)
