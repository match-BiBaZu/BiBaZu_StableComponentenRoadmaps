# Ql4i: exact source pose to destination group

![Roadmap](Ql4i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Ql4i_0012 | 12.66% | 1266 | A |
| 1 | Ql4i_0019 | 12.08% | 1208 | B |
| 2 | Ql4i_0018 | 11.9% | 1190 | C |
| 3 | Ql4i_0013 | 11.78% | 1178 | D |
| 4 | Ql4i_0003 | 11.1% | 1110 | E |
| 5 | Ql4i_0008 | 10.42% | 1042 | F |
| 6 | Ql4i_0002 | 10.4% | 1040 | G |
| 7 | Ql4i_0006 | 10.01% | 1001 | H |
| 8 | Ql4i_0022 | 1.24% | 124 | I |
| 9 | Ql4i_0017 | 1.22% | 122 | J |
| 10 | Ql4i_0011 | 1.14% | 114 | K |
| 11 | Ql4i_0020 | 1.1% | 110 | L |

12 individual poses in 12 groups. Exact-source pose-to-group reachability: **132/132**; **68** pairs have direct candidates.

Each transition starts at an exact individual pose and accepts any qualifying member of its destination group. Actions from other source members are not inherited. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Routes continue automatically only through singleton arrival groups; a multi-member arrival requires another exact pose observation. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and horizontal, vertical or 45° arrow segments. Arrows attach to pose borders and destination-group borders.

Changed export hashes require explicit reimport. Former group-wide choices need fresh exact-source qualification. The previous export is preserved in `history/before_pose_to_group_74fcb40.json.gz`.
