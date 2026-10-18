# BiBaZu grouped roadmaps: individual poses

The grouped catalogue displays **individual observed poses**, numbered from 0 by descending individual frequency, inside coloured group boundaries. Group identities are separate from pose numbers.

## Filtering and planning

The current rollout uses **1%** for both the original group total and each individual pose. Exactly the cutoff qualifies. Percentages retain the original completed-trial denominator; they are not renormalized after filtering. Members below the cutoff are neither shown nor used as transfer witnesses. Groups without any qualifying member are omitted. Full observations and memberships remain in each component's `source/` folder.

Any outgoing action witnessed by a qualifying member is shared by all displayed members of its source group. Any qualifying destination member satisfies the target group. **There are no internal group transitions. A target in the current group is already satisfied and requires no actuation.** Intermediate legs may use different witnesses, with no invented movement between those members.

Exact ±90° and ±180° chute X/Y/Z actions are preferred. Other retained single-axis actions and sampled downhill settling alternatives remain available. Routes rank by non-Cartesian actions, actuations, commanded angle, settling requirements and stable IDs. **No composite fallback bridges are generated or selected.** Ordinary multi-step routes use existing single-axis transfers. Disconnected components are reported and remain disconnected.

All candidates are `geometry_only`; contact feasibility and settling reliability are unverified. Execution requires assigned pressure profiles and explicit source-group calibration. Mathematical commands never create pressure profiles.

## Exports and control integration

Each active component provides JSON, YAML, GraphML, PNG, SVG and individual pose sheets, plus a manifest and byte checksums. Consumer-export **version 3** contains individual nodes, stable groups, applicability sets, target sets, ordered commands, real member witnesses, preview segments, finished calibration choices and exported routes. Big Boi only reads, displays, calibrates and executes these records; it does not generate roadmaps or search for routes.

`pose_groups` and `pose_to_group` separate group identity from individual numbering. Scalar consumer choice endpoints are lookup anchors within the applicability/target sets; they do not designate a representative or guarantee an exact landing pose. Eligibility and target satisfaction use stable group keys. `group_transfers` and `group_routes` retain their group-ID namespace; consumer records provide individual-pose anchors explicitly. Schema-v1 pose/edge structures remain readable only by consumers that also support the declared consumer-export version.

The control GUIs retain v1/v2 support. Recognition models continue to identify groups and report possible displayed members. Selecting an individual pose accepts its group as the target. No internal motion is animated. Recognition classes for omitted groups remain unavailable for routing.

**Explicit reimport is required after export hash changes.** Migration records map old group identities by the exact previous export hash, never by a coincidentally matching numeric pose ID. Compatible stable group choices and qualifications can be retained; removed choices and composite profiles remain unavailable. Each component preserves the previous export in `history/previous_roadmap.json.gz` for restoration. Existing assignments receive no automatic group qualification.

The separate main-branch catalogue and source pose repository are unchanged.

## Application

Start `StableComponentRoadmapsGUI.cmd` on Windows, or run `uv run bibazu-stable-roadmaps`. Select the grouped source pose catalogue, keep member/group planning enabled, choose a cutoff and an output folder separate from the input catalogue. The preview lists individual observation frequencies and exclusions. Saved user settings are preserved; the default cutoff for new GUI settings is 1%.

For offline generation use `uv run bibazu-stable-roadmaps-generate --config request.json`:

```json
{"settings":{"output_root":"OUTPUT_DIRECTORY","minimum_frequency_percent":1,"renumber_by_frequency":true,"include_members":true,"include_composites":false,"estimate_capture_intervals":true,"outputs":["json","yaml","graphml","roadmap_png","roadmap_svg","poses_png","poses_svg"]},"sources":["SOURCE_DIRECTORY/Dk1i/poses.json"]}
```

Source inputs require matching mesh geometry, original member observations and grouping records. Export snapshots preserve their hashes. The application bundles its MIT geometry primitives; see [ENGINE_PROVENANCE.json](ENGINE_PROVENANCE.json), [ENGINE_LICENSE](ENGINE_LICENSE) and [LICENSE](LICENSE).

## Catalogue

38 existing generated entries were processed: **37 active roadmaps** and **Kf4i with no eligible poses at 1%**. Kf1i's pre-existing no-observation entry remains unchanged. Source simulation/grouping statistics remain in [grouped_study.json](grouped_study.json); current graph statistics are in [connectivity_audit.json](connectivity_audit.json), [consumer_export_audit.json](consumer_export_audit.json) and [index.json](index.json).

| Workpiece | Individual poses | Displayed groups | Reachable group pairs | Status |
|---|---:|---:|---:|---|
| [Df1a](Df1a/README.md) | 4 | 4 | 12/12 | complete |
| [Df2i](Df2i/README.md) | 6 | 6 | 30/30 | complete |
| [Df4a](Df4a/README.md) | 12 | 12 | 132/132 | complete |
| [Dk1i](Dk1i/README.md) | 8 | 6 | 30/30 | complete |
| [Dk2a](Dk2a/README.md) | 14 | 12 | 132/132 | complete |
| [Dk4i](Dk4i/README.md) | 24 | 18 | 306/306 | complete |
| [Dl1a](Dl1a/README.md) | 7 | 4 | 12/12 | complete |
| [Dl2i](Dl2i/README.md) | 9 | 6 | 30/30 | complete |
| [Dl4a](Dl4a/README.md) | 8 | 6 | 30/30 | complete |
| [Kf2a](Kf2a/README.md) | 3 | 3 | 2/6 | complete |
| [Kf4i](Kf4i/README.md) | 0 | 0 | 0/0 | no_eligible_poses |
| [Kk1a](Kk1a/README.md) | 2 | 2 | 2/2 | complete |
| [Kk2i](Kk2i/README.md) | 20 | 20 | 116/380 | complete |
| [Kk4a](Kk4a/README.md) | 4 | 4 | 2/12 | complete |
| [Kl1i](Kl1i/README.md) | 2 | 2 | 2/2 | complete |
| [Kl2a](Kl2a/README.md) | 17 | 16 | 174/240 | complete |
| [Kl4i](Kl4i/README.md) | 30 | 30 | 677/870 | complete |
| [Qf1i](Qf1i/README.md) | 4 | 4 | 12/12 | complete |
| [Qf2a](Qf2a/README.md) | 10 | 10 | 90/90 | complete |
| [Qf4i](Qf4i/README.md) | 16 | 16 | 240/240 | complete |
| [Qk1a](Qk1a/README.md) | 10 | 6 | 30/30 | complete |
| [Qk2i](Qk2i/README.md) | 13 | 13 | 144/156 | complete |
| [Qk4a](Qk4a/README.md) | 24 | 24 | 552/552 | complete |
| [Ql1i](Ql1i/README.md) | 5 | 5 | 20/20 | complete |
| [Ql2a](Ql2a/README.md) | 8 | 8 | 56/56 | complete |
| [Ql4i](Ql4i/README.md) | 12 | 12 | 132/132 | complete |
| [Rf1a](Rf1a/README.md) | 16 | 15 | 196/210 | complete |
| [Rf2i](Rf2i/README.md) | 8 | 8 | 56/56 | complete |
| [Rf3a](Rf3a/README.md) | 9 | 9 | 72/72 | complete |
| [Rf4i](Rf4i/README.md) | 16 | 16 | 240/240 | complete |
| [Rk1a](Rk1a/README.md) | 30 | 24 | 552/552 | complete |
| [Rk2i](Rk2i/README.md) | 12 | 12 | 132/132 | complete |
| [Rk3a](Rk3a/README.md) | 13 | 11 | 110/110 | complete |
| [Rk4i](Rk4i/README.md) | 24 | 24 | 552/552 | complete |
| [Rl1a](Rl1a/README.md) | 6 | 6 | 30/30 | complete |
| [Rl2i](Rl2i/README.md) | 6 | 6 | 30/30 | complete |
| [Rl3a](Rl3a/README.md) | 10 | 9 | 72/72 | complete |
| [Rl4i](Rl4i/README.md) | 8 | 8 | 56/56 | complete |
