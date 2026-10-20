"""Codex adaptation helpers by cz007, 2026-10-20. Apache-2.0."""
from pathlib import Path
import hashlib, json, os, re, tempfile

def valid_name(name):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        raise ValueError("system/task must be a plain name")
    return name

def inside(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False

def safe_output(path, root):
    path, root = Path(path).absolute(), Path(root).resolve()
    if not inside(path, root):
        raise ValueError("output leaves workspace")
    # Refuse links/junctions in every existing component, not just the leaf.
    current = path
    while current != root and current != current.parent:
        if current.exists() or current.is_symlink():
            st = current.lstat()
            if current.is_symlink() or getattr(st, "st_file_attributes", 0) & 0x400:
                raise ValueError("output contains symlink/reparse point")
        current = current.parent
    return path

def atomic(path, value, root):
    path = safe_output(path, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=".codex-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(raw)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def read_json(path):
    path = Path(path)
    if path.stat().st_size > 16*1024*1024:
        raise ValueError("JSON too large")
    return json.loads(path.read_text(encoding="utf-8-sig"))

def adir(workspace, system):
    return Path(workspace).resolve() / "analysis" / valid_name(system)

def source_root(workspace, system):
    cfg = adir(workspace, system) / "CONFIG.json"
    if cfg.exists():
        config = read_json(cfg)
        p = Path(config["source"]).resolve()
        if not p.is_dir() or p == Path(p.anchor) or p == Path.home():
            raise ValueError("configured source is unavailable or too broad")
        return p
    return Path(workspace).resolve() / "legacy" / valid_name(system)

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def tree_hashes(root):
    root = Path(root).resolve()
    files, excluded = {}, []
    def onerror(error):
        raise error
    for base, dirs, names in os.walk(root, followlinks=False, onerror=onerror):
        for d in list(dirs):
            p = Path(base)/d
            if d == ".git":
                dirs.remove(d)
                continue
            if p.is_symlink() or getattr(p.lstat(), "st_file_attributes", 0) & 0x400:
                excluded.append(str(p.relative_to(root)))
                dirs.remove(d)
        for n in sorted(names):
            p = Path(base)/n
            rel = p.relative_to(root).as_posix()
            if p.is_symlink() or getattr(p.lstat(), "st_file_attributes", 0) & 0x400:
                excluded.append(rel)
                continue
            files[rel] = digest(p)
            if len(files) > 100000:
                raise ValueError("source exceeds 100000 files; scope to one module")
    return {"files": files, "excluded": sorted(excluded)}

def hash_source_check(workspace, system):
    base = adir(workspace, system)
    baseline = base/"SOURCE_HASHES.json"
    if not baseline.exists():
        if (base/"CONFIG.json").exists():
            return {"state":"unknown","method":"SHA-256","detail":"source hash baseline missing","files":[],"path":"configured source","target":""}
        return None
    out = {"state":"unknown","method":"SHA-256","detail":"","files":[],"path":"configured source","target":""}
    try:
        old = read_json(baseline)
        src = source_root(workspace,system)
        out["target"] = str(src)
        new = tree_hashes(src)
        if str(src) != old["root"]:
            raise ValueError("source mapping differs from baseline")
        changed = sorted(k for k in set(old["files"]) | set(new["files"]) if old["files"].get(k) != new["files"].get(k))
        out["files"] = changed[:40]
        out["state"] = "changed" if changed else ("unknown" if old.get("excluded") or new["excluded"] else "clean")
        out["detail"] = "%d changed/added/deleted files; %d excluded links; SHA-256 compared" % (len(changed),len(new["excluded"]))
    except (OSError,ValueError,KeyError,TypeError) as e:
        out["detail"] = "source could not be checked: " + type(e).__name__
    return out

def input_hash(workspace, system, value):
    if value == "source":
        raw = json.dumps(tree_hashes(source_root(workspace,system)),sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()
    p = safe_output(Path(workspace)/value,workspace)
    return digest(p)
