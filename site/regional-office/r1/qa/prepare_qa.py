import json, hashlib, pathlib, datetime
root=pathlib.Path('/workspace/scratch/6fb8d22046cb'); inp=root/'regional-office-research-r1'; out=root/'regional-office-qa-r1'
d=json.loads((inp/'regional-office.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={str(p.relative_to(inp)):sha(p) for p in sorted(inp.rglob('*')) if p.is_file()}
manifest=json.loads((inp/'artifact-sha256.json').read_text())
assert all(hashes[k]==v for k,v in manifest.items())
notes=[
('accept','官方LICENSE明确多租户与前端标识附加条件；Human Input邮件链接不限账户且仅首答生效。未把人工节点当作强身份或全链权限。','选定release、租户可用性/数据驻留和费用未实测。',['dify-license','dify-human']),
('accept','官方仓库与LICENSE-APACHE支持代码Apache-2.0；README区分商业功能并披露PAT、外部模型/插件配置及公网风险。','未锁release，未评估已安装版本漏洞、托管地区与细粒度ACL。',['coze-repo','coze-license']),
('accept','官方渠道页明确企业工作伙伴与个人助手差别、TAT/UAT、渠道即时生效和扩围需发布；导航文字不够证明全量更名。','aily与豆包工作伙伴精确迁移关系及真实租户许可仍unknown；未独立重取scope搜索摘录。',['aily-channel']),
('accept','宜搭创建页直接支持命名、数据分析/表单填报、非管理员申请、不可修改可见范围与不跨组织。','委托授权页在原包已502，本次不重试；该项仅接受为带弱证据标记的文档陈述，不认定独立验证或运行验证。',['dingtalk-yida']),
('accept','角色页支持四个预设角色、不可定制及Collaborator不可部署；Viewer正文与query矩阵矛盾确实存在。Settings支持组织、积分与BYOK区分。','Viewer实际运行权限、各数据中心/CRM/Desk账户开通未知，不能由文档推断账户可用。',['zia-roles','zia-settings']),
('accept','FAQ区分Agent与Assistant API；权限页明确地域空间隔离、OpenAPI另管；国际页仅对2025-04-21前新加坡创建应用者开放指定旧应用页签且属预览。','不把国际Agent 1.0限制外推中国站/新版Agent Studio；具体租户版本、模型及计费未知。',['bailian-faq','bailian-permissions','bailian-international']),
('accept','2026-07-10权限页确认用户/角色合集、首次成员默认权限、查看可对话测试和高级发布控制。','旧迁移通知仅历史，未独立重取；地区、费用、实际租户默认状态和逐次确认未运行核验。',['tencent-permissions'])]
sources={s['id']:s for s in d['sources']}
rows=[]
for e,(verdict,why,unknown,ids) in zip(d['entities'],notes):
 assert e['runtime_status']=='never-run' and e['runtime_verified'] is False and e['exercise']['status']=='never-run'
 rows.append({'id':e['id'],'name':e['name'],'verdict':verdict,'basis':why,'unknown':unknown,'required_fixes':[], 'evidence':[{'source_id':i,'url':sources[i]['url'],'independent_read':'official page opened 2026-10-28 UTC'} for i in ids]})
r={'audit_id':'regional-office-qa-r1','status':'awaiting-author-final-seal','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_directory':str(inp),'input_sha256':hashes,'author_manifest_matches':True,'verdict_counts':{'accept':7,'fix':0,'unknown_entity':0},'accept_meaning':'Accept qualified documentation-only wording, not product/runtime/security certification; unknown subclaims remain unknown.','entities':rows,'cross_cutting':['全部7条是平台/托管功能，不是基础模型。','全部练习是原创合成纸面设计，never-run；人工验收是目标条件而不是通过结果。','托管功能没有源码许可证据不等于证明闭源；现有措辞使用未核实/未发现，合适。','aliases含扣子、aily、钉钉AI助理等宽检索词，仅能作名称去重检索；不得作产品身份等价或自动合并依据。','主JSON与Markdown抽查一致；固定快照去重结果不代表语义案例全集。'],'blockers':[{'url':'https://opensource.dingtalk.com/developerpedia/docs/develop/permission/ai_assistant/ai_assistant_get_oauth_authcode/','status':'previous-source-502-not-retried','impact':'Delegated authorization detail independently unknown.'},{'url':'https://docs.dify.ai/en/cloud/workspace/manage-members','status':'previous-inaccessible-not-retried','impact':'No role claims inferred.'}],'actions_not_taken':['login','third-party product/model/SDK execution','user-file upload','Mac operation','source package mutation','canonical mutation','blocked-source retry/bypass']}
(out/'qa.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':str(out/'qa.json'),'input_main_sha256':hashes['regional-office.json'],'manifest_sha256':hashes['artifact-sha256.json'],'status':r['status']},ensure_ascii=False))
