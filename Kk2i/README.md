# Kk2i: individual poses with shared group actions

![Roadmap](Kk2i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Kk2i_0018 | 20.23% | 2023 | 0 |
| 1 | Kk2i_0017 | 8.33% | 833 | 1 |
| 2 | Kk2i_0003 | 7.73% | 773 | 2 |
| 3 | Kk2i_0004 | 6.61% | 661 | 3 |
| 4 | Kk2i_0024 | 3.21% | 321 | 4 |
| 5 | Kk2i_0026 | 3.15% | 315 | 5 |
| 6 | Kk2i_0015 | 2.53% | 253 | 7 |
| 7 | Kk2i_0021 | 2.53% | 253 | 8 |
| 8 | Kk2i_0016 | 2.46% | 246 | 9 |
| 9 | Kk2i_0029 | 2.42% | 242 | 10 |
| 10 | Kk2i_0030 | 2.42% | 242 | 11 |
| 11 | Kk2i_0020 | 2.36% | 236 | 12 |
| 12 | Kk2i_0028 | 2.36% | 236 | 13 |
| 13 | Kk2i_0022 | 2.33% | 233 | 14 |
| 14 | Kk2i_0019 | 2.23% | 223 | 15 |
| 15 | Kk2i_0005 | 2.1% | 210 | 16 |
| 16 | Kk2i_0006 | 2.09% | 209 | 17 |
| 17 | Kk2i_0008 | 1.84% | 184 | 18 |
| 18 | Kk2i_0010 | 1.65% | 165 | 19 |
| 19 | Kk2i_0027 | 1.23% | 123 | 6 |

20 individual poses in 20 groups. Candidate group reachability: **116/380**; Cartesian-only: **113/380**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
