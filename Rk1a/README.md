# Rk1a: exact source pose to destination group

![Roadmap](Rk1a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Rk1a_0034 | 7.17% | 717 | A |
| 1 | Rk1a_0026 | 6.56% | 656 | B |
| 2 | Rk1a_0011 | 6.4% | 640 | C |
| 3 | Rk1a_0008 | 6.23% | 623 | D |
| 4 | Rk1a_0010 | 6.04% | 604 | E |
| 5 | Rk1a_0033 | 5.76% | 576 | F |
| 6 | Rk1a_0007 | 3.91% | 391 | G |
| 7 | Rk1a_0022 | 3.85% | 385 | H |
| 8 | Rk1a_0004 | 3.45% | 345 | I |
| 9 | Rk1a_0003 | 3.21% | 321 | J |
| 10 | Rk1a_0035 | 3.19% | 319 | K |
| 11 | Rk1a_0037 | 3.16% | 316 | L |
| 12 | Rk1a_0019 | 2.67% | 267 | M |
| 13 | Rk1a_0006 | 2.57% | 257 | G |
| 14 | Rk1a_0042 | 2.44% | 244 | N |
| 15 | Rk1a_0024 | 2.43% | 243 | O |
| 16 | Rk1a_0001 | 2.38% | 238 | P |
| 17 | Rk1a_0021 | 2.36% | 236 | Q |
| 18 | Rk1a_0030 | 2.29% | 229 | R |
| 19 | Rk1a_0025 | 2.23% | 223 | S |
| 20 | Rk1a_0005 | 2.18% | 218 | T |
| 21 | Rk1a_0023 | 2.18% | 218 | U |
| 22 | Rk1a_0028 | 2.05% | 205 | V |
| 23 | Rk1a_0031 | 2.05% | 205 | H |
| 24 | Rk1a_0009 | 1.89% | 189 | W |
| 25 | Rk1a_0017 | 1.81% | 181 | X |
| 26 | Rk1a_0013 | 1.55% | 155 | X |
| 27 | Rk1a_0012 | 1.52% | 152 | W |
| 28 | Rk1a_0027 | 1.27% | 127 | V |
| 29 | Rk1a_0020 | 1.26% | 126 | M |

30 individual poses in 24 groups. Exact-source pose-to-group reachability: **690/690**; **244** pairs have direct candidates.

Each transition starts at an exact individual pose and accepts any qualifying member of its destination group. Actions from other source members are not inherited. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Routes continue automatically only through singleton arrival groups; a multi-member arrival requires another exact pose observation. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and horizontal, vertical or 45° arrow segments. Arrows attach to pose borders and destination-group borders.

Changed export hashes require explicit reimport. Former group-wide choices need fresh exact-source qualification. The previous export is preserved in `history/before_pose_to_group_74fcb40.json.gz`.
