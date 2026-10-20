---
name: modernize-status
description: 检查现代化产物、任务恢复点、证据时效与批准范围，说明当前进度及下一步。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-status

读取 ../../references/runtime.md。运行 codex_runner.py status；不存在配置时清点旧格式 analysis/<system>/，明确没有哈希基线。
按 intent/preflight/assessment/map/rules/review/brief/build/equivalence/verification 清点实际产物。检查依赖时间与哈希：规则/源码变化→计划过期，代码/测试比结果新→验证过期。done 任务的结果缺失或改变→stale，running 中断→先确认无活跃任务再标 failed/interrupted。
查看三条迁移分支的实际目录和说明；文件存在不代表完成。compare 成功不代表整体验证，报告生成不代表证明。读取当前 VERIFICATION 而不复用历史成功，若过期则标为未重新证明。
显示待人类裁定的规则、计划、差异和签署；不替人批准。刷新报告仅为便利。最终给出最关键未完成项及一个对应 Skill 调用，不虚构自动面板或后台更新。
