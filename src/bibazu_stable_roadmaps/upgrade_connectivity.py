"""Stage connectivity extensions from a Git snapshot without rebuilding direct edges.

Usage: python -m bibazu_stable_roadmaps.upgrade_connectivity --repository PATH
       --staging-root PATH --parts Qk1a Dl1a
"""
from __future__ import annotations

import argparse
import base64
import io
import json
from pathlib import Path
import subprocess
import tarfile

import matplotlib.image as mpimg
import yaml

from .connectivity import augment_roadmap, connectivity
from .generate import _write_graphml, write_json
from .inputs import load_source, sha256
from .roadmap import build_roadmap, _symmetry
from .render import render_roadmap


def git(repository, *args):
    repository = Path(repository).resolve()
    # Per-command trust of this explicitly selected workspace, no global config edit.
    return subprocess.run(['git', '-c', f'safe.directory={repository.as_posix()}', '-C', str(repository),
                           *args], check=True, capture_output=True).stdout


def upgrade_component(folder):
    folder = Path(folder)
    part = folder.name
    path = folder / f'{part}_roadmap.json'
    document = json.loads(path.read_text(encoding='utf-8'))
    before_nodes = json.dumps(document['nodes'], sort_keys=True)
    before_edges = json.dumps(document['edges'], sort_keys=True)
    source = load_source(folder / 'source/poses.json')
    symmetries, _, _ = _symmetry(source)
    augment_roadmap(document, symmetries)
    if before_nodes != json.dumps(document['nodes'], sort_keys=True) or before_edges != json.dumps(document['edges'], sort_keys=True):
        raise ValueError('Connectivity extension modified existing poses or direct edges')
    fields = {key: document[key] for key in ('composite_transfers', 'routes', 'connectivity')}
    write_json(path, document)
    handover_path = path.with_suffix('.yaml')
    handover = yaml.safe_load(handover_path.read_text(encoding='utf-8'))
    handover.update(fields)
    handover_path.write_text(yaml.safe_dump(handover, sort_keys=False, allow_unicode=True), encoding='utf-8')
    _write_graphml(document, path.with_suffix('.graphml'))
    observed = {p.source_id: p for p in source.poses}
    built = build_roadmap(source, [(observed[n['source_pose_ids'][0]], n['node_id']) for n in document['nodes']])
    built.document = document
    images = {n['node_id']: mpimg.imread(io.BytesIO(base64.b64decode(n['thumbnail_png_base64'])), format='png')
              for n in document['nodes']}
    render_roadmap(built, path.with_suffix(''), ('svg', 'png'), images)
    manifest_path = folder / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update(connectivity=document['connectivity'], composite_transfer_count=len(document['composite_transfers']),
                    connectivity_extension={'method': 'fixed_representative_yzy_zyz_v1',
                                            'implementation_sha256': sha256(Path(__file__).with_name('connectivity.py'))})
    write_json(manifest_path, manifest)
    direct, augmented = document['connectivity']['direct'], document['connectivity']['with_candidates']
    readme = folder / 'README.md'
    marker = '\n<!-- COMPOSITE CONNECTIVITY -->\n'
    text = readme.read_text(encoding='utf-8').split(marker)[0]
    text += marker + '\n## Composite orientation candidates\n\n'
    text += (f"Existing connections reach {direct['reachable_pair_count']}/{direct['total_pair_count']} ordered pairs. "
             f"With {len(document['composite_transfers'])} composite bridges, candidate routes reach "
             f"{augmented['reachable_pair_count']}/{augmented['total_pair_count']} pairs.\n\n"
             "Representatives and direct edges are unchanged. Dashed purple bridges are geometry-only candidates: "
             "contact, settling, actuator feasibility and reliability remain unverified. "
             "Transient orientations are not pose catalogue entries. Calibrate a full transfer pressure profile before execution.\n\n"
             "JSON/YAML contain ordered commands, preferred routes and separate directed connectivity reports.\n")
    readme.write_text(text, encoding='utf-8')
    write_json(folder / 'files.sha256.json', {p.relative_to(folder).as_posix(): sha256(p)
               for p in sorted(folder.rglob('*')) if p.is_file() and p.name != 'files.sha256.json'})
    return {'part': part, 'direct': direct, 'with_candidates': augmented,
            'composite_transfer_count': len(document['composite_transfers']),
            'representatives_unchanged': True, 'direct_edges_unchanged': True}


def stage(repository, staging_root, parts):
    repository, staging_root = Path(repository).resolve(), Path(staging_root).resolve()
    staging_root.mkdir(parents=True, exist_ok=True)
    audit = []
    paths = git(repository, 'ls-tree', '-r', '--name-only', 'HEAD').decode().splitlines()
    for name in paths:
        if not name.endswith('_roadmap.json') or len(Path(name).parts) != 2:
            continue
        document = json.loads(git(repository, 'show', f'HEAD:{name}'))
        part = Path(name).parts[0]
        row = {'part': part, 'pose_count': len(document['nodes']), 'direct_edge_count': len(document['edges']),
               'direct': connectivity([n['node_id'] for n in document['nodes']], document['edges'])}
        if part in parts:
            destination = staging_root / part
            if destination.exists():
                raise ValueError(f'Staging destination already exists: {destination}')
            archive = git(repository, 'archive', 'HEAD', part)
            with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
                for member in stream:
                    target = (staging_root / member.name).resolve()
                    if not target.is_relative_to(destination) or member.issym() or member.islnk():
                        raise ValueError('Unsafe archive member')
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                    elif member.isfile():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(stream.extractfile(member).read())
            row.update(upgrade_component(destination))
        audit.append(row)
    missing = set(parts) - {row['part'] for row in audit}
    if missing:
        raise ValueError(f'Parts absent from snapshot: {sorted(missing)}')
    # Completed studies without eligible groups have a manifest but no roadmap.
    for name in paths:
        if name.endswith('/manifest.json') and len(Path(name).parts) == 2:
            part = Path(name).parts[0]
            if part not in {row['part'] for row in audit}:
                manifest = json.loads(git(repository, 'show', f'HEAD:{name}'))
                if manifest.get('status') == 'complete_no_eligible_groups':
                    audit.append({'part': part, 'pose_count': 0, 'direct_edge_count': 0,
                                  'status': 'no_eligible_groups', 'direct': connectivity([], [])})
    audit.sort(key=lambda r: r['part'])
    report = {'schema_version': 1, 'source_commit': git(repository, 'rev-parse', 'HEAD').decode().strip(),
              'workpieces': audit, 'disconnected_workpieces': [r['part'] for r in audit if r['pose_count'] and not r['direct']['strongly_connected']],
              'note': 'Candidates establish orientation-level connectivity, not physical reachability.'}
    write_json(staging_root / 'connectivity_audit.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--staging-root', required=True, type=Path)
    parser.add_argument('--parts', nargs='+', default=['Qk1a', 'Dl1a'])
    args = parser.parse_args()
    report = stage(args.repository, args.staging_root, args.parts)
    print(json.dumps({'audited': len(report['workpieces']), 'disconnected': report['disconnected_workpieces'],
                      'staging_root': str(args.staging_root)}))


if __name__ == '__main__':
    main()
