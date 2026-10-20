---
name: modernize-assess
description: 分析遗留系统的规模、技术债、架构风险与现代化路线；支持多系统组合评估。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-assess

读取 ../../references/runtime.md 及 ../../references/roles/legacy-analyst.md。先 checkpoint。
按源码文件和构建定义清点语言、规模、依赖、入口、部署、数据对象、测试。对架构、业务行为、技术债分别追踪实际调用并引用位置；可推断的规模指标标为估算，不换算工期。
对安全发现读取 ../../references/roles/security-auditor.md，仅报告有代码证据的风险和前置条件，凭证只保留掩码与位置。记录缺失源码、动态调用和未覆盖模块。只有用户提供授权运行数据时才做运行时叠加，不自行连接生产。
写 ASSESSMENT.md 和 ARCHITECTURE.mmd：概要、现状、依赖图、风险、文档差距、路线选择及理由（uplift/transform/reimagine 或仅分析）。无证据不宣称平台可运行。
portfolio 模式按 ../../references/workflows.md 的 portfolio-assess 逐系统执行，任务状态逐项保存，输出可比较清单及覆盖缺口。刷新报告，下一步 map。
