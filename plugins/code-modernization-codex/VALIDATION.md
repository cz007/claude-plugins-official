# 验证结果

版本 1.1.0 / 2026-10-20。验证环境：Windows、Python 3.12.14，使用已有 Node 运行页面脚本测试。本文区分静态检查、脚本测试、合成证据单测、实际程序样例和真实宿主安装。

## 结果

| 类别 | 结果 | 证明范围 |
|---|---|---|
| 原版保护 | 固定 SHA 下原版目录 git diff 为零 | 原版文件未修改；main 保留原版 |
| GitHub 身份和 Fork | CLI 账号 cz007；parent/source 均为 anthropics/claude-plugins-official | GitHub Fork 关系已实查 |
| Skills 静态检查 | 13/13 通过 skill-creator quick_validate.py | 元数据与结构；不证明自动触发 |
| 完整脚本回归 | 273 项，269 通过，4 项平台专属跳过，0 失败 | 证明、比较、规则、报告、状态与安全反例 |
| Windows 启动 | run.ps1 显式解释器与中文/空格路径执行成功 | 当前 Windows 环境 |
| 实际 E2E | 6 个真实 unittest 测试、6 个开发输入、12 个新输入、2 条 P0 规则；样例 proof_pack=PROVEN | 有意构造的小型 Python 程序；非生产验收 |
| 金丝雀 | scratch 副本把 >10 改为 >11，测试出现失败 | 样例测试能检测实际逻辑破坏 |
| 负例 | 未批准 gate 拒绝；输出差异/缺失 test-runs → NOT PROVEN；零案例/缺输出 → 非零退出 | 不把这些失败报告为通过 |
| 源完整性 | SHA-256 未变；同时间戳内容修改和删除可检出 | 内容检测；不是写保护 |
| 包完整性 | ZIP CRC 与逐文件 SHA-256 验证 | 文件封装完整性；主机加载另验 |

4 个跳过项：3 个使用 Windows 禁止的控制字符/竖线文件名，1 个 POSIX 权限语义。均在日志标明，未计入通过。原版部分单元测试使用合成 XML/日志，用于验证判定器，不冒充真实业务运行；E2E 的 XML 来自真实 unittest TestResult 事件。

## 当前 Codex 调用边界

当前会话读取并按迁移后的分析/规则 Skill 复核了样例 pricing.py 的规则引用，发现并修正了原版 render_rules.py 固定宣称“第二个代理已核验”的问题。最终生成器只输出证据中立声明并展示覆盖缺口。

这是当前 Codex 会话的手工流程执行与源码复核，**不是已安装插件的自动触发测试，也不是独立模型复核**。规则验证文件明确 independent=false、businessOwnerConfirmed=false。不能用样例 PROVEN 覆盖这两个限制。

## 首轮失败和修复证据

保留首次日志以及后续完整回归日志，未用跳过全部失败的方式获得通过：

- Windows 短/长绝对路径混用使拓扑分片遗漏：先 canonicalize，再计算源内相对路径。
- 测试对路径分隔符与根目录的 POSIX 假设：仅调整平台表达，保留业务断言。
- Node 的 UTF-8 输出被 Python 按 GBK 解码：子进程显式 encoding=utf-8。
- Mermaid 在 checkout 时发生 CRLF 转换：从固定 Git 对象恢复原始字节，校验上游许可文件记载的 SHA-256。
- 报告调用前缀：Claude slash command 改为 Codex Skill 名。
- 规则生成器无证据宣称独立代理核验：删除固定声明，增加覆盖缺口和反例测试。
- 新控制脚本：增加未授权计划、批准过期、任务结果篡改、源删除、输出越界与拓扑注入测试。

## 未完成的验收

- 未实际安装或全局启用插件；没有验证宿主市场发现、自动 Skill 选择或跨会话加载。
- 浏览器安全策略拒绝 file:// 页面，本轮没有规避该策略；**视觉与交互验收未完成**。Node 页面脚本测试是模拟 DOM，不等于浏览器验收。
- 未执行真实企业项目的 uplift/reimagine，也未做真实独立代理评审。
- 未验证 Linux/macOS、生产环境、远程服务与公共插件目录审核。

## 证据位置和复跑

仓库的 validation/ 保存经过路径归一化的日志、E2E 汇总及样例文档，供审阅；它们是归档证据，不能直接重跑其中的路径。tests/e2e.py 会在新的目录重新生成可执行的全部证据。

```powershell
& $pythonExe -B -m unittest discover -s "$pluginDir\scripts\tests" -v
& $pythonExe -B "$pluginDir\tests\e2e.py" --out 'E:\Path\To\fresh-run'
& $pythonExe -B "$pluginDir\tests\package.py" --out 'E:\Path\To\fresh-dist'
```

官方技能校验器的 PyYAML 本次仅安装在独立 validation-deps 目录，不属于插件运行依赖，也未改变全局配置。
