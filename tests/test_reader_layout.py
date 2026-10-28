"""Static containment contracts; real browser geometry is verified separately."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReaderLayoutTests(unittest.TestCase):
    def test_reader_track_can_shrink_below_code_intrinsic_width(self):
        css = (ROOT / 'web/style.css').read_text()
        self.assertIn('grid-template-columns:230px minmax(0,1fr)', css)
        self.assertRegex(css, r'\.reading\s*\{\s*min-width:\s*0\s*;?\s*\}')

    def test_code_preserves_lines_with_local_horizontal_scroll(self):
        css = (ROOT / 'web/style.css').read_text()
        rules = re.findall(r'(?<![\w.-])pre\s*\{([^}]+)\}', css)
        properties = {}
        for rule in rules:
            for item in rule.split(';'):
                if ':' in item:
                    key, value = item.split(':', 1)
                    properties[key.strip()] = value.strip()
        self.assertEqual(properties['max-width'], '100%')
        self.assertEqual(properties['overflow-x'], 'auto')
        self.assertEqual(properties['white-space'], 'pre')

    def test_mobile_reader_remains_single_column(self):
        css = (ROOT / 'web/style.css').read_text()
        mobile = css.split('@media(max-width:800px)', 1)[1]
        self.assertRegex(mobile, r'main\{grid-template-columns:1fr;')
