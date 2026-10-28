# GitHub Pages 发布（待确认执行）

当前只准备本地候选，不创建仓库、不推送、不启用远端 CI。不要猜测组织名、仓库 URL 或访问地址。

## 简单分支发布

1. 负责人确认组织/仓库名、公开内容与许可证。仅将 `agentwork-r1` 内审核后的文件加入新仓库，不加入父目录或旧项目。
2. 本地运行完整检查并构建 `site/`。人工浏览器验收通过后，将 **site 目录中的文件** 放在专用发布分支的根目录（保留 `.nojekyll`），而不是把整个仓库发布成根目录。
3. 在仓库 Settings → Pages 选择 Deploy from a branch，选实际发布分支和 `/(root)`。此步骤会使页面可公开访问，必须在授权范围内操作。
4. 等待 Pages 部署，核对提交、工作流与 GitHub 返回的真实 URL；检查页面和项目子路径资源后再宣布上线。

也可发布到选定分支的 `/docs`，但本仓库现有 docs 是文档目录，不是构建输出；必须单独规划，不能误发布或覆盖源文档。

官方参考：[发布源配置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。GitHub 支持分支根目录或 `/docs`，也支持自定义 Actions。托管政策与计划适用性以官方文档及目标账号为准。本应用不需付费后端，但不承诺所有账号配置都免费。

## CI 草案

`.github/workflows/checks.yml.example` 不是启用的工作流。确认远端执行权限后再改名为 `.yml`，复核 Action 版本/供应链并按组织政策固定提交 SHA。草案仅检查，不包含部署、写仓库权限或付费服务。自动部署方案应另行审批，避免内容合并即意外公开。
