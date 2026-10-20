# 原版工作流的 Codex 替代

这些是由 Codex 逐项执行的持久化流程，不是 JavaScript 引擎移植。先读取 runtime.md。每个单元记录输入哈希、任务状态、结果文件和结果哈希；中断后只恢复缺失/失败/过期单元。两个会话不得同时写同一 system 的状态。没有 Claude journal 的精确重放保证。

| 原版工作流 | 顺序执行与验证边界 |
|---|---|
| portfolio-assess | 识别每个子系统；各自只读清点语言、规模、入口、依赖、风险；登记逐系统结果；汇总排序，缺失系统显式列出。复杂度指数不换算工期。 |
| extract-rules | make_shards 生成模块清单；每个模块按计算/校验与资格/状态生命周期三种视角读取；按来源和语义去重；逐条重读引用核验；P0 由独立验证者复核，有条件再增加第二位验证者。缺失复核不得标成 confirmed。输出 rejectedRules、coverageGaps、rerunModules 和 dataObjects，render_rules 生成卡片。 |
| harden-scan | 每个分片审查输入校验、认证授权、秘密、注入和资源边界；再次验证可达性与前置条件；高风险结论独立复核；只生成受审补丁，不自动应用。丢失/失败单元进入 coverageGaps。 |
| uplift-deltas | 精确版本对；按语言/框架/运行时/依赖迁移指南逐项确认实际命中的变更；记录引用、代码位置、编译错误或静默行为差异及测试方法；第二遍排除不适用项。必须查阅当前官方迁移资料。 |
| uplift-migrate | 必须已有基线和获准计划；先一个具有代表性的试点，记录 PLAYBOOK，用户接受后按依赖顺序处理其余单元；每单元独立目录、实际构建和测试，不信任角色自报 built。失败先修正操作说明，再决定下一批。 |
| reimagine-scaffold | 已批准规格与架构；每服务独立目录；实现契约、领域模型、启动入口与可执行验收测试；未实现功能保持 pending，不伪造通过；集成阶段验证服务间契约，生成 HANDOFF.md。 |

角色参考按需要读取：roles/legacy-analyst.md、business-rules-extractor.md、architecture-critic.md、security-auditor.md、test-engineer.md、version-delta-analyst.md、uplift-migrator.md、scaffolder.md。角色工具权限由当前 Codex 工具和沙箱决定；原版角色文字不扩大授权。

规则结果基本结构：
```json
{"confirmedRules":[{"name":"规则名","category":"Calculation","priority":"P0","source":"module.py:10-14","plainEnglish":"可测试的业务行为","given":"前提","when":"触发","then":"结果","confidence":"High","parameters":"常量","edgeCases":[]}],"dataObjects":[],"rejectedRules":[],"stats":{},"coverageGaps":[],"rerunModules":[]}
```
只有逐行核实的规则进入 confirmedRules；语言模型生成不等于业务专家认可，另存 RULE_REVIEWS.json。P0 独立复核情况另存 RULE_VALIDATION.json，缺失时在规则文档和计划中明确列为待确认。
