"""Offline executable E2E fixture. Sample evidence, not production acceptance."""
import argparse, json, os, shutil, subprocess, sys, time
from pathlib import Path
PLUGIN=Path(__file__).resolve().parents[1]
SCRIPTS=PLUGIN/"scripts"

LEGACY='''import json, sys
def quote(qty):
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 0:
        return {"error": "invalid quantity"}
    rate = 100
    if qty > 10:
        rate = 90
    return {"quantity": qty, "total": qty * rate}
if __name__ == "__main__":
    print(json.dumps(quote(json.loads(sys.argv[1])), sort_keys=True))
'''
MODERN='''import json, sys
def quote(qty):
    valid = type(qty) is int and qty >= 0
    if not valid:
        return {"error": "invalid quantity"}
    return {"quantity": qty, "total": qty * (90 if qty > 10 else 100)}
if __name__ == "__main__":
    print(json.dumps(quote(json.loads(sys.argv[1])), sort_keys=True))
'''
TESTS='''import unittest
from pricing import quote
class PricingTests(unittest.TestCase):
    def test_rule001_threshold(self):
        self.assertEqual(quote(10), {"quantity":10,"total":1000})
        self.assertEqual(quote(11), {"quantity":11,"total":990})
    def test_rule001_zero(self):
        self.assertEqual(quote(0), {"quantity":0,"total":0})
    def test_rule002_negative(self):
        self.assertEqual(quote(-1), {"error":"invalid quantity"})
    def test_rule002_bool(self):
        self.assertEqual(quote(True), {"error":"invalid quantity"})
    def test_rule002_string(self):
        self.assertEqual(quote("3"), {"error":"invalid quantity"})
    def test_rule001_large(self):
        self.assertEqual(quote(1000000)["total"],90000000)
'''
JUNIT='''import sys, unittest, xml.etree.ElementTree as ET
from pathlib import Path
class Results(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.records=[]
    def addSuccess(self,t):
        super().addSuccess(t); self.records.append((t,None,""))
    def addFailure(self,t,e):
        super().addFailure(t,e); self.records.append((t,"failure",self._exc_info_to_string(e,t)))
    def addError(self,t,e):
        super().addError(t,e); self.records.append((t,"error",self._exc_info_to_string(e,t)))
    def addSkip(self,t,reason):
        super().addSkip(t,reason); self.records.append((t,"skipped",reason))
suite=unittest.defaultTestLoader.discover(str(Path(__file__).parent),pattern="test_pricing.py")
result=unittest.TextTestRunner(verbosity=2,resultclass=Results).run(suite)
root=ET.Element("testsuite",name="PricingTests",tests=str(result.testsRun),failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)))
for t,status,message in result.records:
    case=ET.SubElement(root,"testcase",classname=t.__class__.__name__,name=t._testMethodName)
    if status:
        ET.SubElement(case,status,message=message)
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
ET.ElementTree(root).write(out,encoding="utf-8",xml_declaration=True)
sys.exit(0 if result.wasSuccessful() else 1)
'''

def put(root,rel,value):
    p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(value if isinstance(value,str) else json.dumps(value,indent=2,ensure_ascii=False),encoding="utf-8")
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    root=Path(a.out).resolve()
    if root.exists():
        raise SystemExit("Output must be new; preserves previous runs")
    root.mkdir(parents=True)
    source=root/"旧系统 source"
    put(source,"pricing.py",LEGACY)
    ws=root/"workspace 中文"
    ws.mkdir()
    logs=root/"logs";logs.mkdir()
    records=[]
    def run(name,argv,cwd=ws,expected=0):
        p=subprocess.run([str(x) for x in argv],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60,env=dict(os.environ,PYTHONIOENCODING="utf-8",PYTHONDONTWRITEBYTECODE="1"))
        (logs/(name+".log")).write_bytes(p.stdout)
        records.append({"name":name,"argv":[str(x) for x in argv],"exit":p.returncode,"expected":expected})
        if p.returncode!=expected:
            raise AssertionError(name+": "+p.stdout.decode("utf-8",errors="replace"))
        return p.stdout
    py=[sys.executable,"-B"]
    runner=py+[SCRIPTS/"codex_runner.py"]
    run("init",runner+["init","pricing","--workspace",ws,"--source",source,"--track","transform","--target","Python 3"])
    base=ws/"analysis/pricing"
    put(base,"PREFLIGHT.md","# Preflight\n\nFixture only. Whole one-file system; no external service, packages or credentials. Python runtime exercised by the commands in logs. Human business context is not inferred.\n")
    put(base,"ASSESSMENT.md","# Assessment\n\nA Python JSON CLI exposes quote(qty). pricing.py:2-8 implements quantity validation and tiered pricing. No persistence or network. This purpose-built fixture tests the adapter pipeline only.\n")
    put(base,"topology.json",{"system":"pricing","root":{"id":"sys","name":"Pricing","kind":"system","children":[{"id":"mod","name":"Pricing","kind":"module","language":"python","loc":10,"file":"pricing.py"}]},"edges":[],"entryPoints":["mod"],"deadEnds":[],"observations":["Single-file fixture, no inferred external dependency"],"flows":[{"name":"Quote","persona":"Caller","description":"Calculate amount","steps":[{"label":"Validate and price","nodes":["mod"]}]}]})
    rules=[
      {"name":"Tiered price","category":"Calculation","priority":"P0","source":"pricing.py:5-8","plainEnglish":"Quantities up to 10 cost 100 each; larger quantities cost 90 each.","given":"a non-negative integer quantity","when":"a quote is requested","then":"total equals quantity times 100 if quantity <= 10, otherwise times 90","confidence":"High","edgeCases":["0","10","11"],"parameters":"threshold=10; rates=100,90"},
      {"name":"Reject invalid quantity","category":"Validation","priority":"P0","source":"pricing.py:3-4","plainEnglish":"Negative, boolean and non-integer quantities return an error.","given":"a quantity input","when":"it is negative, boolean or not an integer","then":"return error invalid quantity","confidence":"High","edgeCases":["-1","true","string"]}
    ]
    put(base,"rules_result.json",{"confirmedRules":rules,"dataObjects":[{"name":"Quote","fields":[{"name":"quantity","type":"integer"},{"name":"total","type":"integer"}]}],"stats":{},"coverageGaps":[]})
    put(base,"RULE_VALIDATION.json",{"method":"current Codex authored fixture contract from executable source","independent":False,"businessOwnerConfirmed":False,"note":"This is an adapter sample, not an independently validated business migration."})
    run("shards",py+[SCRIPTS/"make_shards.py","pricing","--workspace",ws])
    run("rules",py+[SCRIPTS/"render_rules.py","pricing","--workspace",ws])
    run("topology",runner+["render-topology","pricing","--workspace",ws])
    run("task-start",runner+["task","pricing","start","rules","--workspace",ws,"--input","source"])
    run("task-done",runner+["task","pricing","done","rules","--workspace",ws,"--result","analysis/pricing/BUSINESS_RULES.md"])
    put(base,"MODERNIZATION_BRIEF.md","# Sample plan\n\nOnly the purpose-built pricing fixture is exercised. No business project is authorized.\n\n### Phase 1 — Pricing\nModules: mod\nCommand: $modernize-transform pricing mod\nEntry criteria: fixture available\nExit criteria:\n- [ ] Owner accepts behavior\n\n## 7. Open questions\n- [ ] Independent reviewer and business owner sign-off\n\n## 8. Approval\nApproved by: ________________\n")
    # No fake approval: this is test-harness execution of a user-authorized disposable fixture.
    run("unapproved-gate",runner+["gate","pricing","--workspace",ws,"--plan","analysis/pricing/MODERNIZATION_BRIEF.md","--scope","Phase 1"],expected=1)
    mod=ws/"modernized/pricing/mod"
    put(mod,"pricing.py",MODERN)
    put(mod,"test_pricing.py",TESTS)
    put(mod,"run_tests.py",JUNIT)
    put(mod,"TRANSFORMATION_NOTES.md","# Fixture transformation\n\nLegacy: pricing.py\nRULE-001 and RULE-002 map to pricing.py and executable tests.\nPurpose-built sample; no business approval or independent reviewer claimed.\n")
    results=mod/"results/TEST-Pricing.xml"
    run("unit",py+[mod/"run_tests.py",results],cwd=mod)
    canary=root/"canary"
    shutil.copytree(mod,canary,ignore=shutil.ignore_patterns("results","__pycache__"))
    put(canary,"pricing.py",MODERN.replace("qty > 10","qty > 11"))
    canary_result=base/"equivalence/canary/mod/TEST-Canary.xml"
    run("canary",py+[canary/"run_tests.py",canary_result],cwd=canary,expected=1)
    eq=base/"equivalence/mod"
    def cases(name,values):
        rows=[]
        for i,value in enumerate(values):
            cid=name+str(i)
            for side,code in [("legacy",source/"pricing.py"),("new",mod/"pricing.py")]:
                output=run(cid+"-"+side,py+[code,json.dumps(value)])
                p=eq/name/side/(cid+".out");p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(output)
            rows.append({"id":cid,"input":cid,"title":json.dumps(value),"legacy":name+"/legacy/"+cid+".out","new":name+"/new/"+cid+".out"})
        f=put(eq,"cases.json" if name=="dev" else "fresh-cases.json",{"system":"pricing","legacy":{"label":"original","command":"Python pricing.py JSON"},"new":{"label":"rewritten","command":"Python pricing.py JSON"},"cases":rows})
        return f
    dev=cases("dev",[0,10,11,-1,True,"3"])
    fresh=cases("fresh",list(range(21,33)))
    run("compare-dev",py+[SCRIPTS/"compare.py",dev,"--out",base/"EQUIVALENCE.json"])
    run("compare-fresh",py+[SCRIPTS/"compare.py",fresh,"--out",eq/"FRESH_EQUIVALENCE.json"])
    runs={"date":time.strftime("%Y-%m-%d"),"legacy":{"ran":True,"how":"local Python CLI from immutable source","why":""},"leftOut":[],"suites":[{"module":"mod","name":"pricing unittest","command":"python -B run_tests.py results/TEST-Pricing.xml","junit":["modernized/pricing/mod/results"],"log":[],"note":"Actual unittest execution; custom JUnit serializer uses TestResult events."}],"canaries":[{"module":"mod","change":"quantity > 10 changed to > 11 in scratch copy","junit":["analysis/pricing/equivalence/canary/mod"],"log":[]}]}
    put(base,"equivalence/test-runs.json",runs)
    run("trace",py+[SCRIPTS/"trace_rules.py","pricing","--workspace",ws,"--module","mod","--results",mod/"results"])
    run("proof",py+[SCRIPTS/"proof_pack.py","pricing","--workspace",ws])
    run("report",py+[SCRIPTS/"build_report.py","pricing","--workspace",ws])
    pack=json.loads((base/"VERIFICATION.json").read_text(encoding="utf-8"))
    assert pack["overall"]["verdict"]=="PROVEN"
    # Negative tests use their own cloned evidence workspace; keep the successful sample intact.
    negative=root/"negative workspace"
    shutil.copytree(ws,negative)
    nb=negative/"analysis/pricing"
    bad=nb/"equivalence/mod/dev/new/dev0.out"
    bad.write_bytes(bad.read_bytes()+b"corrupt")
    run("negative-difference",py+[SCRIPTS/"proof_pack.py","pricing","--workspace",negative],expected=1)
    assert json.loads((nb/"VERIFICATION.json").read_text())["overall"]["verdict"]=="NOT PROVEN"
    run("negative-report",py+[SCRIPTS/"build_report.py","pricing","--workspace",negative])
    # Missing evidence must not fall back to an earlier successful VERIFICATION.
    (nb/"equivalence/test-runs.json").rename(nb/"equivalence/test-runs.saved.json")
    run("negative-missing-run",py+[SCRIPTS/"proof_pack.py","pricing","--workspace",negative],expected=1)
    # Check no-case and missing-output comparators.
    empty=put(root,"empty/cases.json",{"cases":[]})
    run("negative-empty",py+[SCRIPTS/"compare.py",empty],expected=1)
    missing=put(root,"missing/cases.json",{"cases":[{"id":"x","legacy":"absent","new":"absent"}]})
    run("negative-missing-output",py+[SCRIPTS/"compare.py",missing],expected=1)
    run("checkpoint",runner+["checkpoint","pricing","--workspace",ws])
    run("status",runner+["status","pricing","--workspace",ws])
    assert (source/"pricing.py").read_text()==LEGACY
    summary={"classification":"Executable local fixture E2E; discovery contract authored by current Codex; not installed-plugin invocation, independent review or production acceptance","positive":{"verdict":pack["overall"]["verdict"],"testsExecuted":6,"developmentInputs":6,"freshInputs":12,"rules":2,"canaryExpectedFailure":True,"sourceUntouched":True},"negative":["unapproved gate blocked","changed output NOT PROVEN","missing test run NOT PROVEN","zero cases nonzero exit","missing outputs nonzero exit"],"commands":records}
    put(root,"E2E_RESULT.json",summary)
    print(json.dumps({k:v for k,v in summary.items() if k!="commands"},ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
