# Qf2a: individual poses with shared group actions

![Roadmap](Qf2a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Qf2a_0006 | 14.83% | 1483 | A |
| 1 | Qf2a_0013 | 13.7% | 1370 | B |
| 2 | Qf2a_0012 | 12.92% | 1292 | C |
| 3 | Qf2a_0009 | 12.47% | 1247 | D |
| 4 | Qf2a_0001 | 11.91% | 1191 | E |
| 5 | Qf2a_0005 | 11.14% | 1114 | F |
| 6 | Qf2a_0007 | 7.45% | 745 | G |
| 7 | Qf2a_0008 | 5.28% | 528 | H |
| 8 | Qf2a_0011 | 4.09% | 409 | I |
| 9 | Qf2a_0002 | 3.62% | 362 | J |

10 individual poses in 10 groups. Candidate group reachability: **90/90**; Cartesian-only: **66/90**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and straight arrows.
