# Df2i: individual poses with shared group actions

![Roadmap](Df2i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Df2i_0001 | 18.33% | 1833 | A |
| 1 | Df2i_0004 | 17.94% | 1794 | B |
| 2 | Df2i_0005 | 17.85% | 1785 | C |
| 3 | Df2i_0002 | 17.17% | 1717 | D |
| 4 | Df2i_0007 | 14.45% | 1445 | E |
| 5 | Df2i_0006 | 14% | 1400 | F |

6 individual poses in 6 groups. Candidate group reachability: **30/30**; Cartesian-only: **30/30**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and straight arrows.
