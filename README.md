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
Completed and validated: **14/39** workpieces. Each completed workpiece has 10,000 drops; member disturbance tests are additional.

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
| Kk2i | pending | — | — | — | — | — |
| Kk4a | pending | — | — | — | — | — |
| Kl1i | pending | — | — | — | — | — |
| Kl2a | pending | — | — | — | — | — |
| Kl4i | pending | — | — | — | — | — |
| Qf1i | pending | — | — | — | — | — |
| Qf2a | pending | — | — | — | — | — |
| Qf4i | pending | — | — | — | — | — |
| [Qk1a](Qk1a/README.md) | Complete | 9956 | 13 | 6 | 949 | 8 |
| Qk2i | pending | — | — | — | — | — |
| Qk4a | pending | — | — | — | — | — |
| Ql1i | pending | — | — | — | — | — |
| Ql2a | pending | — | — | — | — | — |
| Ql4i | pending | — | — | — | — | — |
| Rf1a | pending | — | — | — | — | — |
| Rf2i | pending | — | — | — | — | — |
| Rf3a | pending | — | — | — | — | — |
| Rf4i | pending | — | — | — | — | — |
| Rk1a | pending | — | — | — | — | — |
| Rk2i | pending | — | — | — | — | — |
| Rk3a | pending | — | — | — | — | — |
| Rk4i | pending | — | — | — | — | — |
| Rl1a | pending | — | — | — | — | — |
| Rl2i | pending | — | — | — | — | — |
| Rl3a | pending | — | — | — | — | — |
| Rl4i | pending | — | — | — | — | — |

Each component page links representative images, full membership and barrier evidence, and individual/member stability curves. Percentages use all completed drops. Roadmap connections are computed from representative orientations.

Published comparison baselines: poses `9e00d03389d3b81013700def03fb1b19504144be`, roadmaps `0b3b5c5fe42e787bd47f381b1f1ac57359d5aa55`. Merge repair: `3523350d8e12a1b7e57467044b9cfe25ff49b0bd`.
