# Ql1i: individual poses with shared group actions

![Roadmap](Ql1i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
|---:|---|---:|---:|---:|
| 0 | Ql1i_0002 | 45.44% | 4544 | 0 |
| 1 | Ql1i_0003 | 43.76% | 4376 | 1 |
| 2 | Ql1i_0004 | 5.32% | 532 | 2 |
| 3 | Ql1i_0005 | 2.66% | 266 | 3 |
| 4 | Ql1i_0006 | 2.28% | 228 | 4 |

5 individual poses in 5 groups. Candidate group reachability: **20/20**; Cartesian-only: **20/20**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.
