"""Schema type adversaries only, no human approval; test temporary files."""
import pathlib,importlib.util,json,copy,tempfile,io,contextlib
root=pathlib.Path(__file__).resolve().parent/'unpacked/meeting-action-lab';spec=importlib.util.spec_from_file_location('reviewed_lab',root/'lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
data=json.loads((root/'fixtures/meeting.json').read_text());sub=json.loads((root/'fixtures/submission-good.json').read_text());review={'schema_version':1,'reviewer':'HUMAN-DEMO','input_sha256':'0'*64,'submission_sha256':'0'*64,'decision':'reject','reason':'SYNTHETIC QA'}
variants=[None,True,False,0,1,1.5,{},[],[{}],{'x':[]}];count=0
with tempfile.TemporaryDirectory() as t:
 t=pathlib.Path(t)
 for mode,obj in [('input',data),('submission',sub),('review',review)]:
  paths=[[]]+[[k] for k in obj]
  if mode!='review':
   collection='facts' if mode=='input' else 'items';paths += [[collection,0]]+[[collection,0,k] for k in obj[collection][0]]
  for path in paths:
   for variant in variants:
    changed=copy.deepcopy(obj)
    if not path:changed=variant
    else:
     at=changed
     for part in path[:-1]:at=at[part]
     at[path[-1]]=variant
    i=t/'i';s=t/'s';r=t/'r'
    for file,value in [(i,changed if mode=='input' else data),(s,changed if mode=='submission' else sub),(r,changed if mode=='review' else review)]:file.write_text(json.dumps(value))
    args=['review','--input',str(i),'--submission',str(s),'--review',str(r)] if mode=='review' else ['validate','--input',str(i),'--submission',str(s)]
    output=io.StringIO()
    with contextlib.redirect_stdout(output):code=lab.main(args)
    report=json.loads(output.getvalue());assert code in (0,1,2) and report['dispatch_allowed'] is False;count+=1
print(json.dumps({'status':'pass','type_mutations':count,'uncaught_exceptions':0,'all_reports_dispatch_allowed':False}))
