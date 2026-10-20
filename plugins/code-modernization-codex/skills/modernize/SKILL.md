---
name: modernize
description: 启动遗留代码现代化，确认目标和来源并衔接分析、计划、迁移与验证。适用于用户要理解、升级、重写或重建现有系统。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize

读取 ../../references/runtime.md。查看工作区是否已有 analysis/<system>/CONFIG.json；有则执行 status，沿用 INTENT 与已有答案，指出过期阶段。
没有则确认源码路径、工作区和系统名。用户尚未指定目标时询问：理解、同技术升级、逐模块重写、新架构重建；再确认目标版本或架构、哪些行为必须保持。未知内容写待确认，不能作为批准。
运行 codex_runner.py init，记录 INTENT.md 的原始用户答案。展示适用路线与产物；已有继续授权就执行 preflight，不额外要求“是否开始”。understand 路线止于计划，不自行进入代码迁移。
路线：preflight → assess → map → extract-rules → review（有待裁定规则时）→ brief → 获准范围内 uplift/transform/reimagine → verify。同栈升级可省略规则提取，但必须有版本差异目录、实测基线和计划；安全优先请求将 harden 放到 assess 后。
