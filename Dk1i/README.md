# Dk1i — grouped roadmap

![Whole-group roadmap](Dk1i_roadmap.png)

Updated on 2026-10-18 from **10,000 drops using the simulator main-branch GUI parameters**.
The six groups, their eight members, representative orientations, thumbnails, stable group keys and existing 16 direct connections are unchanged. Frequencies reflect the new run.

| Group | Representative source pose | Members | Frequency | Count |
| ---: | --- | --- | ---: | ---: |
| 0 | Dk1i_0005 | Dk1i_0003, Dk1i_0005 | 27.77% | 2777 |
| 1 | Dk1i_0002 | Dk1i_0002, Dk1i_0004 | 27.02% | 2702 |
| 2 | Dk1i_0007 | Dk1i_0007 | 16.43% | 1643 |
| 3 | Dk1i_0006 | Dk1i_0006 | 14.28% | 1428 |
| 4 | Dk1i_0001 | Dk1i_0001 | 7.45% | 745 |
| 5 | Dk1i_0008 | Dk1i_0008 | 7.03% | 703 |

## Whole-group reorientations

All **30/30 ordered group pairs** have candidate routes using Cartesian rotations alone.
There are **46 distinct Cartesian group transfers** and **179 group transfers including other single-axis and settling alternatives**. No composite bridge is needed. The original **28 inter-group known-member actions** remain available.

Groups contain all their members. A transfer can start at any witnessed source member and reach any witnessed target member; consecutive transfers may use different members of the shared group. Member interchangeability is the planning assumption. Previews show the actual witnesses and do not invent motion between intermediate members.

Exact **±90° and ±180° chute X/Y/Z commands** are preferred. Commands are never rounded from another rotation. Observed endpoints match within 1° under the permitted part symmetries; other Cartesian landing candidates include a sampled downhill settling path. Arrow labels show the preferred reorientation; all alternatives, witnesses, competing outcomes and settling evidence are retained in the exports.

These candidates are **geometry_only**. Contact feasibility and physical settling reliability are unverified. Execution requires an assigned pressure profile explicitly **calibrated for the source group**, bound to the exported transfer and stable group key. Existing profiles receive no automatic group qualification; changed file hashes require explicit reimport.

## Inputs and exports

The grouping cutoff is 1% after aggregation; no additional representative frequency cutoff is applied. Counts sum to the 9,998 drops that settled during transport; percentages retain all 10,000 completed drops as their denominator. After the belt stop all 10,000 were settled; those later observations do not replace the transport pose counts. The 584 member disturbance assessments are additional tests.

Source poses: [grouped commit 0a4d04a](https://github.com/match-BiBaZu/BiBaZu_StableComponentenPoses/tree/0a4d04a528277c30e036bde72b78c7063ba0dc33/Dk1i). Simulator main parameters: revision `82f8bd43c70a0eb160d27dc0f7232849842efe9c`. See [simulation provenance](source/simulation_provenance.json), [source validation](source/validation.json), [groups](source/groups.json), [membership](membership.csv), [retention curves](source/group_stability.csv), and [barrier evidence](source/grouping_geometry.json). Compressed raw trials remain published in the source pose repository's `Dk1i/run_data/` folder.

[JSON](Dk1i_roadmap.json), [YAML](Dk1i_roadmap.yaml), [GraphML](Dk1i_roadmap.graphml), [PNG](Dk1i_roadmap.png), [SVG](Dk1i_roadmap.svg). JSON/YAML include materialized calibration choices, commands, previews and routes in **consumer-export version 2**, with previous choice and route identities retained for profile restoration. Controls consume these records without constructing routes. Generation settings and provenance are in [manifest.json](manifest.json); byte checksums are in [files.sha256.json](files.sha256.json). The legacy `robust` compatibility tag does not assert analytical robustness.
