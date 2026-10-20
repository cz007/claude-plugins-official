---
name: modernize-harden
description: 审查遗留代码安全风险，复核可达性并生成供审阅的修复补丁。
---

<!-- Adapted from Anthropic Code Modernization 1.0.0 by cz007, 2026-10-20; Codex-native workflow. -->

# modernize-harden

读取 ../../references/runtime.md、workflows.md 的 harden-scan、roles/security-auditor.md。checkpoint 后逐模块审查，凭证只输出类型与位置，不复制原值。
对每个候选风险确认来源→危险操作的实际路径、认证条件、已有过滤和可利用前提；独立复核高风险发现，没有条件就明确未独立复核，记录失败分片及覆盖缺口。
输出 SECURITY_FINDINGS.md：等级、CWE、file:line、证据、影响条件、修复建议、拒绝的误报、coverageGaps。只在隔离副本形成补丁并审查差异；源树保持不变，补丁不得包含凭证。
输出 security_remediation.patch 与验证记录；用户明确授权应用该具体补丁后才能应用到指定目标，不把扫描授权扩展为生产修改。刷新报告，告知剩余风险和待裁定事项。
