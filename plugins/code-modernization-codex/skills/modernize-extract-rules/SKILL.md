---
name: modernize-extract-rules
description: 提取带代码引用的业务规则、数据对象与待确认问题，产出可测试的规则卡片。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-extract-rules

读取 ../../references/runtime.md、../../references/workflows.md 的 extract-rules，以及角色 business-rules-extractor.md。
checkpoint 后运行 scripts/make_shards.py <system> --workspace <workspace>，检查输出清单和覆盖。每模块分别提取计算、验证资格、状态生命周期规则。每条包含 name/category/priority/source/plainEnglish/given/when/then/parameters/edgeCases/confidence/smeQuestion。
重读每个 source 行范围，规则必须来自可执行代码；只在注释中的主张拒绝并记录。按来源与语义去重，保留被合并关系。P0 用独立验证者确认；没有独立执行能力就明示缺口，不能把同一代理两遍阅读叫独立验证。
保存 rules_result.json、RULE_VALIDATION.json（验证者、输入引用、结果、独立性）、coverageGaps 与 rerunModules。运行 render_rules.py <system> --workspace <workspace>。检查 BUSINESS_RULES.md 的 RULE-NNN 卡片、优先级、Given/When/Then、file:line 和 DATA_OBJECTS.md。
结果只是源码行为，尚需业务裁定。对 P0 缺陷/低置信度/未独立确认项先 review，再 brief；任何失败分片都必须在报告中显示。
