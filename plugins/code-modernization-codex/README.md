# Code Modernization Codex

版本 **1.1.0**，日期 **2026-10-20**。社区适配，源自 Anthropic Code Modernization 1.0.0；不代表 Anthropic 或 OpenAI 官方产品。

用于本地遗留系统的分析、业务规则提取、计划审批、同栈升级、逐模块重写、新架构重建及证据验证。13 个 Codex Skills 对应原版 13 个命令；8 个角色保留为按需参考；6 个 Claude 工作流改为有文件检查点的顺序流程。

## 来源与边界

- 原版 Fork：[cz007/claude-plugins-official](https://github.com/cz007/claude-plugins-official)
- 上游：[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- 固定提交：`a0b04d9ddccaabe1976645f68b0eda50f74e7022`，分支 main。
- 适配分支：`codex/code-modernization-v1.1.0-20261020`。
- 原版路径 `plugins/code-modernization` 保留完整；本包在独立的 `plugins/code-modernization-codex`。
- 许可：Apache-2.0；Mermaid 的 MIT 许可在 assets/vendor。出处、提取清单和文件哈希见 PROVENANCE.json 与 NOTICE。

## 使用条件

Codex 本地文件/终端能力，Python 3.8+ 标准库。实际项目还需其语言的构建工具。Node 仅用于本包的 JavaScript 回归测试，不是核心 Python 工具的运行依赖。官方技能结构校验器需要 PyYAML；这也是开发验证依赖，不随插件安装。

没有 Claude AskUserQuestion、Workflow、userConfig、生命周期钩子或实时 pane 依赖。没有遥测、自动联网或后台启动逻辑。任务记录保存在调用者选择的工作区，不写 Codex 全局配置。

## 安装

详见 [INSTALL.md](INSTALL.md)。交付物仅供安装，未自动全局启用。优先使用本地市场 ZIP，它包含 `.agents/plugins/marketplace.json` 和 `plugins/code-modernization-codex`。

## 使用

安装后在 Codex 中明确调用：

```text
$modernize 请分析 E:\Projects\example，工作区使用 E:\Projects\example-modernization。
系统名 example，先理解现有系统并生成计划，未经批准不进入迁移。
```

也可按需调用 `$modernize-preflight`、`$modernize-assess`、`$modernize-map`、`$modernize-extract-rules`、`$modernize-review`、`$modernize-brief`、`$modernize-uplift`、`$modernize-transform`、`$modernize-reimagine`、`$modernize-verify`、`$modernize-harden`、`$modernize-status`。主机若显示插件前缀，以其 Skills 选择器显示名称为准。

不安装也能手动验证脚本（先替换为实际路径）：

```powershell
$pythonExe = 'C:\Path\To\python.exe'
$pluginDir = 'E:\Path\To\plugins\code-modernization-codex'
& "$pluginDir\scripts\run.ps1" -Python $pythonExe init example --workspace 'E:\Path\To\work' --source 'E:\Path\To\source' --track understand
& "$pluginDir\scripts\run.ps1" -Python $pythonExe status example --workspace 'E:\Path\To\work'
```

新初始化会保存源目录映射与 SHA-256，不复制、链接或修改源目录。构建只在隔离副本执行。哈希检查检测修改，不能替代操作系统写保护。

## 验证

```powershell
& $pythonExe -B -m unittest discover -s "$pluginDir\scripts\tests" -v
& $pythonExe -B "$pluginDir\tests\e2e.py" --out 'E:\Path\To\new-e2e-run'
```

E2E 输出目录必须不存在。样例真实运行新旧程序、测试、金丝雀和差异比较；发现契约是有意构造的样例，不表示可以自动理解任意项目。验证等级和未实测项见 [VALIDATION.md](VALIDATION.md)、[COMPATIBILITY.md](COMPATIBILITY.md)。

## 修订记录

| 版本 | 日期 | 内容 |
|---|---|---|
| 上游 1.0.0 | 固定于 2026-10-20 | 原版 Claude 插件 |
| Codex 1.1.0 | 2026-10-20 | Skills 流程迁移、本地状态/批准哈希、Windows 路径与启动、源完整性检测、离线验证及安装包 |

## 未确认事项

插件未在当前 Codex 主机安装和启用，因此尚未验证目录发现、自动触发与跨会话实际加载。未执行真实企业系统的三条迁移路线，也未完成独立模型复核或生产验收。实时 pane 已替换为手动 HTML 报告，不承诺功能等价。
