#!/usr/bin/env python3
"""Codex local state, source mapping and report helpers. No network or model calls."""
import argparse, datetime, json, os, re, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
from codex_support import adir, atomic, digest, hash_source_check, input_hash, inside, read_json, safe_output, source_root, tree_hashes, valid_name

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def state_file(ws, system):
    return adir(ws,system)/"STATE.json"

def read_state(ws, system):
    return read_json(state_file(ws,system))

def init(a):
    ws=Path(a.workspace).resolve()
    src=Path(a.source).resolve()
    base=adir(ws,a.system)
    if not src.is_dir() or src==Path(src.anchor) or src==Path.home():
        raise ValueError("source must be a scoped existing directory")
    for out in (ws/"analysis",ws/"modernized"):
        if inside(out,src) or inside(src,out):
            raise ValueError("source and output trees overlap; use a separate workspace")
    if base.exists():
        raise ValueError("analysis already exists; use status, do not reset evidence")
    hashes=tree_hashes(src)
    if not hashes["files"]:
        raise ValueError("source contains no readable regular files")
    atomic(base/"CONFIG.json",{"schema":1,"system":a.system,"source":str(src),"track":a.track,"target":a.target,"panel":"manual","xray":"manual","telemetry":False,"created":stamp()},ws)
    atomic(base/"SOURCE_HASHES.json",dict(hashes,root=str(src),created=stamp()),ws)
    atomic(base/"STATE.json",{"schema":1,"tasks":{},"approvals":[],"created":stamp()},ws)
    atomic(base/"INTENT.md","# Intent\n\nGoal: "+a.track+"\nTarget: "+(a.target or "待确认")+"\nSource: "+str(src)+"\n\nScope, constraints and human answers: 待确认。No approval is inferred.\n",ws)
    print(json.dumps({"system":a.system,"files":len(hashes["files"]),"source":str(src),"excluded":hashes["excluded"]},ensure_ascii=False))

def checkpoint(a):
    ws=Path(a.workspace).resolve()
    base=adir(ws,a.system)
    if not base.is_dir():
        raise ValueError("system not initialized")
    snap=base/"history"/datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    safe_output(snap,ws).mkdir(parents=True,exist_ok=False)
    count=0
    for p in base.iterdir():
        if p.is_file():
            safe_output(p,ws)
            shutil.copy2(p,snap/p.name)
            count+=1
    print(json.dumps({"checkpoint":str(snap),"files":count}))

def task(a):
    ws=Path(a.workspace).resolve()
    state=read_state(ws,a.system)
    tid=valid_name(a.task_id)
    if a.action=="start":
        previous=state["tasks"].get(tid)
        if previous and previous["status"]=="running":
            raise ValueError("task already running; record failed/interrupted first")
        inputs=a.input or ["source"]
        state["tasks"][tid]={"status":"running","started":stamp(),"inputs":{x:input_hash(ws,a.system,x) for x in inputs}}
    else:
        rec=state["tasks"].get(tid)
        if not rec or rec["status"]!="running":
            raise ValueError("only a running task can finish")
        if a.action=="done":
            if not a.result:
                raise ValueError("done requires a result file")
            result=safe_output(ws/a.result,ws)
            if not result.is_file() or result.stat().st_size==0:
                raise ValueError("result missing/empty")
            if any(input_hash(ws,a.system,k)!=v for k,v in rec["inputs"].items()):
                raise ValueError("inputs changed during task")
            rec.update(result=a.result,resultSha256=digest(result))
        rec.update(status=a.action,finished=stamp(),note=a.note or "")
    atomic(state_file(ws,a.system),state,ws)
    print(json.dumps(state["tasks"][tid],ensure_ascii=False))

def status(a):
    ws=Path(a.workspace).resolve()
    state=read_state(ws,a.system)
    rows={}
    for tid,rec in state["tasks"].items():
        row=dict(rec)
        if row["status"]=="done":
            try:
                stale=any(input_hash(ws,a.system,k)!=v for k,v in rec["inputs"].items()) or digest(safe_output(ws/rec["result"],ws))!=rec["resultSha256"]
            except (OSError,ValueError):
                stale=True
            if stale:
                row["status"]="stale"
        rows[tid]=row
    print(json.dumps({"system":a.system,"tasks":rows,"source":hash_source_check(ws,a.system),"approvals":state["approvals"],"note":"File-state evidence only; not a business verification verdict."},ensure_ascii=False,indent=2))

def approval(a):
    ws=Path(a.workspace).resolve()
    state=read_state(ws,a.system)
    plan=safe_output(ws/a.plan,ws)
    if not a.human_message.strip() or not a.evidence.strip():
        raise ValueError("approval requires actual human message and source reference")
    rec={"plan":a.plan,"sha256":digest(plan),"scope":a.scope,"humanMessage":a.human_message,"evidence":a.evidence,"date":stamp(),"sourceHash":input_hash(ws,a.system,"source")}
    rules=adir(ws,a.system)/"BUSINESS_RULES.md"
    rec["rulesSha256"]=digest(rules) if rules.exists() else None
    state["approvals"].append(rec)
    atomic(state_file(ws,a.system),state,ws)
    print("Recorded human decision; this helper does not authenticate identity.")

def gate(a):
    ws=Path(a.workspace).resolve()
    plan=safe_output(ws/a.plan,ws)
    rules=adir(ws,a.system)/"BUSINESS_RULES.md"
    for rec in reversed(read_state(ws,a.system)["approvals"]):
        if rec["plan"]==a.plan and rec["scope"]==a.scope and rec["sha256"]==digest(plan) and rec["sourceHash"]==input_hash(ws,a.system,"source") and rec["rulesSha256"]==(digest(rules) if rules.exists() else None):
            print("Recorded approval matches current plan/source/rules and scope; confirm human evidence in chat.")
            return 0
    print("BLOCKED: no matching current approval")
    return 1

def topology(a):
    ws=Path(a.workspace).resolve()
    base=adir(ws,a.system)
    data=read_json(base/"topology.json")
    if not isinstance(data,dict) or not isinstance(data.get("root"),dict):
        raise ValueError("topology requires a root")
    nodes=set()
    def walk(n):
        if not isinstance(n,dict) or not isinstance(n.get("id"),str) or n["id"] in nodes:
            raise ValueError("invalid/duplicate node")
        nodes.add(n["id"])
        for child in n.get("children",[]): walk(child)
    walk(data["root"])
    for e in data.get("edges",[]):
        if e.get("source") not in nodes or e.get("target") not in nodes:
            raise ValueError("edge references missing node")
    raw=json.dumps(data,ensure_ascii=True).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    template=(Path(__file__).resolve().parent.parent/"assets/topology-viewer.html").read_text(encoding="utf-8")
    marker=re.search(r"/\*__TOPOLOGY_DATA__\*/\s*\{.*?\}\s*;?",template,re.S)
    # Upstream uses an exact placeholder; refuse a changed template instead of replacing arbitrary code.
    start=template.find("/*__TOPOLOGY_DATA__*/")
    if start<0:
        raise ValueError("topology template marker missing")
    tail=template[start:]
    match=re.match(r"/\*__TOPOLOGY_DATA__\*/\s*(?:null|\{\})",tail)
    if not match:
        raise ValueError("topology template marker shape changed; inspect template")
    html=template[:start]+"/*__TOPOLOGY_DATA__*/ "+raw+tail[match.end():]
    atomic(base/"TOPOLOGY.html",html,ws)
    print("TOPOLOGY.html generated")

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    subs=ap.add_subparsers(dest="cmd",required=True)
    for name in ["init","checkpoint","status","task","record-approval","gate","render-topology"]:
        p=subs.add_parser(name)
        p.add_argument("system",type=valid_name)
        p.add_argument("--workspace",default=".")
        if name=="init":
            p.add_argument("--source",required=True)
            p.add_argument("--track",choices=["understand","uplift","transform","reimagine"],default="understand")
            p.add_argument("--target",default="")
        if name=="task":
            p.add_argument("action",choices=["start","done","failed"])
            p.add_argument("task_id")
            p.add_argument("--input",action="append")
            p.add_argument("--result")
            p.add_argument("--note")
        if name in ("record-approval","gate"):
            p.add_argument("--plan",required=True)
            p.add_argument("--scope",required=True)
        if name=="record-approval":
            p.add_argument("--human-message",required=True)
            p.add_argument("--evidence",required=True)
    a=ap.parse_args(argv)
    try:
        result={"init":init,"checkpoint":checkpoint,"status":status,"task":task,"record-approval":approval,"gate":gate,"render-topology":topology}[a.cmd](a)
        return result or 0
    except (OSError,ValueError,KeyError,TypeError) as e:
        print(type(e).__name__+": "+str(e),file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
