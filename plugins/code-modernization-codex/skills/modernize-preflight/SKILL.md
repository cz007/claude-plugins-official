---
name: modernize-preflight
description: 核验遗留代码范围、构建条件、版本及外部依赖，生成现代化预检报告。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-preflight

先读取 ../../references/runtime.md。使用 CONFIG.json 的 source 路径；不创建链接，不在源树编译。
未初始化则先执行 init；有记录则 checkpoint。只补齐五项人类信息：完整系统或切片及外部消费者、本地构建测试和耗时、私有依赖与自定义构建、以前迁移经验、不可修改范围。保留用户原话，未知写待确认。
读取构建清单、CI、上层工作区引用和数据定义，记录语言、精确运行时、私有源名称（不输出凭证）、入站/出站依赖、缺失源码和生成文件。不凭文件名断言死代码。
检测 Python 3.8+、目标工具链和可选 scc/cloc；缺少可选工具时用文件清点并声明指标估算。审查真实构建命令及服务配置后，仅在独立 scratch 副本执行一个代表性编译和一个最小完整单元构建/测试，保存原始日志。未知外部服务不运行。
输出 PREFLIGHT.md：五项答案、范围边界、工具与构建证据、各后续步骤 Ready/Ready-with-gaps/Not ready、实际失败和补救。说明源保护是行为约束与哈希检测；不得声称已设置 OS 保护。检查 SOURCE_HASHES，刷新报告，下一步 assess。
