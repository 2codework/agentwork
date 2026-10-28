import json, pathlib
P=pathlib.Path(__file__).parent
items=json.loads((P/'research.json').read_text())['items']
sources=json.loads((P/'sources.json').read_text())
# Renderer only: no canonical reads/writes, no product/network calls; never regenerates research data.
md=['# 通用助手与研究工作区：有限学习指南','', '核验日：2026-10-28。8个实体，全部 documentation-only / never-run。仅官方资料，不是使用实测或性能排名。canonical未修改。','', '## 先看重要区别','- ChatGPT agent当前帮助页顶部称不再可用，同页残留旧启动/套餐说明；仅确认文档冲突，不推断所有账号或代理能力停用。','- Cowork当前云端/统一体验不能套用2026年1月本地VM教程。','- Spaces→Projects、Labs→Create files and apps按官方关系去重；只确认明确的迁移对象，不推断功能或权限全量继承。','- Research功能、工作区容器、客户端表面和模型分别登记。','', '## 执行边界','下面的步骤都是可供将来授权后练习的设计稿。本轮只查官方网页并制作本地文件；不登录、不调用产品模型、不上传用户材料、不连接账号、不运行自动化。涉及分享/导出到外部服务也需单独授权。','']
S={s['id']:s for s in sources}
for x in items:
 md += ['## '+x['name'],f"- 类型：`{x['entity_type']}`；状态：`{x['lifecycle_status']}`",'- 范围：'+x['version_scope_zh'],'- 日期：'+json.dumps(x['dates'],ensure_ascii=False),'- 可用条件：'+x['availability_zh'],'- 价格：未核实，不猜测；套餐资格不等于账号已可用。','### 权限与人类确认']+['- '+v for v in x['permissions_and_human_confirmation_zh']]+['### 原创合成学习任务：'+x['learning_task']['title_zh']]+[f'{i+1}. {v}' for i,v in enumerate(x['learning_task']['steps_zh'])]+['### 输出验收']+['- '+v for v in x['learning_task']['acceptance_zh']]+['### 限制与未知']+['- '+v for v in x['limitations_zh']+x['unknowns_zh']]+['### 官方来源']+['- ['+S[s]['title']+']('+S[s]['url']+')' for s in x['source_ids']]+['','**执行状态：never-run。**','']
(P/'GUIDE.zh-CN.md').write_text('\n'.join(md))
(P/'EVIDENCE.md').write_text('# 来源证据账本\n\n以下为原创概括和定位，不是网页全文快照。访问日与发布/更新日严格分离。相对更新时间不换算成首发日期。搜索结果只用于发现；OpenAI采用已打开官方页面的具体范围，搜索摘录与打开版本差异保留为未知。\n\n'+'\n\n'.join(f"## {s['id']}\n[{s['title']}]({s['url']})\n\n定位：{s['evidence_locator']}\n\n{s['evidence_summary_zh']}\n\n事件：{s['event_date']}；文档更新：{s['document_updated']}；访问：{s['accessed_at']}" for s in sources))

# Preserve QA observation history in rendered evidence as well.
f=P/'EVIDENCE.md'
f.write_text(f.read_text()+'\n\n# QA补充观察（原观察不删除）\n\n'+'\n\n'.join('## '+x['id']+'\n'+json.dumps({'qa':x.get('qa_review'),'document_observations':x.get('document_observations'),'raw_date':x.get('raw_date'),'normalized_date':x.get('normalized_date'),'date_status':x.get('date_status')},ensure_ascii=False,indent=2) for x in sources))
