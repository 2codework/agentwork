"""Regression tests for offline publication gates; no network or packages."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('pages_check', Path(__file__).resolve().parents[1] / 'scripts/check_pages.py')
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)


class PagesChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'dist').mkdir()
        self.write('index.html', '<main id="main"><a href="#main">Read</a></main>')
        self.write('data.json', '{"schema_version":1}')
        self.write('.nojekyll', '')
        shutil.copytree(self.root / 'dist', self.root / 'docs')

    def write(self, name, text, both=False):
        (self.root / 'dist' / name).write_text(text)
        if both:
            (self.root / 'docs' / name).write_text(text)

    def test_matching_site(self):
        pages.check(self.root)

    def test_pages_drift(self):
        self.write('data.json', '{}')
        with self.assertRaisesRegex(ValueError, 'differs'):
            pages.check(self.root)

    def test_missing_page(self):
        (self.root / 'docs/data.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            pages.check(self.root)

    def test_duplicate_json_key(self):
        self.write('data.json', '{"a":1,"a":2}', both=True)
        with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
            pages.check(self.root)

    def test_nonfinite_json(self):
        self.write('data.json', '{"a":NaN}', both=True)
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            pages.check(self.root)

    def test_missing_local_link(self):
        self.write('index.html', '<a href="missing.js">Missing</a>', both=True)
        with self.assertRaisesRegex(ValueError, 'broken local'):
            pages.check(self.root)

    def test_missing_fragment(self):
        self.write('index.html', '<a href="#missing">Missing</a>', both=True)
        with self.assertRaisesRegex(ValueError, 'broken anchor'):
            pages.check(self.root)

    def test_project_absolute_path(self):
        self.write('index.html', '<a href="/index.html">Root</a>', both=True)
        with self.assertRaisesRegex(ValueError, 'project-path'):
            pages.check(self.root)

    def test_unsafe_protocol(self):
        self.write('index.html', '<a href="javascript:alert(1)">Unsafe</a>', both=True)
        with self.assertRaisesRegex(ValueError, 'unsafe link'):
            pages.check(self.root)

    def test_documentation_extra_allowed(self):
        (self.root / 'docs/QUALITY.md').write_text('Project documentation')
        pages.check(self.root)


if __name__ == '__main__':
    unittest.main()
