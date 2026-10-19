# Qk2i: exact source pose to destination group

![Roadmap](Qk2i_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Qk2i_0004 | 11.88% | 1188 | A |
| 1 | Qk2i_0012 | 11.47% | 1147 | B |
| 2 | Qk2i_0011 | 11.45% | 1145 | C |
| 3 | Qk2i_0006 | 11.13% | 1113 | D |
| 4 | Qk2i_0003 | 7.12% | 712 | E |
| 5 | Qk2i_0015 | 7.05% | 705 | F |
| 6 | Qk2i_0005 | 6.72% | 672 | G |
| 7 | Qk2i_0009 | 6.67% | 667 | H |
| 8 | Qk2i_0002 | 6.44% | 644 | I |
| 9 | Qk2i_0001 | 6.43% | 643 | J |
| 10 | Qk2i_0010 | 6.22% | 622 | K |
| 11 | Qk2i_0014 | 5.75% | 575 | L |
| 12 | Qk2i_0013 | 1.25% | 125 | M |

13 individual poses in 13 groups. Exact-source pose-to-group reachability: **144/156**; **74** pairs have direct candidates.

Each transition starts at an exact individual pose and accepts any qualifying member of its destination group. Actions from other source members are not inherited. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Routes continue automatically only through singleton arrival groups; a multi-member arrival requires another exact pose observation. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and horizontal, vertical or 45° arrow segments. Arrows attach to pose borders and destination-group borders.

Changed export hashes require explicit reimport. Former group-wide choices need fresh exact-source qualification. The previous export is preserved in `history/before_pose_to_group_74fcb40.json.gz`.
