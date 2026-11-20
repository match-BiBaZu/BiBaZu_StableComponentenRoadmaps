# Dk4i

Observed simulation poses; geometry supplies untested direct connection candidates.

Observation phase: **transport**.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count | Geometric quality | Lift to tip (mm) | Easiest target |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 0 | Dk4i_0006 | 7.59% | 759 | Marginal | 0.4652 | Dk4i_0004 (within group) |
| 1 | Dk4i_0003 | 7.23% | 723 | Marginal | 0.4679 | Dk4i_0005 (within group) |
| 2 | Dk4i_0009 | 7.06% | 706 | Marginal | 0.4668 | Dk4i_0011 (within group) |
| 3 | Dk4i_0022 | 6.98% | 698 | Marginal | 0.4658 | Dk4i_0021 (within group) |
| 4 | Dk4i_0020 | 5.38% | 538 | Marginal | 0.4036 | Dk4i_0023 (within group) |
| 5 | Dk4i_0010 | 5.09% | 509 | Marginal | 0.3996 | Dk4i_0012 (within group) |
| 6 | Dk4i_0012 | 5.09% | 509 | Marginal | 0.4042 | Dk4i_0010 (within group) |
| 7 | Dk4i_0023 | 4.91% | 491 | Marginal | 0.4044 | Dk4i_0020 (within group) |
| 8 | Dk4i_0021 | 4.52% | 452 | Marginal | 0.3137 | Dk4i_0022 (within group) |
| 9 | Dk4i_0011 | 4.4% | 440 | Marginal | 0.3141 | Dk4i_0009 (within group) |
| 10 | Dk4i_0004 | 4.3% | 430 | Marginal | 0.3123 | Dk4i_0006 (within group) |
| 11 | Dk4i_0005 | 3.92% | 392 | Marginal | 0.3130 | Dk4i_0003 (within group) |
| 12 | Dk4i_0017 | 3.81% | 381 | Resistant | 2.3000 | Dk4i_0006 |
| 13 | Dk4i_0015 | 3.35% | 335 | Resistant | 2.1782 | Dk4i_0005 |
| 14 | Dk4i_0007 | 3.26% | 326 | Resistant | 2.2974 | Dk4i_0003 |
| 15 | Dk4i_0014 | 3.26% | 326 | Resistant | 2.1763 | Dk4i_0011 |
| 16 | Dk4i_0016 | 2.95% | 295 | Resistant | 2.1788 | Dk4i_0021 |
| 17 | Dk4i_0008 | 2.62% | 262 | Resistant | 2.1734 | Dk4i_0004 |
| 18 | Dk4i_0002 | 2.41% | 241 | Resistant | 1.9990 | Dk4i_0022 |
| 19 | Dk4i_0018 | 2.36% | 236 | Resistant | 1.9993 | Dk4i_0003 |
| 20 | Dk4i_0013 | 2.25% | 225 | Resistant | 1.8914 | Dk4i_0011 |
| 21 | Dk4i_0001 | 2.23% | 223 | Resistant | 1.8913 | Dk4i_0015 |
| 22 | Dk4i_0019 | 2.21% | 221 | Resistant | 1.8920 | Dk4i_0004 |
| 23 | Dk4i_0024 | 1.88% | 188 | Resistant | 1.8896 | Dk4i_0021 |

[Pose quality report](pose_quality.json) includes every input pose, including those below the frequency cutoff. Fragile: below 0.1 mm; marginal: 0.1–below 0.5 mm; resistant: at least 0.5 mm. These are sampled geometric lift estimates, not measured survival probabilities. Within-group movement describes rocking in that group and does not classify the whole group as unstable. Quality does not filter or renumber poses.

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; dynamic and experimental reliability remain untested.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Dk4i_roadmap.graphml](Dk4i_roadmap.graphml), [Dk4i_roadmap.json](Dk4i_roadmap.json), [Dk4i_roadmap.png](Dk4i_roadmap.png), [Dk4i_roadmap.svg](Dk4i_roadmap.svg), [Dk4i_roadmap.yaml](Dk4i_roadmap.yaml)
