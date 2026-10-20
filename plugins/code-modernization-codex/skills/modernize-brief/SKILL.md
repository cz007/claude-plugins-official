---
name: modernize-brief
description: 将发现、业务规则和版本差异汇总为分阶段现代化计划，并保留人类批准边界。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-brief

读取 ../../references/runtime.md。输入 INTENT、PREFLIGHT、ASSESSMENT、topology、规则与人工复核。同栈升级必须先获得 DELTA_CATALOG，缺失则按 uplift 的只读差异分析生成，不擅自进入代码修改。
checkpoint 后输出 MODERNIZATION_BRIEF.md：1 目标与范围；2 路线、精确目标版本、架构边界；3 分阶段计划（Modules/Command/Entry criteria/Exit criteria，明确外部消费者兼容决策）；4 用户业务流程；5 行为契约（已确认 P0 或实测升级基线）；6 风险、依赖、回退；7 待决问题和验收条件；8 空白批准区。
阶段范围、目标、入口条件必须可检查，技术复杂度不是交付工期。wrong 规则不作为 oracle，discuss/P0 独立复核缺口列为待决事项。
先呈现具体可审阅计划，再等用户批准相应阶段；用户已有与该具体范围一致的授权就记录引用，不重复索要。用 record-approval 登记实际人类答复、来源及 scope；后续 gate 核验计划/源码/规则哈希。无批准不生成迁移代码。
