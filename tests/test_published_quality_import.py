import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import pytest
from bibazu_stable_roadmaps.import_catalogues import import_catalogues
from bibazu_stable_roadmaps.inputs import sha256, load_source
from bibazu_stable_roadmaps.published_quality import analyze_pose_quality

def make_git_catalogue(source_folder,tmp_path,*,bad_report=False):
    repo=tmp_path/'upstream'
    folder=repo/'Test/catalogue/moving'
    folder.mkdir(parents=True)
    (repo/'Test/run').mkdir()
    mesh=repo/'Test/Test.stl'
    shutil.copyfile(source_folder/'Test1.stl',mesh)
    config=repo/'Test/run/config.json'
    config.write_bytes(b'{"alpha_deg":45,"beta_deg":0}\n')
    evidence=folder/'grouping-evidence.json'
    evidence.write_bytes(b'{"model":"observed-seated-geodesic-basins-v1","paths":[]}\n')
    entry={'label':'unknown','stability':'unknown','escape_lift_mm':None,'escape_target_source_id':None,'escape_within_group':None}
    data={'schema_version':1,'workpiece':'Test','condition':'moving','total_trials':10000,'settled_trials':10000,'model':'observed-seated-geodesic-basins-v1',
        'settings':{'recognition':{'symmetry_quaternions_xyzw':[[0,0,0,1]]}},
        'source':{'mesh_path':'Test/Test.stl','mesh_sha256':sha256(mesh),'run_dir':'Test/run','config_sha256':sha256(config)},
        'poses':[{'id':'Test_0001','count':10000,'incidence_percent':100.,'quaternion_xyzw':[0,0,0,1],'pose_quality':entry}],
        'pose_quality_assessment':{'input_signature':'fixture'},'grouping_evidence':'grouping-evidence.json','grouping_evidence_sha256':sha256(evidence)}
    (folder/'catalogue.json').write_text(json.dumps(data),encoding='utf-8')
    report={'schema_version':1,'producer':'dashas_drop_sim','method':'sampled_seated_escape_lift','method_version':1,
        'input_signature':'fixture','source_sha256':'invalid' if bad_report else sha256(folder/'catalogue.json'),
        'mesh_sha256':sha256(mesh),'config_sha256':sha256(config),'thresholds_mm':{'fragile':.1,'resistant':.5},'poses':{'Test_0001':entry}}
    (folder/'pose_quality.json').write_text(json.dumps(report),encoding='utf-8')
    (folder/'files.sha256.json').write_text(json.dumps({p.name:sha256(p) for p in folder.iterdir()}),encoding='utf-8')
    (repo/'index.json').write_text(json.dumps({'workpieces':[{'workpiece':'Test','grouped_10000_catalogues':{'moving':{'path':'Test/catalogue/moving/catalogue.json'}}}]}))
    subprocess.run(['git','init',str(repo)],check=True,capture_output=True)
    git=['git','-c',f'safe.directory={repo.as_posix()}','-C',str(repo)]
    subprocess.run(git+['add','-A'],check=True,capture_output=True)
    subprocess.run(git+['-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','fixture'],check=True,capture_output=True)
    return repo,folder

def test_import_rebases_local_hashes_and_preserves_upstream_provenance(source_folder,tmp_path):
    repo,original=make_git_catalogue(source_folder,tmp_path)
    sources=import_catalogues(repo,tmp_path/'imported','HEAD','moving')
    report=analyze_pose_quality(load_source(sources[0]))
    assert report['producer']=='dashas_drop_sim' and report['published'] is True
    assert report['source_sha256']==sha256(sources[0])
    assert report['upstream_provenance']['catalogue_sha256']==sha256(original/'catalogue.json')
    assert report['upstream_provenance']['report_sha256']==sha256(original/'pose_quality.json')
    assert report['poses']['Test_0001']['stability']=='unknown'
    from bibazu_stable_roadmaps.generate import generate_one, GenerationConfig
    status,result=generate_one(sources[0],GenerationConfig(str(tmp_path/'exports'),outputs=('yaml',)))
    assert status=='completed'
    portable=load_source(Path(result['folder'])/'source/poses.json')
    assert analyze_pose_quality(portable)['poses']==report['poses']
    sources[0].with_name('upstream_pose_quality.json').write_bytes(b'changed original report')
    with pytest.raises(ValueError,match='provenance'):
        analyze_pose_quality(load_source(sources[0]))

def test_import_rejects_catalogue_report_mismatch_even_with_valid_inventory(source_folder,tmp_path):
    repo,_=make_git_catalogue(source_folder,tmp_path,bad_report=True)
    with pytest.raises(ValueError,match='stability differs'):
        import_catalogues(repo,tmp_path/'imported','HEAD','moving')
