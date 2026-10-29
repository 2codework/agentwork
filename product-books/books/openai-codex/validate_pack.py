"""Validate authored fixtures/reference only; never invokes Codex, network, SDK or LLM."""
import json, pathlib, tempfile, shutil, subprocess, sys, hashlib
R=pathlib.Path(__file__).resolve().parent
pack=json.loads((R/'recipes.json').read_text())
results=[]
for rec in pack['recipes']:
    assert rec['status']=='not_run' and rec['run_record']['actual_output'] is None
    assert rec['reference_provenance']=='author_created_synthetic_not_codex_output'
    assert len(rec['human_rubric'])==3 and len(rec['objective_checks'])>=2
    fixture=R/rec['fixture_path'];reference=R/rec['reference_path'];test=R/rec['acceptance_path']
    row={'recipe_id':rec['id'],'product_execution':'not_run','observed_product_results':None,'human_review':'not_run'}
    with tempfile.TemporaryDirectory(prefix='aw-codex-offline-') as temp:
        work=pathlib.Path(temp)/'exercise';shutil.copytree(fixture,work)
        env={'PYTHONDONTWRITEBYTECODE':'1'}
        # Use current process environment for executable/PATH, never inspect secrets.
        before=subprocess.run([sys.executable,str(test),str(work)],capture_output=True,text=True,timeout=30)
        assert before.returncode!=0,(rec['id'],'baseline unexpectedly accepted')
        shutil.copytree(reference,work,dirs_exist_ok=True)
        after=subprocess.run([sys.executable,str(test),str(work)],capture_output=True,text=True,timeout=30)
        assert after.returncode==0,(rec['id'],after.stdout,after.stderr)
        row.update(baseline_expected_rejection=True,author_reference_check='passed',stdout=after.stdout.strip())
    results.append(row)
report={'scope':'author_reference_stdlib_validation_only','checked_at':'2026-10-29','codex_executed':False,'llm_or_paid_api_executed':False,'hosted_ci_executed':False,'browser_or_accessibility_executed':False,'recipes':results}
(R/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
