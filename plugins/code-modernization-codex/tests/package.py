"""Build fresh versioned archives and verify archive contents (no installation)."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, zipfile
HERE=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    out=Path(a.out).resolve()
    if out.exists(): raise SystemExit("Output must be a new directory")
    out.mkdir(parents=True)
    manifest=json.loads((HERE/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"]=="code-modernization-codex" and manifest["version"]=="1.1.0"
    assert len(list((HERE/"skills").glob("*/SKILL.md")))==13
    for key in ("composerIcon","logo"):
        assert (HERE/manifest["interface"][key]).is_file()
    assert not (HERE/"hooks").exists()
    assert not (HERE/"scripts/telemetry.py").exists()
    marketplace={"name":"cz007-code-modernization","interface":{"displayName":"cz007 Code Modernization"},"plugins":[{"name":"code-modernization-codex","source":{"source":"local","path":"./plugins/code-modernization-codex"},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"Developer Tools"}]}
    names=["CodeModernization_Codex_Plugin_V1.1.0_20261020.zip","CodeModernization_Codex_LocalMarketplace_V1.1.0_20261020.zip"]
    listing=[]
    for name in names:
        market="LocalMarketplace" in name
        prefix="plugins/code-modernization-codex/" if market else ""
        target=out/name
        with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as z:
            for p in files(HERE):
                z.write(p,prefix+p.relative_to(HERE).as_posix())
            if market:
                z.writestr(".agents/plugins/marketplace.json",json.dumps(marketplace,indent=2))
        with zipfile.ZipFile(target) as z:
            assert z.testzip() is None
            for n in z.namelist():
                assert not Path(n).is_absolute() and ".." not in Path(n).parts
            for p in files(HERE):
                assert hashlib.sha256(z.read(prefix+p.relative_to(HERE).as_posix())).hexdigest()==sha(p)
            count=len(z.namelist())
        listing.append({"name":name,"sha256":sha(target),"bytes":target.stat().st_size,"entries":count})
    (out/"SHA256SUMS.txt").write_text("".join(x["sha256"]+"  "+x["name"]+"\n" for x in listing),encoding="utf-8")
    (out/"PACKAGE_VERIFICATION.json").write_text(json.dumps({"version":"1.1.0","archives":listing,"archiveIntegrity":"passed","manifestAndResources":"passed","hostInstallation":"not performed"},indent=2),encoding="utf-8")
    print(json.dumps(listing,indent=2))
if __name__=="__main__":main()
