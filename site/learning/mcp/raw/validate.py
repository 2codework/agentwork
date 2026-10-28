"""Original offline teaching contract, not an MCP implementation or conformance suite."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def id_key(x):
    need(type(x) in (int, str), 'request ID must be integer or string in this contract')
    return type(x).__name__, x

def validate_wire(events, modern=False):
    need(isinstance(events, list), 'events must be a list')
    pending, used, cancelled, tools = {}, set(), set(), {}
    ready = False
    negotiated = False
    counts = {'requests': 0, 'responses': 0}
    for event in events:
        direction, m = event['direction'], event['message']
        need(direction in ('client_to_server', 'server_to_client'), 'bad direction')
        need(isinstance(m, dict) and m.get('jsonrpc') == '2.0', 'JSON-RPC object required; no batches')
        if 'method' in m:
            need(direction == 'client_to_server', 'contract only models client-initiated methods')
            need('result' not in m and 'error' not in m, 'method cannot carry result/error')
            method = m['method']
            p = m.get('params', {})
            need(isinstance(p, dict), 'params object required')
            if 'id' not in m:
                need(not modern, 'modern notifications outside this teaching subset')
                if method == 'notifications/initialized':
                    need(negotiated and not ready, 'initialize response required before ready')
                    ready = True
                elif method == 'notifications/cancelled':
                    key = id_key(p['requestId'])
                    need(key in pending, 'cancel must reference in-flight request')
                    need(pending[key]['method'] != 'initialize', 'cannot cancel initialize')
                    cancelled.add(key)
                    del pending[key]
                else:
                    raise ValueError('notification outside teaching subset')
                continue
            key = id_key(m['id'])
            need(key not in used, 'duplicate request ID')
            if modern:
                need(method == 'tools/list', 'modern subset only demonstrates tools/list')
                meta = p.get('_meta', {})
                need(meta.get('io.modelcontextprotocol/protocolVersion') == '2026-07-28', 'modern version missing')
                need(isinstance(meta.get('io.modelcontextprotocol/clientCapabilities'), dict), 'modern capabilities missing')
            elif method == 'initialize':
                need(not used, 'initialize must be first')
                need(p.get('protocolVersion') == '2025-11-25', 'legacy version unsupported')
                need(isinstance(p.get('capabilities'), dict) and p.get('clientInfo', {}).get('name'), 'client fields missing')
            else:
                need(ready, 'business request before initialize/initialized')
                if method == 'tools/call':
                    name = p.get('name')
                    need(name in tools, 'tool not discovered')
                    args = p.get('arguments', {})
                    need(set(args) == {'a', 'b'} and all(type(v) is int for v in args.values()), 'bad argument schema')
            used.add(key)
            pending[key] = m
            counts['requests'] += 1
        else:
            need(direction == 'server_to_client', 'response must come from server')
            key = id_key(m.get('id'))
            need(key in pending, 'response has no pending request')
            need(('result' in m) != ('error' in m), 'response must have result XOR error')
            q = pending.pop(key)
            method = q['method']
            counts['responses'] += 1
            if 'error' in m:
                e = m['error']
                need(type(e.get('code')) is int and isinstance(e.get('message'), str), 'bad error object')
                continue
            r = m['result']
            need(isinstance(r, dict), 'result object required')
            if modern:
                need(r.get('resultType') == 'complete', 'modern resultType missing')
            if method == 'initialize':
                need(r.get('protocolVersion') == '2025-11-25', 'negotiated version unsupported')
                need(all(k in r.get('capabilities', {}) for k in ('tools', 'resources', 'prompts')), 'fixture server capabilities missing')
                negotiated = True
            elif method == 'tools/list':
                for t in r['tools']:
                    need(t.get('inputSchema', {}).get('type') == 'object', 'tool schema missing')
                    tools[t['name']] = t
            elif method == 'tools/call':
                need(isinstance(r.get('content'), list), 'tool content missing')
                if not r.get('isError', False):
                    n = sum(q['params']['arguments'].values())
                    structured = r.get('structuredContent', {})
                    need(set(structured) == {'total'} and type(structured['total']) is int and structured['total'] == n, 'wrong structured total')
                    need(json.loads(r['content'][0]['text']) == structured, 'text/structured mismatch')
            elif method == 'resources/read':
                need(r['contents'][0]['uri'] == q['params']['uri'], 'resource URI mismatch')
            elif method == 'prompts/get':
                need(all(x.get('role') in ('user', 'assistant') and x.get('content', {}).get('type') == 'text' for x in r['messages']), 'bad prompt message')
    need(not pending, 'unresolved requests in fixture')
    if modern:
        return dict(protocol_version='2026-07-28', **counts)
    need(ready, 'legacy fixture never became ready')
    return dict(status='ready', **counts, cancelled=len(cancelled))

def evaluate(f):
    kind, data = f['kind'], f['input']
    if kind in ('legacy', 'modern'):
        return validate_wire(data, modern=kind == 'modern')
    if kind == 'roles':
        need(all(isinstance(data.get(k), str) and data[k] for k in ('host', 'client', 'server')), 'three roles required')
        return {'role_count': 3, 'network_calls': 0}
    if kind == 'scope':
        allowed, denied = [], []
        for a in data['actions']:
            ok = set(a['requires']) <= set(data['granted_scopes']) and (not a['external_effect'] or data['user_approved_effects'])
            (allowed if ok else denied).append(a['name'])
        return dict(allowed=allowed, denied=denied)
    if kind == 'injection':
        need(data['allowed_fields'] == ['units'] and data['allowed_actions'] == [], 'exercise only permits units extraction')
        return {'extracted': {'units': data['untrusted_resource']['units']}, 'executed_actions': []}
    if kind == 'skill':
        lines = data['skill_md'].splitlines()
        need(lines[0] == '---' and '---' in lines[1:], 'frontmatter missing')
        fields = dict(line.split(': ', 1) for line in lines[1:lines[1:].index('---') + 1])
        need(fields.get('name') == data['directory'] and fields.get('description'), 'skill metadata mismatch')
        return dict(skill_name=fields['name'], installed=False, executed_scripts=0)
    if kind == 'migration':
        need(data['archived_versions'] == ['2025-06-18', '2025-11-25'] and data['history_policy'] == 'retain original fixtures', 'history lost')
        need(data['target_protocol'] == '2026-07-28', 'unexpected target')
        return dict(history_retained=True, target=data['target_protocol'], sdk_executed=False)
    raise ValueError('unknown lesson kind')

def validate_fixture(f):
    actual = evaluate(f)
    need(actual == f['expected'], 'actual teaching output does not match expected')
    return actual

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case')
    args = p.parse_args()
    paths = sorted((ROOT / 'fixtures').glob('*.json'))
    selected = [x for x in paths if not args.case or x.stem == args.case]
    need(bool(selected), 'unknown case')
    reports = [{'case_id': f['case_id'], 'output': validate_fixture(f)} for path in selected for f in [json.loads(path.read_text())]]
    print(json.dumps({'verification': 'original_offline_contract_only', 'cases_passed': len(reports), 'results': reports}, ensure_ascii=False, indent=2))
