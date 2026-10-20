# Verification: pricing

Written by `scripts/proof_pack.py` on 2026-10-20 01:41 UTC. Each module's verdict is computed from the evidence files by the fixed rules at the end of this page. No model's opinion is part of it.

**Overall: PROVEN** (1 proven)


Legacy source: `configured source` (a link to `[WORKSPACE]\evidence\e2e-final\旧系统 source`). Could it run here: yes. The source was checked SHA-256.

| Module | Track | Verdict | Tests executed | Failed | P0 rules tested | Same behavior | Fresh inputs |
|---|---|---|---|---|---|---|---|
| mod | rewrite | **PROVEN** | 6 | 0 | 2 of 2 | pass | pass |

## mod: PROVEN

Track: rewrite. Folder: `modernized/pricing/mod`. Checked 2026-10-20 01:41 UTC.

**What passed**

- Tests ran: 6 test(s) executed, 0 failed, 0 skipped. Note: Actual unittest execution; custom JUnit serializer uses TestResult events.
- Rules traced: All 2 P0 rule(s) this module answers for are backed by a test that ran and passed.
- Same behavior: 6 of 6 development case(s) executed: 6 same, 0 differ, 0 missing; comparator self-check passed.
- Fresh inputs: 12 new input(s), 12 comparison(s), ran on the legacy and the new code with no difference.
- Canary: 1 canary run(s) shown by a result file or log; the first (quantity > 10 changed to > 11 in scratch copy) made 1 more test(s) fail than the clean run (analysis/pricing/equivalence/canary/mod).
- Source untouched: legacy/pricing is untouched: 0 changed/added/deleted files; 0 excluded links; SHA-256 compared. Checked SHA-256.

| Check | Result | Detail |
|---|---|---|
| Tests ran | pass | 6 test(s) executed, 0 failed, 0 skipped. Note: Actual unittest execution; custom JUnit serializer uses TestResult events. |
| Rules traced | pass | All 2 P0 rule(s) this module answers for are backed by a test that ran and passed. |
| Same behavior | pass | 6 of 6 development case(s) executed: 6 same, 0 differ, 0 missing; comparator self-check passed. |
| Fresh inputs | pass | 12 new input(s), 12 comparison(s), ran on the legacy and the new code with no difference. |
| Canary | pass | 1 canary run(s) shown by a result file or log; the first (quantity > 10 changed to > 11 in scratch copy) made 1 more test(s) fail than the clean run (analysis/pricing/equivalence/canary/mod). |
| Source untouched | pass | legacy/pricing is untouched: 0 changed/added/deleted files; 0 excluded links; SHA-256 compared. Checked SHA-256. |

tests executed: 6, failed 0, skipped 0

- pricing unittest: `python -B run_tests.py results/TEST-Pricing.xml` (from result files): 6 executed, 0 failed, 0 skipped, 1 result files written 2026-10-20 01:41 UTC. Note: Actual unittest execution; custom JUnit serializer uses TestResult events.

### P0 business rules

| Rule | Name | Confidence | Result | Tests | Code | A test that names it |
|---|---|---|---|---|---|---|
| RULE-001 | Tiered price | High | tested | 3 | 3 | `modernized/pricing/mod/test_pricing.py:4` |
| RULE-002 | Reject invalid quantity | High | tested | 3 | 3 | `modernized/pricing/mod/test_pricing.py:9` |

### Development cases, judged again

6 of 6 executed: 6 same, 0 differ, 0 missing.

### Fresh inputs

12 new input(s) counted from 12 comparison(s) executed: 12 same, 0 differ, 0 missing.

### Waiting for a person

Claude never ticks these. A person decides them.

- [ ] Owner accepts behavior [Phase 1 exit criterion]
- [ ] Independent reviewer and business owner sign-off [open question, section 7]

### What this does not prove

- It does not prove behavior on inputs nobody tried: the equivalence cases and the fresh inputs are samples, not the whole input space.
- It does not cover speed, capacity, security, concurrency, or anything the tests and cases do not exercise.
- It traces only the rules that were extracted: behavior nobody wrote down as a rule has no rule to trace.
- A test that names a rule shows the rule is mentioned, not that the test is a good one. The canary shows only that some test can fail.
- It does not replace the review and sign-off of the people who own the system.

## Sign-off

A person fills this in. Claude leaves it blank.

| | |
|---|---|
| Name | ________________ |
| Role | ________________ |
| Date | __________ |
| Decision | accept / accept with conditions / reject |

## How each verdict is computed

PROVEN needs every check to pass: the six below, and for an uplift three more (7 to 9). NOT PROVEN when any check fails. PARTLY PROVEN when nothing failed but a check could not pass.

1. Tests ran: at least one test executed in a fresh run, none failed, none was skipped without a reason, and every result file is newer than the code. The counts must be read by this script from result files or a saved raw runner log; counts only typed in cannot reach PROVEN.
2. Rules traced (rewrite and reimagine): every P0 rule the module answers for is backed by a test that ran and passed: its id is in the test or class name of a result this script parsed, or a test file names it on a line not marked skipped or pending and that file's class ran and passed. A rule named only by skipped, pending or failing tests is named, not run; one only the notes name is claimed. Neither is tested.
3. Same behavior: the development cases, judged again by compare.py, executed at least one case and none differs or is missing (a difference a person approved is allowed and listed); for an uplift, no regression, no new failure, no missing test and no drop in executed tests against BASELINE.md.
4. Fresh inputs: at least 10 new inputs, none with the same output as a development case, ran on the legacy and the new code with no difference. Needed whenever the legacy could run here; when it could not, the proof is trace-based and the best verdict is PARTLY PROVEN.
5. Canary: a deliberate one-line break whose own result file or saved runner log shows failing tests. A line in the notes is a claim.
6. Source untouched: no file under legacy/<system> is newer than the analysis (PREFLIGHT.md), by a plain file walk; no version-control tool is run.
7. Baseline measured (uplift): the old version's numbers in BASELINE.md come from per-test result files, a per-test results file or a raw runner log that this script parsed (in analysis/<system>/baseline/, or on a Recorded: or Machine-readable: line of BASELINE.md), and the typed table agrees with them. A table typed by hand, or sources that disagree, cannot reach PROVEN.
8. Tests kept (uplift): no test file of the untouched legacy tree is missing from the working copy, no more than 25% of them changed, and the legacy tree has test files to compare against (walked by file, no process is run). The list is for a person to review; weakened assertions cannot be detected, only that files changed.
9. Deltas covered (uplift): every Behavioral-silent delta in DELTA_CATALOG.md has its site's file named, as a whole word, by some test file of the working copy. A name is not proof that the test exercises the change.
Open questions, unticked criteria and the sign-off are for a person. They never change the verdict.
A folder that holds only test code and the files that build it is test tooling: it is listed, not judged, and not counted.
