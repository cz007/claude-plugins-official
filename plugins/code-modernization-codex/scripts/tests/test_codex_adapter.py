"""Meaningful adapter invariants. Temporary fixtures only."""
import contextlib, io, json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import codex_runner as cr
import codex_support as cs

class Adapter(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.source=self.root/"旧源 code";self.source.mkdir()
        (self.source/"app.py").write_text("value = 1\n")
        self.ws=self.root/"work space";self.ws.mkdir()
        self.call("init","demo","--source",str(self.source))
        self.base=self.ws/"analysis/demo"
    def call(self,*args,expected=0):
        out=io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
            code=cr.main(list(args)+["--workspace",str(self.ws)])
        self.assertEqual(code,expected,out.getvalue())
        return out.getvalue()
    def test_external_unicode_source_without_link(self):
        self.assertEqual(cs.source_root(self.ws,"demo"),self.source.resolve())
        self.assertFalse((self.ws/"legacy").exists())
        self.assertEqual(cs.hash_source_check(self.ws,"demo")["state"],"clean")
    def test_source_hash_detects_same_timestamp_change_and_deletion(self):
        p=self.source/"app.py";mtime=p.stat().st_mtime
        p.write_text("value = 2\n");os.utime(p,(mtime,mtime))
        self.assertEqual(cs.hash_source_check(self.ws,"demo")["state"],"changed")
        p.unlink()
        self.assertEqual(cs.hash_source_check(self.ws,"demo")["state"],"changed")
    def test_missing_baseline_is_not_clean(self):
        (self.base/"SOURCE_HASHES.json").unlink()
        self.assertEqual(cs.hash_source_check(self.ws,"demo")["state"],"unknown")
    def test_existing_init_is_refused(self):
        original=(self.base/"STATE.json").read_bytes()
        self.call("init","demo","--source",str(self.source),expected=2)
        self.assertEqual(original,(self.base/"STATE.json").read_bytes())
    def test_source_containing_output_is_refused(self):
        self.call("init","overlap","--source",str(self.root),expected=2)
        self.assertFalse((self.ws/"analysis/overlap").exists())
    def test_task_requires_result_and_detects_stale_source(self):
        self.call("task","demo","start","analysis")
        self.call("task","demo","done","analysis",expected=2)
        p=self.base/"result.json";p.write_text('{"evidence":true}')
        self.call("task","demo","done","analysis","--result","analysis/demo/result.json")
        self.assertEqual(json.loads(self.call("status","demo"))["tasks"]["analysis"]["status"],"done")
        (self.source/"app.py").write_text("value = 3\n")
        self.assertEqual(json.loads(self.call("status","demo"))["tasks"]["analysis"]["status"],"stale")
    def test_tampered_result_is_stale(self):
        p=self.base/"result.json";p.write_text("before")
        self.call("task","demo","start","x")
        self.call("task","demo","done","x","--result","analysis/demo/result.json")
        p.write_text("after")
        self.assertEqual(json.loads(self.call("status","demo"))["tasks"]["x"]["status"],"stale")
    def test_approval_scope_and_content_gate(self):
        plan=self.base/"PLAN.md";plan.write_text("phase one")
        args=["demo","--plan","analysis/demo/PLAN.md","--scope","Phase 1"]
        self.call("gate",*args,expected=1)
        # Synthetic approval is confined to this unit fixture; not a user decision.
        self.call("record-approval",*args,"--human-message","SYNTHETIC fixture decision","--evidence","test fixture")
        self.call("gate",*args)
        self.call("gate","demo","--plan","analysis/demo/PLAN.md","--scope","Phase 2",expected=1)
        plan.write_text("changed")
        self.call("gate",*args,expected=1)
    def test_checkpoint_keeps_previous_content(self):
        result=json.loads(self.call("checkpoint","demo"))
        saved=Path(result["checkpoint"])/"INTENT.md"
        before=saved.read_text(encoding="utf-8")
        (self.base/"INTENT.md").write_text("new")
        self.assertEqual(saved.read_text(encoding="utf-8"),before)
    def test_output_traversal_refused(self):
        with self.assertRaises(ValueError):
            cs.atomic(self.ws/"../outside.json",{},self.ws)
        self.assertFalse((self.root/"outside.json").exists())
    def test_junction_or_symlink_output_refused(self):
        outside=self.root/"outside";outside.mkdir()
        link=self.ws/"linked"
        try: os.symlink(outside,link,target_is_directory=True)
        except OSError: self.skipTest("symlinks unavailable")
        with self.assertRaises(ValueError):
            cs.atomic(link/"payload.json",{},self.ws)
        self.assertFalse((outside/"payload.json").exists())
    def test_topology_rejects_missing_endpoint(self):
        (self.base/"topology.json").write_text(json.dumps({"root":{"id":"sys"},"edges":[{"source":"sys","target":"missing"}]}))
        self.call("render-topology","demo",expected=2)
        self.assertFalse((self.base/"TOPOLOGY.html").exists())
    def test_topology_injection_remains_json_data(self):
        evil="</script><script>alert(1)</script>"
        (self.base/"topology.json").write_text(json.dumps({"root":{"id":"sys","name":evil},"edges":[]}))
        self.call("render-topology","demo")
        out=(self.base/"TOPOLOGY.html").read_text(encoding="utf-8")
        self.assertNotIn(evil,out)
        self.assertIn("\\u003c/script",out)


class RuleRendererHonesty(unittest.TestCase):
    def test_renderer_does_not_claim_a_second_agent_without_evidence(self):
        import render_rules
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder)/"analysis/demo";base.mkdir(parents=True)
            (base/"rules_result.json").write_text(json.dumps({"confirmedRules":[],"coverageGaps":["independent review unavailable"]}),encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                code=render_rules.main(["render_rules.py","demo","--workspace",folder])
            self.assertEqual(code,0)
            text=(base/"BUSINESS_RULES.md").read_text(encoding="utf-8")
            self.assertNotIn("checked by a second agent",text)
            self.assertIn("Independent review is not established",text)
            self.assertIn("independent review unavailable",text)

if __name__=="__main__": unittest.main()
