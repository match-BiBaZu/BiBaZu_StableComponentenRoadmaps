"""Stage whole-group exports without replacing the original poses or direct edges."""

from __future__ import annotations

import argparse
import base64
import io
import json
from pathlib import Path
import shutil

import matplotlib.image as mpimg
import yaml

from .consumer_export import attach_consumer_export
from .generate import _write_graphml, write_json
from .group_transfers import augment_groups
from .inputs import load_source, sha256
from .roadmap import build_roadmap
from .render import render_roadmap


def stage_component(original, destination, progress=print):
    original, destination = Path(original), Path(destination)
    if destination.exists():
        raise ValueError(f"Staging destination already exists: {destination}")
    part = original.name
    mutable = {
        f"{part}_roadmap.{ext}" for ext in ("json", "yaml", "graphml", "png", "svg")
    }
    mutable |= {"manifest.json", "README.md", "files.sha256.json"}
    document = json.loads(
        (original / f"{part}_roadmap.json").read_text(encoding="utf-8")
    )
    before = {
        key: json.dumps(document[key], sort_keys=True) for key in ("nodes", "edges")
    }
    source = load_source(original / "source/poses.json")
    observed = {pose.source_id: pose for pose in source.poses}
    built = build_roadmap(
        source,
        [(observed[n["source_pose_ids"][0]], n["node_id"]) for n in document["nodes"]],
    )
    built.document = document
    augment_groups(source, built, progress=progress)
    attach_consumer_export(document)
    for key in before:
        if json.dumps(document[key], sort_keys=True) != before[key]:
            raise ValueError(f"Whole-group upgrade changed {key}")
    destination.mkdir(parents=True)
    # Unchanged assets are copied only once. Mutable files are newly produced;
    # no staged write can affect an original through a hard link.
    for path in original.rglob("*"):
        if not path.is_file() or path.parent == original and path.name in mutable:
            continue
        target = destination / path.relative_to(original)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    path = destination / f"{part}_roadmap.json"
    path.write_text(
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    handover = yaml.load(
        (original / path.with_suffix(".yaml").name).read_text(encoding="utf-8"),
        Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader),
    )
    for key in (
        "member_states",
        "member_transfers",
        "member_routes",
        "capture_analysis",
        "connectivity",
        "group_keys",
        "group_transfers",
        "group_routes",
        "consumer_export",
    ):
        handover[key] = document[key]
    path.with_suffix(".yaml").write_text(
        yaml.dump(
            handover,
            Dumper=getattr(yaml, "CSafeDumper", yaml.SafeDumper),
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    _write_graphml(document, path.with_suffix(".graphml"))
    images = {
        n["node_id"]: mpimg.imread(
            io.BytesIO(base64.b64decode(n["thumbnail_png_base64"])), format="png"
        )
        for n in document["nodes"]
    }
    render_roadmap(built, path.with_suffix(""), ("svg", "png"), images)
    manifest = json.loads((original / "manifest.json").read_text(encoding="utf-8"))
    manifest.update(
        connectivity=document["connectivity"],
        group_transfer_count=len(document["group_transfers"]),
        group_route_count=len(document["group_routes"]),
        group_extension=dict(
            planning_assumption=document["connectivity"]["groups"][
                "planning_assumption"
            ],
            implementation_sha256=sha256(
                Path(__file__).with_name("group_transfers.py")
            ),
        ),
        consumer_export=dict(
            version=2,
            route_policy="exported_only",
            calibration_choice_count=len(
                document["consumer_export"]["calibration_choices"]
            ),
            execution_route_count=len(document["consumer_export"]["execution_routes"]),
        ),
    )
    write_json(destination / "manifest.json", manifest)
    text = (
        (original / "README.md")
        .read_text(encoding="utf-8")
        .split("<!-- COMPOSITE CONNECTIVITY -->")[0]
    )
    text = text.replace(
        "Nodes use the chosen representative orientations. Direct connections remain geometric action candidates.",
        "Thumbnails retain the chosen representative orientations. Each group contains all its observed members.",
    )
    stats = document["connectivity"]["groups"]
    total = stats["all_candidates"]["total_pair_count"]
    text += "\n## Whole-group reorientations\n\n"
    text += (
        f"Cartesian-only routes reach **{stats['cartesian']['reachable_pair_count']}/{total}** ordered group pairs; "
        f"all candidate routes reach **{stats['all_candidates']['reachable_pair_count']}/{total}**.\n\n"
        "A transfer may use any source member and reach any target member. Consecutive transfers may use different members of the same intermediate group. "
        "This interchangeability is the planning assumption; no extra motion is invented between those witnesses.\n\n"
        "Exact ±90° and ±180° chute X/Y/Z commands are evaluated without contact/support pruning and preferred over other rotations. "
        "Arrow labels show the preferred reorientation; exports and control pickers retain alternatives and member witnesses. "
        "Competing landing outcomes and sampled downhill evidence remain in the records.\n\n"
        "The additive `group_transfers`, `group_routes` and consumer-export version 2 records contain finished choices and previews. "
        "Execution requires an assigned pressure profile explicitly calibrated for the exported source group. "
        "Existing profiles receive no automatic group qualification. Contact feasibility and physical settling reliability remain unverified.\n"
    )
    (destination / "README.md").write_text(text, encoding="utf-8")
    write_json(
        destination / "files.sha256.json",
        {
            p.relative_to(destination).as_posix(): sha256(p)
            for p in sorted(destination.rglob("*"))
            if p.is_file()
        },
    )
    return dict(
        part=part,
        group_transfers=len(document["group_transfers"]),
        group_routes=len(document["group_routes"]),
        cartesian=stats["cartesian"],
        all_candidates=stats["all_candidates"],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--parts", nargs="+", required=True)
    args = parser.parse_args()
    for part in args.parts:
        result = stage_component(args.repository / part, args.staging_root / part)
        write_json(args.staging_root / (part + "_audit.json"), result)
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
