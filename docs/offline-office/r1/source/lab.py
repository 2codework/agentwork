"""Original deterministic teaching exercise; no model or external dispatch."""
import argparse
import hashlib
import json
import os
import stat
import re
import sys
from datetime import date
from pathlib import Path

MAX_BYTES = 65536
KINDS = {'suggestion', 'offer', 'open_question', 'prerequisite', 'decision', 'blocked_action'}
FACT_KEYS = {'fact_id', 'text', 'kind', 'owner', 'due_date', 'depends_on', 'acceptance'}
ITEM_KEYS = {'item_id', 'fact_id', 'quote', 'kind', 'owner', 'due_date', 'depends_on', 'acceptance'}

class ContractError(ValueError):
    pass

def require(ok, code):
    if not ok:
        raise ContractError(code)

def keys(obj, expected):
    require(type(obj) is dict and set(obj) == expected, 'SCHEMA_FIELDS')

def nonempty(value):
    return type(value) is str and 0 < len(value.strip()) <= 1000

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def constant(_):
    raise ContractError('NONFINITE_JSON_NUMBER')

def read_json(path):
    # Refuse special files before open; O_NONBLOCK prevents a swapped FIFO hanging.
    # O_NOFOLLOW rejects a swapped final symlink; inode/device checks catch replacement.
    path = Path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'REGULAR_FILE_REQUIRED')
    require(hasattr(os, 'O_NOFOLLOW') and hasattr(os, 'O_NONBLOCK'), 'SAFE_OPEN_UNSUPPORTED')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        opened = os.fstat(fd)
        require(stat.S_ISREG(opened.st_mode), 'REGULAR_FILE_REQUIRED')
        require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'FILE_CHANGED_DURING_OPEN')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            raw = stream.read(MAX_BYTES + 1)
    finally:
        os.close(fd)
    require(len(raw) <= MAX_BYTES, 'FILE_TOO_LARGE')
    data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=constant)
    return data, hashlib.sha256(raw).hexdigest()

# Fixed authored answer key, not loaded from editable fixtures or golden reports.
# Editing this source changes the exercise trust root and is outside its assurance.
FIXED_ROWS = (
    ('F1', '提议先测试两版说明页，尚未决定。', 'suggestion', None, None, (), None),
    ('F2', '乙表示可以协助，但未承诺负责。', 'offer', None, None, (), None),
    ('F3', '发布日期尚未确定。', 'open_question', None, None, (), None),
    ('F4', '隐私审核未完成，完成前不得发布。', 'prerequisite', None, None, (), '隐私审核状态为完成'),
    ('F5', '决定由角色甲在2026-11-02前整理测试方案，完成标准为列出两版说明页及比较维度。', 'decision', 'ROLE-A', '2026-11-02', (), '列出两版说明页及比较维度'),
    ('F6', '发布须待隐私审核完成且发布日期确认。', 'blocked_action', None, None, ('F3', 'F4'), '隐私审核完成且发布日期已确认'),
)

def common(row):
    require(type(row['kind']) is str and row['kind'] in KINDS, 'INVALID_KIND')
    require(row['owner'] is None or (type(row['owner']) is str and re.fullmatch(r'ROLE-[A-Z]', row['owner'])), 'INVALID_OWNER')
    d = row['due_date']
    if d is not None:
        require(type(d) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}', d), 'INVALID_DATE')
        try:
            date.fromisoformat(d)
        except ValueError:
            raise ContractError('INVALID_DATE') from None
    deps = row['depends_on']
    require(type(deps) is list and len(deps) <= 20 and all(type(v) is str and re.fullmatch(r'F[1-9][0-9]*', v) for v in deps), 'INVALID_DEPENDENCIES')
    require(len(set(deps)) == len(deps), 'DUPLICATE_DEPENDENCY')
    require(row['acceptance'] is None or nonempty(row['acceptance']), 'INVALID_ACCEPTANCE')

def input_schema(data):
    keys(data, {'schema_version', 'synthetic', 'meeting_id', 'facts'})
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'INVALID_VERSION')
    require(data['synthetic'] is True and data['meeting_id'] == 'DEMO-M1', 'SYNTHETIC_ONLY')
    facts = data['facts']
    require(type(facts) is list and 1 <= len(facts) <= 20, 'INVALID_FACT_COUNT')
    seen = set()
    for row in facts:
        keys(row, FACT_KEYS)
        require(type(row['fact_id']) is str and re.fullmatch(r'F[1-9][0-9]*', row['fact_id']), 'INVALID_FACT_ID')
        require(row['fact_id'] not in seen, 'DUPLICATE_FACT_ID')
        seen.add(row['fact_id'])
        require(nonempty(row['text']), 'INVALID_TEXT')
        common(row)
        if row['kind'] in {'suggestion', 'offer', 'open_question'}:
            require(row['owner'] is None and row['due_date'] is None and row['acceptance'] is None, 'INVALID_NONCOMMITMENT')
    for row in facts:
        require(set(row['depends_on']) <= seen and row['fact_id'] not in row['depends_on'], 'INVALID_FACT_DEPENDENCY')
    actual = [(f['fact_id'], f['text'], f['kind'], f['owner'], f['due_date'], tuple(f['depends_on']), f['acceptance']) for f in facts]
    require(actual == list(FIXED_ROWS), 'FIXED_INPUT_CONTRACT_MISMATCH')
    # No semantic inference: this is an explicitly human-authored answer key.
    return {row['fact_id']: row for row in facts}

def submission_schema(data):
    keys(data, {'schema_version', 'meeting_id', 'items'})
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'INVALID_VERSION')
    require(data['meeting_id'] == 'DEMO-M1', 'WRONG_MEETING')
    items = data['items']
    require(type(items) is list and len(items) <= 20, 'INVALID_ITEM_COUNT')
    seen_items, seen_facts = set(), set()
    for row in items:
        keys(row, ITEM_KEYS)
        require(type(row['item_id']) is str and re.fullmatch(r'I[1-9][0-9]*', row['item_id']), 'INVALID_ITEM_ID')
        require(type(row['fact_id']) is str and re.fullmatch(r'F[1-9][0-9]*', row['fact_id']), 'INVALID_FACT_ID')
        require(row['item_id'] not in seen_items, 'DUPLICATE_ITEM_ID')
        require(row['fact_id'] not in seen_facts, 'DUPLICATE_ITEM_FACT')
        seen_items.add(row['item_id']); seen_facts.add(row['fact_id'])
        require(type(row['quote']) is str and len(row['quote']) <= 1000, 'INVALID_QUOTE')
        common(row)
    return items

def validate(data, submission, input_sha, submission_sha):
    facts = input_schema(data)
    items = submission_schema(submission)
    errors = []
    def error(item_id, fact_id, field, code):
        errors.append({'item_id': item_id, 'fact_id': fact_id, 'field': field, 'code': code})
    covered = set()
    for row in items:
        iid, fid = row['item_id'], row['fact_id']
        if fid not in facts:
            error(iid, fid, 'fact_id', 'UNKNOWN_FACT'); continue
        covered.add(fid)
        expected = facts[fid]
        if iid != 'I' + fid[1:]:
            error(iid, fid, 'item_id', 'ITEM_ID_MISMATCH')
        checks = [('quote', 'text', 'QUOTE_MISMATCH'), ('kind', 'kind', 'KIND_MISMATCH'),
                  ('owner', 'owner', 'UNCONFIRMED_OWNER' if expected['owner'] is None else 'OWNER_MISMATCH'),
                  ('due_date', 'due_date', 'UNCONFIRMED_DATE' if expected['due_date'] is None else 'DATE_MISMATCH'),
                  ('acceptance', 'acceptance', 'ACCEPTANCE_MISMATCH')]
        for field, ref, code in checks:
            if row[field] != expected[ref]:
                error(iid, fid, field, code)
        if set(row['depends_on']) != set(expected['depends_on']):
            error(iid, fid, 'depends_on', 'DEPENDENCY_MISMATCH')
    for fid in sorted(set(facts) - covered):
        error('I' + fid[1:], fid, 'fact_id', 'MISSING_FACT')
    errors.sort(key=lambda e: (e['item_id'], e['code']))
    return {'mode': 'rule-simulation', 'status': 'fail' if errors else 'pass', 'dispatch_allowed': False,
            'errors': errors, 'input_sha256': input_sha, 'submission_sha256': submission_sha,
            'counts': {'facts': len(facts), 'items': len(items), 'errors': len(errors)}}

def review_report(report, review):
    keys(review, {'schema_version', 'reviewer', 'input_sha256', 'submission_sha256', 'decision', 'reason'})
    require(type(review['schema_version']) is int and review['schema_version'] == 1, 'INVALID_VERSION')
    require(review['reviewer'] == 'HUMAN-DEMO', 'INVALID_REVIEWER')
    require(type(review['decision']) is str and review['decision'] in {'approve', 'reject'}, 'INVALID_DECISION')
    require(type(review['reason']) is str and len(review['reason']) <= 1000, 'INVALID_REASON')
    require(review['decision'] != 'reject' or nonempty(review['reason']), 'REJECT_REASON_REQUIRED')
    for field in ('input_sha256', 'submission_sha256'):
        require(type(review[field]) is str and re.fullmatch(r'[0-9a-f]{64}', review[field]), 'INVALID_REVIEW_HASH')
    result = dict(report)
    result['approved'] = False
    if report['status'] != 'pass':
        return result
    if any(review[f] != report[f] for f in ('input_sha256', 'submission_sha256')):
        result['status'] = 'fail'
        result['review_error'] = 'STALE_REVIEW'
        return result
    result['status'] = 'reviewed-draft' if review['decision'] == 'approve' else 'needs-revision'
    result['approved'] = review['decision'] == 'approve'
    result['reviewer'] = review['reviewer']
    result['decision'] = review['decision']
    # Do not echo arbitrary reason text into the report.
    return result

def evaluate(input_path, submission_path, review_path=None):
    data, ih = read_json(input_path)
    sub, sh = read_json(submission_path)
    report = validate(data, sub, ih, sh)
    if review_path is not None:
        review, _ = read_json(review_path)
        report = review_report(report, review)
    return report

def golden_check():
    root = Path(__file__).resolve().parent
    results = []
    for name in ('good', 'bad'):
        report = evaluate(root / 'fixtures/meeting.json', root / f'fixtures/submission-{name}.json')
        expected, _ = read_json(root / f'expected/{name}-report.json')
        results.append(report == expected)
    return {'mode': 'rule-simulation', 'status': 'pass' if all(results) else 'fail',
            'dispatch_allowed': False, 'checks': len(results)}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for command in ('validate', 'review'):
        p = subs.add_parser(command)
        p.add_argument('--input', required=True)
        p.add_argument('--submission', required=True)
        if command == 'review':
            p.add_argument('--review', required=True)
    subs.add_parser('check-golden')
    args = parser.parse_args(argv)
    try:
        result = golden_check() if args.command == 'check-golden' else evaluate(args.input, args.submission, getattr(args, 'review', None))
    except (ValueError, OSError, RecursionError) as exc:
        code = str(exc) if isinstance(exc, ContractError) else type(exc).__name__
        print(json.dumps({'mode': 'rule-simulation', 'status': 'invalid-input', 'error': code, 'dispatch_allowed': False}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result['status'] == 'fail' else 0

if __name__ == '__main__':
    sys.exit(main())
