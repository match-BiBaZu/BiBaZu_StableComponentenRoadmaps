# Qf4i: individual poses with shared group actions

![Roadmap](Qf4i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Qf4i_0007 | 7.52% | 752 | 0 |
| 1 | Qf4i_0012 | 7.06% | 706 | 1 |
| 2 | Qf4i_0005 | 7.02% | 702 | 2 |
| 3 | Qf4i_0009 | 7.02% | 702 | 3 |
| 4 | Qf4i_0006 | 6.34% | 634 | 4 |
| 5 | Qf4i_0013 | 6.16% | 616 | 5 |
| 6 | Qf4i_0010 | 6.13% | 613 | 6 |
| 7 | Qf4i_0015 | 6.1% | 610 | 7 |
| 8 | Qf4i_0017 | 6.01% | 601 | 8 |
| 9 | Qf4i_0002 | 5.94% | 594 | 9 |
| 10 | Qf4i_0008 | 5.9% | 590 | 10 |
| 11 | Qf4i_0003 | 5.68% | 568 | 11 |
| 12 | Qf4i_0016 | 5.53% | 553 | 12 |
| 13 | Qf4i_0011 | 5.47% | 547 | 13 |
| 14 | Qf4i_0004 | 5.01% | 501 | 14 |
| 15 | Qf4i_0001 | 4.98% | 498 | 15 |

16 individual poses in 16 groups. Candidate group reachability: **240/240**; Cartesian-only: **240/240**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
