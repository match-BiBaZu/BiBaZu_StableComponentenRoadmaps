# Rf3a: exact source pose to destination group

![Roadmap](Rf3a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Rf3a_0001 | 18.43% | 1843 | A |
| 1 | Rf3a_0009 | 15.69% | 1569 | B |
| 2 | Rf3a_0012 | 15.19% | 1519 | C |
| 3 | Rf3a_0002 | 13.72% | 1372 | D |
| 4 | Rf3a_0003 | 13.63% | 1363 | E |
| 5 | Rf3a_0006 | 11.91% | 1191 | F |
| 6 | Rf3a_0011 | 4.35% | 435 | G |
| 7 | Rf3a_0007 | 4.27% | 427 | H |
| 8 | Rf3a_0013 | 1.18% | 118 | I |

9 individual poses in 9 groups. Exact-source pose-to-group reachability: **72/72**; **47** pairs have direct candidates.

Each transition starts at an exact individual pose and accepts any qualifying member of its destination group. Actions from other source members are not inherited. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Routes continue automatically only through singleton arrival groups; a multi-member arrival requires another exact pose observation. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and horizontal, vertical or 45° arrow segments. Arrows attach to pose borders and destination-group borders.

Changed export hashes require explicit reimport. Former group-wide choices need fresh exact-source qualification. The previous export is preserved in `history/before_pose_to_group_74fcb40.json.gz`.
