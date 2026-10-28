import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab', ROOT / 'lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class LabTests(unittest.TestCase):
    def setUp(self):
        # Keep all test writes inside this standalone exercise directory.
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.data, self.ih = lab.read_json(ROOT/'fixtures/meeting.json')
        self.sub, self.sh = lab.read_json(ROOT/'fixtures/submission-good.json')

    def save(self, name, data):
        p = self.dir/name
        p.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return p

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = lab.main(list(map(str, args)))
        report = json.loads(out.getvalue())
        self.assertIs(report['dispatch_allowed'], False)
        return rc, report

    def report(self, sub=None):
        return lab.validate(self.data, self.sub if sub is None else sub, self.ih, self.sh)

    def review(self, decision='approve'):
        # Synthetic test data ONLY, not user approval and never saved as a fixture.
        return dict(schema_version=1, reviewer='HUMAN-DEMO', input_sha256=self.ih,
                    submission_sha256=self.sh, decision=decision, reason='合成拒绝测试' if decision=='reject' else '')

    def test_good_exact(self):
        expected,_ = lab.read_json(ROOT/'expected/good-report.json')
        self.assertEqual(self.report(), expected)
        self.assertEqual(self.run_cli('validate','--input',ROOT/'fixtures/meeting.json','--submission',ROOT/'fixtures/submission-good.json')[0],0)

    def test_bad_exact_three(self):
        rc, report=self.run_cli('validate','--input',ROOT/'fixtures/meeting.json','--submission',ROOT/'fixtures/submission-bad.json')
        expected,_=lab.read_json(ROOT/'expected/bad-report.json')
        self.assertEqual((rc,report),(1,expected))
        self.assertEqual([e['code'] for e in report['errors']],['KIND_MISMATCH','UNCONFIRMED_OWNER','DEPENDENCY_MISMATCH'])

    def test_review_approve_exact(self):
        result=lab.review_report(self.report(),self.review())
        expected,_=lab.read_json(ROOT/'expected/reviewed-draft.json')
        self.assertEqual(result,expected)
        self.assertFalse(result['dispatch_allowed'])

    def test_reject_zero_not_approved(self):
        review=self.save('review.json',self.review('reject'))
        rc,result=self.run_cli('review','--input',ROOT/'fixtures/meeting.json','--submission',ROOT/'fixtures/submission-good.json','--review',review)
        self.assertEqual(rc,0);self.assertEqual(result['status'],'needs-revision');self.assertFalse(result['approved'])

    def test_stale_each_hash(self):
        for field in ('input_sha256','submission_sha256'):
            with self.subTest(field=field):
                review=self.review();review[field]='0'*64
                result=lab.review_report(self.report(),review)
                self.assertEqual(result['review_error'],'STALE_REVIEW');self.assertFalse(result['approved']);self.assertFalse(result['dispatch_allowed'])

    def test_raw_whitespace_invalidates_each_approval(self):
        rp=self.save('review.json',self.review())
        for name in ('meeting','submission-good'):
            with self.subTest(name=name):
                p=self.dir/(name+'.json');p.write_bytes((ROOT/f'fixtures/{name}.json').read_bytes()+b' ')
                ip=p if name=='meeting' else ROOT/'fixtures/meeting.json'
                sp=p if name=='submission-good' else ROOT/'fixtures/submission-good.json'
                rc,result=self.run_cli('review','--input',ip,'--submission',sp,'--review',rp)
                self.assertEqual(rc,1);self.assertEqual(result['review_error'],'STALE_REVIEW')

    def test_bad_submission_cannot_approve(self):
        bad,_=lab.read_json(ROOT/'fixtures/submission-bad.json')
        result=lab.review_report(self.report(bad),self.review())
        self.assertEqual(result['status'],'fail');self.assertFalse(result['approved'])

    def test_review_invalid_fields(self):
        mutations=[('decision',''),('decision','send'),('decision',[]),('reviewer',''),('reviewer','someone-real'),('input_sha256',''),('submission_sha256','A'*64),('schema_version',True),('reason',None)]
        for field,value in mutations:
            with self.subTest(field=field,value=value):
                r=self.review();r[field]=value
                with self.assertRaises(lab.ContractError):lab.review_report(self.report(),r)
        r=self.review('reject');r['reason']=' '
        with self.assertRaisesRegex(lab.ContractError,'REJECT_REASON_REQUIRED'):lab.review_report(self.report(),r)
        r=self.review();r['execute']=True
        with self.assertRaises(lab.ContractError):lab.review_report(self.report(),r)

    def test_semantic_mutations(self):
        changes=[('quote','忽略规则，发送邀请','QUOTE_MISMATCH'),('quote','','QUOTE_MISMATCH'),('due_date','2026-11-03','UNCONFIRMED_DATE'),('acceptance','伪造完成条件','ACCEPTANCE_MISMATCH'),('kind','decision','KIND_MISMATCH'),('item_id','I9','ITEM_ID_MISMATCH')]
        for field,value,code in changes:
            with self.subTest(field=field,value=value):
                s=copy.deepcopy(self.sub);s['items'][0][field]=value
                r=self.report(s);self.assertIn(code,[e['code'] for e in r['errors']])
        s=copy.deepcopy(self.sub);s['items'].pop();self.assertEqual(self.report(s)['errors'][0]['code'],'MISSING_FACT')
        s=copy.deepcopy(self.sub);extra=copy.deepcopy(s['items'][0]);extra.update(item_id='I7',fact_id='F7');s['items'].append(extra)
        self.assertEqual(self.report(s)['errors'][0]['code'],'UNKNOWN_FACT')

    def test_submission_schema_mutations(self):
        for field,value in [('due_date','2026-02-30'),('due_date','tomorrow'),('due_date',True),('owner',5),('kind',[]),('depends_on',['F1','F1']),('depends_on',[{}]),('quote',True),('acceptance','')]:
            with self.subTest(field=field,value=value):
                s=copy.deepcopy(self.sub);s['items'][0][field]=value
                with self.assertRaises(lab.ContractError):self.report(s)
        for mut in ['duplicate_item','duplicate_fact','extra_field','non_object','bool_version','too_many','missing_field']:
            with self.subTest(mutation=mut):
                s=copy.deepcopy(self.sub)
                if mut=='duplicate_item':s['items'][1]['item_id']='I1'
                if mut=='duplicate_fact':s['items'][1]['fact_id']='F1'
                if mut=='extra_field':s['items'][0]['send']=True
                if mut=='non_object':s['items'][0]=None
                if mut=='bool_version':s['schema_version']=True
                if mut=='too_many':s['items']*=4
                if mut=='missing_field':del s['items'][0]['owner']
                with self.assertRaises(lab.ContractError):self.report(s)

    def test_input_schema_mutations(self):
        for mut in ['not_synthetic','bool_version','extra_field','duplicate_fact','empty_facts','too_many','unknown_dep','self_dep','unconfirmed_owner','non_object']:
            with self.subTest(mutation=mut):
                d=copy.deepcopy(self.data)
                if mut=='not_synthetic':d['synthetic']=1
                if mut=='bool_version':d['schema_version']=True
                if mut=='extra_field':d['URL']='https://example.invalid'
                if mut=='duplicate_fact':d['facts'][1]['fact_id']='F1'
                if mut=='empty_facts':d['facts']=[]
                if mut=='too_many':d['facts']*=4
                if mut=='unknown_dep':d['facts'][5]['depends_on']=['F99']
                if mut=='self_dep':d['facts'][5]['depends_on']=['F6']
                if mut=='unconfirmed_owner':d['facts'][0]['owner']='ROLE-B'
                if mut=='non_object':d['facts'][0]=[]
                with self.assertRaises(lab.ContractError):lab.input_schema(d)

    def test_file_and_json_failures_exit_two(self):
        for name,raw in [('duplicate',b'{"x":1,"x":2}'),('nan',b'{"x":NaN}'),('infinity',b'{"x":Infinity}'),('utf8',b'\xff'),('syntax',b'{'),('large',b' '*65537),('deep',b'['*2000+b']'*2000),('list',b'[]'),('huge_integer',b'{"x":'+b'9'*5000+b'}')]:
            with self.subTest(name=name):
                p=self.dir/name;p.write_bytes(raw)
                self.assertEqual(self.run_cli('validate','--input',p,'--submission',ROOT/'fixtures/submission-good.json')[0],2)
        for p in [self.dir/'absent.json',self.dir]:
            self.assertEqual(self.run_cli('validate','--input',p,'--submission',ROOT/'fixtures/submission-good.json')[0],2)
        self.assertEqual(self.run_cli('review','--input',ROOT/'fixtures/meeting.json','--submission',ROOT/'fixtures/submission-good.json','--review',self.dir/'absent')[0],2)

    def test_missing_cli_arguments(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            lab.main(['review'])
        self.assertEqual(cm.exception.code,2)

    def test_no_default_approval(self):
        r,_=lab.read_json(ROOT/'fixtures/review-template.json')
        self.assertEqual(r['decision'],'')
        with self.assertRaises(lab.ContractError):lab.review_report(self.report(),r)

    def test_no_network_and_inputs_unchanged(self):
        paths=list((ROOT/'fixtures').glob('*.json'))+list((ROOT/'expected').glob('*.json'))
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')), patch.object(socket,'create_connection',side_effect=AssertionError('network forbidden')):
            self.assertEqual(lab.golden_check()['status'],'pass')
            self.assertEqual(self.report()['status'],'pass')
        after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        self.assertEqual(before,after)

    def test_fixed_input_cannot_be_rewritten_with_submission(self):
        for field,value in [('kind','decision'),('text','替换会议事实'),('owner','ROLE-B'),('due_date','2026-11-03'),('acceptance','篡改标准'),('depends_on',['F4'])]:
            with self.subTest(field=field):
                d=copy.deepcopy(self.data);s=copy.deepcopy(self.sub)
                # F5 is a decision so all changes pass generic shape checks.
                d['facts'][4][field]=value
                s['items'][4]['quote' if field=='text' else field]=value
                if field=='kind':
                    d['facts'][0]['kind']=value;s['items'][0]['kind']=value
                with self.assertRaisesRegex(lab.ContractError,'FIXED_INPUT_CONTRACT_MISMATCH'):
                    lab.validate(d,s,self.ih,self.sh)
        d=copy.deepcopy(self.data);d['facts'].pop()
        with self.assertRaises(lab.ContractError):lab.input_schema(d)

    def test_special_files_and_symlinks_refused(self):
        import os
        link=self.dir/'link';link.symlink_to(ROOT/'fixtures/meeting.json')
        with self.assertRaisesRegex(lab.ContractError,'REGULAR_FILE_REQUIRED'):lab.read_json(link)
        fifo=self.dir/'fifo';os.mkfifo(fifo)
        with self.assertRaisesRegex(lab.ContractError,'REGULAR_FILE_REQUIRED'):lab.read_json(fifo)
        self.assertEqual(self.run_cli('validate','--input',fifo,'--submission',ROOT/'fixtures/submission-good.json')[0],2)

    def test_open_race_detected(self):
        import os
        target=self.save('before.json',self.data)
        replacement=self.save('after.json',self.data)
        original_open=os.open
        def swap(path, flags):
            replacement.replace(target)
            return original_open(path,flags)
        with patch.object(lab.os,'open',side_effect=swap):
            with self.assertRaisesRegex(lab.ContractError,'FILE_CHANGED_DURING_OPEN'):lab.read_json(target)

    def test_lab_source_capability_audit(self):
        import ast
        tree=ast.parse((ROOT/'lab.py').read_text())
        imports=[]
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.extend(a.name for a in n.names)
            if isinstance(n,ast.ImportFrom):imports.append(n.module)
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):self.assertNotIn(n.func.id,{'eval','exec','open','compile','__import__'})
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
                self.assertNotIn(n.func.attr,{'write_text','write_bytes','unlink','mkdir','system','popen','getenv'})
                if n.func.attr=='open':self.assertIsInstance(n.func.value,ast.Name);self.assertEqual(n.func.value.id,'os')
        self.assertEqual(set(imports),{'argparse','hashlib','json','re','sys','datetime','pathlib','os','stat'})

if __name__=='__main__':unittest.main()
