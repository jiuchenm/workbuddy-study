# WorkBuddy 运行机制学习报告

[在线阅读](https://jiuchenm.github.io/workbuddy-study/)

基于 Windows WorkBuddy 5.6.2 安装包的原创静态分析，覆盖上下文装配、Skill 路由、Agent 编排、工具与权限、结果验证和会话恢复。

报告保留交互案例、证据定位和不确定性说明。证据元数据中的路径均相对于安装资源目录；未发布安装文件、供应商原始源码、完整 Prompt、用户聊天或本机绝对路径。此项目为独立学习分析，非腾讯官方文档。

## 发布

GitHub Actions 校验 site/ 后部署至 GitHub Pages。发布方式参考个人 money 仓库的 Pages workflow。此站点使用独立仓库，不依赖投资研究站点。

```powershell
python scripts/verify_public.py
```

更新报告时，传入本地 HTML 与对应证据索引，生成公开副本：

```powershell
python scripts/export_report.py <report.html> <mechanism-evidence.json>
python scripts/verify_public.py
```

只将 site/ 上传为 Pages artifact。提交并推送 main 后自动部署，也支持手动运行 workflow。
