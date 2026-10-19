# Qk4a: exact source pose to destination group

![Roadmap](Qk4a_roadmap.png)

Cutoff: **1%**, applied separately to original group totals and individual observation frequencies. Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.

| Pose | Original observation | Individual frequency | Count | Group |
| ---: | --- | ---: | ---: | --- |
| 0 | Qk4a_0021 | 6.39% | 639 | A |
| 1 | Qk4a_0019 | 6.29% | 629 | B |
| 2 | Qk4a_0004 | 5.92% | 592 | C |
| 3 | Qk4a_0014 | 5.79% | 579 | D |
| 4 | Qk4a_0010 | 5.71% | 571 | E |
| 5 | Qk4a_0006 | 5.7% | 570 | F |
| 6 | Qk4a_0024 | 5.68% | 568 | G |
| 7 | Qk4a_0007 | 4.78% | 478 | H |
| 8 | Qk4a_0001 | 4.03% | 403 | I |
| 9 | Qk4a_0017 | 3.82% | 382 | J |
| 10 | Qk4a_0016 | 3.65% | 365 | K |
| 11 | Qk4a_0002 | 3.63% | 363 | L |
| 12 | Qk4a_0018 | 3.59% | 359 | M |
| 13 | Qk4a_0020 | 3.58% | 358 | N |
| 14 | Qk4a_0003 | 3.52% | 352 | O |
| 15 | Qk4a_0013 | 3.48% | 348 | P |
| 16 | Qk4a_0025 | 3.44% | 344 | Q |
| 17 | Qk4a_0022 | 3.4% | 340 | R |
| 18 | Qk4a_0015 | 3.24% | 324 | S |
| 19 | Qk4a_0009 | 3.08% | 308 | T |
| 20 | Qk4a_0005 | 2.85% | 285 | U |
| 21 | Qk4a_0023 | 2.82% | 282 | V |
| 22 | Qk4a_0011 | 2.56% | 256 | W |
| 23 | Qk4a_0012 | 2.53% | 253 | X |

24 individual poses in 24 groups. Exact-source pose-to-group reachability: **552/552**; **212** pairs have direct candidates.

Each transition starts at an exact individual pose and accepts any qualifying member of its destination group. Actions from other source members are not inherited. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Routes continue automatically only through singleton arrival groups; a multi-member arrival requires another exact pose observation. Disconnected components remain disconnected.

Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.

Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.

The roadmap uses alphabetic group labels in row order (A–Z, then AA onward), numeric pose labels, and horizontal, vertical or 45° arrow segments. Arrows attach to pose borders and destination-group borders.

Changed export hashes require explicit reimport. Former group-wide choices need fresh exact-source qualification. The previous export is preserved in `history/before_pose_to_group_74fcb40.json.gz`.
