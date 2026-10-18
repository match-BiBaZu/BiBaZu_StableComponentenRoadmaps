# Dk4i: individual poses with shared group actions

![Roadmap](Dk4i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Dk4i_0003 | 6.33% | 633 | 1 |
| 1 | Dk4i_0009 | 6.09% | 609 | 0 |
| 2 | Dk4i_0006 | 5.84% | 584 | 2 |
| 3 | Dk4i_0015 | 5.52% | 552 | 6 |
| 4 | Dk4i_0023 | 5.41% | 541 | 4 |
| 5 | Dk4i_0010 | 5.02% | 502 | 5 |
| 6 | Dk4i_0022 | 4.95% | 495 | 3 |
| 7 | Dk4i_0017 | 4.56% | 456 | 7 |
| 8 | Dk4i_0016 | 4.45% | 445 | 8 |
| 9 | Dk4i_0008 | 4.4% | 440 | 9 |
| 10 | Dk4i_0020 | 4.25% | 425 | 3 |
| 11 | Dk4i_0007 | 4.05% | 405 | 10 |
| 12 | Dk4i_0014 | 4.05% | 405 | 11 |
| 13 | Dk4i_0012 | 4.03% | 403 | 5 |
| 14 | Dk4i_0021 | 3.7% | 370 | 4 |
| 15 | Dk4i_0011 | 3.66% | 366 | 0 |
| 16 | Dk4i_0004 | 3.6% | 360 | 2 |
| 17 | Dk4i_0001 | 3.25% | 325 | 12 |
| 18 | Dk4i_0005 | 3.15% | 315 | 1 |
| 19 | Dk4i_0002 | 2.81% | 281 | 13 |
| 20 | Dk4i_0024 | 2.8% | 280 | 14 |
| 21 | Dk4i_0013 | 2.75% | 275 | 15 |
| 22 | Dk4i_0019 | 2.68% | 268 | 16 |
| 23 | Dk4i_0018 | 2.64% | 264 | 17 |

24 individual poses in 18 groups. Candidate group reachability: **306/306**; Cartesian-only: **306/306**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
