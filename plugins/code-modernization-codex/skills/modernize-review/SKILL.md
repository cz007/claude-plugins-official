---
name: modernize-review
description: 由业务人员确认或纠正已提取的规则，将人类裁定传递给计划和迁移。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-review

读取 ../../references/runtime.md。读取 BUSINESS_RULES.md、RULE_VALIDATION.json 和既有 RULE_REVIEWS.json；优先处理 P0 的缺陷、低置信度、未独立验证或 SME 问题。只询问尚未裁定或用户要改判的条目。
逐条展示规则、代码引用和具体疑点，请用户给 confirmed/wrong/discuss 及理由。保存原话、时间、消息来源，不推测业务正确性。无回复维持 pending/discuss。
checkpoint 后合并 RULE_REVIEWS.json，格式 {"reviews":{"RULE-001":{"verdict":"confirmed","title":"...","note":"用户原话","at":"ISO-8601"}}}；输出 RULE_REVIEWS.md 表格。不要修改原规则来隐藏差异。
wrong 不作为测试 oracle；discuss 的 P0 不得进入已确认行为契约。规则变化使旧计划批准过期。刷新报告并进入/重做 brief。
