# Dk1i: exact source pose to destination group

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

8 individual poses in 6 groups. The exports contain **39/40 direct pose-to-group connections** and **40/40 reachable pose-to-group pairs** using finished routes. The picture labels the preferred action for each direct connection. Group-projection connectivity is an overview, not evidence of source-pose applicability.

Each arrow starts at an **exact individual source pose** and ends at a **destination group boundary**. Its command is witnessed from that source pose; an action from another source-group member is not inherited. Any qualifying destination member satisfies the target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Multi-step routes use retained single-axis actions and continue only through singleton arrival groups. An uncertain arrival in a multi-member group needs another exact pose observation before departing. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. Group-only recognition cannot qualify an exact source pose in a multi-member group; runtime must report the missing observation instead of executing a member-specific action. See `manifest.json` and `files.sha256.json`.
