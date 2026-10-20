---
name: modernize-uplift
description: 将现有代码升级到同技术栈的新版本，以版本差异、原版测试基线和试点控制迁移。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-uplift

读取 ../../references/runtime.md、workflows.md 的 uplift-deltas/uplift-migrate，以及 roles/version-delta-analyst.md、uplift-migrator.md。
固定来源和目标版本；实际验证两个运行时。只读收集 DELTA_CATALOG：当前官方迁移文档、项目命中位置、编译型/行为显式/行为静默变化、验证方法。没有旧运行时就写 target-only，不假装双版本比较。
读取计划和入站消费者；无计划时先产出具体计划，批准后才创建 modernized/<system>-uplifted/ 的干净工作副本。用 gate 检查；不覆盖源目录，不自动安装迁移工具。
在旧版本 scratch 副本运行原测试，保存 runner XML/JSON/日志和 BASELINE.md，包含既有失败；手填计数不作基线。建立相同命令的双版本驱动。
先迁移一个代表单元，执行 baseline_diff.py 对比每个测试；行为静默差异追加真实特征测试。记录 PLAYBOOK.md 和试点结论，获得扩大范围授权后按依赖顺序处理其他单元，并持久化逐任务结果。
删除/削弱测试不得用作消除差异。用户接受的差异单独登记。输出 UPLIFT_NOTES.md：差异→改动→证据、未完成项、测试增删变更、回退方式；运行 verify。若多数逻辑需重写，停下提出 transform 路线供用户决定。
