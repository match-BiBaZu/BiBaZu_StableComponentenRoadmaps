"""Stage frequency-filtered individual/group exports from an existing catalogue."""
import argparse
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import shutil

import yaml

from .generate import _write_graphml, write_json
from .individual_groups import individualize
from .inputs import load_source, sha256
from .roadmap import build_roadmap, handover_dict
from .render import thumbnails, embed_thumbnails, render_roadmap, render_pose_sheets


def stage_component(original, destination, cutoff=1., progress=print):
    original,destination=Path(original),Path(destination)
    if destination.exists(): raise ValueError(f'Staging folder exists: {destination}')
    name=original.name
    old_path=original/f'{name}_roadmap.json'
    document=json.loads(old_path.read_text(encoding='utf-8'))
    source=load_source(original/'source/poses.json')
    by_id={p.source_id:p for p in source.poses}
    built=build_roadmap(source,[(by_id[n['source_pose_ids'][0]],n['node_id']) for n in document['nodes']])
    built.document=document
    previous_keys=dict(document.get('group_keys',{}))
    previous_choices=[c['edge_id'] for c in document.get('consumer_export',{}).get('calibration_choices',[])]
    previous_hash=sha256(old_path)
    built=individualize(source,built,cutoff,progress)
    doc=built.document
    timestamp=datetime.now(timezone.utc).isoformat()
    doc['generation']=dict(doc.get('generation',{}),generated_utc=timestamp,
        minimum_frequency_percent=cutoff,renumber_by_frequency=True,
        pose_id_mapping={p.source_id:i for p,i in built.numbered},
        numbering_tie_break='original source ID',source_sha256=sha256(source.path))
    doc['migration']=dict(previous_roadmap_sha256=previous_hash,
        previous_pose_groups=previous_keys,previous_choice_ids=previous_choices,
        historical_export='history/previous_roadmap.json.gz',requires_explicit_reimport=True)
    destination.mkdir(parents=True)
    shutil.copytree(original/'source',destination/'source')
    if (original/'membership.csv').is_file(): shutil.copyfile(original/'membership.csv',destination/'membership.csv')
    history=destination/'history';history.mkdir()
    with gzip.open(history/'previous_roadmap.json.gz','wb') as handle: handle.write(old_path.read_bytes())
    manifest=json.loads((original/'manifest.json').read_text(encoding='utf-8'))
    manifest.update(generated_utc=timestamp,pose_count=len(doc['nodes']),group_count=len(doc['pose_groups']),
        transition_count=len(doc['edges']),minimum_frequency_percent=cutoff,
        status='complete' if doc['nodes'] else 'no_eligible_poses',input=doc['generation'],
        connectivity={'groups':doc['connectivity']['groups']},
        composite_transfer_count=0,member_transfer_count=0,
        group_transfer_count=len(doc['group_transfers']),group_route_count=len(doc['group_routes']),
        consumer_export=dict(version=3,route_policy='exported_only; no composite bridges',
            calibration_choice_count=len(doc['consumer_export']['calibration_choices']),
            execution_route_count=len(doc['consumer_export']['execution_routes'])))
    manifest['settings'].update(minimum_frequency_percent=cutoff,include_composites=False,renumber_by_frequency=True)
    if doc['nodes']:
        images=thumbnails(built);embed_thumbnails(doc,images)
        stem=destination/f'{name}_roadmap'
        stem.with_suffix('.json').write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        stem.with_suffix('.yaml').write_text(yaml.dump(handover_dict(doc),Dumper=yaml.CSafeDumper,
            sort_keys=False,allow_unicode=True),encoding='utf-8')
        _write_graphml(doc,stem.with_suffix('.graphml'))
        render_roadmap(built,stem,('png','svg'),images)
        render_pose_sheets(built,destination/'pose_sheets',('png','svg'))
    else:
        write_json(destination/'no_eligible_poses.json',dict(status='no_eligible_poses',cutoff=cutoff,
            reason='No source group has an individual member at or above the cutoff.',migration=doc['migration']))
    write_json(destination/'manifest.json',manifest)
    stats=doc['connectivity']['groups']
    text=f'# {name}: individual poses with shared group actions\n\n'
    if doc['nodes']: text+=f'![Roadmap]({name}_roadmap.png)\n\n'
    text+=f"Cutoff: **{cutoff:g}%**, applied separately to original group totals and individual observation frequencies. "
    text+='Exactly the cutoff qualifies; the source trial denominator is unchanged. Below-cutoff members are not displayed or used as witnesses. Groups without qualifying members are omitted.\n\n'
    text+='| Pose | Original observation | Individual frequency | Count | Group |\n|---:|---|---:|---:|---:|\n'
    for n in doc['nodes']:
        text+=f"| {n['node_id']} | {n['source_pose_ids'][0]} | {n['observed_frequency_percent']:g}% | {n['observed_count']} | {n['group_id']} |\n"
    text+=f"\n{len(doc['nodes'])} individual poses in {len(doc['pose_groups'])} groups. "
    all_stats=stats['all_candidates'];cart=stats['cartesian']
    text+=f"Candidate group reachability: **{all_stats['reachable_pair_count']}/{all_stats['total_pair_count']}**; Cartesian-only: **{cart['reachable_pair_count']}/{cart['total_pair_count']}**.\n\n"
    text+='Every outgoing action applies to all displayed members of its source group; any qualifying destination member satisfies its target group. A target in the current group requires no motion. There are no internal group transitions and no composite fallback bridges. Ordinary multi-step routes use retained single-axis actions. Disconnected components remain disconnected.\n\n'
    text+='Commands, witnesses, competing landing outcomes, previews and finished routes are in consumer-export version 3. Poses are numbered by individual frequency; stable group identities are separate. Previews use actual witnesses and invent no internal movement. Contact feasibility and settling reliability remain unverified; assigned pressure profiles and explicit source-group calibration are required.\n\n'
    text+='Original observations and memberships remain in `source/`. Historical exports are preserved under `history/` for explicit, hash-checked reimport; numeric group IDs must never be interpreted as new pose IDs. Existing recognition models continue to identify groups. See `manifest.json` and `files.sha256.json`.\n'
    if not doc['nodes']: text+='\n**No eligible poses at this cutoff. No active roadmap files are published.**\n'
    (destination/'README.md').write_text(text,encoding='utf-8')
    write_json(destination/'files.sha256.json',{p.relative_to(destination).as_posix():sha256(p)
        for p in sorted(destination.rglob('*')) if p.is_file()})
    return dict(part=name,pose_count=len(doc['nodes']),group_count=len(doc['pose_groups']),
        group_transfer_count=len(doc['group_transfers']),cartesian=cart,all_candidates=all_stats,status=manifest['status'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,required=True)
    parser.add_argument('--staging-root',type=Path,required=True)
    parser.add_argument('--parts',nargs='+',required=True)
    parser.add_argument('--cutoff',type=float,default=1.)
    args=parser.parse_args()
    for name in args.parts:
        result=stage_component(args.repository/name,args.staging_root/name,args.cutoff,lambda m:print(m,flush=True))
        write_json(args.staging_root/(name+'_audit.json'),result)
        print(json.dumps(result),flush=True)

if __name__=='__main__': main()
