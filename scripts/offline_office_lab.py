"""Publish frozen original offline exercise; never execute user data or products."""
import hashlib,json,shutil

def verify(root):
    lab=root/'learning/offline-office/r1'
    manifest=json.loads((lab/'integration-manifest.json').read_text())
    actual={p.relative_to(lab).as_posix() for p in lab.rglob('*') if p.is_file()}
    if actual != set(manifest['source_and_qa_sha256']) | {'integration-manifest.json'}:
        raise ValueError('offline lab file set changed')
    for name,digest in manifest['source_and_qa_sha256'].items():
        if name.startswith('/') or '..' in name.split('/') or '\\' in name:
            raise ValueError('unsafe offline lab manifest path')
        if hashlib.sha256((lab/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('offline lab frozen bytes changed: '+name)
    return manifest

def publish(root,dest):
    verify(root)
    shutil.copytree(root/'learning/offline-office/r1',dest/'offline-office/r1',dirs_exist_ok=True)
