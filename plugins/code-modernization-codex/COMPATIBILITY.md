# 兼容性清单

版本 1.1.0 / 2026-10-20。以下“已实现”指适配代码或流程已提供，不自动代表全部模型工作流实测通过。

| 原版组件 | Codex 处理 | 验证边界 |
|---|---|---|
| .claude-plugin/plugin.json | 新增 .codex-plugin/plugin.json，独立名称与版本 | 静态元数据/路径校验；主机安装未测 |
| 13 个 commands | 对应 13 个 Skills，保留阶段产物和批准边界 | 全部官方技能结构校验通过；任意项目自动触发未测 |
| 8 个 agents | references/roles 按需读取，去除 Claude 工具声明 | 角色内容已迁移；不宣称八个独立代理已执行 |
| 6 个 workflows | references/workflows 的顺序任务流程，STATE 文件保存结果/输入哈希 | 恢复与过期检测测试通过；无 Claude journal 重放等价性 |
| userConfig system/track/legacyDir | 显式参数与工作区 CONFIG.json source | 中文/空格/外部源路径样例通过；无安装问卷 |
| AskUserQuestion | 使用宿主可用输入工具，否则聊天提问 | 不填默认批准，不自动签署 |
| 计划审批 | 计划、规则、源哈希与 scope 记录；gate 阻止缺失/过期批准 | 机械门禁有测试；聊天身份与批准真实性仍需人工核验 |
| 源码分析 | Skills 引用实际控制流与部署配置，分片器复用 | 单文件样例产物；非任意语言解析器保证 |
| 业务规则 | 保留 Given/When/Then、RULE-NNN、引用与人工裁定 | 两条样例规则产物/执行覆盖；独立模型复核未测 |
| 拓扑 | 原版本地 HTML viewer + 安全 JSON 注入 | 生成与注入反例测试；浏览器视觉/交互未验收 |
| uplift | 版本差异、真实基线、试点、PLAYBOOK、分批与三项升级证据 | 流程迁移与原版证明器单测；真实版本升级未跑 |
| transform | 特征测试→重写→同输入比较→金丝雀→独立验证 | Python 小样例真实执行；非企业项目验收 |
| reimagine | 规格确认→架构批准→服务构建→契约测试与 HANDOFF | 流程迁移；真实多服务重建未跑 |
| compare/proof/trace/baseline | 原版脚本优先保留；proof 加源映射/哈希检查 | 实际 E2E 与正反例回归 |
| source untouched | 新工作区使用 SHA-256；旧工作区保留 mtime 回退 | 检测同时间戳修改/删除；不是 OS 写保护 |
| Python/Windows | 显式解释器、PowerShell 参数数组、UTF-8、长短路径规范化 | Windows Python 3.12 实测；不装全局软件 |
| 报告 | 原版自包含 HTML、CSP、脚本哈希、文本转义；统一微软雅黑 | 生成与 Node DOM 模拟测试；file:// 浏览器被策略阻断 |
| 自动 panel/review-pane/sign | 不打包；使用 status、review、brief 和手动 REPORT.html | 明确替代，不宣称实时面板等价 |
| xray 自动读取钩子 | 手动关联 topology 与规则引用 | 流程说明；无自动上下文注入 |
| telemetry | 完全移除遥测脚本与钩子；CONFIG telemetry=false | 包内容检查；不向 Anthropic/OpenAI 发遥测 |
| Claude hooks/experimental | 不打包 hooks | 不依赖生命周期或实验运行时 |
| Bash 命令 | 核心控制改用 Python/PowerShell；原版脚本保留跨平台入口说明 | 不需要 Git Bash；具体项目构建命令依项目决定 |

## 证明与批准

proof_pack 的 PROVEN 只表示当前文件证据满足其固定检查。它不证明业务政策正确、不认证人类身份、不自动证明模型独立性，也不代表部署上线。旧系统不能运行时按原版规则最多 PARTLY PROVEN；丢失结果、错误输出、零案例不可报告比较成功。

## 尚未实测

当前主机插件安装/启用与自动发现；实际独立模型的规则和架构复核；真实 Java/.NET 等升级；真实新架构多服务重建；Linux/macOS；报告的浏览器视觉、缩放和完整交互。不得将这些项目标为“已兼容验收”。
