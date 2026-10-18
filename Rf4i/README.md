# Rf4i: individual poses with shared group actions

![Roadmap](Rf4i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Rf4i_0008 | 10.61% | 1061 | 0 |
| 1 | Rf4i_0005 | 10.52% | 1052 | 1 |
| 2 | Rf4i_0015 | 8.16% | 816 | 2 |
| 3 | Rf4i_0003 | 7.76% | 776 | 3 |
| 4 | Rf4i_0006 | 6.16% | 616 | 4 |
| 5 | Rf4i_0010 | 5.71% | 571 | 5 |
| 6 | Rf4i_0016 | 5.57% | 557 | 6 |
| 7 | Rf4i_0011 | 5.5% | 550 | 7 |
| 8 | Rf4i_0002 | 5.44% | 544 | 8 |
| 9 | Rf4i_0013 | 5.44% | 544 | 9 |
| 10 | Rf4i_0009 | 4.99% | 499 | 10 |
| 11 | Rf4i_0004 | 4.96% | 496 | 11 |
| 12 | Rf4i_0020 | 4.69% | 469 | 12 |
| 13 | Rf4i_0012 | 4.66% | 466 | 13 |
| 14 | Rf4i_0014 | 4.43% | 443 | 14 |
| 15 | Rf4i_0001 | 3.96% | 396 | 15 |

16 individual poses in 16 groups. Candidate group reachability: **240/240**; Cartesian-only: **240/240**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
