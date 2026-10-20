# 安装说明

版本 1.1.0 / 2026-10-20。适用本地 Codex 桌面环境。此文档不授权全局安装、组织发布或向公共插件目录提交。

## 推荐：独立目录的本地市场包

1. 将 `CodeModernization_Codex_LocalMarketplace_V1.1.0_20261020.zip` 解压到一个新的目录。不要覆盖已有 Skills、市场清单或配置。
2. 确认目录内存在 `.agents/plugins/marketplace.json` 与 `plugins/code-modernization-codex/.codex-plugin/plugin.json`。
3. 在 Codex 中将该目录作为项目打开。按官方本地市场流程重启桌面应用，然后在插件目录选择 **cz007 Code Modernization**，检查名称、版本与路径，再由用户点击安装/启用。
4. 新建测试聊天，先调用 `$modernize-status` 或 `$modernize` 对小型样例执行；在真实项目使用前核验源路径和批准边界。

市场声明是 AVAILABLE，不含自动启用配置。此流程按当前官方说明制作，**本轮未执行主机安装/发现验收**。

## 可选：CLI 登记 Git 市场

有支持插件市场命令的 Codex CLI 时，可由用户执行：

```text
codex plugin marketplace add cz007/claude-plugins-official --ref codex/code-modernization-v1.1.0-20261020
codex plugin marketplace list
```

分支中的市场只指向新增 Codex 插件目录。登记会修改本机市场配置；本次交付没有代为运行。不要使用上游 main 作为适配分支。

## 插件单体包

`CodeModernization_Codex_Plugin_V1.1.0_20261020.zip` 的根目录是插件内容，包含 `.codex-plugin/plugin.json`、skills、scripts、references、assets、许可和文档。可用于人工审查或按官方机制导入；本次未提交公共目录，也不宣称通过门户扫描或组织审核。

## Python

优先显式指定已验证的 Python 3.8+：

```powershell
& '.\plugins\code-modernization-codex\scripts\run.ps1' -Python 'C:\Path\To\python.exe' status demo --workspace 'E:\Path\To\workspace'
```

也支持当前进程环境变量 `CODE_MODERNIZATION_PYTHON`。缺失解释器时启动器报错，不自动安装。核心脚本只需标准库。Linux/macOS 使用 `python3 -B <plugin>/scripts/codex_runner.py ...`；这两个平台本轮未实测。

## 回退和更新

在插件 UI 停用/卸载本次插件；保留工作区 analysis 和 modernized 产物供复核。移除 CLI 市场时使用其官方 remove 命令，不删除原版 Fork。新版本放入新目录，再更新市场来源；不要覆盖当前验收证据。

## 官方依据（核验于 2026-10-20）

- [Claude 插件迁移](https://developers.openai.com/plugins/guides/submit-claude-plugin)
- [插件封装与本地市场](https://developers.openai.com/plugins/build/plugins)
- [Skills 构建](https://developers.openai.com/plugins/build/skills)
