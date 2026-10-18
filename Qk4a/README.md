# Qk4a: individual poses with shared group actions

![Roadmap](Qk4a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Qk4a_0021 | 6.39% | 639 | 0 |
| 1 | Qk4a_0019 | 6.29% | 629 | 1 |
| 2 | Qk4a_0004 | 5.92% | 592 | 2 |
| 3 | Qk4a_0014 | 5.79% | 579 | 3 |
| 4 | Qk4a_0010 | 5.71% | 571 | 4 |
| 5 | Qk4a_0006 | 5.7% | 570 | 5 |
| 6 | Qk4a_0024 | 5.68% | 568 | 6 |
| 7 | Qk4a_0007 | 4.78% | 478 | 7 |
| 8 | Qk4a_0001 | 4.03% | 403 | 8 |
| 9 | Qk4a_0017 | 3.82% | 382 | 9 |
| 10 | Qk4a_0016 | 3.65% | 365 | 10 |
| 11 | Qk4a_0002 | 3.63% | 363 | 11 |
| 12 | Qk4a_0018 | 3.59% | 359 | 12 |
| 13 | Qk4a_0020 | 3.58% | 358 | 13 |
| 14 | Qk4a_0003 | 3.52% | 352 | 14 |
| 15 | Qk4a_0013 | 3.48% | 348 | 15 |
| 16 | Qk4a_0025 | 3.44% | 344 | 16 |
| 17 | Qk4a_0022 | 3.4% | 340 | 17 |
| 18 | Qk4a_0015 | 3.24% | 324 | 18 |
| 19 | Qk4a_0009 | 3.08% | 308 | 19 |
| 20 | Qk4a_0005 | 2.85% | 285 | 20 |
| 21 | Qk4a_0023 | 2.82% | 282 | 21 |
| 22 | Qk4a_0011 | 2.56% | 256 | 22 |
| 23 | Qk4a_0012 | 2.53% | 253 | 23 |

24 individual poses in 24 groups. Candidate group reachability: **552/552**; Cartesian-only: **552/552**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
