# Dl4a: individual poses with shared group actions

![Roadmap](Dl4a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Dl4a_0004 | 16.11% | 1611 | A |
| 1 | Dl4a_0011 | 15.41% | 1541 | B |
| 2 | Dl4a_0002 | 15.03% | 1503 | C |
| 3 | Dl4a_0021 | 14.7% | 1470 | D |
| 4 | Dl4a_0022 | 8.16% | 816 | E |
| 5 | Dl4a_0009 | 7.97% | 797 | F |
| 6 | Dl4a_0010 | 7.3% | 730 | F |
| 7 | Dl4a_0024 | 7.17% | 717 | E |

8 individual poses in 6 groups. Candidate group reachability: **30/30**; Cartesian-only: **30/30**.

Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and straight arrows.
