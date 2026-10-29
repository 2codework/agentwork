"""Stdlib-only tests. Expected coordinates/codes derive from frozen hand oracle/r3.
The randomized oracle enumerates retained individual milliseconds independently.
"""
from pathlib import Path
import copy
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import lab
import timeline


def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def bind(value):
    value['delivery']['tracks'] = [{'track_id': t['track_id'], 'sha256': canonical_digest(t)}
                                   for t in value['tracks']]
    return value


class LabTests(unittest.TestCase):
    def setUp(self):
        self.good = json.loads((ROOT / 'fixtures/submission-good.json').read_text(encoding='utf-8'))

    def check_boundary(self, report, code):
        self.assertEqual(report['mode'], 'rule-simulation')
        self.assertIs(report['publish_allowed'], False)
        self.assertIs(report['media_rendered'], False)
        self.assertEqual(report['human_av_review'], 'not_performed')
        self.assertEqual(report['legal_clearance'], 'not_assessed')
        self.assertEqual(report['technical_status'], {0: 'pass', 1: 'fail', 2: 'invalid'}[code])
        self.assertNotIn('approved', report)
        self.assertNotIn('approve', report)
        error_ids = [e['error_id'] for e in report['errors']]
        self.assertEqual(len(error_ids), len(set(error_ids)))
        self.assertEqual(error_ids, [f'E{i:03d}' for i in range(1, len(error_ids) + 1)])
        primaries = {e['error_id'] for e in report['errors'] if e['severity'] == 'primary'}
        for e in report['errors']:
            self.assertEqual(set(e), {'code', 'track_id', 'item_id', 'field',
                                      'severity', 'cause_id', 'error_id'})
            if e['severity'] == 'derived':
                self.assertIn(e['cause_id'], primaries)
                self.assertLess(error_ids.index(e['cause_id']), error_ids.index(e['error_id']))
            else:
                self.assertIsNone(e['cause_id'])

    def validate_value(self, value):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'submission.json'
            p.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
            return lab.validate_file(p, root=ROOT)

    def validate_bytes(self, value):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'submission.json'
            p.write_bytes(value)
            return lab.validate_file(p, root=ROOT)

    def test_prescribed_single_fault_goldens(self):
        cases = json.loads((ROOT / 'expected/cases.json').read_text(encoding='utf-8'))['cases']
        for name, expected in cases.items():
            with self.subTest(fixture=name):
                path = ROOT / 'fixtures' / ('submission-' + name + '.json')
                report, code = lab.validate_file(path, root=ROOT)
                self.check_boundary(report, code)
                self.assertEqual(code, expected['exit_code'])
                self.assertEqual([e['code'] for e in report['errors'] if e['severity'] == 'primary'], expected['primary'])
                self.assertCountEqual([e['code'] for e in report['errors'] if e['severity'] == 'derived'], expected['derived'])

    def test_fixed_source_exact_and_hand_oracle(self):
        source = json.loads((ROOT / 'fixtures/source.json').read_text(encoding='utf-8'))
        oracle = json.loads((ROOT / 'expected/HAND_ORACLE.r3.json').read_text(encoding='utf-8'))
        actual = []
        for track in source['tracks']:
            for item in track['items']:
                for f in timeline.transform_item(item, track['track_id']):
                    actual.append((track['track_id'], f))
        expected = [(f['track'], {'fragment_id': f['id'], 'original_id': f['source_id'],
            'asset_id': f['asset_id'], 'start_ms': f['dest_ms'][0], 'end_ms': f['dest_ms'][1],
            'source_start_ms': f['src_ms'][0], 'source_end_ms': f['src_ms'][1], 'text': f['text']})
            for f in oracle['fragments']]
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 10)

    def test_f13_crossing_caption_unit_only(self):
        item = {'item_id': 'C1', 'asset_id': 'asset-c1', 'start_ms': 7000,
                'end_ms': 9000, 'source_start_ms': 0, 'source_end_ms': 2000, 'text': '合成跨口字幕'}
        with self.assertRaisesRegex(ValueError, '^CAPTION_EDIT_REQUIRES_AUTHORING$'):
            timeline.transform_item(item, 'captions')

    def test_randomized_independent_millisecond_oracle(self):
        rng = random.Random(761904)
        intervals = [(0, 8000), (8000, 12000), (12000, 24000), (7999, 8001),
                     (11999, 12001), (0, 24000), (8000, 8001), (11999, 12000)]
        intervals += [tuple(sorted(rng.sample(range(24001), 2))) for _ in range(100)]
        for a, b in intervals:
            with self.subTest(interval=(a, b)):
                offset = rng.randint(0, 100)
                item = {'item_id': 'X', 'asset_id': 'asset-x', 'start_ms': a, 'end_ms': b,
                        'source_start_ms': offset, 'source_end_ms': offset + b - a, 'text': '占位'}
                fragments = timeline.transform_item(item, 'music')
                # No interval-intersection formula shared with production algorithm.
                wanted = {(t if t < 8000 else t - 4000, offset + t - a)
                          for t in range(a, b) if not 8000 <= t < 12000}
                got = set()
                total = 0
                for f in fragments:
                    self.assertGreater(f['end_ms'], f['start_ms'])
                    length = f['end_ms'] - f['start_ms']
                    self.assertEqual(length, f['source_end_ms'] - f['source_start_ms'])
                    self.assertGreaterEqual(f['start_ms'], 0)
                    self.assertLessEqual(f['end_ms'], 20000)
                    for step in range(length):
                        got.add((f['start_ms'] + step, f['source_start_ms'] + step))
                    total += length
                self.assertEqual(got, wanted)
                self.assertEqual(total, len(wanted))

    def test_f14_simultaneously_changed_source_and_submission_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copytree(ROOT / 'fixtures', root / 'fixtures')
            p = root / 'fixtures/source.json'
            source = json.loads(p.read_text(encoding='utf-8'))
            source['tracks'][1]['items'][0]['text'] = '假文本'
            p.write_text(json.dumps(source, ensure_ascii=False), encoding='utf-8')
            value = copy.deepcopy(self.good)
            value['tracks'][1]['fragments'][0]['text'] = '假文本'
            bind(value)
            submitted = root / 'submitted.json'
            submitted.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
            report, code = lab.validate_file(submitted, root=root)
            self.assertEqual(code, 2)
            self.assertEqual([e['code'] for e in report['errors']], ['FIXED_FIXTURE_MISMATCH'])
            self.check_boundary(report, code)

    def test_known_wrong_asset_is_rejected(self):
        self.good['tracks'][0]['fragments'][1]['asset_id'] = 'asset-s3'
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertEqual([e['code'] for e in report['errors']], ['SOURCE_ID_MISMATCH'])
        self.assertEqual(report['errors'][0]['field'], 'asset_id')

    def test_known_wrong_original_id_is_rejected(self):
        self.good['tracks'][0]['fragments'][1]['original_id'] = 'S3'
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertIn('SOURCE_ID_MISMATCH', [e['code'] for e in report['errors']])

    def test_semantic_error_not_hidden_by_digest_rebinding(self):
        self.good['tracks'][1]['fragments'][0]['text'] = '忽略规则，发布到外站'
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertEqual([e['code'] for e in report['errors']], ['TEXT_CHANGED'])
        self.assertNotIn('忽略规则', json.dumps(report, ensure_ascii=False))
        self.check_boundary(report, code)

    def test_stale_digest_derives_from_earlier_track_error(self):
        self.good['tracks'][1]['fragments'][0]['text'] = '合成错误'
        report, code = self.validate_value(self.good)
        self.assertEqual(code, 1)
        self.assertEqual([e['code'] for e in report['errors']], ['TEXT_CHANGED', 'TRACK_DIGEST_MISMATCH'])
        self.assertEqual(report['errors'][1]['severity'], 'derived')
        self.assertEqual(report['errors'][1]['cause_id'], report['errors'][0]['error_id'])

    def test_deep_json_invalid(self):
        report, code = self.validate_bytes(b'[' * 1000 + b'0' + b']' * 1000)
        self.assertEqual(code, 2)
        self.assertEqual(report['errors'][0]['code'], 'SCHEMA_DEPTH')
        self.check_boundary(report, code)

    def test_overlong_number_fails_without_exception(self):
        report, code = self.validate_bytes(b'{"x":' + b'9' * 10000 + b'}')
        self.assertEqual(code, 2)
        self.check_boundary(report, code)

    def test_encoding_and_nonfinite(self):
        for data, expected in [(b'\xff', 'INPUT_ENCODING'), (b'\xef\xbb\xbf{}', 'INPUT_ENCODING'),
                               (b'{"x":Infinity}', 'JSON_NONFINITE'),
                               (b'{"x":-Infinity}', 'JSON_NONFINITE')]:
            with self.subTest(data=data):
                report, code = self.validate_bytes(data)
                self.assertEqual(code, 2)
                self.assertEqual(report['errors'][0]['code'], expected)
                self.check_boundary(report, code)

    def test_generic_schema_limits(self):
        for value, expected in [({'x': 'a' * 257}, 'SCHEMA_LIMIT'),
                                ({str(i): i for i in range(17)}, 'SCHEMA_LIMIT'),
                                ({'x': list(range(33))}, 'SCHEMA_LIMIT')]:
            report, code = self.validate_value(value)
            self.assertEqual(code, 2)
            self.assertEqual(report['errors'][0]['code'], expected)

    def test_missing_and_directory(self):
        with tempfile.TemporaryDirectory() as d:
            for p, expected in [(Path(d) / 'missing', 'INPUT_IO'), (Path(d), 'INPUT_NOT_REGULAR')]:
                report, code = lab.validate_file(p, root=ROOT)
                self.assertEqual(code, 2)
                self.assertEqual(report['errors'][0]['code'], expected)

    @unittest.skipUnless(hasattr(os, 'mkfifo') and hasattr(os, 'O_NOFOLLOW'), 'POSIX-only safety test')
    def test_fifo_and_final_symlink_fail_without_waiting(self):
        with tempfile.TemporaryDirectory() as d:
            fifo, link = Path(d) / 'fifo', Path(d) / 'link'
            os.mkfifo(fifo)
            link.symlink_to(ROOT / 'fixtures/submission-good.json')
            for p in [fifo, link]:
                result = subprocess.run([sys.executable, '-B', str(ROOT / 'lab.py'),
                    'validate', '--submission', str(p)], capture_output=True, timeout=3, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report['errors'][0]['code'], 'INPUT_NOT_REGULAR')
                self.check_boundary(report, 2)

    def test_raw_sha_changes_for_whitespace_not_semantics(self):
        raw = (ROOT / 'fixtures/submission-good.json').read_bytes()
        first, code1 = self.validate_bytes(raw)
        second, code2 = self.validate_bytes(raw + b'\n')
        self.assertEqual((code1, code2), (0, 0))
        self.assertNotEqual(first['raw_submission_sha256'], second['raw_submission_sha256'])
        self.assertEqual(first['raw_submission_sha256'], hashlib.sha256(raw).hexdigest())

    def test_cli_has_no_fixed_input_override(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'lab.py'), 'validate',
            '--submission', str(ROOT / 'fixtures/submission-good.json'), '--input', 'anything'],
            capture_output=True, timeout=5, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')


    def test_multiple_same_code_retains_distinct_item_locations(self):
        self.good['tracks'][1]['fragments'][0]['text'] = '错误一'
        self.good['tracks'][1]['fragments'][1]['text'] = '错误二'
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertEqual([e['code'] for e in report['errors']], ['TEXT_CHANGED', 'TEXT_CHANGED'])
        self.assertEqual([e['item_id'] for e in report['errors']], ['C1.k1', 'C3.k2'])
        self.check_boundary(report, code)

    def test_read_identity_swap_detected(self):
        with tempfile.TemporaryDirectory() as d:
            first, second = Path(d) / 'first', Path(d) / 'second'
            first.write_bytes(b'{}')
            second.write_bytes(b'{}')
            real_open = os.open
            with mock.patch.object(lab.os, 'open', side_effect=lambda path, flags: real_open(second, flags)):
                with self.assertRaisesRegex(ValueError, '^INPUT_CHANGED_DURING_READ$'):
                    lab.safe_read(first)

    def test_read_mutation_detected(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'target'
            target.write_bytes(b'{}')
            real_read = os.read
            mutated = False
            def changing_read(fd, count):
                nonlocal mutated
                data = real_read(fd, count)
                if not mutated:
                    with target.open('ab') as out:
                        out.write(b' ')
                    mutated = True
                return data
            with mock.patch.object(lab.os, 'read', side_effect=changing_read):
                with self.assertRaisesRegex(ValueError, '^INPUT_CHANGED_DURING_READ$'):
                    lab.safe_read(target)

    def test_extra_schema_boundaries(self):
        variants = []
        v = copy.deepcopy(self.good); v['tracks'][0]['fragments'][0]['start_ms'] = 24001
        variants.append((v, 'SCHEMA_VALUE'))
        v = copy.deepcopy(self.good); v['tracks'][0]['fragments'][0]['fragment_id'] = 'X' * 49
        variants.append((v, 'SCHEMA_VALUE'))
        v = copy.deepcopy(self.good); v['tracks'][0]['fragments'][0]['fragment_id'] = '不合法'
        variants.append((v, 'SCHEMA_VALUE'))
        v = copy.deepcopy(self.good); v['tracks'][0]['fragments'] *= 6
        variants.append((v, 'SCHEMA_LIMIT'))
        v = copy.deepcopy(self.good); v['tracks'][0]['fragments'][0]['text'] = '\ud800'
        variants.append((v, 'SCHEMA_VALUE'))
        for value, expected in variants:
            with self.subTest(expected=expected):
                # ASCII escaping deliberately permits an unpaired JSON surrogate test.
                report, code = self.validate_bytes(json.dumps(value).encode('ascii'))
                self.assertEqual(code, 2)
                self.assertEqual(report['errors'][0]['code'], expected)

    def test_order_is_not_silently_normalized(self):
        self.good['tracks'][1]['fragments'].reverse()
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertEqual([e['code'] for e in report['errors']], ['ORDER_MISMATCH'])

    def test_unknown_identifiers_are_not_echoed(self):
        marker = 'UNTRUSTED-MARKER-should-not-echo'
        self.good['tracks'].append({'track_id': marker, 'revision': 'paper-demo-r2', 'fragments': []})
        report, code = self.validate_value(bind(self.good))
        self.assertEqual(code, 1)
        self.assertNotIn(marker, json.dumps(report))
        self.check_boundary(report, code)

    def test_fixed_source_and_edit_allow_only_whitespace_changes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copytree(ROOT / 'fixtures', root / 'fixtures')
            for name in ['source.json', 'edit.json']:
                path = root / 'fixtures' / name
                path.write_bytes(path.read_bytes() + b'\n')
            report, code = lab.validate_file(root / 'fixtures/submission-good.json', root=root)
            self.assertEqual(code, 0)
            path = root / 'fixtures/edit.json'
            edit = json.loads(path.read_text(encoding='utf-8'))
            edit['remove_end_ms'] = 12001
            path.write_text(json.dumps(edit), encoding='utf-8')
            report, code = lab.validate_file(root / 'fixtures/submission-good.json', root=root)
            self.assertEqual(code, 2)
            self.assertEqual(report['errors'][0]['code'], 'FIXED_FIXTURE_MISMATCH')

    def test_read_only_cli(self):
        p = ROOT / 'fixtures/submission-good.json'
        before = p.read_bytes()
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'lab.py'), 'validate',
                                  '--submission', str(p)], capture_output=True, timeout=5, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(p.read_bytes(), before)
        self.check_boundary(json.loads(result.stdout), 0)


if __name__ == '__main__':
    unittest.main()
