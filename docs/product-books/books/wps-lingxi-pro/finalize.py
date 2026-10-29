import pathlib,json,hashlib
P=pathlib.Path(__file__).parent
read=lambda n:json.loads((P/n).read_text())
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
d=read('playbooks.json')
s={'id':'cmcc-download','url':'https://ai.soho.komect.com/download','title':'中国移动灵犀AI助手下载','checked_at':'2026-10-29','evidence':'列出macOS/Windows/Linux；中国大陆手机号验证码登录；未下载，未验证最低版本','kind':'official_product_documentation','execution':'not_run'}
if not any(x['id']==s['id'] for x in d['sources']):d['sources'].append(s)
cs=d['identity_resolution']['candidates']
cs[0]['tutorial_status']='eight_authored_recipes_not_run'
cs[1].update({'tutorial_status':'catalog_only_playbooks_pending','platform':'官网下载页列macOS、Windows、Linux；最低系统版本未确认','account':'官网说明中国大陆手机号验证码登录；未登录','version':'未核验具体版本号','capability_boundary':'工作区/模型/附加资料/查看执行/授权工具与文件；扩展智能体按账号可用范围，不保证所有用户均可安装。未把营销描述当实测。','privacy_cost':'独立隐私政策适用；本轮未核实价格和额度，不承诺免费；不套用WPS不训练声明。','sources':['cmcc-home','cmcc-privacy','cmcc-download']})
cs[2].update({'tutorial_status':'catalog_only_playbooks_pending','platform':'官网列桌面/CLI/VS Code/HTTP；检查时Windows/Linux安装包不可用，macOS即将推出；CLI标Node.js22+，未安装','account':'账号与API接入前置条件未充分核验，不能套用WPS或中国移动账号','version':'官网beta；未运行，未将npm搜索版本当安装版本','capability_boundary':'办公文件、代码工具、模型接入、MCP是厂商声明；未核实每端能力等价。','privacy_cost':'网站宣传本地优先不等于零网络处理；API模型可能有独立计费与数据处理，未配置Key。'})
d['product_profile']['privacy_evidence_conflict']={'docs_claim':'docs对本地执行描述原始数据不上传，同时说明云端记忆。','policy_scope':'隐私政策说明处理输入文本、上传文件、历史上下文、记忆等提供服务。','interpretation':'两者作用域不同，不可推广为全产品离线/零上传承诺；真实资料需组织审查。本轮仅合成资料。','sources':['lx-docs','lx-privacy']}
save('playbooks.json',d);save('identity.json',d['identity_resolution']);save('sources.json',d['sources'])
dedup=read('dedup.json');dedup['semantic_relationships']=[{'recipe':'wps-lingxi-pro-meeting-actions','related_existing_case':'meeting-action-log','relationship':'shared business task; new vendor-qualified documented input/output workflow and executable sidecar evaluation; retain original generic case'}, {'recipe':'wps-lingxi-pro-support-faq','related_existing_case':'support-triage','relationship':'related support workflow, not a product duplicate'}, {'recipe':'wps-lingxi-pro-budget-variance','related_existing_case':'roles-r16','relationship':'same task family; product tutorial adds concrete input/prompt/documented steps/expected rubric'}, {'recipe':'wps-lingxi-pro-hr-onboarding','related_existing_case':'roles-r06','relationship':'related HR process; new constrained scheduling negative example, not employee selection'}];dedup['decision']='No lingxi/灵犀 identity hits in canonical 138 cases / 254 nodes. Preserve generic exercises and link related task families; no replacement or canonical edit performed.';save('dedup.json',dedup)
with (P/'README.md').open('a') as f:
 f.write('\n## 其他同名产品：独立身份，不计作操作包完成\n')
 for c in cs[1:]:
  f.write('\n### '+c['name']+'\n')
  for k in ['tutorial_status','platform','account','version','capability_boundary','privacy_cost']:f.write('- '+k+'：'+c[k]+'\n')
 f.write('\n## 隐私证据范围\n官方说明的本地执行宣传，不能覆盖隐私政策中对上传文件、对话、历史上下文、记忆的服务处理。本包不承诺数据不离设备；第三方模型另有规则。\n\n## Canonical 去重\n只读核验 github-migration-r1/public/agentwork/docs/data.json（138 cases）与 modelatlas/docs/data.json（254 nodes），均没有灵犀/lingxi身份记录。会议、客服、预算、入职等任务家族已有通用练习；本包新增的是限定产品的操作协议与fixture，不声称这些业务主题全新。详见 dedup.json 的路径、SHA和关联。\n\n## 校验与复现\n`python validate.py` 仅检验本地材料和评分器，不运行任何产品。`build.py` 为初稿生成器，`finalize.py`补充身份/去重记录（再次运行会追加README，勿在最终包无目的重跑）；以封存JSON/Markdown为交付基线。\n')
