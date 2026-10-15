# BiBaZu observed component roadmaps

A focused GUI that turns simulator pose exports into frequency-filtered
reorientation roadmaps. The simulator's list determines the nodes. Geometry
calculates direct connection candidates and renders the observed orientations.

This repository owns its application, bundled geometry code and Python
environment. No geometry-to-pose checkout is required. It initially contains
no generated component roadmaps; use your pose files to create them.

## Setup and Windows launching

Install Python 3.11 or newer and `uv`, then run:

```powershell
cd BiBaZu_StableComponentenRoadmaps
uv sync
.\StableComponentRoadmapsGUI.cmd
```

For Desktop and Start Menu shortcuts with the supplied icon, double-click
`WindowsLaunchers/Verknuepfungen-installieren.cmd`. See
[Windows launcher instructions](WindowsLaunchers/README.md).

## Using the GUI

1. Choose a `poses.json`, a `pose_registry.json`, or your poses repository folder.
   Folder mode lists each component once, preferring `poses.json` when both files
   are present. Selecting a registry requires the neighboring `poses.json` for
   frequencies; historical registry IDs absent from observations have 0%.
2. Select components. The preview shows the original IDs, percentages, retained
   or removed status, and proposed roadmap IDs.
3. Set **Minimum frequency**, default **5%**. Below the threshold is removed;
   exactly the threshold is retained. **0% disables filtering.** Percentages are
   never rescaled after filtering. If only counts are present, use all completed
   trials as the denominator, or all listed counts if no trial total is recorded.
4. Enable **Renumber by frequency**, on by default, for contiguous IDs from zero
   in descending frequency. Ties use the original source ID. If disabled, numeric
   source suffixes are preserved: `Dl1a_0007` becomes roadmap ID 7. Full original
   IDs are always retained. Sources without numeric suffixes require renumbering.
5. Choose formats and Generate. Empty exports or a cutoff removing every pose
   are logged as skipped, preserving any previous result. Cancel stops at a safe
   boundary and retains completed results.

The STL is resolved beside the JSON and checked against its stored hash. Angles
are taken from the neighboring simulation `config.json`, defaulting to X=45°,
Y=0° if it is absent. Each retained entry remains a separate node, including
symmetry-equivalent observations. Original quaternions are normalized without
changing their physical orientation. No theoretical enumeration, snapping,
analytical stability selection, clustering, or rocking-based ordering occurs.

Connections use the bundled engine's directed action domains, contact/main-face
requirements, 25 mm opposite-X support rule, and 1° axis tolerance. Part symmetry
is used to find equivalent connection representations; it never merges nodes.
Uncertain contacts can prevent constrained actions but do not remove poses.
Direct connections retain those rules. The grouped application also offers
**Add geometry-only composite bridges**, enabled by default. It keeps each
representative fixed and adds ordered Y–Z–Y or Z–Y–Z orientation transfers between
disconnected components. Transient orientations do not become catalogue poses.
Contact feasibility, settling, actuator feasibility and reliability are unverified;
calibrate a full transfer pressure profile before execution. Rocking barriers,
capture widths and reliability scores remain unknown.

## Repository and export format

Generation creates one folder per component, such as `Dl1a/`, containing:

- `<component>_roadmap.yaml`, `.json`, `.graphml`, `.svg`, `.png`, as selected.
- Optional `pose_sheets/` with images named by the **output roadmap IDs**.
- `source/` snapshots of the input pose JSON, registry, STL and available config.
- `manifest.json`, `files.sha256.json` and a component `README.md`.

Each component has **one current result set**. Regeneration replaces that set
and removes obsolete generated formats, after staging and validation. Manual
changes or extra files in a managed component folder block replacement rather
than being deleted. Save those changes elsewhere before regenerating. The poses
repository is always input-only and cannot be selected as the output repository.
Output paths are relative to the exported component folder, so moving a saved
roadmap and its `source/` together preserves mesh access.

JSON/YAML use the existing schema version 1 and action names accepted by the
BiBaZu Reorientation Control GUI. The Pressure Control GUI uses the JSON export,
including its directed edges, numeric roadmap IDs, signed angles, relative STL
path and embedded pose previews. Use its updated `roadmap_transition_dialog.py`
loader, which accepts null capture widths and geometric scores. Restart an
already-running Pressure Control GUI after updating that loader; older versions
try to convert these uncomputed metrics to floats and cannot load them.
The YAML experimental block follows the existing handover fields (`trials`,
`successes`, `empirical_success_rate`, `difficulty_rating`, `notes`).

Schema version 1 keeps direct `edges`/`transitions` and their IDs intact. Optional
`composite_transfers`, `routes` and `connectivity` sections describe separate
orientation candidates, one preferred route per ordered pose pair, and directed
reachability before/after candidate augmentation. GraphML keeps direct edges and
stores these optional sections as graph metadata. Representative-only roadmap
images use dashed purple arrows for composite candidates. Existing-only routes are preferred;
otherwise route costs minimize composite transfers, rotation count, and total
absolute angle, followed by stable IDs. Generated composite IDs include a digest
of their endpoints and commands; equivalent quaternion signs have the same ID.

Updated Reorientation Control and Pressure Control display these candidates and
their transient rotation previews. Selecting a candidate for calibration does not
create or assign an executable pressure profile. Runtime routing uses assigned
profiles only and supports simple routes through up to `pose_count - 1` transfers.
Legacy two/three-flip choices retain their IDs; longer routes use bounded shortest
path searches instead of enumerating every simple path.

The [catalogue connectivity audit](connectivity_audit.json) covers 39 workpieces:
13 direct roadmaps are disconnected and Kf1i has no eligible groups. Qk1a now has
3 composite bridges (candidate reachability 30/30 pairs); Dl1a has 4 (20/20).
Representatives, memberships, frequencies, and direct edges were preserved.

To stage the same extension against a selected Git snapshot without rebuilding
direct edges or overwriting existing output, use a fresh staging directory:

```powershell
uv run python -m bibazu_stable_roadmaps.upgrade_connectivity --repository . --staging-root ../.task_artifacts/connectivity-review --parts Qk1a Dl1a
```

Inspect the staged JSON/YAML, rendered roadmap, manifest and checksums before
replacing generated folders. `include_composites: false` in worker settings
disables bridge generation for new exports.

### Member-conditioned transfers and capture ranges

**Use all group members and estimate capture intervals** is enabled by default
for grouped inputs. Representatives remain the displayed group anchors. The
generator loads every retained group's member orientations from
`original_observations.json`, including rare members, and retains the original
direct edges and their IDs. Missing declared member data blocks generation
instead of silently reverting to the representative. Needed evidence is copied
into the exported `source/` snapshot.

Optional schema-v1 sections `member_states`, `member_transfers`, `member_routes`
and `capture_analysis` store source conditions, possible arrivals, ordered
commands, settling witnesses and sampled intervals. GraphML stores the same
sections as graph metadata. Overview arrows aggregate conditional alternatives:
**K** = known member endpoint, **C** = sampled downhill capture, **F** = composite
fallback. An overview connection does not imply that any arrival member can use
every outgoing action. Internal route searches preserve member states and
possible arrival sets, charging explicit intra-group repositioning actions.

Capture estimation samples permitted actions at 1°, refines changed outcomes at
0.1°, and samples seated shortest settling paths at 0.1° within a 60° guard.
Potential must decrease without an uphill step beyond 0.000001 mm equivalent lift;
the 0.5 mm grouping barrier is not a passive-motion allowance. Excluded observed
groups remain competing destinations. Unresolved intervals and multiple outcomes
are retained. These sampled geometric witnesses do not establish physical
settling reliability.

Qk1a recovers **20** known-member inter-group actions; Dl1a recovers **34**.
Composite fallbacks ensure every retained source member has a candidate path to
every retained target group. Existing representative quaternions, thumbnails,
memberships, frequencies and direct edges are unchanged.

The control GUIs show member endpoints, capture intervals and settling previews.
Profiles must explicitly declare `covered_source_member_ids`. Pressure Control
offers a comma-separated field; `*` explicitly declares testing for all source
group members. Reorientation setup offers the same declaration, saved in
`transition_source_coverage` or read from matching pressure-profile metadata.
Blank coverage means calibration only. Legacy profiles are retained without
automatic group-wide promotion. Runtime carries possible member states and
requires each assigned profile to cover all currently possible source members.

Worker settings `include_members: false` disable the member extension;
`estimate_capture_intervals: false` retain member endpoints and fallback routes
without running angle sampling.

Original IDs are in `source_pose_ids`; counts
and percentages are in `observed_count` and `observed_frequency_percent`.
The `generation` section records filtering, numbering and excluded poses.
`original_catalog_pose_id` / `pose_ids` refer to **input-list indices**, recorded
as `catalogue_id_namespace: input_pose_list_index`, rather than theoretical poses.

For compatibility with the existing consumer, the legacy `robust` tag designates
an observed stable target. **It does not assert analytical robustness.**
`classification_basis` is `observed_simulation`,
`analytical_stability_evaluated` is false, and uncomputed physical metrics are
null (omitted in GraphML, which cannot represent null values). The GUI and
images display observed frequencies rather than analytical ranks.



## Batch worker and development

```powershell
uv sync --extra dev
uv run pytest
uv run python -m bibazu_stable_roadmaps.generate --config request.json
```

The worker accepts a JSON object containing `sources` (pose JSON paths) and
`settings`: `output_root`, `minimum_frequency_percent`, `renumber_by_frequency`,
and `outputs` (`yaml`, `json`, `graphml`, `roadmap_svg`, `roadmap_png`, `poses_svg`,
`poses_png`). It emits progress as JSON lines. The GUI uses the same worker in
a separate process. Settings are stored under BiBaZu/StableComponentRoadmaps;
they do not affect the original geometry GUI.

The MIT geometry/rendering primitives are bundled under the application's
`_engine` package. [ENGINE_PROVENANCE.json](ENGINE_PROVENANCE.json) records their
upstream revision and source hashes. Geometric action rules are extracted from
the upstream roadmap implementation; its stability and ranking code is not
bundled. Preserve [ENGINE_LICENSE](ENGINE_LICENSE) when redistributing them.

<!-- GROUPED STUDY -->
Completed and validated: **39/39** workpieces. Each completed workpiece has 10,000 drops; member disturbance tests are additional.

All workpieces use identical simulation settings, a 0.5 mm equivalent-lift grouping barrier, a 60° diameter guard, and a 1% cutoff after aggregation. Representatives are selected using complete member group-retention curves.

Qk1a, Dl1a, and Dk1i reuse the previously audited grouped runs. Full raw trial data remains in the simulator's ignored results directories.

| Workpiece | Status | Settled | Source poses | Eligible groups | Disturbance tests | Roadmap connections |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Df1a](Df1a/README.md) | Complete | 9997 | 7 | 4 | 511 | 6 |
| [Df2i](Df2i/README.md) | Complete | 9996 | 9 | 6 | 657 | 22 |
| [Df4a](Df4a/README.md) | Complete | 9999 | 20 | 12 | 1460 | 42 |
| [Dk1i](Dk1i/README.md) | Complete | 9998 | 8 | 6 | 584 | 16 |
| [Dk2a](Dk2a/README.md) | Complete | 9845 | 17 | 12 | 1241 | 56 |
| [Dk4i](Dk4i/README.md) | Complete | 9999 | 24 | 18 | 1752 | 80 |
| [Dl1a](Dl1a/README.md) | Complete | 9983 | 16 | 5 | 1168 | 2 |
| [Dl2i](Dl2i/README.md) | Complete | 9965 | 19 | 6 | 1387 | 21 |
| [Dl4a](Dl4a/README.md) | Complete | 9973 | 29 | 6 | 2117 | 10 |
| [Kf1i](Kf1i/README.md) | Complete | 0 | 0 | 0 | 0 | 0 |
| [Kf2a](Kf2a/README.md) | Complete | 7584 | 6 | 3 | 438 | 2 |
| [Kf4i](Kf4i/README.md) | Complete | 1333 | 35 | 3 | 2555 | 2 |
| [Kk1a](Kk1a/README.md) | Complete | 2887 | 3 | 2 | 219 | 4 |
| [Kk2i](Kk2i/README.md) | Complete | 8448 | 31 | 20 | 2263 | 22 |
| [Kk4a](Kk4a/README.md) | Complete | 7726 | 121 | 4 | 8833 | 2 |
| [Kl1i](Kl1i/README.md) | Complete | 9333 | 2 | 2 | 146 | 4 |
| [Kl2a](Kl2a/README.md) | Complete | 9912 | 27 | 16 | 1971 | 23 |
| [Kl4i](Kl4i/README.md) | Complete | 9620 | 41 | 30 | 2993 | 20 |
| [Qf1i](Qf1i/README.md) | Complete | 9870 | 13 | 4 | 949 | 13 |
| [Qf2a](Qf2a/README.md) | Complete | 9829 | 24 | 10 | 1752 | 62 |
| [Qf4i](Qf4i/README.md) | Complete | 9835 | 29 | 16 | 2117 | 112 |
| [Qk1a](Qk1a/README.md) | Complete | 9956 | 13 | 6 | 949 | 8 |
| [Qk2i](Qk2i/README.md) | Complete | 10000 | 15 | 13 | 1095 | 63 |
| [Qk4a](Qk4a/README.md) | Complete | 9997 | 26 | 24 | 1898 | 157 |
| [Ql1i](Ql1i/README.md) | Complete | 9985 | 6 | 5 | 438 | 21 |
| [Ql2a](Ql2a/README.md) | Complete | 9942 | 19 | 8 | 1387 | 39 |
| [Ql4i](Ql4i/README.md) | Complete | 9979 | 24 | 12 | 1752 | 68 |
| [Rf1a](Rf1a/README.md) | Complete | 9963 | 25 | 15 | 1825 | 56 |
| [Rf2i](Rf2i/README.md) | Complete | 9839 | 19 | 8 | 1387 | 45 |
| [Rf3a](Rf3a/README.md) | Complete | 9965 | 19 | 9 | 1387 | 48 |
| [Rf4i](Rf4i/README.md) | Complete | 9885 | 27 | 16 | 1971 | 112 |
| [Rk1a](Rk1a/README.md) | Complete | 9976 | 45 | 24 | 3285 | 120 |
| [Rk2i](Rk2i/README.md) | Complete | 9999 | 12 | 12 | 876 | 68 |
| [Rk3a](Rk3a/README.md) | Complete | 9995 | 17 | 11 | 1241 | 58 |
| [Rk4i](Rk4i/README.md) | Complete | 9999 | 24 | 24 | 1752 | 168 |
| [Rl1a](Rl1a/README.md) | Complete | 9830 | 30 | 7 | 2190 | 16 |
| [Rl2i](Rl2i/README.md) | Complete | 9980 | 9 | 6 | 657 | 17 |
| [Rl3a](Rl3a/README.md) | Complete | 9883 | 18 | 9 | 1314 | 30 |
| [Rl4i](Rl4i/README.md) | Complete | 9992 | 19 | 8 | 1387 | 28 |

Each component page links representative images, full membership and barrier evidence, and individual/member stability curves. Percentages use all completed drops. Roadmap connections are computed from representative orientations.

Published comparison baselines: poses `9e00d03389d3b81013700def03fb1b19504144be`, roadmaps `0b3b5c5fe42e787bd47f381b1f1ac57359d5aa55`. Merge repair: `3523350d8e12a1b7e57467044b9cfe25ff49b0bd`.


## Finished exports for control applications

This application owns roadmap generation, geometric verification, member/capture
analysis, connectivity, route construction, deterministic IDs and preview segments.
The Big Boi control GUIs read the finished files directly. They do not import this
application, generate roadmaps, or search for new routes.

The additive JSON/YAML `consumer_export` section has `version: 1` and contains:

- `calibration_choices`: complete records with stable edge IDs, endpoints, ordered
  commands, component edge IDs, source/arrival members, evidence, costs and flattened
  `preview_segments`. Representative thumbnails and schema-v1 direct data are preserved.
- `execution_routes`: exported profile sequences, their endpoint references, selection
  priority, and explicit per-step source-member coverage requirements. An entire macro
  can have its own calibrated profile, or its exported component profiles may be used.

Only assigned pressure profiles may execute. Missing source coverage is not inferred
from geometry or older profiles. Group recognition leaves every retained source member
possible. If calibrated coverage extends beyond a geometric witness, exported requirements
conservatively retain every target-group member. A consumer reports missing calibration
or ambiguity instead of constructing another path. Previews interpolate exported segments
for display; they do not establish physical feasibility.

To upgrade existing schema-v1 exports offline without recomputing their poses or edges:

```powershell
python -m bibazu_stable_roadmaps.upgrade_consumer_exports --repository PATH_TO_CATALOGUE --staging-root NEW_STAGING_DIRECTORY
```

Review staging, validate checksums, and publish with rollback backups. The utility also
works on ungrouped/main-branch exports; this rollout leaves the separate main catalogue
unchanged. Both GUIs still accept its explicit transitions without an upgrade.

The former Big Boi bundled roadmaps live under `legacy_catalogue/originals/`, separated
from grouped targets. `legacy_catalogue/path_migrations.json` records exact old paths and
SHA-256 hashes. Their original files remain byte-for-byte intact. Offline-produced,
hash-bound `<filename>.consumer.json` sidecars preserve existing derived route identities:

```powershell
python -m bibazu_stable_roadmaps.upgrade_consumer_exports --legacy-root legacy_catalogue/originals
```

No migration substitutes grouped poses for similarly numbered ungrouped poses.
Big Boi defaults to this grouped catalogue; `BIBAZU_ROADMAPS_DIR` or an explicitly selected
file can choose another external catalogue. Calibration profiles and recognition mappings
remain in the control application.
