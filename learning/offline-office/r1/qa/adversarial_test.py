"""Independent offline adversarial CLI QA. All generated receipts are test simulations, never human review."""
import pathlib,sys,tempfile,subprocess,json,copy,hashlib,os
ROOT=pathlib.Path(sys.argv[1]).resolve();SCRIPT=ROOT/'lab.py';F=ROOT/'fixtures';results=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if p.is_file()}
with tempfile.TemporaryDirectory(prefix='office-qa-') as tmp:
 T=pathlib.Path(tmp);ip=T/'input.json';sp=T/'sub.json';rp=T/'test-only-receipt.json'
 original=json.loads((F/'meeting.json').read_text());good=json.loads((F/'submission-good.json').read_text())
 def write(i=None,s=None):
  ip.write_text(json.dumps(original if i is None else i,ensure_ascii=False));sp.write_text(json.dumps(good if s is None else s,ensure_ascii=False))
 def run(name,code,status,mode='validate',path=None,sub=None,receipt=True):
  args=[sys.executable,'-B',str(SCRIPT),mode]
  if mode!='check-golden':args+=['--input',str(ip if path is None else path),'--submission',str(sp if sub is None else sub)]
  if mode=='review' and receipt:args+=['--review',str(rp)]
  p=subprocess.run(args,text=True,capture_output=True,timeout=4)
  assert p.returncode==code,(name,p.returncode,p.stdout,p.stderr)
  d=json.loads(p.stdout);assert d['status']==status,(name,d);assert d['dispatch_allowed'] is False;assert 'Traceback' not in p.stderr
  results.append({'name':name,'exit':p.returncode,'status':d['status']});return d
 write();valid=run('good',0,'pass');bad=json.loads((F/'submission-bad.json').read_text());write(s=bad);report=run('three-fixed-errors',1,'fail');assert len(report['errors'])==3
 for key,value in [('kind','decision'),('owner','ROLE-Z'),('due_date','2026-11-01'),('acceptance','发布完成')]:
  i=copy.deepcopy(original);s=copy.deepcopy(good);i['facts'][0][key]=value;s['items'][0][key]=value;write(i,s);run('self-consistent-forgery-'+key,2,'invalid-input')
 i=copy.deepcopy(original);s=copy.deepcopy(good);i['facts'].pop(3);s['items'].pop(3);i['facts'][-1]['depends_on']=['F3'];s['items'][-1]['depends_on']=['F3'];write(i,s);run('delete-prerequisite-and-submission',2,'invalid-input')
 for raw,name in [(b'{"n":'+b'1'*5000+b'}','huge-integer'),(b'{"n":NaN}','nan'),(b'{"n":1,"n":2}','duplicate-key'),(b'['*2000+b']'*2000,'deep-json'),(b'\xff','bad-utf8'),(b'x'*65537,'oversize'),(b'{','broken-json')]:
  write();ip.write_bytes(raw);run(name,2,'invalid-input')
 write();run('directory',2,'invalid-input',path=T);run('missing-file',2,'invalid-input',path=T/'absent')
 sy=T/'symlink.json';sy.symlink_to(ip);run('last-component-symlink',2,'invalid-input',path=sy)
 if hasattr(os,'mkfifo'):
  fifo=T/'pipe';os.mkfifo(fifo);run('fifo-nonblocking-reject',2,'invalid-input',path=fifo)
 write();d=run('pre-review',0,'pass');receipt={'schema_version':1,'reviewer':'HUMAN-DEMO','input_sha256':d['input_sha256'],'submission_sha256':d['submission_sha256'],'decision':'approve','reason':'TEST-ONLY synthetic state transition, no human review'};rp.write_text(json.dumps(receipt));a=run('synthetic-approve-transition',0,'reviewed-draft',mode='review');assert a['approved'] is True
 receipt['decision']='reject';rp.write_text(json.dumps(receipt));a=run('reject-exit0-not-approved',0,'needs-revision',mode='review');assert a['approved'] is False
 receipt['decision']='approve';rp.write_text(json.dumps(receipt));ip.write_text(ip.read_text()+'\n');a=run('whitespace-input-stales-receipt',1,'fail',mode='review');assert a['approved'] is False
 write();sp.write_text(sp.read_text()+'\n');a=run('whitespace-submission-stales-receipt',1,'fail',mode='review');assert a['approved'] is False
 write();rp.write_text('{}');run('invalid-receipt',2,'invalid-input',mode='review');run('golden-has-no-human-review',0,'pass',mode='check-golden')
after={str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if p.is_file()};assert before==after,'fixture/package mutation'
print(json.dumps({'status':'pass','tests':results,'package_unchanged':True,'receipt_scope':'synthetic state transition tests only; not actual human review'},ensure_ascii=False,indent=2))
