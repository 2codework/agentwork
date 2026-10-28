# 区域办公平台独立 QA

**结论：7 accept / 0 fix；文档级核验通过，运行与租户未知项保持 unknown。**

只读官方公开页与本地研究包；未登录、运行产品/模型/SDK、上传用户文件、操作 Mac、修改原包或 canonical。

## 逐实体结论

### Dify — accept
官方LICENSE明确多租户与前端标识附加条件；Human Input邮件链接不限账户且仅首答生效。未把人工节点当作强身份或全链权限。
未知与限制：选定release、租户可用性/数据驻留和费用未实测。
证据：[dify-license](https://github.com/langgenius/dify/blob/main/LICENSE)；[dify-human](https://docs.dify.ai/en/cloud/use-dify/nodes/human-input)

### Coze Studio — accept
官方仓库与LICENSE-APACHE支持代码Apache-2.0；README区分商业功能并披露PAT、外部模型/插件配置及公网风险。
未知与限制：未锁release，未评估已安装版本漏洞、托管地区与细粒度ACL。
证据：[coze-repo](https://github.com/coze-dev/coze-studio)；[coze-license](https://github.com/coze-dev/coze-studio/blob/main/LICENSE-APACHE)

### 飞书 aily 企业工作伙伴 — accept
官方渠道页明确企业工作伙伴与个人助手差别、TAT/UAT、渠道即时生效和扩围需发布；导航文字不够证明全量更名。
未知与限制：aily与豆包工作伙伴精确迁移关系及真实租户许可仍unknown；未独立重取scope搜索摘录。
证据：[aily-channel](https://aily.feishu.cn/hc/1u7kleqg_uv8vbhxz)

### 钉钉宜搭 AI 助理 — accept
宜搭创建页直接支持命名、数据分析/表单填报、非管理员申请、不可修改可见范围与不跨组织。
未知与限制：委托授权页在原包已502，本次不重试；该项仅接受为带弱证据标记的文档陈述，不认定独立验证或运行验证。
证据：[dingtalk-yida](https://docs.aliwork.com/docs/yida_support/_12/du6zs1ze7inyxws3/duw7gpd4punhyrgb)

### Zoho Zia Agents — accept
角色页支持四个预设角色、不可定制及Collaborator不可部署；Viewer正文与query矩阵矛盾确实存在。Settings支持组织、积分与BYOK区分。
未知与限制：Viewer实际运行权限、各数据中心/CRM/Desk账户开通未知，不能由文档推断账户可用。
证据：[zia-roles](https://www.zoho.com/agents/resources/help/platform-reference/roles-permissions.html)；[zia-settings](https://www.zoho.com/agents/resources/help/platform-reference/settings.html)

### 阿里云百炼智能体应用（Agent） — accept
FAQ区分Agent与Assistant API；权限页明确地域空间隔离、OpenAPI另管；国际页仅对2025-04-21前新加坡创建应用者开放指定旧应用页签且属预览。
未知与限制：不把国际Agent 1.0限制外推中国站/新版Agent Studio；具体租户版本、模型及计费未知。
证据：[bailian-faq](https://docs.agent.bailian.aliyun.com/zh/resources/faq)；[bailian-permissions](https://help.aliyun.com/zh/model-studio/permission-management-overview)；[bailian-international](https://www.alibabacloud.com/help/zh/model-studio/application-introduction)

### 腾讯云智能体开发平台 — accept
2026-07-10权限页确认用户/角色合集、首次成员默认权限、查看可对话测试和高级发布控制。
未知与限制：旧迁移通知仅历史，未独立重取；地区、费用、实际租户默认状态和逐次确认未运行核验。
证据：[tencent-permissions](https://cloud.tencent.cn/document/product/1759/122574)

## 跨项与阻断边界
- 全部7条是平台/托管功能，不是基础模型。
- 全部练习是原创合成纸面设计，never-run；人工验收是目标条件而不是通过结果。
- 托管功能没有源码许可证据不等于证明闭源；现有措辞使用未核实/未发现，合适。
- aliases含扣子、aily、钉钉AI助理等宽检索词，仅能作名称去重检索；不得作产品身份等价或自动合并依据。
- 主JSON与Markdown抽查一致；固定快照去重结果不代表语义案例全集。
- 钉钉委托授权页原先502与Dify成员页不可访问均未重试或绕过。
- 2份基线快照哈希与14次别名扫描已独立复算，零名称命中不代表不存在语义重叠。
- 作者completed交付已观察；封存时全部被审输入再次哈希一致。

## 精确输入 SHA256

- `artifact-sha256.json`：`14261882b98c4af561208ab47ffbd18eaa28289f5162374ea7a52b4485718766`
- `baselines/agentwork-data.json`：`d16e7ee00c95dab28cf1f3827173ed50a793100676dc7a40cd4a4a268af8afff`
- `baselines/modelatlas-data.json`：`2a70db13b024f55bc1624f1da3b6be02e3c78843c30889b6fafcb6a0b2aa8082`
- `baselines.json`：`38f969d191fcac6d439f31df9e6fef07bc72052924f0aab3ff5b4b73d3c3e4bc`
- `build_research.py`：`f69daad93db341bf11dd5193795aef8bee0259f377c6f6f629ed8553de915ba1`
- `regional-office.json`：`8e9b56f433866391ac09e521730bbc0e4783b85696ed282cd2db8f9c8d35631c`
- `regional-office.zh.md`：`02887594860aee1213af381a87bf8eafa3fa97193331dc9e76b1698e128f3872`
- `source-checks.json`：`a37259fb2f0b9dedadf889bfaae283f0ace68de94899e129f97422f19570c570`
- `unknowns.json`：`99184e10f08d27561a450b9d61f9694521a2d8a74442324af7c7b418b6b43da3`
- `validation.json`：`03b1a1c2d07cc39801ea6ac769cb36308fe61a22aa494d65eacf2878315f7337`
