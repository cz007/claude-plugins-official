---
name: modernize-transform
description: 在已批准范围内逐模块重写遗留代码，使用特征测试和新旧输出比较保持行为。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-transform

读取 ../../references/runtime.md、roles/test-engineer.md 与 roles/architecture-critic.md。核验目标运行时真实可运行，读取批准计划的模块/范围、入口条件和 RULE_REVIEWS。用 gate 验证批准；缺少具体模块计划则先完成计划再等待批准。
先在安全 scratch 副本运行旧实现，保存特征输入和原始输出；不能运行则明确 trace-based 上限。创建 modernized/<system>/<module>/。先写命名 RULE-NNN 的可执行特征测试，再以目标栈惯用方式实现，不擅自纠正旧行为。
把相同输入馈送旧/新实现，保存真实输出到 analysis/<system>/equivalence/<module>/，cases.json 路径相对此文件；运行 compare.py。只掩码有明确依据的不稳定字段；不同结果提交用户判定，不自动写 approvedDifference。
在隔离副本故意破坏一项关键逻辑，保留失败的测试报告证明测试有效。记录文件/规则映射、命令、测试结果、未迁移内容和 trace-based 限制到 TRANSFORMATION_NOTES.md。
进行架构复核，修复获准范围内缺陷，保留复测证据；同一代理复核标明独立性限制。刷新报告，下一步 modernize-verify，不把本步骤自测作为独立验收。
