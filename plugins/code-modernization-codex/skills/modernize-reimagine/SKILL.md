---
name: modernize-reimagine
description: 依据遗留业务行为在获准架构下重建系统，分开规格确认、架构批准和服务验收。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-reimagine

读取 ../../references/runtime.md、workflows.md 的 reimagine-scaffold、roles/scaffolder.md、architecture-critic.md。
复用 ASSESSMENT、topology、BUSINESS_RULES、DATA_OBJECTS 与人工规则裁定，只补缺失发现。输出 AI_NATIVE_SPEC.md：能力、领域实体、行为契约、角色流程、异常、非功能约束、数据迁移、未确认事项；先让用户确认规格。
按目标设计 REIMAGINED_ARCHITECTURE.md，包含服务边界、接口、数据所有权、幂等、失败恢复、部署与回退。独立批判审查过度设计和规则遗漏；条件不足明确标注独立性未验证。具体架构批准后才 scaffold，用 gate 验证范围。
每个服务写入 modernized/<system>-reimagined/<service>/，实现可运行入口、领域模型、接口契约与验收测试。未实现功能保持 pending，不生成虚假通过结果。顺序服务任务在 STATE 中记录；需要并行时遵守当前授权和工具限制。
完成集成契约验证及 HANDOFF.md（启动命令、配置占位符、规则映射、未完成项，不含秘密）。再运行 verify；仅生成脚手架不代表业务重建完成。
