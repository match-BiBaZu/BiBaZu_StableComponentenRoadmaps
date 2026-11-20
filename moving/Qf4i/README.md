# Qf4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Qf4i_0011 | 7.81% | 781 | Resistant | 11.4529 | Qf4i_0006 |
| 1 | Qf4i_0006 | 7.7% | 770 | Resistant | 11.4563 | Qf4i_0011 |
| 2 | Qf4i_0015 | 7.21% | 721 | Resistant | 11.4533 | Qf4i_0013 |
| 3 | Qf4i_0007 | 6.76% | 676 | Resistant | 11.1003 | Qf4i_0011 |
| 4 | Qf4i_0013 | 6.76% | 676 | Resistant | 11.4539 | Qf4i_0015 |
| 5 | Qf4i_0018 | 6.6% | 660 | Resistant | 11.4554 | Qf4i_0021 |
| 6 | Qf4i_0021 | 6.42% | 642 | Resistant | 11.4555 | Qf4i_0018 |
| 7 | Qf4i_0003 | 6.21% | 621 | Resistant | 11.0992 | Qf4i_0006 |
| 8 | Qf4i_0012 | 5.96% | 596 | Resistant | 11.0964 | Qf4i_0013 |
| 9 | Qf4i_0002 | 5.89% | 589 | Resistant | 11.4540 | Qf4i_0010 |
| 10 | Qf4i_0017 | 5.89% | 589 | Resistant | 11.0970 | Qf4i_0021 |
| 11 | Qf4i_0014 | 5.79% | 579 | Resistant | 11.0962 | Qf4i_0015 |
| 12 | Qf4i_0009 | 5.69% | 569 | Resistant | 11.0976 | Qf4i_0018 |
| 13 | Qf4i_0010 | 5.48% | 548 | Resistant | 11.4572 | Qf4i_0002 |
| 14 | Qf4i_0004 | 4.89% | 489 | Resistant | 11.0957 | Qf4i_0010 |
| 15 | Qf4i_0001 | 4.77% | 477 | Resistant | 11.0964 | Qf4i_0002 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Qf4i_roadmap.graphml](Qf4i_roadmap.graphml), [Qf4i_roadmap.json](Qf4i_roadmap.json), [Qf4i_roadmap.png](Qf4i_roadmap.png), [Qf4i_roadmap.svg](Qf4i_roadmap.svg), [Qf4i_roadmap.yaml](Qf4i_roadmap.yaml)
