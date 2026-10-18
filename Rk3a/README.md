# Rk3a: individual poses with shared group actions

![Roadmap](Rk3a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Rk3a_0014 | 13.49% | 1349 | 0 |
| 1 | Rk3a_0012 | 12.67% | 1267 | 2 |
| 2 | Rk3a_0010 | 11.09% | 1109 | 1 |
| 3 | Rk3a_0004 | 10.53% | 1053 | 3 |
| 4 | Rk3a_0003 | 10.35% | 1035 | 4 |
| 5 | Rk3a_0009 | 10.27% | 1027 | 5 |
| 6 | Rk3a_0002 | 8.99% | 899 | 6 |
| 7 | Rk3a_0008 | 8.49% | 849 | 7 |
| 8 | Rk3a_0011 | 4.26% | 426 | 8 |
| 9 | Rk3a_0013 | 4.09% | 409 | 9 |
| 10 | Rk3a_0007 | 2.01% | 201 | 1 |
| 11 | Rk3a_0006 | 1.62% | 162 | 3 |
| 12 | Rk3a_0001 | 1.33% | 133 | 10 |

13 individual poses in 11 groups. Candidate group reachability: **110/110**; Cartesian-only: **110/110**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
