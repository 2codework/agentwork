import json,hashlib,pathlib
root=pathlib.Path('assistant-workspace-research-r1'); out=pathlib.Path('assistant-workspace-qa-r1')
read=lambda p:json.loads(p.read_text())
sources=read(root/'sources.json'); research=read(root/'research.json')
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.is_file()}
def dump(n,v): (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
notes={
'oa-agent-help':('accept','Overview L16 声明 no longer available；L19–33 保留启动及套餐说明。仅接受文档冲突事实，不足以证明所有代理功能或所有账号停用。'),
'oa-agent-launch':('accept','L13 2025-07-17；L21 发布文已过时；L59–60 历史虚拟电脑与重大动作授权。'),
'oa-dr-launch':('accept','L13 2025-02-02；L39 2026-02-10更新；L42 原研究功能与agent增强功能并列，不能合并生命周期。'),
'oa-dr-help':('accept','L19–24审改计划；L56–59应用权限及只读动作；L104–106国家/套餐约束。'),
'cl-cowork':('accept','L47–53付费及平台/组织条件；L60云会话；L159–173新体验Auto/Manual及旧Skip表。Manual不等于每项工具必问。'),
'cl-safety':('accept','L63–65云隔离、桌面桥接、服务器处理、权限风险相互独立。'),
'cl-releases':('accept','2026-01-12 Max/macOS本地VM预览；04-09 macOS/Windows GA；07-07从Max起逐步云会话扩展；09-16逐步统一对话。不可把当前云架构回填历史。'),
'cl-research':('fix','L40 当前相对更新时间为 over 2 weeks ago，不是原 over a week ago；L46–55核心功能支持原结论；L73–75当前模型文档不可等于账号实测。'),
'cl-research-launch':('accept','请求URL自动重定向到 https://claude.com/resources/articles/research；L29 2025-04-15。首发early beta地区/计划不同于当前。'),
'g-dr':('accept','L25–42年龄、登录、Thinking与Pro、限额；L48–55连接来源/审计划；L65视觉限制、L76 Keep Activity。仅Gemini Apps范围。'),
'p-projects':('accept','FAQ L520–534明确Spaces自动迁移threads/files/history；L530–531个人连接/记忆不合并，fork不继承作者访问权。新能力并非仅改名。'),
'p-projects-change':('fix','显示08/04/26；本页及slug未明确月日顺序。原2026-08-04应改raw_date=08/04/26、normalized_date=null；不是首次Spaces发布日。'),
'p-feb-change':('fix','显示02/05/26，URL含February-6th-2026，提供二月上下文但具体日期不一致。保留raw_date与URL日期提示、normalized_date=null，不把二者强行消歧。L33确认Labs旧名，不证明准确改名生效时刻或旧资产迁移。'),
'p-pro':('fix','L125–130支持Research自动模型组合和Create产物；L215 Last modified on October 26, 2026，原2026-07-21不能当本次当前元数据。'),
'p-plans':('fix','L159每30天生成额度；L272–280 Free研究有限、无文件/app生成；L235 API另计；L413更新时间2026-10-08，原09-02需修。组织文件库退役不等于Spaces迁移。'),
'p-labs':('unknown','本次唯一打开失败：(400) Timeout fetching。未重试、未改路径、未用索引补正文。原资料无原始快照，无法独立复验其历史代码/资产/Research命名主张。')}
dump('sources.qa.json',[dict(id=s['id'],url=s['url'],checked_at='2026-10-28',verdict=notes[s['id']][0],evidence_zh=notes[s['id']][1],raw_snapshot_saved=False) for s in sources])
items=[]
fixes={
'assistant-chatgpt-agent':['将 scope_zh 的“1历史停用实体”、availability_zh 的“已停用”、练习“记录停用结论”改为：当前官方帮助页顶部称不再可用，同页保留旧启动/套餐文案；当前文档存在冲突。','建议 lifecycle_status=documentation_unavailability_notice_with_conflicting_legacy_text；retirement继续null。禁止推断所有代理能力停用或Work功能/计费等价。'],
'assistant-claude-research':['刷新相对更新时间为本轮看到的 over 2 weeks ago，不能换算精确日。'],
'assistant-perplexity-projects':['documented_migration_update从ISO断言改为raw_date=08/04/26、normalized_date=null（月日序未独立证实）。关联p-plans更新时间改为2026-10-08。明确自动迁移对象为threads/files/history，不延伸到所有连接器、私人记忆、权限或组织文件库。'],
'assistant-perplexity-research':['upgrade_visible_date保留02/05/26，另记URL February-6th-2026；精确升级事件日期为unknown。关联p-pro/p-plans更新时间分别改为2026-10-26和2026-10-08。首发日期保持null，不重试已失败首发页。'],
'assistant-perplexity-create-files-apps':['rename_evidence_date保留02/05/26及URL日期冲突，规范日期null。document_update及p-pro改为2026-10-26；p-plans改为2026-10-08。','p-labs历史正文在本轮无法复验，证据状态unknown；可保留由p-feb-change独立证实的旧名关系，不声称Labs旧资产全部迁移、执行环境或权限完全相同。']}
for it in research['items']:
 items.append({'id':it['id'],'name':it['name'],'verdict':'fix' if it['id'] in fixes else 'accept','fixes_zh':fixes.get(it['id'],[]),'accepted_scope_zh':'仅官方文档所述功能/版本边界；不是账户资格、真实执行效果或全球穷尽目录验证。','source_ids':it['source_ids'],'unknowns_zh':it['unknowns_zh']})
dump('entities.qa.json',items)
dump('input-sha256.json',hashes)
dump('VALIDATION.json',{'schema':'assistant-workspace-qa-r1','checked_at':'2026-10-28','entities':8,'entity_verdict_counts':{'accept':3,'fix':5,'unknown':0},'sources':16,'source_verdict_counts':{'accept':10,'fix':5,'unknown':1},'source_fetch_success':15,'source_fetch_failed':1,'json_parse':True,'ids_unique':len(set(x['id'] for x in research['items']))==8,'source_references_resolve':all(set(i['source_ids'])<=set(s['id'] for s in sources) for i in research['items']),'original_files_unchanged_at_end':hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()},'canonical_written':False,'products_executed':False,'login':False,'model_called':False,'user_data_uploaded':False,'mac_operated':False,'blocked_first_launch_page_requested':False,'limitations':['原研究无raw snapshot，不能重现其先前访问版本；本轮记录为来源定位和原创摘要，不是全文快照。','8项属于有限抽样，不足以满足全球完整市场与历史版本全覆盖。','日期/权限结论限定文档，用户账号迁移结果未验证。']})
