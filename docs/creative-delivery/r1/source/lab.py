"""Read-only original cross-track cut validator; no media, network or approvals."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys

from contract import SOURCE, EDIT, SOURCE_SHA256, EDIT_SHA256, TRACKS, REVISION, Invalid, digest, schema
from timeline import transform_item
ROOT=Path(__file__).resolve().parent
LIMIT=65536


def safe_read(path, max_bytes=LIMIT):
    if not hasattr(os,'O_NOFOLLOW') or not hasattr(os,'O_NONBLOCK'):
        raise Invalid('INPUT_IO')
    try:
        before=os.lstat(path)
        if not stat.S_ISREG(before.st_mode): raise Invalid('INPUT_NOT_REGULAR')
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        try:
            opened=os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode): raise Invalid('INPUT_NOT_REGULAR')
            if (before.st_dev,before.st_ino)!=(opened.st_dev,opened.st_ino): raise Invalid('INPUT_CHANGED_DURING_READ')
            if opened.st_size>max_bytes: raise Invalid('INPUT_TOO_LARGE')
            data=bytearray()
            while len(data)<=max_bytes:
                part=os.read(fd,min(8192,max_bytes+1-len(data)))
                if not part: break
                data.extend(part)
            if len(data)>max_bytes: raise Invalid('INPUT_TOO_LARGE')
            after=os.fstat(fd)
            if (opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns)!=(after.st_size,after.st_mtime_ns,after.st_ctime_ns): raise Invalid('INPUT_CHANGED_DURING_READ')
            return bytes(data)
        finally: os.close(fd)
    except OSError:
        raise Invalid('INPUT_IO') from None


def parse(data):
    try:
        text=data.decode('utf-8')
        if text.startswith('\ufeff'): raise Invalid('INPUT_ENCODING')
    except UnicodeError: raise Invalid('INPUT_ENCODING') from None
    # Bounded pre-scan prevents recursive decoder exhaustion, ignoring quoted brackets.
    depth=0; quoted=False; escaped=False
    for char in text:
        if quoted:
            if escaped: escaped=False
            elif char=='\\': escaped=True
            elif char=='"': quoted=False
        elif char=='"': quoted=True
        elif char in '[{':
            depth+=1
            if depth>8: raise Invalid('SCHEMA_DEPTH')
        elif char in ']}': depth-=1
    def pairs(rows):
        result={}
        for k,v in rows:
            if k in result: raise Invalid('JSON_DUPLICATE_KEY')
            result[k]=v
        return result
    def integer(s):
        if len(s)>32: raise Invalid('SCHEMA_VALUE')
        return int(s)
    def floating(s):
        if len(s)>128: raise Invalid('SCHEMA_VALUE')
        n=float(s)
        if not math.isfinite(n): raise Invalid('JSON_NONFINITE')
        return n
    def constant(_): raise Invalid('JSON_NONFINITE')
    try: return json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=floating,parse_constant=constant)
    except (json.JSONDecodeError,RecursionError): raise Invalid('JSON_SYNTAX') from None


class Errors:
    def __init__(self): self.entries=[]
    def add(self,code,phase=5,track=None,item=None,field=None,cause=None):
        # Callers supply only contract-known labels, never arbitrary input strings.
        key=(code,track,item,field)
        for e in self.entries:
            if e['key']==key: return e
        e=dict(key=key,code=code,phase=phase,track=track,item=item,field=field,cause=cause)
        self.entries.append(e); return e
    def first(self,track):
        primary=[e for e in self.entries if e['track']==track and e['cause'] is None]
        return min(primary,key=self.order) if primary else None
    @staticmethod
    def order(e):
        ti=TRACKS.index(e['track']) if e['track'] in TRACKS else -1
        ids=['S1','S2','S3','C1','C2','C3','C4','M1','G1','G2']
        item=(e['item'] or '').split('.')[0]
        ii=ids.index(item) if item in ids else -1
        return (e['phase'],ti,ii,e['code'],e['field'] or '')
    def output(self):
        primary=sorted([e for e in self.entries if e['cause'] is None],key=self.order)
        ordered=[]
        for e in primary:
            ordered.append(e)
            ordered.extend(sorted([d for d in self.entries if d['cause'] is e],key=self.order))
        identity={id(e):f'E{n:03d}' for n,e in enumerate(ordered,1)}
        return [dict(code=e['code'],track_id=e['track'],item_id=e['item'],field=e['field'],severity='derived' if e['cause'] else 'primary',cause_id=identity[id(e['cause'])] if e['cause'] else None,error_id=identity[id(e)]) for e in ordered]


def semantic(submission):
    errors=Errors()
    def add(code,track=None,item=None,field=None,phase=5,cause=None):
        return errors.add(code,phase,track,item,field,cause)
    for obj,prefix in ((submission,''),(submission['delivery'],'delivery.')):
        if obj['revision']!=REVISION: add('REVISION_MISMATCH',field=prefix+'revision',phase=3)
        if obj['edit_sha256']!=EDIT_SHA256: add('EDIT_DIGEST_MISMATCH',field=prefix+'edit_sha256',phase=3)
    if submission['project_id']!='paper-demo': add('PROJECT_MISMATCH',field='project_id',phase=3)
    track_ids=[t['track_id'] for t in submission['tracks']]
    delivery_ids=[t['track_id'] for t in submission['delivery']['tracks']]
    duplicate_tracks={x for x in track_ids if track_ids.count(x)>1}
    for t in sorted(duplicate_tracks): add('DUPLICATE_ID',track=t if t in TRACKS else None,field='track_id',phase=3)
    unknown_tracks=set(track_ids)-set(TRACKS)
    if unknown_tracks: add('UNEXPECTED_TRACK',field='track_id',phase=3)
    for t in TRACKS:
        if t not in track_ids: add('MISSING_TRACK',track=t,field='track_id',phase=3)
    if set(track_ids)==set(TRACKS) and len(track_ids)==4 and track_ids!=list(TRACKS): add('ORDER_MISMATCH',field='tracks',phase=3)
    duplicate_delivery={x for x in delivery_ids if delivery_ids.count(x)>1}
    for t in sorted(duplicate_delivery): add('DUPLICATE_ID',track=t if t in TRACKS else None,field='delivery.track_id',phase=3)
    if set(delivery_ids)!=set(track_ids): add('DELIVERY_TRACK_SET_MISMATCH',field='delivery.tracks',phase=3)
    elif len(delivery_ids)==len(track_ids) and delivery_ids!=track_ids:
        add('ORDER_MISMATCH',field='delivery.tracks',phase=3)
    assets={a['asset_id'] for a in SOURCE['assets']}
    for track in TRACKS:
        if track not in track_ids or track in duplicate_tracks: continue
        t=next(t for t in submission['tracks'] if t['track_id']==track)
        if t['revision']!=REVISION: add('REVISION_MISMATCH',track,field='revision',phase=3)
        expected=[]
        for item in next(t for t in SOURCE['tracks'] if t['track_id']==track)['items']:
            expected.extend(transform_item(item,track))
        exp={f['fragment_id']:f for f in expected}
        actual=t['fragments']; ids=[f['fragment_id'] for f in actual]
        if len(ids)!=len(set(ids)):
            for fid in sorted(set(ids)):
                if ids.count(fid)>1: add('DUPLICATE_ID',track,fid if fid in exp else None,'fragment_id',3)
            # Stop per-item checks but still validate actual digest below.
        else:
            extra=set(ids)-set(exp); missing=set(exp)-set(ids)
            for fid in sorted(missing): add('MISSING_FRAGMENT',track,fid,'fragment_id',3)
            for f in actual:
                fid=f['fragment_id']
                if fid in extra:
                    removed=f['original_id']=='C2' or fid in ('C2.k1','C2.k2')
                    add('REMOVED_ITEM_RETAINED' if removed else 'UNEXPECTED_FRAGMENT',track,'C2' if removed else None,'fragment_id',3)
            if not extra and not missing and ids!=list(exp): add('ORDER_MISMATCH',track,field='fragments',phase=3)
            coverage={}
            if track=='shots' and not extra and not missing and all(f['start_ms']<f['end_ms'] for f in actual):
                previous=0
                # Inspect in expected order; wrong order has its own error but no arbitrary sorting semantics.
                for fid in exp:
                    f=next(f for f in actual if f['fragment_id']==fid)
                    if f['start_ms']!=previous:
                        coverage[fid]=add('SHOT_COVERAGE_GAP' if f['start_ms']>previous else 'SHOT_COVERAGE_OVERLAP',track,fid,'start_ms',4)
                    previous=f['end_ms']
                if previous!=20000:
                    fid=list(exp)[-1]
                    coverage[fid]=add('SHOT_COVERAGE_GAP' if previous<20000 else 'SHOT_COVERAGE_OVERLAP',track,fid,'end_ms',4)
            for f in actual:
                fid=f['fragment_id']
                if fid not in exp: continue
                e=exp[fid]
                for key in ('original_id','asset_id'):
                    if key=='asset_id' and f[key] not in assets: add('UNKNOWN_ASSET',track,fid,key,3)
                    elif f[key]!=e[key]: add('SOURCE_ID_MISMATCH',track,fid,key)
                if f['text']!=e['text']: add('TEXT_CHANGED',track,fid,'text')
                a,b,sa,sb=(f[k] for k in ('start_ms','end_ms','source_start_ms','source_end_ms'))
                if a>=b or sa>=sb:
                    add('INVALID_INTERVAL',track,fid,'interval'); continue
                cause=coverage.get(fid)
                if b>20000:
                    bound=add('OUT_OF_BOUNDS',track,fid,'end_ms')
                    if cause is None: cause=bound
                src=None;dst=None
                if (sa,sb)!=(e['source_start_ms'],e['source_end_ms']): src=add('SOURCE_INTERVAL_MISMATCH',track,fid,'source_interval')
                if (a,b)!=(e['start_ms'],e['end_ms']): dst=add('DEST_INTERVAL_MISMATCH',track,fid,'interval',cause=cause)
                if b-a!=sb-sa:
                    # Attach only to primary; no derived-of-derived chains.
                    parent=cause or src or dst
                    add('SOURCE_DEST_LENGTH_MISMATCH',track,fid,'interval',cause=parent)
        if track in delivery_ids and track not in duplicate_delivery:
            d=next(d for d in submission['delivery']['tracks'] if d['track_id']==track)
            if d['sha256']!=digest(t): add('TRACK_DIGEST_MISMATCH',track,field='sha256',phase=6,cause=errors.first(track))
    return errors.output()


def base_report():
    return dict(schema_version='creative-cut-report/1',mode='rule-simulation',technical_status='invalid',publish_allowed=False,media_rendered=False,human_av_review='not_performed',legal_clearance='not_assessed',raw_input_sha256=None,raw_edit_sha256=None,raw_submission_sha256=None,errors=[],manual_checks=['在8000ms剪口人工观看与试听；本课未执行'])


def validate_file(submission_path,root=ROOT):
    report=base_report()
    try:
        values=[]
        for path,kind,key in ((Path(root)/'fixtures/source.json','source','raw_input_sha256'),(Path(root)/'fixtures/edit.json','edit','raw_edit_sha256'),(submission_path,'submission','raw_submission_sha256')):
            data=safe_read(path);report[key]=hashlib.sha256(data).hexdigest()
            value=parse(data);schema(value,kind);values.append(value)
            if kind=='source' and (value!=SOURCE or digest(value)!=SOURCE_SHA256): raise Invalid('FIXED_FIXTURE_MISMATCH')
            if kind=='edit' and (value!=EDIT or digest(value)!=EDIT_SHA256): raise Invalid('FIXED_FIXTURE_MISMATCH')
        report['errors']=semantic(values[-1])
        code=1 if report['errors'] else 0
        report['technical_status']='fail' if code else 'pass'
    except Invalid as error:
        errors=Errors();errors.add(error.code,phase=1)
        report['errors']=errors.output();code=2
    return report,code


def check_golden():
    # Expected outcomes authored from independent hand oracle and contract, not this validator.
    data=safe_read(ROOT/'expected/cases.json')
    if hashlib.sha256(data).hexdigest()!='28d40a865929d5f9c5af2b2d22dbaf6309dd10ee7687d8f8504d318914e79f01': raise Invalid('FIXED_FIXTURE_MISMATCH')
    outcomes=parse(data)
    failures=[]
    for name,case in outcomes['cases'].items():
        report,code=validate_file(ROOT/'fixtures'/('submission-'+name+'.json'))
        primary=[e['code'] for e in report['errors'] if e['severity']=='primary']
        derived=[e['code'] for e in report['errors'] if e['severity']=='derived']
        if code!=case['exit_code'] or sorted(primary)!=sorted(case['primary']) or sorted(derived)!=sorted(case['derived']):
            failures.append(name)
    report=base_report();report['technical_status']='fail' if failures else 'pass'
    report['golden_cases_checked']=len(outcomes['cases']);report['golden_mismatches']=failures
    return report,1 if failures else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    val=commands.add_parser('validate');val.add_argument('--submission',required=True)
    commands.add_parser('check-golden')
    args=parser.parse_args()
    if args.command=='validate': report,code=validate_file(args.submission)
    else:
        try: report,code=check_golden()
        except Invalid as error:
            report=base_report();errors=Errors();errors.add(error.code,phase=1);report['errors']=errors.output();code=2
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2))
    return code

if __name__=='__main__': sys.exit(main())
