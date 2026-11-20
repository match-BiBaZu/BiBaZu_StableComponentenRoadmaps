"""Compatibility CLI for reloading published DropSim stability reports."""
import argparse
import json
import os
from pathlib import Path
import tempfile
from .inputs import load_source
from .published_quality import analyze_pose_quality, quality_label, METHOD, METHOD_VERSION, THRESHOLDS_MM

class QualityCancelled(Exception):
    pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cancel-file", type=Path)
    args = parser.parse_args()

    def emit(**event):
        print(json.dumps(event, ensure_ascii=False, allow_nan=False), flush=True)

    def check_cancel():
        if args.cancel_file is not None and args.cancel_file.exists():
            raise QualityCancelled()

    temporary = None
    try:
        check_cancel()
        destination = args.output.expanduser().resolve()
        source_file = args.source.expanduser().resolve()
        if destination.is_relative_to(source_file.parent):
            raise ValueError("Save the quality report outside the input catalogue folder; source inputs are read-only.")
        if destination.is_file() and destination.name in {
                "poses.json", "pose_registry.json", "catalogue.json", "config.json", "grouping-evidence.json",
                "files.sha256.json", "manifest.json"}:
            raise ValueError("The quality report cannot overwrite an existing catalogue or inventory file.")
        source = load_source(source_file)
        report = analyze_pose_quality(source, progress=lambda message: emit(message=message), check_cancel=check_cancel)
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=".pose-quality-", suffix=".tmp", dir=destination.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
        check_cancel()
        os.replace(temporary, destination)
        emit(status="completed", report_path=str(destination))
        return 0
    except QualityCancelled:
        emit(status="cancelled", message="Pose-quality analysis cancelled.")
        return 0
    except Exception as error:
        emit(status="failed", message=str(error))
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
