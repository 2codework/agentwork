"""Explicit research adapters. Preserve original records; reject unknown schemas."""
def required(record, fields):
    missing = [k for k in fields if k not in record]
    if missing: raise ValueError('Missing research fields: '+', '.join(missing))

def normalize(name, doc):
    required(doc,['cases','sources','checked_at'])
    refs = {s['id']:s for s in doc['sources']}
    result=[]
    for c in doc['cases']:
        required(c,['id','source_ids'])
        sources=[]
        for sid in c['source_ids']:
            if sid not in refs: raise ValueError(f'{name}/{c["id"]}: missing source {sid}')
            s=refs[sid]
            urls=s.get('urls',[s.get('url')])
            for url in urls:
                sources.append(dict(title=s.get('title',s.get('publisher_title')),url=url,evidence='reference',checked_at=s.get('checked_at',doc['checked_at']),claim=s.get('verified_claim',s.get('notes',s.get('supports',''))),raw_source=s))
        if name=='roles':
            required(c,['role','task','inputs','steps','output_template','human_acceptance','risk_and_authorization','synthetic_exercise','evidence_level','expected_value_and_measurement','execution_mode','skill_modules'])
            title=c['task']; roles=[c['role']];industries=['跨行业'];input_text='\n'.join(c['inputs'])+'\n合成练习：'+c['synthetic_exercise'];rubric=c['human_acceptance'];risks=c['risk_and_authorization'];output=c['output_template'];bodies=c['steps'];note=c['evidence_level'];summary=c['synthetic_exercise']
        elif name=='industries':
            required(c,['title','industry','status','input','steps','expected_output','acceptance','risk_cost_limits','content_markdown'])
            title=c['title'];roles=['跨岗位'];industries=[c['industry']];input_text=c['input'];rubric=[c['acceptance']];risks=c['risk_cost_limits'];output=c['expected_output'];bodies=[v.strip('。 ') for v in c['steps'].split('；') if v.strip('。 ')];note=c['status'];summary='原创合成行业练习；以人工验收为最终检查。'
        elif name=='learning':
            required(c,['title','category','roles','level','estimated_minutes','inputs','goal','steps','prompt','outputs','rubric','failure_recovery','authorization_boundary','evidence_level','tested'])
            if c['tested'] is not False: raise ValueError('Learning evidence needs manual review')
            title=c['title'];roles=c['roles'];industries=['教育与学习'];input_text=c['inputs'];rubric=c['rubric'];risks=c['authorization_boundary']+'\n失败恢复：'+'\n'.join(c['failure_recovery']);output='\n'.join(c['outputs']);bodies=c['steps'];note=c['evidence_level'];summary=c['goal']
        else: raise ValueError('Unknown research adapter: '+name)
        result.append(dict(id=name+'-'+c['id'].lower(),title=title,summary=summary,roles=roles,industries=industries,steps=[dict(title=f'步骤 {i+1}',body=body,check='对照下方整体验收标准逐项核验；此步骤不代表获得外部操作授权。')for i,body in enumerate(bodies)],sources=sources,evidence='synthetic',synthetic=True,input=input_text,prompt=c.get('prompt','仅使用下方合成输入。按给定步骤生成草稿，不执行外部动作。缺失信息标记待确认，不补造事实。输出遵循模板，并列出不确定性与人工审批点。\n\n输入：'+input_text+'\n\n输出模板：'+output),output=output,rubric=rubric,risks=risks,checked_at=doc['checked_at'],evidence_note=note,raw_record=c,lifecycle='unknown',applicable_versions='未核查；来源提及的版本不自动等于本案例适用版本。',lifecycle_as_of='未核查',replacement_case='',historical_context='首次收录于 '+doc['checked_at']+'；来源核查日期不是生命周期确认日期。',practice_status='原创教学模板；未核验为行业公认最佳实践。'))
    if len(result)!=len(doc['cases']): raise ValueError('Case count changed')
    return result
