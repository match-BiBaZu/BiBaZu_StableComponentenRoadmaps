# Stable Component Roadmaps

A focused GUI that turns observed simulator pose catalogues into frequency-filtered
reorientation roadmaps. Observations determine the nodes; geometry calculates
direct connection candidates and renders the saved orientations.

The current roadmaps use the newest published [BiBaZu Stable Component Poses
release](https://github.com/match-BiBaZu/BiBaZu_Stable_ComponentPoses/tree/b045887db591ff969b182d4a4ab1e9e14f11ab30),
covering **39 workpieces**. These exports use only its 39 moving-belt runs,
with **10,000 completed trials per workpiece** (390,000 moving-belt drops).
The current roadmaps are in [moving/](moving/README.md). The exports retain the
existing **1%** frequency cutoff and frequency numbering; the GUI default for new
requests remains 5%.

The current set contains **38 roadmaps, 439 retained poses and 2,376 directed connections**.

**Kf1i has no moving-belt export at this cutoff:** its two observed poses have
incidences of 0.06% and 0.03%. The current inputs retain both observations, but
neither qualifies for a roadmap node. Historical and post-braking roadmaps have
been removed from this checkout. Git commit history is preserved.

## Pose derivation and provenance

Current frequency-counted catalogues are included in
`pose_catalogues/moving/<workpiece>/`. The importer reads the pinned Git
revision and verifies the published catalogue, mesh, configuration and grouping
evidence checksums. `catalogue.json` is the original published file; `poses.json`
adapts its field names for the generator. Original pose IDs, counts, orientations,
group membership and member trial IDs are preserved. No observations are
reclassified during import. The source's grouping model is
`observed-seated-geodesic-basins-v1`.

Moving outcomes use the virtual exit with the belt running. Post-braking
observations are not substituted for transport outcomes. Frequencies use all
10,000 completed drops, including
unsettled outcomes. Each individual retained pose remains a separate roadmap node;
source groups do not merge roadmap nodes.

Each export records its condition, observation phase, source revision, catalogue
path and checksum, original run provenance and source pose mapping. Numeric
roadmap IDs are assigned in descending frequency; consumers retain their explicit
re-import and roadmap-hash checks when an export changes. Current PNG/SVG pose
images, portable source snapshots, JSON/YAML/GraphML exports and roadmap diagrams
are included. Superseded roadmap and derived-catalogue files are removed.

## Setup and Windows launching

Install Python 3.11 or newer and `uv`, then run:

```powershell
cd BiBaZu_StableComponentsRoadmaps
uv sync
.\StableComponentRoadmapsGUI.cmd
```

For Desktop and Start Menu shortcuts with the supplied icon, double-click
`WindowsLaunchers/Verknuepfungen-installieren.cmd`. See
[Windows launcher instructions](WindowsLaunchers/README.md).

## Rebuild from the current published pose catalogues

The bundled inputs are sufficient to regenerate the moving-belt roadmaps from this
repository's root:

```powershell
uv run python -m bibazu_stable_roadmaps.generate --config generation_request.json
```

To import a newer published release, fetch the poses repository and import the
moving-belt catalogues to a fresh directory. For example:

```powershell
git -C ..\BiBaZu_StableComponentenPoses fetch origin
uv run python -m bibazu_stable_roadmaps.import_catalogues --poses-repo ..\BiBaZu_StableComponentenPoses --revision origin/main --condition moving --output-root .\new_catalogues\moving
```

Select the new inputs in the GUI or update the request's source paths.
The legacy `derive` command
is retained for reproducibility of the earlier complete-link classifier; it is
not used for the current published catalogues.
[Legacy classifier provenance](DERIVATION_PROVENANCE.json) · [License](DERIVATION_LICENSE)

## Using the GUI

1. Choose a `poses.json`, a `pose_registry.json`, or a pose catalogue folder.
   The default input is `pose_catalogues/moving` and the default output is `moving`.
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
analytical stability selection, clustering, or rocking-based ordering occurs
during roadmap generation.

Connections use the bundled engine's directed action domains, contact/main-face
requirements, 25 mm opposite-X support rule, and 1° axis tolerance. Part symmetry
is used to find equivalent connection representations; it never merges nodes.
Uncertain contacts can prevent constrained actions but do not remove poses.
Only direct connections between retained nodes are exported, with no generated
intermediate nodes or passive settling paths. Connections remain experimentally
untested. Rocking barriers, capture widths and reliability scores are unknown.

## Repository and export format

Generation creates one folder per component, such as `moving/Dl1a/`, containing:

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

<!-- GENERATED ROADMAP INDEX START -->
| Component | Poses | Connections |
| --- | ---: | ---: |
| [Df1a](moving/Df1a/README.md) | 4 | 6 |
| [Df2i](moving/Df2i/README.md) | 6 | 22 |
| [Df4a](moving/Df4a/README.md) | 12 | 42 |
| [Dk1i](moving/Dk1i/README.md) | 8 | 32 |
| [Dk2a](moving/Dk2a/README.md) | 14 | 74 |
| [Dk4i](moving/Dk4i/README.md) | 24 | 132 |
| [Dl1a](moving/Dl1a/README.md) | 6 | 16 |
| [Dl2i](moving/Dl2i/README.md) | 6 | 16 |
| [Dl4a](moving/Dl4a/README.md) | 8 | 20 |
| [Kf2a](moving/Kf2a/README.md) | 29 | 422 |
| [Kf4i](moving/Kf4i/README.md) | 19 | 84 |
| [Kk1a](moving/Kk1a/README.md) | 5 | 10 |
| [Kk2i](moving/Kk2i/README.md) | 24 | 138 |
| [Kk4a](moving/Kk4a/README.md) | 2 | 0 |
| [Kl1i](moving/Kl1i/README.md) | 4 | 14 |
| [Kl2a](moving/Kl2a/README.md) | 15 | 26 |
| [Kl4i](moving/Kl4i/README.md) | 8 | 0 |
| [Qf1i](moving/Qf1i/README.md) | 4 | 16 |
| [Qf2a](moving/Qf2a/README.md) | 10 | 62 |
| [Qf4i](moving/Qf4i/README.md) | 16 | 112 |
| [Qk1a](moving/Qk1a/README.md) | 15 | 59 |
| [Qk2i](moving/Qk2i/README.md) | 12 | 62 |
| [Qk4a](moving/Qk4a/README.md) | 24 | 160 |
| [Ql1i](moving/Ql1i/README.md) | 5 | 21 |
| [Ql2a](moving/Ql2a/README.md) | 5 | 17 |
| [Ql4i](moving/Ql4i/README.md) | 8 | 40 |
| [Rf1a](moving/Rf1a/README.md) | 15 | 68 |
| [Rf2i](moving/Rf2i/README.md) | 8 | 48 |
| [Rf3a](moving/Rf3a/README.md) | 8 | 44 |
| [Rf4i](moving/Rf4i/README.md) | 16 | 112 |
| [Rk1a](moving/Rk1a/README.md) | 24 | 124 |
| [Rk2i](moving/Rk2i/README.md) | 12 | 68 |
| [Rk3a](moving/Rk3a/README.md) | 14 | 90 |
| [Rk4i](moving/Rk4i/README.md) | 20 | 124 |
| [Rl1a](moving/Rl1a/README.md) | 7 | 20 |
| [Rl2i](moving/Rl2i/README.md) | 6 | 17 |
| [Rl3a](moving/Rl3a/README.md) | 8 | 30 |
| [Rl4i](moving/Rl4i/README.md) | 8 | 28 |
<!-- GENERATED ROADMAP INDEX END -->

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
