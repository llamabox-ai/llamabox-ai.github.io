import json
from pathlib import Path

p = Path(r"D:/coding/llamabox-ai.github.io/assets/hero-video/session.log")
ev = []
for l in p.read_text(encoding="utf-8").splitlines():
    l = l.strip()
    if not l:
        continue
    try:
        o = json.loads(l)
    except json.JSONDecodeError:
        continue
    for e in o.get("batch") or [o]:
        ev.append(e)

sid = "s_ms5so5av_j3a2vy"
s = [e for e in ev if e.get("session") == sid]
print("n", len(s), "first_t", s[0].get("t") if s else None, "last_t", s[-1].get("t") if s else None)
for e in s[:40]:
    print(
        e.get("t"),
        e.get("type"),
        e.get("mode"),
        "p",
        e.get("p"),
        "vp",
        e.get("vp"),
        "fr",
        e.get("frame"),
        "y",
        e.get("scrollY"),
        e.get("msg"),
        e.get("extra") or e.get("perf"),
    )
print("--- key ---")
for e in s:
    if e.get("type") in (
        "input_wheel",
        "auto_request",
        "auto_start",
        "auto_complete",
        "disturb",
        "disturb_ignored",
        "mode",
        "boot",
        "load_complete",
    ):
        print(e.get("t"), e.get("type"), e.get("mode"), e.get("scrollY"), e.get("extra") or e.get("perf") or e.get("msg"))
