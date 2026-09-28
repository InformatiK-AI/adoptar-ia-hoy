"""Run the layout audit on deck/index.html at several viewport sizes.

Usage: python deck/tools/run_audit.py            -> summary + exit code 1 if any issue
       python deck/tools/run_audit.py --json     -> full JSON per viewport
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile

DECK = pathlib.Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VIEWPORTS = [(1920, 1080), (1600, 900), (1440, 900), (1366, 768), (1280, 800), (1024, 768)]


def main() -> int:
    src = (DECK / "index.html").read_text(encoding="utf-8")
    audit = (DECK / "tools" / "audit.js").read_text(encoding="utf-8")
    page = src.replace("</body>", "<script>" + audit + "</script></body>")
    tmp = DECK / "_audit.html"  # same folder so media/ resolves
    tmp.write_text(page, encoding="utf-8")
    total = 0
    results = {}
    try:
        for w, h in VIEWPORTS:
            out = subprocess.run(
                [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                 f"--window-size={w},{h}", "--virtual-time-budget=8000", "--dump-dom",
                 tmp.as_uri()],
                capture_output=True, text=True, encoding="utf-8", timeout=120)
            m = list(re.finditer(r"<pre id=\"__audit\">({.*?)</pre>", out.stdout, re.S))
            m = m[-1] if m else None
            if not m:
                print(f"{w}x{h}: audit did not run")
                total += 1
                continue
            data = json.loads(html.unescape(m.group(1)))
            results[f"{w}x{h}"] = data
            total += len(data["issues"])
    finally:
        tmp.unlink(missing_ok=True)

    if "--json" in sys.argv:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for vp, data in results.items():
            print(f"{vp}: {len(data['issues'])} issues ({data['slides']} slides)")
            for i in data["issues"]:
                print("   ", json.dumps(i, ensure_ascii=False))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
