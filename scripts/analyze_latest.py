"""Analyze latest session for pass/fail of auto film."""
import json
from collections import defaultdict
from pathlib import Path

p = Path(r"D:/coding/llamabox-ai.github.io/assets/hero-video/session.log")
if not p.exists() or p.stat().st_size == 0:
    print("EMPTY_LOG")
    raise SystemExit(0)

ev = []
for line in p.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    for e in o.get("batch") or [o]:
        ev.append(e)

sess = defaultdict(list)
for e in ev:
    sess[e.get("session", "?")].append(e)

best = None
for sid, evs in sess.items():
    types = {x.get("type") for x in evs}
    score = len(evs)
    if "auto_complete" in types:
        score += 10000
    if "auto_start" in types or "auto_request" in types:
        score += 1000
    if "input_wheel" in types:
        score += 100
    if best is None or score > best[0]:
        best = (score, sid, evs)

sid, evs = best[1], best[2]
print("=" * 60)
print("SESSION", sid, "events", len(evs))
print("=" * 60)

def show(e):
    print(
        f"  t={e.get('t'):>6} {e.get('type'):20} mode={e.get('mode'):8} "
        f"p={e.get('p')} vp={e.get('vp')} fr={e.get('frame')} y={e.get('scrollY')} "
        f"{e.get('msg') or ''} {e.get('extra') or e.get('perf') or ''}"
    )

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
    "film_layout_done",
    "jump_past_hero",
    "jump_past_hero_after",
    "jump_past_hero_final",
    "hold_release",
    "mode",
    "cinematic",
}
print("\nKEY EVENTS:")
for e in evs:
    if e.get("type") in keys or (
        e.get("type") == "paint"
        and e.get("mode") == "auto"
        and e.get("frame") in (0, 1, 36, 72, 108, 143)
    ):
        show(e)

acs = [e for e in evs if e.get("type") == "auto_complete"]
starts = [e for e in evs if e.get("type") == "auto_start"]
dist = [e for e in evs if e.get("type") == "disturb"]
layout = [e for e in evs if e.get("type") == "film_layout_done"]
resets = [e for e in evs if e.get("type") == "mode" and e.get("msg") == "reset_waiting"]

print("\nVERDICT:")
ok_start = len(starts) >= 1 or any(e.get("mode") == "auto" for e in evs)
ok_complete = len(acs) >= 1
ok_full = False
if acs:
    fr = acs[-1].get("frame")
    ok_full = fr is not None and fr >= 140
ok_no_early_disturb = len(dist) == 0 or (
    starts and dist and dist[0].get("t", 0) > starts[0].get("t", 0) + 3500
)
# After complete, should NOT immediately paint frame 0
snap_back = False
if acs:
    t_done = acs[-1].get("t", 0)
    for e in evs:
        if e.get("t", 0) <= t_done:
            continue
        if e.get("t", 0) > t_done + 200:
            break
        if e.get("type") == "paint" and (e.get("frame") or 0) < 5:
            snap_back = True
        if e.get("type") == "mode" and e.get("msg") == "reset_waiting":
            snap_back = True

layout_ok = False
if layout:
    extra = layout[-1].get("extra") or {}
    layout_ok = bool(extra.get("isDone")) and extra.get("sectionH", 9999) <= 1200
elif acs:
    perf = acs[-1].get("perf") or {}
    layout_ok = bool(perf.get("doneClass")) or (perf.get("sectionH") or 9999) <= 1200

print(f"  auto started:     {ok_start}")
print(f"  auto completed:   {ok_complete}")
print(f"  full frames(~143):{ok_full}  complete_frame={acs[-1].get('frame') if acs else None}")
print(f"  no early disturb: {ok_no_early_disturb}  disturbs={len(dist)}")
print(f"  no snap-back:     {not snap_back}")
print(f"  layout collapsed: {layout_ok}  layout_events={len(layout)}")
if acs:
    print(f"  complete perf:    {acs[-1].get('perf')}")
if layout:
    print(f"  layout:           {layout[-1].get('extra')}")

passed = ok_start and ok_complete and ok_full and not snap_back
print("\n" + ("PASS" if passed else "FAIL"))
