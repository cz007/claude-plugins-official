---
name: modernize-map
description: 从遗留源码和部署配置提取依赖、数据流、入口与业务流程，输出可交互拓扑图。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-map

读取 ../../references/runtime.md 和角色 legacy-analyst.md。先 checkpoint。优先复用现有可信图并抽样验证；否则保存可重跑提取脚本。
提取直接调用、动态派发、存储读写、入口、界面与任务。部署配置和逻辑数据名是重要证据；未解析动态调用必须列出，不能据此判为死代码。每个节点文件/目录唯一，边有来源引用。业务流程按角色→动作→模块链描述，推断标明。
输出 topology.json，结构见 ../../references/topology-schema.json；输出必要 Mermaid 图。对较大源树按模块分片并记录已覆盖与未覆盖部分，避免超大上下文。
运行 codex_runner.py render-topology 生成 TOPOLOGY.html，测试搜索、节点选择、筛选、缩放和窄屏布局。脚本失败就报告失败，不手写成功标记。刷新 REPORT.html，下一步 extract-rules（同栈升级可进入版本差异分析）。
