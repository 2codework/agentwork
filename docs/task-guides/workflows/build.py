import json,pathlib,hashlib,zipfile
R=pathlib.Path(__file__).parent
recipes=[]
WB='腾讯 WorkBuddy（已有桌面客户端）'
LX='WPS 灵犀专业版（已有桌面客户端，不是 WPS Office 内嵌旧入口）'
NO={'tools':'不需要额外工具；用产品自带对话和文件上传。','mcp':'不需要。MCP 是连接外部系统的接口，这次不连接任何公司系统。','skills':'不需要安装 Skill；先把这一次做对，再考虑保存重复流程。'}
wb_steps=['打开已有的 WorkBuddy 桌面客户端，进入创建任务页。','本练习只处理一个小文件：将下方输入文件拖进输入框；不选择整个桌面或公司共享盘。','把下方提示词完整复制到同一输入框并发送。','先在对话中检查全文；需要文件时在右侧结果区查看产物。不要只看“已完成”三个字。']
lx_steps=['打开已有的 WPS 灵犀专业版，点击左上角“+”新建任务。','点输入框旁的附件按钮，选择本页的小输入文件；也可以将文件拖进对话框。','粘贴本页完整提示词，发送。无须去找模板、插件市场或模型 API。','在对话中看结果；如果生成了文件，点击文件链接下载，再用你已有的办公软件打开检查。']
def add(id,title,product,audience,outcome,inputs,prompt,output,checks,recovery,sources,steps=None,tools=None,extra=None):
 d={'id':id,'title':title,'product':product,'audience':audience,'outcome':outcome,'prerequisites':(['电脑上已有可用的 WorkBuddy，账号已由你本人完成登录，允许用现有额度处理练习。'] if product==WB else ['电脑上已有可用的 WPS 灵犀专业版，WPS 账号已由你本人登录，允许用现有智点处理练习。'] if product==LX else ['已有且已获准使用的 Codex CLI，账号已登录；电脑已有 Python 3；能打开终端。不要求购买套餐或创建 API key。']), 'access_cost':'只用下面的虚构练习材料，不上传真实客户资料。联网 AI 服务可能消耗账户额度；没有访问权、额度或所需客户端时，先阅读输入和参考结果，不为本练习安装、登录、购买或放宽权限。','steps':steps or (wb_steps if product==WB else lx_steps),'tools':tools or NO.copy(),'prompt':prompt,'sample_output':output,'checks':checks,'recovery':recovery,'sources':sources,'sample_note':'示例由作者编写，步骤据2026-10-29官方文档；未在产品内执行。','input_files':[]}
 for name,content in inputs.items():
  p=R/'inputs'/id/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8');d['input_files'].append({'name':name,'path':str(p.relative_to(R)),'content':content,'synthetic':True})
 if extra:d.update(extra)
 recipes.append(d)
meeting='''虚构练习｜春芽书店会员活动筹备会
会议时间：2026-10-26 10:00—10:25
参会：林青（运营）、陈禾（设计）、周宁（店长）
林青：活动定在11月7日周六14点到16点，主题是旧书交换。只邀请现有会员，先不投广告。
陈禾：我周四17点前交海报初稿。报名二维码还没有，先留位置。
林青：报名表我来做，明天下午3点前发给陈禾。字段只收昵称和人数，不收电话。
周宁：每场最多30人，我来确认场地。截止时间我稍后再定。
林青：原计划预算3000元，今天只批准1500元。是否买饮料尚未决定。
周宁：好的，报名满30人就关闭。群通知先给我看，不要直接发。
'''
add('meeting-actions','把一页会议记录变成能跟进的待办',WB,'开完会要发纪要的行政、运营、项目助理；不需要懂 AI。','一份可复制的纪要：结论、3项待办、未定事项；不自动发群。',{'meeting.txt':meeting},'''请只根据附件 meeting.txt 整理会议纪要，不联网、不发消息、不创建日历事件。按“会议信息、已确定的事、行动清单、还要问清楚的事”四部分输出。行动清单每行写事情、负责人、截止时间、交付物；把相对日期换为具体日期。未明确的信息写“待确认”，不要猜负责人或时间。预算只写已批准金额，同时说明原计划不是已批准。把群通知审核要求单列。请先把完整结果写在对话中，不要求生成 Word。''','''# 春芽书店会员活动筹备会纪要
时间：2026-10-26 10:00—10:25
参会：林青、陈禾、周宁

## 已确定的事
- 11月7日14:00—16:00举办旧书交换活动，仅邀请现有会员，暂不投广告。
- 限额30人，满额关闭报名。
- 批准预算1500元；原计划3000元不等于可支出金额。
- 报名只收昵称、人数，不收电话。
- 群通知须先交周宁审核，不能直接发送。

## 行动清单
| 事情 | 负责人 | 截止时间 | 交付物 |
|---|---|---|---|
| 做报名表并发给陈禾 | 林青 | 2026-10-27 15:00 | 含昵称、人数的报名表 |
| 完成海报初稿 | 陈禾 | 2026-10-29 17:00 | 留有报名二维码位置的海报初稿 |
| 确认场地 | 周宁 | 待确认 | 场地确认结果 |

## 还要问清楚的事
1. 周宁何时完成场地确认？
2. 是否购买饮料、花费多少？
3. 群通知由谁起草、何时送审？记录未说明。
''',['对照原文找出3名负责人；场地截止时间必须还是“待确认”。','日期必须是10月27日、10月29日；预算1500元，不能写成3000元。','确认没有自动发群、建会议或收集手机号。'],['日期算错：回复“会议日是2026-10-26，请只重算相对日期，别改其他内容”。','漏读附件：直接把 meeting.txt 的全部文字粘贴在同一对话后再发提示词。','只有录音：本例不含转写；先用已有且获准的转写结果替换文本，不把“上传录音”当成这条路线已支持。'],['wb-create','wb-meeting'])
weekly='''虚构练习｜运营助理林青｜2026-10-19至10-23
本周目标：清理会员资料、完成两场活动、准备下周报名页。
周一：整理会员资料80条，发现重复6条，已请店长确认，尚未删除。
周二：完成读书会，报名18人，实际到场15人。
周三：完成作者分享会，报名25人，实际到场20人。
周四：报名页文案完成，设计图未收到，无法上线。陈禾说下周一12点前给图。
周五：发出会员问卷30份，收到12份有效回复。没有上周可比数据。
下周计划：拿到设计图后检查并上线报名页；跟进6条疑似重复资料；整理问卷意见。
需要店长帮助：确认6条疑似重复是否合并，最晚希望下周二回复。
'''
add('weekly-report','把五天零散记录写成一份周报',WB,'每周要向主管汇报的运营、销售助理或行政。','一份可直接复制到邮件的周报，包含数字、卡点、下周计划；不替你发送。',{'week-notes.txt':weekly},'''请只用附件 week-notes.txt，为运营助理林青写本周周报，面向店长。标题注明2026-10-19至10-23。正文分“本周完成、当前卡点、下周计划、需要支持”，控制在500字以内。两场活动报名数和到场数可相加，写清到场率的分子分母，百分比保留1位小数。问卷回复率另算，不能和活动混在一起。未上线、未合并必须保留。没有上周数据，不写环比增长，不添加积极形容词或编造业绩。将相对日期换成日期，直接输出周报，不发送邮件。''','''# 运营周报｜林青｜2026-10-19—10-23

## 本周完成
- 整理会员资料80条，发现6条疑似重复，尚未删除或合并。
- 完成读书会和作者分享会：合计报名43人、到场35人，到场率81.4%（35÷43）。
- 完成报名页文案。
- 发出问卷30份，收到有效回复12份，回复率40.0%（12÷30）。暂无上周数据，不作环比比较。

## 当前卡点
报名页设计图未收到，页面尚未上线。陈禾预计10月26日12:00前交图。

## 下周计划
收到设计图后检查并上线报名页；跟进6条疑似重复资料；整理问卷意见。

## 需要支持
请店长确认6条疑似重复资料是否合并，希望10月27日前回复。
''',['35÷43约81.4%，不是两场到场率的简单平均。','设计图未收到、报名页未上线、重复资料未合并三点不能被“优化”掉。','文案中不能出现“较上周增长”。'],['出现夸张表述：回复“删除没有原始记录支持的成绩和评价，只保留事实”。','数字不对：回复“重新按18+25与15+20计算，列出算式；不要改原始人数”。'],['wb-create','wb-docs'])
orders='''行号,订单号,日期,金额,状态
1,A001,2026/10/01,100,已支付
2, A002 ,2026-10-02,200,已支付
3,A002,2026-10-02,200,已支付
4,A003,2026-10-03,,已支付
5,A004,2026-10-04,50,已取消
6,A005,2026-10-05,-20,已支付
7,A006,2026-10-06,80, paid 
8,A007,2026-10-07,0,已支付
'''
add('clean-orders','清理8行订单，算出可信的已支付金额',WB,'拿到订单导出表、需要交出干净数据的电商运营；不用会公式。','clean-orders.csv（4行有效订单）和 exceptions.csv（3行待处理记录），外加核对说明。',{'orders.csv':orders},'''请读取附件 orders.csv，不改原文件，不联网。所有行保留原始行号。清理规则：订单号和状态去首尾空格；日期统一YYYY-MM-DD；paid映射为已支付。规范化后，订单号、日期、金额、状态全相同才算重复，保留最早行；同订单号但内容冲突必须进异常表，不能自行择一。金额为空或负数进异常表，不补0；金额0是合法的。已取消订单保留在干净表里，但不计已支付金额。输出新文件clean-orders.csv和exceptions.csv；异常表写原行号、订单号、原因。先在对话中完整展示两张表，再给出总行数核对，以及有效已支付订单数和金额合计。如果无法生成文件，输出完整CSV代码块，不能说已经下载完成。''','''## clean-orders.csv
```csv
行号,订单号,日期,金额,状态
1,A001,2026-10-01,100,已支付
2,A002,2026-10-02,200,已支付
5,A004,2026-10-04,50,已取消
7,A006,2026-10-06,80,已支付
8,A007,2026-10-07,0,已支付
```

## exceptions.csv
```csv
原行号,订单号,原因
3,A002,规范化后与第2行完全重复
4,A003,金额为空
6,A005,金额为负数
```

## 核对
- 输入8行 = 干净表5行 + 异常表3行。
- 有效已支付订单4笔：A001、A002、A006、A007。
- 有效已支付金额380元（100+200+80+0）。
- A004已取消，保留记录但50元不计入合计。
- A003和A005的真实金额需业务人员核对，不能自动纠正。
''',['干净表应有5行，而不是只留下4笔已支付订单。','8行必须都有去向；第3行进异常表，不悄悄消失。','合计380元；0元合法；负数和空值不参与合计。','下载后用已有表格软件打开，两文件必须有不同内容且原表未变。'],['中文乱码：在表格软件“从文本/CSV导入”中选UTF-8，不反复另存覆盖原件。','模型补0：回复“第4行金额未知，不是0，请放回异常表并重算”。','文件链接打不开：使用对话里的完整CSV保存为对应文件名；检查内容再交付。'],['wb-create','wb-data'])
# correct outcome wording to distinguish valid paid vs cleaned
recipes[-1]['outcome']='clean-orders.csv（5行保留记录，其中4笔已支付）和 exceptions.csv（3行待处理记录），外加核对说明。'
slides='''虚构练习｜春芽书店会员活动试点复盘
听众：店长。演讲：5分钟。目的：申请下一轮1500元预算，不代表已获批。
试点：2026年10月，两场活动。报名43人，到场35人，收入1200元，支出900元。
问卷：发出30份，有效回复12份；8份希望增加周末场，4份希望增加亲子场。仅代表这12份回复。
问题：第一场签到排队；第二场提前分组后缓解。没有计时数据。
下轮方案：两场周末活动，先预约后签到；设计一场亲子主题。
风险：样本小；新活动可能报名不足；没有与上月的可比数据。
建议：先批准预算上限1500元，每场结束记录报名、到场、收入、支出和反馈。
'''
add('six-slide-outline','把一段复盘材料变成6页汇报大纲',LX,'需要先向主管确认内容、再做PPT的运营或行政。','6页逐页大纲：每页标题、3个要点、画面建议、讲稿。先不纠结排版。',{'brief.txt':slides},'''请根据附件 brief.txt，写一份给店长看的6页演示大纲，讲5分钟。只输出大纲文字，不要声称已生成PPT文件。每页必须有标题、最多3个要点、一个画面建议、约40至70字讲稿。六页依次为：结论与请求、参与情况、收支、反馈与问题、下一轮安排、预算决策与风险。区分事实、建议、待批准事项。计算到场率及收入减支出差额；不要把差额称作净利润。问卷只代表12份有效回复，不能推广到所有会员。没有计时数据，不写排队改善百分比；没有上月数据，不写环比。''','''## 第1页｜申请下一轮1500元预算上限
- 本轮完成2场会员活动。
- 建议继续小规模试点，不直接扩大。
- 请求批准下一轮预算上限1500元，尚未批准。
画面：左侧试点结论，右侧突出“待批准：1500元”。
讲稿：这次先汇报两场活动的实际结果，再说明下一轮安排。我们建议继续小规模验证，今天请求的是1500元预算上限，并不是宣告预算已经获批。

## 第2页｜43人报名，35人到场
- 两场合计报名43人。
- 合计到场35人。
- 到场率81.4%（35÷43）。
画面：报名43与到场35两根同刻度柱形条。
讲稿：两场活动共报名43人，实际到场35人，到场率约81.4%。这里是合并人数后的比例，不是两场比例的平均值，也没有与上月比较。

## 第3页｜收入1200元，支出900元
- 收入1200元。
- 支出900元。
- 本次记录的收支差额300元。
画面：收入、支出两张数字卡和差额算式。
讲稿：现有记录显示收入1200元、支出900元，差额300元。材料没有提供完整成本口径，因此这里只称收支差额，不将它写成净利润。

## 第4页｜反馈指向周末场，样本仍小
- 有效问卷12份：8份希望增加周末场，4份希望增加亲子场。
- 第一场出现签到排队。
- 第二场提前分组后有所缓解，但无计时数据。
画面：12份反馈分成8与4两组；另列签到问题。
讲稿：反馈来自12份有效问卷，不代表所有会员。周末和亲子主题值得继续验证。提前分组后排队有所缓解，但没有计时记录，不能量化改善幅度。

## 第5页｜下一轮仍做两场
- 安排两场周末活动。
- 先预约后签到，减少现场信息核对。
- 其中设计一场亲子主题。
画面：两场活动时间线，日期标“待定”。
讲稿：下一轮建议仍以两场为限，保留先预约后签到的安排，并试做一场亲子主题。具体日期尚未确定，需结合场地和人员安排另行确认。

## 第6页｜批准预算后再推进
- 待决策：预算上限1500元。
- 风险：样本小、报名可能不足、无上月可比数据。
- 每场记录报名、到场、收入、支出和反馈。
画面：决策框与五项记录清单。
讲稿：请店长决定是否批准1500元预算上限。若获批，我们将逐场记录这五项数据，再判断是否继续。若报名不足，先调整安排，不直接追加支出。
''',['刚好6页，每页不超过3个要点；数字43、35、1200、900、300一致。','1500元只能写申请或待批准；300元不能叫净利润。','反馈范围限定12份，排队改善没有虚构百分比。'],['只有通篇长文：回复“请拆成编号1至6的六页，每页补齐标题、要点、画面和讲稿”。','想要真正PPT：先审完大纲，再用下面的可选升级；文件没生成时仍只算大纲完成。'],['lx-docs'],extra={'optional_upgrade':'内容确认后，可在同一会话发送：“把刚才确认的6页内容制作成可编辑的.pptx，16:9，白底深蓝标题，不增加新数据。生成后提供文件链接；若无法生成请明确说明。”官方文档支持PPT文件能力，但本页只交付作者大纲，未在灵犀生成或验证原生PPT。下载后须用已有WPS或PowerPoint打开，逐页确认文字可编辑；截图式6页不算可编辑PPT。'})
research='''虚构委托｜春芽书店准备选一款办公AI
比较对象：腾讯 WorkBuddy 与 WPS 灵犀专业版。
用途：把会议文字整理成待办；把材料整理成PPT；偶尔分析订单CSV。
不比较：模型跑分、自动发消息、购买、真实客户数据上传。
请优先查两家的官方文档，不凭广告判断谁效果更好。
起始网址：
https://www.workbuddy.cn/docs/workbuddy/Create-Task
https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-One
https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-Three
https://www.lingxi.cn/docs
需要核实的问题：怎样提交文件？是否支持办公产物？有哪些费用或账户条件需要本人再确认？
'''
add('competitor-research','做一页有出处的竞品对照，不抄宣传语',WB,'要给主管一份初步选型材料的运营或市场人员；不是做采购结论。','一页对照：已核实的能力、仍未知的问题、下一步试用清单；每条产品事实可点回官方来源。',{'research-brief.txt':research},'''请阅读 research-brief.txt，按其中用途比较腾讯WorkBuddy和WPS灵犀专业版。只查官方文档和官方定价页，不安装软件、不登录网站、不连接账户、不付款。请先打开给定页面，再补充必要的官方页面。输出一页中文比较：提交材料方式、三类任务（会议文字转待办、材料转6页PPT、订单CSV清理）分别对应两款产品的六格对照、费用/访问待核实项、适合下一步怎样验证。六格每格都写“文档支持”或“待核实”，附具体来源链接、下一步检查方法和本次核查日期；待核实不能写成不支持。把“官方文档支持”“我们实际测过”“作者建议”分开；本任务没有进行产品实测。网页打不开就写无法核实，不编造内容；未公布价格不猜。不要据厂商文案写谁准确率更高、无限免费或一定可用。若当前不能联网，请停止时效性结论，仅列出待查清单。''','''# 办公AI初步对照｜资料核查：2026-10-29

## 怎样提交材料
- **WorkBuddy**：在任务输入区点击上传按钮，或直接把文件拖进输入框。[创建任务](https://www.workbuddy.cn/docs/workbuddy/Create-Task)
- **WPS 灵犀专业版**：点击输入框旁的附件按钮选择文件，或将文件拖进对话框。[任务对话](https://www.lingxi.cn/docs)

## 三种任务，逐项看两款产品
以下六格只说明本次读到的文档，不是实测判定；“待核实”不等于“不支持”。

| 要完成的任务 | 腾讯 WorkBuddy | WPS 灵犀专业版 |
|---|---|---|
| 会议文字 → 待办清单 | **文档支持**：官方有会议文本整理示例，覆盖结论、行动项、负责人和截止时间。[会议记录](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-One)。下一步：用本套 meeting.txt 检查3项待办及“场地时间待确认”。 | **具体效果待核实**：官方说明可上传TXT并进行对话，但本次未找到这份会议待办的专门验收证据，不据此承诺提取准确。[任务对话](https://www.lingxi.cn/docs)。下一步：提交同一 meeting.txt，核对3名负责人、两个明确日期和一个待确认时间。 |
| 文字材料 → 6页PPT | **文档支持**：官方提供按文本素材、页数与受众制作PPT的路线。[根据素材制作PPT](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-Two)。下一步：先审6页大纲，再检查交付文件确有6页、数字未变、文字可编辑；文档声明不代替文件检查。 | **文档支持**：官方列出PPT生成与可编辑办公文件能力。[文档能力](https://www.lingxi.cn/docs)。下一步：用同一 brief.txt，先确认大纲，再打开生成的.pptx检查6页及文字可编辑性；本次没有生成文件。 |
| 订单CSV → 清理与合计 | **文档支持**：官方说明CSV可直接提交并进行数据分析。[数据任务](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-Three)。下一步：按本套清理规则处理 orders.csv，检查5行保留、3行异常、4笔已支付和380元合计。 | **文档支持基础能力，具体清理结果待核实**：官方列出CSV上传和表格数据分析，不代表已经通过本例去重与异常规则。[文件与表格能力](https://www.lingxi.cn/docs)。下一步：提交同一 orders.csv 和清理提示，核对相同的5/3/4行数与380元，不接受只给图表。 |

## 还不能决定的事
- 哪家能准确完成本店材料：未实测，无法排名。
- 本人账号能用哪些功能、现有额度够不够：需在实际账户核对，不能用公开文档替代。
- 最终成本：WorkBuddy存在不同套餐及积分条件；这里只确认费用需核查，不承诺免费。[定价](https://www.workbuddy.cn/docs/workbuddy/Pricing)
- 灵犀当前个人费用与权益：本次未取得可核对的账户报价，标为待确认，不估价。

## 建议的下一步（作者建议）
只用同一份虚构会议稿、8行订单CSV和6页大纲各试一次；记录漏掉的待办、金额是否正确、PPT是否可编辑。先比较交付质量，再看账户费用。不要先连接邮箱、公司网盘或客户系统。

这是一份文档核查样稿，不是两款产品的实测评测或采购建议。
''',['随机点开3个链接，确认到达对应官方文档而不是首页或搜索页。','找每一条“更好、最快、免费”，没有直接证据就删掉。','核查日期应使用你真正打开网页的日期；不要沿用示例日期假装今天查过。','若任何页面无法读取，对应结论写待核实，保留其余可验证部分。'],['无法联网：不要装浏览器插件。改成手动打开官方页面，把相关短段落和完整URL粘贴给它，要求标注“用户提供资料，未在线复核”。','引用不存在：回复“删掉无法打开的来源和依赖它的结论，保留证据不足清单”。','开始推荐付费套餐：回复“停止购买建议，只列需本人核查的费用与权益，不接触账户”。'],['wb-create','wb-data','wb-meeting','wb-price','lx-docs','wb-docs'],tools={'tools':'需要产品原生联网检索能力；无需额外安装。不能联网时用手动提供的官方摘录，但明确不是实时核查。','mcp':'不需要；公开资料比较不必连接邮箱、网盘或付费数据库。','skills':'不需要安装 Skill。先让每项结论有可打开的来源。'})
shipping='''def shipping_fee(order_cents):
    """订单金额为非负整数分；满5000分免运费，否则收600分。"""
    if order_cents > 5000:
        return 0
    return 600
'''
tests='''import unittest
from shipping import shipping_fee

class ShippingTests(unittest.TestCase):
    def test_empty_order(self):
        self.assertEqual(shipping_fee(0), 600)
    def test_below_threshold(self):
        self.assertEqual(shipping_fee(4999), 600)
    def test_exact_threshold(self):
        self.assertEqual(shipping_fee(5000), 0)
    def test_above_threshold(self):
        self.assertEqual(shipping_fee(5001), 0)

if __name__ == "__main__":
    unittest.main()
'''
add('fix-small-bug','修复“刚好满50元仍收运费”的小错误','OpenAI Codex CLI（已有终端工具）','刚接触AI编程、会打开终端的开发者或测试人员；完全不写代码的人可先读前5个任务。','一个只改一处条件的 shipping.py，以及4项测试结果和修复说明；不提交代码、不上线。',{'shipping.py':shipping,'test_shipping.py':tests,'README.txt':'虚构商店练习。Python 3标准库，无第三方依赖。输入是非负整数分。满5000分免运费，否则600分。运行：python -m unittest -v。只在练习副本运行，不用于真实结算。\n'},'''你现在只处理当前练习目录里的 shipping.py、test_shipping.py、README.txt。业务规则：输入为非负整数分，订单金额满5000分免运费，否则收600分。现在刚好5000分时收了600分，请找原因并做最小修复。先阅读文件并运行 python -m unittest -v，记录修复前失败；只修改shipping.py，不改测试期望、不改单位、不添加新功能。然后再次运行同一命令。最后给我代码差异、修复前后实际测试结果和一句原因说明。只用已有Python标准库，不联网、不装依赖、不读取目录外文件、不提交Git、不推送、不部署。如果命令不可用或权限不足，请停下说明，不能把未运行写成通过。''','''## 最小修改
```diff
-    if order_cents > 5000:
+    if order_cents >= 5000:
```

## 完整 shipping.py
```python
def shipping_fee(order_cents):
    """订单金额为非负整数分；满5000分免运费，否则收600分。"""
    if order_cents >= 5000:
        return 0
    return 600
```

## 作者参考测试结果
- 修复前：4项测试中，刚好5000分一项失败，实际600、预期0。
- 修复后：0、4999、5000、5001分四种输入，运费依次为600、600、0、0，4项通过。
- 原因：“满5000”包含5000本身，因此比较条件应为大于或等于。
- 范围：未增加负数、字符串等非法输入处理；这些不在本次约定中。

这是作者在本地验证的参考实现，不是Codex执行日志。你自己的任务必须保留实际命令与结果。
''',['看差异：仅 > 变成 >=，测试文件没有被改。','四项测试都运行，而不是只试5000一个数字。','确认实际货币单位仍是分，不是把5000改成50。','如果没有Python或Codex，本例停在阅读，不能标“修好了”。'],['提示找不到codex：你尚未具备这条路线的前提；先看完整参考结果，不在本练习安装。','提示找不到python：若机器已有python3，可将命令换为python3 -m unittest -v；否则停止，不安装依赖。','测试仍失败：把完整错误文本贴回同一任务，要求只解释失败原因，再局部修复。','改动太大：丢弃练习副本，重新复制输入，强调只改一个条件；不要对真实仓库执行回滚命令。'],['cx-cli'],steps=['将本页3个输入文件下载到一个新建的空文件夹，例如“运费练习”；不要把参考答案放进去。','复制这个文件夹为“运费练习-副本”，原输入留作备份。','在副本文件夹打开终端，先确认能看到 shipping.py、test_shipping.py、README.txt，再输入 codex 并回车。','Codex打开后输入 /status 核对当前目录，输入 /permissions 查看权限；只允许这个副本目录的读写和测试，不开启全盘权限。','粘贴完整提示词。遇到命令确认时核对是当前目录的 python -m unittest -v，不批准安装、联网、提交或部署。','查看文件差异和测试输出；用下方清单验收。'],tools={'tools':'需要已有Python 3与Codex自带文件编辑、终端执行能力。不需要第三方Python包。','mcp':'不需要。本例不连GitHub、数据库或生产系统。','skills':'不需要。一个边界判断修复，用明确规则和测试即可。'})
# First-use guidance is for the reader; no software/account action was performed by the author.
for d in recipes:
 if d['product']==WB:
  d['product']='腾讯 WorkBuddy'
  d['first_time']=['还没有软件：由你本人打开 [WorkBuddy 官网](https://www.workbuddy.cn/)，点“立即下载”并选择你的系统。Windows 10及以上的x64设备可按 [官方安装图解](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide) 完成；公司电脑先取得安装许可，不关闭安全软件。', '打开客户端点“登录”，在自动打开的官网页面选择可用的登录方式（如微信扫码）；由你本人完成，密码和验证码不发给AI。成功后回到客户端的创建任务页。', '先确认账户可用额度。本页不承诺免费；如果暂时不能安装或登录，先打开下载的文本，读提示词和参考结果做纸面练习，这不等于完成了产品任务。']
  d['sources'].append('wb-start')
 elif d['product']==LX:
  d['product']='WPS 灵犀专业版'
  d['first_time']=['还没有软件：由你本人打开 [WPS灵犀官网](https://www.lingxi.cn/)，从“下载 灵犀专业版”进入 [官方下载页](https://www.lingxi.cn/download)，选择匹配系统的包。官方指南推荐Windows 10+；公司电脑先确认安装许可。', '按 [快速开始](https://www.lingxi.cn/docs) 完成安装后，由你本人使用WPS账号或页面提供的验证码等方式登录，再到左上角“+”开始。不要把账号凭据发给AI。', '官网也有“使用网页版”入口（https://lingxi.kdocs.cn），官方说明支持对话和文档处理；可先在那里练习文字大纲。但本页的“+”、附件和可编辑PPT步骤按专业版桌面文档编写，不把桌面全部能力照搬到网页。', '先确认智点与功能权益；不能使用时先读完整样稿，不为练习被动购买。']
 else:
  d['first_time']=['还没有Codex：这条适合愿意使用终端的读者。先看 [Codex CLI官方快速开始](https://learn.chatgpt.com/docs/codex/cli)，由你本人选择对应系统的安装方式并完成；这里不代你运行安装脚本。Windows用户不要照抄其他系统命令。', '在项目目录输入codex，首次按提示选择“Sign in with ChatGPT”或你获准的现有方式，自行完成登录。只用账号现有权益，不要求新建API key；组织禁用时找管理员，不绕过。', 'Python 3若尚不可用，本页只做代码阅读；不要让AI为了这4项测试装一堆依赖。准备好后再从下方第1步开始。']
 d['prerequisites']=['先有能联网的电脑和你获准使用的产品账号。没有客户端请按下面“第一次打开”操作；本教程没有替你安装、登录或购买。']+(['本例还需要已有Python 3与可用终端。'] if d['id']=='fix-small-bug' else [])
 d['access_cost']='只用虚构练习材料，不上传真实客户资料。AI服务可能消耗现有额度；账号功能、地区和组织许可需本人确认。没有额度时停止，不自动购买。首次安装与登录均由读者自行操作；暂不具备条件可做纸面练习，不能记为产品执行成功。'
 for x in d['input_files']:x['sha256']=hashlib.sha256(x['content'].encode()).hexdigest()

# UI-friendly aliases, not a replacement for original content.
for d in recipes:
 d['materials']=d['input_files'];d['tool_choices']=d['tools'];d['setup']=d['prerequisites']+d['first_time']+d['steps'];d['sample_input']='\n\n'.join(x['name']+'\n'+x['content'] for x in d['input_files']);d['repair']=d['recovery'];d['cost']=d['access_cost'];d['privacy']='仅合成材料；不含真人资料、密码或客户数据，不连接外部账户。';d['connection_guide_ids']=[]
 d['download_bundle']='downloads/'+d['id']+'-inputs.zip'
 p=R/d['download_bundle'];p.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
  for x in d['input_files']:z.write(R/x['path'],x['name'])
 (R/'outputs'/d['id']).mkdir(parents=True,exist_ok=True)
 (R/'outputs'/d['id']/'sample.md').write_text(d['sample_output'],encoding='utf-8')
 parts=[f"# {d['title']}",d['outcome'],f"适合：{d['audience']}",'## 1. 准备什么',*['- '+x for x in d['prerequisites']],*['- [下载 '+x['name']+']('+x['path']+')' for x in d['input_files']],'### 输入全文（也可直接复制）',*['#### '+x['name']+'\n```text\n'+x['content']+'\n```' for x in d['input_files']],'## 2. 用什么，不用什么',d['product'],*['- '+{'tools':'工具','mcp':'MCP','skills':'Skill'}[k]+'：'+v for k,v in d['tools'].items()],'## 3. 打开哪里，怎么开始','### 第一次打开',*['- '+x for x in d['first_time']],'### 已经可以使用，开始任务',*[(str(i+1)+'. '+x) for i,x in enumerate(d['steps'])],d['access_cost'],'## 4. 复制这段提示词','```text\n'+d['prompt']+'\n```','## 5. 完整参考结果',d['sample_note'],d['sample_output'],'## 6. 怎么检查，出错怎么办',*['- '+x for x in d['checks']],*['- '+x for x in d['recovery']]]
 if d.get('optional_upgrade'):parts+=['### 做完后再考虑',d['optional_upgrade']]
 (R/(d['id']+'.md')).write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
source_defs=[
 ('wb-start','WorkBuddy Windows安装与登录','https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide','lines 212–260','系统要求、官方下载、客户端登录及返回入口'),
 ('wb-create','WorkBuddy 创建任务','https://www.workbuddy.cn/docs/workbuddy/Create-Task','lines 239–269','工作空间、上传、输入、结果区入口'),
 ('wb-meeting','WorkBuddy 文件与会议文本','https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-One','lines 253–267','会议文字粘贴/文件拖拽；音频先转写'),
 ('wb-docs','WorkBuddy 文档生成','https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-Two','lines 214,240–249','报告及按文字素材、页数、受众制作PPT的官方路线；不证明任何实际产物通过验收'),
 ('wb-data','WorkBuddy 数据分析','https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Practice-Three','lines 218–267','CSV/Excel提交与公开来源研究路线'),
 ('wb-price','WorkBuddy 定价','https://www.workbuddy.cn/docs/workbuddy/Pricing','定价详情','套餐和积分；具体权益不作账户保证'),
 ('lx-docs','WPS 灵犀专业版文档','https://www.lingxi.cn/docs','lines 98–102,143–175,192–204','账号条件、附件、+新任务、文件下载、PPT与办公文件能力'),
 ('cx-cli','Codex CLI','https://learn.chatgpt.com/docs/codex/cli','lines 940–1024,1098–1099','项目目录运行codex，检查目录与权限、编辑与运行已有工具'),
 ('zcode-agents','ZCode Agent（选型参考，未选作新手办公入口）','https://zcode.z.ai/en/docs/agents','lines 40–43','代码任务入口；已有模型连接与客户端仍为前提')]
sources=[dict(id=a,title=b,url=c,evidence_location=e,evidence=f,checked_at='2026-10-29',verification='official page opened in web tool',product_executed=False) for a,b,c,e,f in source_defs]
obj={'title':'今天先完成一件事','intro':'不用先学MCP，也不用先装一堆技能。选一个你今天真的要交的东西：下载小材料，打开已有工具，复制提示词，再拿完整参考结果对照。','version':'r3','checked_at':'2026-10-29','recipes':recipes,'sources':sources,'method':'作者原创练习与参考结果；产品步骤仅经官方文档核查，未在原产品执行。只对本地合成代码参考和数字做校验。','sourcepacks':['agentwork-workbuddy-playbooks-r2','agentwork-lingxi-playbooks-r3','agentwork-zcode-playbooks-r4','agentwork-codex-playbooks-r2']}
(R/'workflows.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'README.md').write_text('# 今天先完成一件事\n\n'+obj['intro']+'\n\n'+obj['method']+'\n\n'+'\n'.join('- ['+d['title']+']('+d['id']+'.md)' for d in recipes)+'\n\n每条都有完整输入、完整提示词、完整作者参考结果和可下载输入ZIP。无需读取任何隐藏背景。来源和精确支持位置见 sources.json；不将产品文档核查当作产品实测。\n',encoding='utf-8')
print('Wrote',len(recipes),'complete workflows')
