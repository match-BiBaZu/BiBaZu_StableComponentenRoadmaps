# Rk2i: individual poses with shared group actions

![Roadmap](Rk2i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Rk2i_0009 | 13.42% | 1342 | A |
| 1 | Rk2i_0010 | 12.98% | 1298 | B |
| 2 | Rk2i_0003 | 12.97% | 1297 | C |
| 3 | Rk2i_0006 | 12.55% | 1255 | D |
| 4 | Rk2i_0002 | 8.18% | 818 | E |
| 5 | Rk2i_0008 | 7.51% | 751 | F |
| 6 | Rk2i_0005 | 7.08% | 708 | G |
| 7 | Rk2i_0007 | 7.07% | 707 | H |
| 8 | Rk2i_0001 | 4.74% | 474 | I |
| 9 | Rk2i_0012 | 4.72% | 472 | J |
| 10 | Rk2i_0004 | 4.52% | 452 | K |
| 11 | Rk2i_0011 | 4.25% | 425 | L |

12 individual poses in 12 groups. Candidate group reachability: **132/132**; Cartesian-only: **132/132**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and straight arrows.
