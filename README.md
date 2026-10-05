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
Only direct connections between retained nodes are exported, with no generated
intermediate nodes or passive settling paths. Connections remain experimentally
untested. Rocking barriers, capture widths and reliability scores are unknown.

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
| Component | Poses | Connections | Minimum frequency | Numbering |
| --- | ---: | ---: | ---: | --- |
| [Df1a](Df1a/README.md) | 4 | 6 | 5% | Frequency |
| [Dk1i](Dk1i/README.md) | 8 | 32 | 5% | Frequency |
| [Dl1a](Dl1a/README.md) | 4 | 8 | 5% | Frequency |
| [Kk1a](Kk1a/README.md) | 2 | 4 | 5% | Frequency |
| [Kl1i](Kl1i/README.md) | 2 | 4 | 5% | Frequency |
| [Qf1i](Qf1i/README.md) | 4 | 13 | 5% | Frequency |
| [Qk1a](Qk1a/README.md) | 6 | 8 | 5% | Frequency |
| [Ql1i](Ql1i/README.md) | 3 | 8 | 5% | Frequency |
| [Rf1a](Rf1a/README.md) | 7 | 16 | 5% | Frequency |
| [Rk1a](Rk1a/README.md) | 4 | 2 | 5% | Frequency |
| [Rl1a](Rl1a/README.md) | 4 | 8 | 5% | Frequency |
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
