"""Frozen original creative rules lab: stdlib integrity, unpack tests and publication copy."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='bfb3bf300c8536f7b591307c39d4cec41be10104e8ff6b21c2308d34f1e6b75a'
ZIP_SHA='c1cdcd93b0cee224d76bc589d5622840e3030409da82ea3973e927a8e3049cbf'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root=ROOT,execute=False):
    base=Path(root)/'learning/creative-delivery/r1'
    manifest=base/'integration-manifest.json'
    if sha(manifest)!=MANIFEST_SHA: raise ValueError('creative lab integration manifest changed')
    m=json.loads(manifest.read_text())
    paths={p.relative_to(base).as_posix():p for p in base.rglob('*') if p.is_file() or p.is_symlink()}
    if set(paths)!=set(m['files'])|{'integration-manifest.json'}: raise ValueError('creative lab file set changed')
    for name,expected in m['files'].items():
        if name.startswith('/') or '..' in name.split('/') or '\\' in name: raise ValueError('unsafe manifest path')
        p=paths[name]
        if p.is_symlink() or not p.is_file() or sha(p)!=expected: raise ValueError('creative lab frozen bytes changed: '+name)
    archive=base/'creative-delivery-lab-r1.zip'
    if sha(archive)!=ZIP_SHA: raise ValueError('creative lab ZIP changed')
    members=json.loads((base/'SHA256.json').read_text())['members']
    with zipfile.ZipFile(archive) as z:
        if sorted(z.namelist())!=sorted(members) or len(z.namelist())!=36 or len(set(z.namelist()))!=36: raise ValueError('creative lab ZIP members changed')
        for name in z.namelist():
            if not name.startswith('creative-delivery-lab/') or '..' in name.split('/'): raise ValueError('unsafe ZIP path')
            data=z.read(name)
            if hashlib.sha256(data).hexdigest()!=members[name] or data!=(base/'source'/name.removeprefix('creative-delivery-lab/')).read_bytes(): raise ValueError('creative lab member differs')
        if execute:
            with tempfile.TemporaryDirectory(prefix='creative-rule-check-') as tmp:
                z.extractall(tmp)
                cwd=Path(tmp)/'creative-delivery-lab'
                test=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=cwd,capture_output=True,text=True,timeout=90)
                if test.returncode or 'Ran 25 tests' not in test.stderr: raise ValueError('creative lab 25 tests failed: '+test.stderr)
                gold=subprocess.run([sys.executable,'-B','lab.py','check-golden'],cwd=cwd,capture_output=True,text=True,timeout=90)
                if gold.returncode: raise ValueError('creative lab goldens failed: '+gold.stderr)
                report=json.loads(gold.stdout)
                if report['golden_cases_checked']!=24 or report['golden_mismatches'] or report['publish_allowed'] is not False: raise ValueError('creative lab golden result differs')
    return m

def publish(root,dest):
    verify(root,execute=True)
    shutil.copytree(Path(root)/'learning/creative-delivery/r1',Path(dest)/'creative-delivery/r1',dirs_exist_ok=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true',required=True);parser.parse_args()
    verify(execute=True)
    print('Frozen creative lab: 36 ZIP members; unpacked 25 tests + 24 golden cases passed. Original rules only; no product/media/publication approval.')
