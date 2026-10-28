# 通用助手/研究工作区独立 QA r1

结论：8实体中 **3 accept / 5 fix / 0 unknown**（含保留的字段级未知）；16来源中 **10 accept / 5 fix / 1 unknown**。15页本轮成功读取，1页超时。只审原资料及公开官方文档，未改原研究或canonical。

## 必须修正
- ChatGPT agent：只确认当前帮助页顶部不再可用提示及同页旧启动/套餐文案冲突；发布页标outdated。不能称已独立确认全产品停用，不推断所有代理功能停用；retirement=null。ChatGPT deep research独立保留。
- Perplexity日期：08/04/26在所读页面无明确月日序，规范日期=null。02/05/26有URL February-6th-2026上下文但日期冲突；保留两者、规范日期=null，不宣布准确升级/改名日。
- 当前文档元数据：p-pro Last modified 2026-10-26；p-plans 2026-10-08；Claude Research相对更新为over 2 weeks ago。旧观察可保留在历史访问记录，不覆盖成发布/迁移事件日期。
- Spaces→Projects：官方明确自动带入threads/files/history，新增能力不能简化为完全相同产品；个人连接器/记忆不共享，fork不继承原作者访问权。不可扩展为组织文件库等所有资产自动迁移。
- Labs→Create files and apps：变更日志直接证明旧名关系，不证明所有历史资产自动迁移或权限/执行环境完全等价。

## 保留及历史学习补充
ChatGPT deep research、Cowork、Gemini Apps Deep Research核心范围可接受。Cowork历史学习宜加：2026-01-12是Max/macOS本地VM预览，当前云会话不能反填历史；04-09桌面GA、07-07从Max开始逐步扩展、09-16渐进统一，不等于所有账户同时切换。Claude Research当前连接器自动调用与移动端仅web限制成立。此8项不是全球完整产品/历史版本目录。

## 精确阻断与边界
- p-labs一次请求失败：`Failed to fetch https://www.perplexity.ai/en-GB/hub/blog/introducing-perplexity-labs: (400) Timeout fetching`。未重试或换路径；原研究无raw snapshot，本轮不能复核其历史正文主张。
- 先前被标记non-retryable的Perplexity Deep Research首发页，本轮未请求、未换路径绕过；首发日未知。
- 未登录、执行产品、调用产品模型、上传用户数据、操作Mac、对外发布；本地只生成本QA目录。

详见entities.qa.json逐实体动作、sources.qa.json逐来源URL/定位。input-sha256.json记录原包9文件指纹；VALIDATION.json记录结构校验。SHA256SUMS涵盖QA载荷，HASH.sha256给出其清单哈希（不宣称网页内容哈希）。
