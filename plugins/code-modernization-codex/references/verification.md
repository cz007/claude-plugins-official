# 验证证据契约

改编自 Anthropic modernize-verify，2026-10-20。脚本负责证据计算，模型负责执行、记录、解释。验证者不得修改待验实现、测试断言或旧输出以改善结论。

1. 识别真实构建单元：rewrite 为 modernized/<system>/<module>；uplift 为 modernized/<system>-uplifted；reimagine 为 modernized/<system>-reimagined/<service>。仅含测试工具的目录不作业务模块判定。
2. 检查测试命令和服务配置；运行前限定本地或明确授权的测试环境。缓存清理只能在本次生成的工作区构建目录，先核验绝对路径，不拼接跨 shell 删除。也可复制到新的干净 scratch 目录运行，避免删已有文件。
3. 重新运行完整测试，保存 JUnit/TRX 或原始日志。只有真实 runner 结果计数有效；P0 覆盖需要执行且通过的测试名/类名包含 RULE-NNN（或 ruleNNN），单纯注释/文档不等于覆盖。跳过必须有原因，零测试不能通过。
4. 在 scratch 副本改一行关键计算/条件作为 canary，执行同一相关测试，保存失败 XML/日志；原验收代码不变。不能用伪造失败日志代替破坏实验。
5. 开发案例保存在 analysis/<system>/equivalence/<module>/cases.json。真实旧/新程序用同样输入运行，保存输出，调用 compare.py。已知差异也必须由人类接受，模型不能自行加入 approvedDifference。
6. 独立提出至少 10 个开发未用的新输入：边界、空值、大值、顺序及符合范围的错误输入。fresh-cases.json 中每个 input 标识一个输入；输出不能只是重复的 OK/COMPLETED。旧程序拒绝的输入查明原因，写 leftOut 并补充其余输入；不得静默删失败案例。
7. 源不可运行时 legacy.ran=false，说明 recorded trace 的出处；结论上限 PARTLY PROVEN。代码行为的业务正确性、人类批准、部署验收和验证者独立性不是 proof_pack 可自行证明的事项。
8. uplift 先用 baseline_diff.py 对比实测原版结果；BASELINE.md 的 Recorded: 行指向真实结果，不能仅手填表格。审查测试删改、静默变化的命名测试及目标版本差异。
9. 记录下列 test-runs.json，执行 proof_pack.py。新初始化工作区以 SOURCE_HASHES 检查源文件内容/增删；旧格式工作区仍使用上游 mtime 回退，必须披露其限制。源码哈希缺失/读取失败不能判为未变。
10. 报告原始判定并保留空白签署区。PROVEN 仅覆盖证据中的模块和输入；当前代理执行的证明包不是独立模型复核。

cases.json 示例（路径相对此 JSON）：
```json
{"system":"billing","legacy":{"label":"original","command":"实际命令"},"new":{"label":"adapted","command":"实际命令"},"cases":[{"id":"C01","input":"C01","title":"threshold boundary","legacy":"out/legacy/C01.txt","new":"out/new/C01.txt"}]}
```

test-runs.json 位于 analysis/<system>/equivalence/，内部路径相对 workspace：
```json
{"date":"实际日期","legacy":{"ran":true,"how":"实际本地命令","why":""},"leftOut":[],"suites":[{"module":"mod","name":"unit tests","command":"实际命令","junit":["modernized/billing/mod/results"],"log":["analysis/billing/equivalence/unit.log"],"skippedReason":"","note":""}],"canaries":[{"module":"mod","change":"实际破坏点","junit":["analysis/billing/equivalence/canary/mod"],"log":[]}]}
```

命令使用已核验的 Python 路径，不依赖 python3 名称：
```
<python> -B <plugin>/scripts/compare.py <cases.json> --out <EQUIVALENCE.json>
<python> -B <plugin>/scripts/trace_rules.py <system> --workspace <workspace> --module <module> --results <results-folder>
<python> -B <plugin>/scripts/proof_pack.py <system> --workspace <workspace>
<python> -B <plugin>/scripts/build_report.py <system> --workspace <workspace>
```
