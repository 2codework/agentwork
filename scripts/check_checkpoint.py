#!/usr/bin/env python3
"""Read-only checkpoint consistency prototype; Python standard library only.
Not an authenticity, provenance, content-quality, or test-execution proof.
Use on a quiescent, trusted checkout; concurrent adversarial mutation is out of scope.
Exact exclusions: root .git (file/directory and descendants), any __pycache__
component, paths ending .pyc, and root VALIDATION.json. Other ignored files
(including .DS_Store) are NOT excluded; nested validation files remain covered.
This is a checkout-file check, not a Git index or remote publication check.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat

SCOPE = 'all repo files excluding .git, caches, pyc and this VALIDATION.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError('non-finite JSON constant: ' + value)


def valid_path(name):
    require(isinstance(name, str) and name, 'invalid manifest path')
    require(not any(c in name for c in ('\\', ':', '\0')), 'unsafe manifest path: ' + repr(name))
    parts = name.split('/')
    require(all(p not in ('', '.', '..') for p in parts), 'noncanonical manifest path: ' + repr(name))
    require(not excluded(name), 'excluded manifest path: ' + name)


def excluded(name):
    parts = name.split('/')
    return (parts[0] == '.git' or '__pycache__' in parts or
            name.endswith('.pyc') or name == 'VALIDATION.json')


def inventory(root):
    """Never follow directory/file symlinks; prune metadata before descending."""
    found = {}
    def visit(directory):
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda e: e.name):
                path = Path(entry.path)
                name = path.relative_to(root).as_posix()
                if excluded(name):
                    continue
                mode = entry.stat(follow_symlinks=False).st_mode
                require(not stat.S_ISLNK(mode), 'symlink not supported: ' + name)
                if stat.S_ISDIR(mode):
                    visit(path)
                else:
                    require(stat.S_ISREG(mode), 'nonregular file: ' + name)
                    found[name] = path
    visit(root)
    return found


def check(root):
    root = Path(root).resolve(strict=True)
    checkpoint = root / 'VALIDATION.json'
    require(stat.S_ISREG(checkpoint.lstat().st_mode), 'checkpoint must be a regular non-symlink file')
    doc = json.loads(checkpoint.read_text(encoding='utf-8'), object_pairs_hook=unique,
                     parse_constant=invalid_constant)
    require(isinstance(doc, dict), 'checkpoint must be an object')
    require(doc.get('manifest_scope') == SCOPE, 'unsupported manifest_scope')
    manifest = doc.get('sha256')
    require(isinstance(manifest, dict) and manifest, 'sha256 must be a nonempty object')
    for name, digest in manifest.items():
        valid_path(name)
        require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest),
                'invalid SHA-256: ' + name)
    actual = inventory(root)
    missing = sorted(manifest.keys() - actual.keys())
    added = sorted(actual.keys() - manifest.keys())
    require(not missing and not added, f'file-set mismatch: missing={missing}; unlisted={added}')
    changed = []
    for name, path in actual.items():
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(chunk)
        if h.hexdigest() != manifest[name]:
            changed.append(name)
    require(not changed, 'SHA-256 mismatch: ' + ', '.join(changed))
    return len(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    try:
        print(f'Checkpoint consistent: {check(args.root)} files. Evidence claims not verified.')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Checkpoint failed: {error}\n')


if __name__ == '__main__':
    main()
