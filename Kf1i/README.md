# Kf1i

Observed simulation poses measured **after the belt stopped**; geometry supplies untested direct connection candidates.

Source: `BiBaZu_StableComponentenPoses` branch `main`, commit `0006791c9f77c2359f04abf01035d9d78e18d456`, `Kf1i/poses_after_stop.json` and `pose_registry_after_stop.json`. The moving-belt `poses.json` contains no settled poses.

The four poses represent 9445 settled outcomes from 10000 completed drop trials. Frequencies use all 10000 trials, including 84 unsettled and 471 missing stop observations; they are not rescaled to settled outcomes.

Minimum frequency: **1%**. Percentages retain the source denominator.

| Roadmap pose | Source pose | Frequency | Count |
| ---: | --- | ---: | ---: |
| 0 | Kf1i_stop_0001 | 29.25% | 2925 |
| 1 | Kf1i_stop_0004 | 26.94% | 2694 |
| 2 | Kf1i_stop_0002 | 19.2% | 1920 |
| 3 | Kf1i_stop_0003 | 19.06% | 1906 |

The legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.

Original inputs are in `source/`; generation settings and exclusions are in `manifest.json`.

Files: [Kf1i_roadmap.graphml](Kf1i_roadmap.graphml), [Kf1i_roadmap.json](Kf1i_roadmap.json), [Kf1i_roadmap.png](Kf1i_roadmap.png), [Kf1i_roadmap.svg](Kf1i_roadmap.svg), [Kf1i_roadmap.yaml](Kf1i_roadmap.yaml)
