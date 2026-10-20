---
name: modernize-verify
description: 根据真实测试、新旧比较、全新输入、金丝雀和源完整性证据验证迁移结果，拒绝空测或伪造通过。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-verify

读取 ../../references/runtime.md 和 ../../references/verification.md。这是验收检查，不修改代码以改善结论；发现缺陷交回对应迁移步骤。
使用新会话或独立执行者重新推导输入和运行测试；若只能当前代理操作，报告“同一代理执行，独立验证未完成”。先审查环境只指向本地/授权测试服务。
保留每个模块的真实 runner 结果、原始日志、开发案例和至少 10 个不重复新输入的旧/新输出；在 scratch 副本运行一行关键破坏的 canary。缺失环境、零测试、跳过、差异都不可改成成功。
保存 test-runs.json（仅命令、路径、说明，不手填测试计数），执行 proof_pack.py <system> --workspace <workspace>。原样报告每模块 PROVEN/PARTLY PROVEN/NOT PROVEN、失败理由、未覆盖范围和独立性限制。用户签署区保持空白。刷新 REPORT.html，下一步由失败项决定。
