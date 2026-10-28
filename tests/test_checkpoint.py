import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_checkpoint import SCOPE, check


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'README.md').write_bytes(b'hello\n')
        self.doc = {'manifest_scope': SCOPE, 'sha256': {
            'README.md': hashlib.sha256(b'hello\n').hexdigest()}}
        self.save()

    def save(self):
        (self.root / 'VALIDATION.json').write_text(json.dumps(self.doc))

    def reject(self):
        with self.assertRaises((ValueError, OSError)):
            check(self.root)

    def test_clean(self):
        self.assertEqual(check(self.root), 1)

    def test_changed(self):
        (self.root / 'README.md').write_bytes(b'changed')
        self.reject()

    def test_missing(self):
        (self.root / 'README.md').unlink()
        self.reject()

    def test_extra(self):
        (self.root / 'extra.txt').write_bytes(b'new')
        self.reject()

    def test_rename(self):
        (self.root / 'README.md').rename(self.root / 'renamed.md')
        self.reject()

    def test_exact_exclusions(self):
        for name in ('.git/config', 'nested/__pycache__/ignored', 'nested/module.pyc'):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b'ignored')
        self.assertEqual(check(self.root), 1)

    def test_ds_store_not_silently_excluded(self):
        (self.root / '.DS_Store').write_bytes(b'ignored by git is not ignored by gate')
        self.reject()

    def test_nested_validation_is_included(self):
        (self.root / 'nested').mkdir()
        (self.root / 'nested/VALIDATION.json').write_text('{}')
        self.reject()

    def test_unsafe_and_excluded_paths(self):
        for name in ('../outside', '/absolute', './README.md', 'a//b', 'a/../b',
                     'C:/outside', 'a\\b', '.git/config', '__pycache__/x',
                     'x.pyc', 'VALIDATION.json', ''):
            with self.subTest(name=name):
                self.doc['sha256'] = {name: '0' * 64}
                self.save()
                self.reject()

    def test_digest_shape(self):
        for digest in ('f' * 63, 'A' * 64, None, 1):
            with self.subTest(digest=digest):
                self.doc['sha256']['README.md'] = digest
                self.save()
                self.reject()

    def test_duplicate_keys(self):
        (self.root / 'VALIDATION.json').write_text('{"sha256":{},"sha256":{}}')
        self.reject()

    def test_nonfinite_json(self):
        (self.root / 'VALIDATION.json').write_text('{"value":NaN}')
        self.reject()

    def test_scope_and_shape(self):
        for doc in ([], {}, {'manifest_scope': 'something else', 'sha256': {}},
                    {'manifest_scope': SCOPE, 'sha256': []}):
            self.doc = doc
            self.save()
            self.reject()

    def test_file_symlink(self):
        (self.root / 'link').symlink_to(self.root / 'README.md')
        self.reject()

    def test_directory_symlink(self):
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        self.reject()

    def test_checkpoint_symlink(self):
        p = self.root / 'VALIDATION.json'
        p.rename(self.root / 'other.json')
        p.symlink_to(self.root / 'other.json')
        self.reject()

    def test_nonregular(self):
        import os
        os.mkfifo(self.root / 'pipe')
        self.reject()

    def test_claims_not_verified(self):
        self.doc['python_tests_passed'] = 99999
        self.save()
        self.assertEqual(check(self.root), 1)


if __name__ == '__main__':
    unittest.main()
