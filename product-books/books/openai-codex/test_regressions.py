"""Negative checks on author-only copies. Not a product runner or arbitrary submission service."""
from pathlib import Path
import json,shutil,tempfile,subprocess,sys
R=Path(__file__).resolve().parent
book=json.loads((R/'product-book.json').read_text());cases=[]
def trial(id,label,mutate):
    with tempfile.TemporaryDirectory(prefix='aw-codex-r2-negative-') as temp:
        root=Path(temp)/'copy';shutil.copytree(R/f'recipes/{id}/fixture',root);shutil.copytree(R/f'recipes/{id}/reference',root,dirs_exist_ok=True)
        mutate(root)
        r=subprocess.run([sys.executable,'-B',str(R/f'recipes/{id}/acceptance.py'),str(root)],capture_output=True,text=True,timeout=30)
        assert r.returncode!=0,(id,label,'incorrectly accepted')
        assert 'PASS:' not in r.stdout,(id,label,'misleading success print')
        cases.append({'recipe_id':id,'negative_case':label,'rejected':True})
def modify_json(root,file,fn):
    p=root/file;v=json.loads(p.read_text());fn(v);p.write_text(json.dumps(v))
# Every requested reference file must be needed by its acceptance contract.
for rec in book['recipes']:
    for name in rec['expected_output']['files']:
        rel=Path(name).relative_to(Path('recipes')/rec['recipe_id']/'reference')
        trial(rec['recipe_id'],'missing '+str(rel),lambda p,rel=rel:(p/rel).unlink())
trial('cx04-legacy-map','duplicate examples omit supplied inputs',lambda p:modify_json(p,'architecture.json',lambda x:x.update(examples=[x['examples'][0]]*3)))
trial('cx04-legacy-map','missing change_seams',lambda p:modify_json(p,'architecture.json',lambda x:x.pop('change_seams')))
trial('cx05-money-migration','wrong field mapping',lambda p:modify_json(p,'migration-plan.json',lambda x:x.update(mapping={})))
trial('cx06-sales-script','wrong expected JSON',lambda p:(p/'expected.json').write_text('{}'))
trial('cx06-sales-script','CLI emits wrong JSON',lambda p:(p/'summarize.py').write_text((p/'summarize.py').read_text().replace("print(json.dumps(summarize(sys.argv[1]),sort_keys=True))","print('{}')")))
trial('cx06-sales-script','incorrectly rejects zero cents',lambda p:(p/'summarize.py').write_text((p/'summarize.py').read_text().replace('if amount<0','if amount<=0')))
trial('cx05-money-migration','empty migration prose',lambda p:(p/'MIGRATION.md').write_text(''))
trial('cx07-triage-prototype','empty manual checklist',lambda p:(p/'MANUAL-QA.md').write_text(''))
trial('cx01-shipping-bug','protected policy modified',lambda p:(p/'policy.md').write_text('changed'))
trial('cx01-shipping-bug','unexpected output path',lambda p:(p/'surprise.txt').write_text('unexpected'))
report={'scope':'author_reference_negative_regressions_only','product_execution':'not_run','runner_implemented':False,'count':len(cases),'cases':cases}
(R/'negative-regressions.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(cases)} author-only negative regressions rejected; no product executed')
