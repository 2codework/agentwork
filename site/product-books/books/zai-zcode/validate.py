from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess,csv
import jsonschema
P=Path(__file__).parent
x=json.loads((P/'playbooks.json').read_text())
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['status','aliases','recipes','sources'],'properties':{'status':{'const':'multiple_distinct_products_catalogued'},'recipes':{'type':'array','minItems':8,'maxItems':8,'items':{'type':'object','required':['id','product_id','prompt','input_files','expected_files','objective_checks','human_rubric','failure_recovery','sources'],'properties':{'product_id':{'const':'zai-zcode'},'product_execution':{'const':'not_run'},'reference_output_origin':{'const':'author_created_not_product_output'},'objective_checks':{'type':'array','minItems':2},'human_rubric':{'type':'array','minItems':2}}}},'sources':{'type':'array','maxItems':16}}}
(P/'playbooks.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n')
jsonschema.validate(x,schema)
assert x['aliases']['zcode']['default'] is None
ids={s['id'] for s in x['sources']}; results=[]
for r in x['recipes']:
 assert set(r['sources'])<=ids
 root=P/r['fixture_root']
 for group,files in [('input',r['input_files']),('reference',r['expected_files'])]:
  for f in files: assert (root/group/f).is_file()
 with tempfile.TemporaryDirectory(dir=P) as tmp:
  t=Path(tmp); shutil.copytree(root/'input',t,dirs_exist_ok=True); shutil.copytree(root/'reference',t,dirs_exist_ok=True)
  slug=root.name
  def run(*a): return subprocess.run(a,cwd=t,capture_output=True,text=True)
  if slug=='refund-fix':
   z=run('python','-m','unittest','-v'); assert z.returncode==0,z.stderr; evidence=z.stderr
  elif slug=='qa-boundaries':
   z=run('python','-m','unittest','-v'); assert z.returncode!=0 and '10000 != 9000' in z.stderr; evidence='Expected failing boundary confirmed: '+z.stderr
  elif slug=='ops-csv':
   for _ in range(2): assert run('python','summarize.py').returncode==0
   assert json.loads((t/'summary.json').read_text())=={'paid_count':2,'revenue_cents':2000}
   assert list(csv.DictReader((t/'errors.csv').open()))==[{'order_id':'O4','status':'paid','amount_cents':'invalid'}]; evidence='Two repeated runs yielded count=2,revenue=2000; only O4 quarantined.'
  elif slug=='docs-maintenance':
   z=run('python','tool.py','--name','Ada'); assert z.stdout=='Hello, Ada!\n' and z.returncode==0
   assert run('python','tool.py').returncode==2; evidence='CLI sample and missing-argument code 2 checked.'
  elif slug=='pm-spec':
   a=json.loads((t/'acceptance.json').read_text()); assert len(a)==4 and a[0]['self_refund'] and not a[1]['self_refund']; evidence='Four acceptance records and threshold checked; human requirements review not_run.'
  elif slug=='design-handoff':
   a=(t/'index.html').read_text(); assert all(s in a for s in ['viewport','focus-visible','role="status"','this.disabled=true']) and 'http' not in a; evidence='Static markup only checked; actual browser layout/keyboard rubric not_run.'
  elif slug=='security-review':
   a=json.loads((t/'review.json').read_text())['findings'][0]; assert a['line']==3 and a['production_exploitability']=='not tested'; evidence='Finding structure and source line checked; exploit execution not_run.'
  else:
   a=json.loads((t/'gate.json').read_text()); assert a['decision']=='blocked' and a['blocking_ids']==['C2'] and not a['published']; evidence='Blocked gate assertions checked; release not_run.'
  results.append({'recipe_id':r['id'],'author_fixture_check':'pass','evidence':evidence,'product_execution':'not_run','human_rubric':'not_run'})
# framework-compatible single-product export, separate catalogue identity for second vendor
sources=[{'id':s['id'],'title':s['id'],'url':s['url'],'accessed_at':s['checked_at'],'claim_scope':s['note']} for s in x['sources']]
sc={s['id']:s for s in sources}
p=x['candidates'][0]
out={'schema_version':'1.0','product':{'product_id':'zai-zcode','vendor':p['vendor'],'name':'ZCode','display_name':'智谱/Z.ai ZCode','status':'researched','version_scope':'桌面下载3.16.3（2026-10-23）；源码README3.16.2；GitHub Releases渲染3.14.3。文档核查2026-10-29；产品未运行。','channel_versions':p['versions'],'sources':[sc[i] for i in p['identity_evidence']]},'recipes':[]}
for r in x['recipes']:
 inputs=[]
 for f in r['input_files']:
  path=r['fixture_root']+'/input/'+f
  inputs.append({'path':path,'sha256':hashlib.sha256((P/path).read_bytes()).hexdigest(),'description':'作者原创合成输入；不含真实数据'})
 out['recipes'].append({'recipe_id':r['id'],'product_id':'zai-zcode','runner_implemented':False,'reference_format':r['reference_format'],'expected_product_artifact_format':r['expected_product_artifact_format'],'task_id':None,'title':r['title'],'role':r['roles'][0],'business_goal':r['business_goal'],'input_artifacts':inputs,'prompt':r['prompt'],'steps':[{'title':'步骤'+str(i+1),'instruction':v,'check':r['objective_checks'][min(i,len(r['objective_checks'])-1)],'failure_recovery':'；'.join(r['failure_recovery'])} for i,v in enumerate(r['official_operation_path'])],'expected_output_origin':'author_reference','expected_output':{'files':[{'path':r['fixture_root']+'/reference/'+f,'content':(P/r['fixture_root']/'reference'/f).read_text()} for f in r['expected_files']]},'objective_checks':r['objective_checks'],'human_rubric':r['human_rubric'],'authorization':r['permissions'],'cost':r['cost_boundary'],'privacy':r['privacy_boundary'],'version_scope':r['applicable_versions'],'sources':[sc[i] for i in r['sources']],'evidence_tier':'documentation_review','product_execution':'not_run','observed_results':None,'checked_at':r['checked_at'],'lifecycle':r['lifecycle'],'practice_status':r['practice_status'],'original_record':r,'expected_output_artifacts':[{'path':r['fixture_root']+'/reference/'+f,'sha256':hashlib.sha256((P/r['fixture_root']/'reference'/f).read_bytes()).hexdigest(),'description':'作者合成参考文件，非实际产品输出'} for f in r['expected_files']]})
out['research_record']={k:v for k,v in x.items() if k!='recipes'}
out['aliases']=x['aliases']
out['coverage_gaps']=x['coverage_gaps']
out['checked_at']=x['checked_at']
(P/'product-book.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'other-product-identity.json').write_text(json.dumps({'status':'identity_only_tutorials_pending','product':x['candidates'][1],'aliases':x['aliases'],'sources':[sc[i] for i in x['candidates'][1]['identity_evidence']],'product_execution':'not_run'},ensure_ascii=False,indent=2)+'\n')
report={'status':'pass','schema':'Draft2020-12','product_execution':'not_run','reference_validation_only':True,'recipe_count':8,'source_count':len(sources),'results':results,'canonical_deduplication':x['deduplication'],'limits':['No vendor binary/model/account/API executed','Browser visual QA not_run','Human rubric not_run','Reference checks do not measure ZCode performance']}
(P/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=sorted(f for f in P.rglob('*') if f.is_file() and f.name!='SHA256SUMS' and '__pycache__' not in str(f))
(P/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n' for f in files))
print('PASS 8 author-fixture checks, JSON schema, references, hashes; product_execution=not_run')
