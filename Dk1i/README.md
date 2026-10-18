# Dk1i: individual poses with shared group actions

![Roadmap](Dk1i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Dk1i_0007 | 16.43% | 1643 | 2 |
| 1 | Dk1i_0002 | 14.87% | 1487 | 1 |
| 2 | Dk1i_0005 | 14.39% | 1439 | 0 |
| 3 | Dk1i_0006 | 14.28% | 1428 | 3 |
| 4 | Dk1i_0003 | 13.38% | 1338 | 0 |
| 5 | Dk1i_0004 | 12.15% | 1215 | 1 |
| 6 | Dk1i_0001 | 7.45% | 745 | 4 |
| 7 | Dk1i_0008 | 7.03% | 703 | 5 |

8 individual poses in 6 groups. Candidate group reachability: **30/30**; Cartesian-only: **30/30**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
