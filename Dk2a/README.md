# Dk2a: individual poses with shared group actions

![Roadmap](Dk2a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Dk2a_0006 | 16.94% | 1694 | A |
| 1 | Dk2a_0004 | 15.57% | 1557 | B |
| 2 | Dk2a_0002 | 7.85% | 785 | C |
| 3 | Dk2a_0015 | 7.13% | 713 | D |
| 4 | Dk2a_0014 | 6.88% | 688 | E |
| 5 | Dk2a_0007 | 6.75% | 675 | F |
| 6 | Dk2a_0016 | 6.67% | 667 | G |
| 7 | Dk2a_0013 | 6.29% | 629 | G |
| 8 | Dk2a_0005 | 5.24% | 524 | H |
| 9 | Dk2a_0003 | 5.11% | 511 | I |
| 10 | Dk2a_0012 | 4.78% | 478 | J |
| 11 | Dk2a_0011 | 4.69% | 469 | J |
| 12 | Dk2a_0001 | 2.58% | 258 | K |
| 13 | Dk2a_0009 | 1.31% | 131 | L |

14 individual poses in 12 groups. Candidate group reachability: **132/132**; Cartesian-only: **110/132**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and straight arrows.
