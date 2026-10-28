"""Stable IDs define reviewed vendor families; display titles never infer facts."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path(os.environ.get('ASSISTANT_MAPPING_ROOT', Path(__file__).resolve().parents[1]))
spec = importlib.util.spec_from_file_location('mapping_adapter', ROOT / 'scripts/assistant_workspace.py')
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
EXPECTED = {
    'assistant-chatgpt-agent': 'OpenAI',
    'assistant-chatgpt-deep-research': 'OpenAI',
    'assistant-claude-cowork': 'Anthropic',
    'assistant-claude-research': 'Anthropic',
    'assistant-gemini-apps-deep-research': 'Google',
    'assistant-perplexity-projects': 'Perplexity',
    'assistant-perplexity-research': 'Perplexity',
    'assistant-perplexity-create-files-apps': 'Perplexity',
}


class PlatformFamilyTests(unittest.TestCase):
    def setUp(self):
        raw = ROOT / 'learning/assistant-workspace/r1/raw'
        self.research = json.loads((raw / 'research.json').read_text())
        self.sources = json.loads((raw / 'sources.json').read_text())

    def test_all_eight_reviewed_id_mappings(self):
        actual = {c['raw_record']['id']: c['assistant_workspace']['platform_family_id']
                  for c in A.adapt(self.research, self.sources)}
        self.assertEqual(actual, EXPECTED)

    def test_titles_cannot_change_vendor_family(self):
        for entity in self.research['items']:
            entity['name'] = 'Unrelated arbitrary title'
        actual = {c['raw_record']['id']: c['assistant_workspace']['platform_family_id']
                  for c in A.adapt(self.research, self.sources)}
        self.assertEqual(actual, EXPECTED)

    def test_each_unknown_id_rejected_even_with_known_title(self):
        for i in range(8):
            with self.subTest(index=i):
                mutated = copy.deepcopy(self.research)
                mutated['items'][i]['id'] += '-unknown'
                with self.assertRaisesRegex(ValueError, 'assistant cardinality'):
                    A.adapt(mutated, self.sources)


if __name__ == '__main__':
    unittest.main()
