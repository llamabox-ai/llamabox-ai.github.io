import json
from collections import defaultdict
from pathlib import Path

p = Path(r"D:/coding/llamabox-ai.github.io/assets/hero-video/session.log")
print("size", p.stat().st_size)
events = []
for line in p.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    batch = o.get("batch") or [o]
    for e in batch:
        e["_server"] = o.get("server_ts")
        events.append(e)
print("events", len(events))

sess = defaultdict(list)
for e in events:
    sess[e.get("session", "?")].append(e)

best = None
for sid, evs in sess.items():
    types = {x.get("type") for x in evs}
    score = len(evs)
    if "auto_start" in types:
        score += 1000
    if "auto_complete" in types:
        score += 5000
    if "input_wheel" in types:
        score += 200
    if best is None or score > best[0]:
        best = (score, sid, evs)

print("best session", best[1], "score", best[0], "n", len(best[2]))
evs = best[2]
keys = {
    "boot",
    "load_complete",
    "first_frame_ready",
    "input_wheel",
    "auto_request",
    "auto_start",
    "auto_complete",
    "auto_cancel",
    "disturb",
    "disturb_ignored",
    "mode",
    "phase",
    "cinematic",
    "idle",
    "unload",
}
for e in evs:
    t = e.get("type")
    fr = e.get("frame")
    pval = e.get("p")
    interesting = t in keys or (
        t == "paint" and fr in (0, 1, 36, 72, 108, 143)
    ) or (t == "scroll" and pval is not None and (pval == 0 or pval > 0.9))
    if not interesting:
        continue
    print(
        f"t={e.get('t'):>6} {t:18} mode={str(e.get('mode')):8} "
        f"p={e.get('p')} vp={e.get('vp')} fr={e.get('frame')} y={e.get('scrollY')} "
        f"msg={e.get('msg')} extra={e.get('extra')} perf={e.get('perf')}"
    )

types = defaultdict(int)
for e in evs:
    types[e.get("type")] += 1
print("--- counts ---")
for k, v in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("--- mode transitions ---")
prev = None
for e in evs:
    m = e.get("mode")
    if m != prev:
        print(f"  t={e.get('t')} type={e.get('type')} mode {prev} -> {m}")
        prev = m

acs = [e for e in evs if e.get("type") == "auto_complete"]
ads = [e for e in evs if e.get("type") == "disturb"]
ais = [e for e in evs if e.get("type") == "auto_start"]
dis_ign = [e for e in evs if e.get("type") == "disturb_ignored"]
print("auto_starts", len(ais), "auto_completes", len(acs), "disturbs", len(ads), "ignored", len(dis_ign))
if acs:
    print("complete", json.dumps(acs[-1], indent=2))
if ads:
    print("disturb", json.dumps(ads, indent=2))
if dis_ign:
    print("disturb_ignored sample", json.dumps(dis_ign[:5], indent=2))

auto_frames = [e.get("frame") for e in evs if e.get("mode") == "auto" and e.get("frame") is not None]
print(
    "auto frame min/max",
    (min(auto_frames) if auto_frames else None),
    (max(auto_frames) if auto_frames else None),
)
wheels = [e for e in evs if e.get("type") == "input_wheel"]
print("wheels", len(wheels))
for w in wheels[:20]:
    print("  wheel", w.get("t"), w.get("extra"), "mode", w.get("mode"), "y", w.get("scrollY"), "vp", w.get("vp"))
