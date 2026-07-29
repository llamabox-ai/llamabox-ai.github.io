/**
 * Canvas frame-sequence hero + first-scroll autoplay.
 *
 * FIXES from session logs (s_ms5slb4n / s_ms5slkze):
 * - window.scrollTo during auto did NOT move scrollY (stuck ~41) while frames
 *   advanced on a separate eased p → desync. Auto now uses a VIRTUAL timeline
 *   (time → progress → frame) and only snaps scroll when complete.
 * - Trackpad reverse deltaY immediately "disturb"ed auto at p≈1.5%.
 *   Grace period + ignore tiny/opposite inertia; Escape or deliberate wheel after grace takes over.
 */
(function () {
  var section = document.getElementById("scrollHero");
  var canvas = document.getElementById("heroCanvas");
  var bar = document.getElementById("heroProgress");
  if (!section || !canvas) return;

  var ctx = canvas.getContext("2d", { alpha: false, desynchronized: true });
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var FRAME_COUNT = 144;
  var SEQ_PREFIX = "assets/hero-video/seq/f_";
  var SEQ_PAD = 4;
  var SEQ_EXT = ".jpg";
  var AUTO_MS = 4000;
  /** Ignore take-over attempts for this long after auto starts (trackpad burst) */
  var DISTURB_GRACE_MS = 500;
  /**
   * Human "one scroll" = many wheel/touchmove events. Events closer than this
   * gap are the SAME gesture (mouse wheel ticks, trackpad inertia, finger fling).
   */
  var GESTURE_GAP_MS = 200;

  var frames = new Array(FRAME_COUNT);
  var loaded = 0;
  var lastFrameIdx = -1;
  var paintCount = 0;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);

  /** @type {'waiting'|'auto'|'free'} */
  var autoMode = "waiting";
  var autoRaf = null;
  var autoToken = 0;
  var autoStartPerf = 0;
  var virtualP = 0; // 0..1 driven by auto timeline

  var touchStartY = 0;
  var lastScrollY = window.pageYOffset;
  var lastMove = performance.now();
  var idle = false;
  /** After auto finishes, keep last frame until page has actually scrolled past the film */
  var holdEndFrame = false;

  // Gesture coalescing — one human scroll ≠ one event
  var lastInputTime = 0;
  var gestureId = 0;
  var autoStartGestureId = -1;
  var touchGestureId = -1;

  var sessionId = "s_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
  var t0 = performance.now();
  var logQueue = [];
  var logFlushTimer = null;
  var eventSeq = 0;
  var lastLoggedP = -1;

  function nowMs() {
    return Math.round(performance.now() - t0);
  }

  function log(type, data) {
    data = data || {};
    var entry = {
      seq: ++eventSeq,
      t: nowMs(),
      type: type,
      session: sessionId,
      mode: autoMode,
      scrollY: Math.round(window.pageYOffset * 10) / 10,
      p: data.p != null ? Math.round(data.p * 10000) / 10000 : undefined,
      vp: Math.round(virtualP * 10000) / 10000,
      frame: data.frame != null ? data.frame : lastFrameIdx,
      msg: data.msg,
      extra: data.extra,
      perf: data.perf,
    };
    Object.keys(entry).forEach(function (k) {
      if (entry[k] === undefined) delete entry[k];
    });
    try {
      console.log("[LB]", entry.t + "ms", type, entry);
    } catch (e) {}
    logQueue.push(entry);
    if (!logFlushTimer) logFlushTimer = setTimeout(flushLogs, 32);
    var hud = document.getElementById("lbDebugHud");
    if (hud) {
      hud.textContent =
        "#" +
        entry.seq +
        " " +
        type +
        " @" +
        entry.t +
        "ms\nmode=" +
        autoMode +
        " vp=" +
        (entry.vp != null ? entry.vp : "-") +
        " fr=" +
        entry.frame +
        " y=" +
        entry.scrollY +
        " L=" +
        loaded +
        "/" +
        FRAME_COUNT;
    }
  }

  function flushLogs() {
    logFlushTimer = null;
    if (!logQueue.length) return;
    var batch = logQueue.splice(0, logQueue.length);
    try {
      var prev = JSON.parse(localStorage.getItem("lb_hero_log") || "[]");
      localStorage.setItem("lb_hero_log", JSON.stringify(prev.concat(batch).slice(-600)));
    } catch (e) {}
    if (location.hostname === "127.0.0.1" || location.hostname === "localhost") {
      fetch("/__log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ batch: batch }),
        keepalive: true,
      }).catch(function () {});
    }
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }
  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
  function pad(n) {
    var s = String(n);
    while (s.length < SEQ_PAD) s = "0" + s;
    return s;
  }
  function frameUrl(i) {
    return SEQ_PREFIX + pad(i + 1) + SEQ_EXT;
  }

  function scrollProgress() {
    var rect = section.getBoundingClientRect();
    var total = Math.max(1, section.offsetHeight - window.innerHeight);
    return clamp(-rect.top, 0, total) / total;
  }

  /** Effective film progress: virtual during auto, scroll otherwise */
  function filmProgress() {
    if (autoMode === "auto") return virtualP;
    // Brief hold only until we've landed at end of tall track (allows reverse scrub after)
    if (holdEndFrame) {
      var sp = scrollProgress();
      var y = window.pageYOffset;
      var endY = heroEndScrollY();
      // Released once we're actually at the open-box scroll position
      if (sp >= 0.97 || y >= endY - 8) {
        holdEndFrame = false;
        log("hold_release", { p: sp, extra: { y: y, endY: endY } });
        return sp;
      }
      return 1;
    }
    return scrollProgress();
  }

  function heroEndScrollY() {
    var top = section.getBoundingClientRect().top + window.pageYOffset;
    return Math.max(0, top + section.offsetHeight - window.innerHeight);
  }

  function forceScrollTop(y) {
    y = Math.max(0, Math.round(y));
    var se = document.scrollingElement || document.documentElement;
    try {
      se.scrollTop = y;
    } catch (e) {}
    try {
      document.documentElement.scrollTop = y;
      document.body.scrollTop = y;
    } catch (e2) {}
    try {
      window.scrollTo({ top: y, left: 0, behavior: "instant" });
    } catch (e3) {
      try {
        window.scrollTo(0, y);
      } catch (e4) {}
    }
    return window.pageYOffset || se.scrollTop || 0;
  }

  function finishFilmLayout() {
    // Keep tall track (340vh) so user can scroll BACK UP → reverse film → closed box.
    // Park at end of track = open frame. Prefer scrollIntoView(anchor) over scrollTo
    // (logs: scrollTo alone often left finalY=0).
    section.classList.remove("is-done");
    holdEndFrame = true;
    virtualP = 1;
    paint(1);
    setCinematic(false);

    var anchor = document.getElementById("afterHero");
    var tries = 0;

    function settle() {
      tries++;
      var endY = heroEndScrollY();

      if (anchor && typeof anchor.scrollIntoView === "function") {
        try {
          anchor.scrollIntoView({ block: "start", behavior: "instant", inline: "nearest" });
        } catch (e) {
          try {
            anchor.scrollIntoView(true);
          } catch (e2) {}
        }
      }
      forceScrollTop(endY);

      var y = window.pageYOffset;
      var anchorTop = anchor ? anchor.getBoundingClientRect().top : 9999;
      var ok = y >= endY - 16 || anchorTop < window.innerHeight * 0.2;

      log("film_layout_settle", {
        extra: {
          try: tries,
          y: y,
          endY: endY,
          anchorTop: Math.round(anchorTop),
          ok: ok,
        },
      });

      if (ok || tries >= 16) {
        holdEndFrame = false;
        paint(Math.max(scrollProgress(), ok ? 1 : scrollProgress()));
        // If still stuck at top, keep hold so we at least show open frame
        if (!ok && y < 24) {
          holdEndFrame = true;
          paint(1);
        }
        log("film_layout_done", {
          extra: {
            y: window.pageYOffset,
            endY: endY,
            sectionH: section.offsetHeight,
            hold: holdEndFrame,
            tries: tries,
            ok: ok,
          },
        });
        return;
      }
      requestAnimationFrame(settle);
    }
    requestAnimationFrame(settle);
  }

  function setCinematic(on) {
    var was = document.body.classList.contains("is-hero-cinematic");
    document.body.classList.toggle("is-hero-cinematic", on);
    if (was !== on) log("cinematic", { extra: { on: on } });
  }

  function setPhase(p) {
    section.classList.toggle("is-mid", p > 0.08 && p < 0.88);
    section.classList.toggle("is-end", p >= 0.88);
    if (p <= 0.08) section.classList.remove("is-mid", "is-end");
    var pastHero = section.getBoundingClientRect().bottom <= window.innerHeight * 0.55;
    // Keep cinematic during auto regardless of scroll position
    if (autoMode === "auto") setCinematic(true);
    else setCinematic(!pastHero && p < 0.92 && !reduce);
  }

  function setIdle(on) {
    if (idle === on) return;
    idle = on;
    section.classList.toggle("is-idle", on);
    log("idle", { extra: { on: on } });
  }

  function resizeCanvas() {
    var w = section.clientWidth || window.innerWidth;
    var h = window.innerHeight;
    var bw = Math.round(w * dpr);
    var bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) {
      canvas.width = bw;
      canvas.height = bh;
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      lastFrameIdx = -1;
      log("resize", { extra: { cssW: w, cssH: h, bufW: bw, bufH: bh } });
    }
  }

  function drawFrame(idx) {
    idx = clamp(idx | 0, 0, FRAME_COUNT - 1);
    var img = frames[idx];
    if (!img) return false;
    var cw = canvas.width;
    var ch = canvas.height;
    var iw = img.width || img.naturalWidth || 1280;
    var ih = img.height || img.naturalHeight || 720;
    var scale = Math.max(cw / iw, ch / ih);
    var dw = iw * scale;
    var dh = ih * scale;
    var dx = (cw - dw) * 0.5;
    var dy = (ch - dh) * 0.5;
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, cw, ch);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(img, dx, dy, dw, dh);
    lastFrameIdx = idx;
    paintCount++;
    section.classList.add("is-ready");
    return true;
  }

  function frameIndexFromProgress(p) {
    return clamp(Math.round(p * (FRAME_COUNT - 1)), 0, FRAME_COUNT - 1);
  }

  function paint(p) {
    resizeCanvas();
    var idx = frameIndexFromProgress(p);
    if (idx !== lastFrameIdx || lastFrameIdx < 0) {
      if (drawFrame(idx)) {
        log("paint", { p: p, frame: idx, perf: { paintCount: paintCount } });
      }
    }
    if (bar) bar.style.width = (p * 100).toFixed(2) + "%";
    setPhase(p);
  }

  function cancelAuto(reason) {
    if (autoRaf != null) {
      cancelAnimationFrame(autoRaf);
      autoRaf = null;
    }
    autoToken++;
    section.classList.remove("is-autoplaying");
    if (reason) log("auto_cancel", { msg: reason, p: virtualP, frame: lastFrameIdx });
  }

  /**
   * Mark input and return current gesture id.
   * Continuous wheel ticks / touchmoves within GESTURE_GAP_MS = one gesture.
   */
  function noteGesture(kind) {
    var now = performance.now();
    if (now - lastInputTime > GESTURE_GAP_MS) {
      gestureId++;
      log("gesture_new", {
        msg: kind,
        extra: { gestureId: gestureId, gapMs: Math.round(now - lastInputTime) },
      });
    }
    lastInputTime = now;
    return gestureId;
  }

  function disturb(source, gId) {
    if (autoMode !== "auto") return;
    var age = performance.now() - autoStartPerf;

    // Same gesture that started auto (extra wheel ticks / inertia) — ignore
    if (gId != null && gId === autoStartGestureId) {
      log("disturb_ignored", {
        msg: source,
        extra: { reason: "same_gesture", gestureId: gId, ageMs: Math.round(age) },
        p: virtualP,
      });
      return;
    }
    // Still in grace window after auto start
    if (age < DISTURB_GRACE_MS) {
      log("disturb_ignored", {
        msg: source,
        extra: { reason: "grace", ageMs: Math.round(age), gestureId: gId },
        p: virtualP,
      });
      return;
    }

    cancelAuto("disturb:" + source);
    autoMode = "free";
    setIdle(false);
    var endY = heroEndScrollY();
    forceScrollTop(virtualP * endY);
    log("disturb", {
      msg: source,
      p: virtualP,
      frame: lastFrameIdx,
      extra: { gestureId: gId, ageMs: Math.round(age) },
    });
  }

  function atTopForAuto() {
    return window.pageYOffset < 24 && scrollProgress() < 0.03;
  }

  function startAutoScroll(trigger) {
    log("auto_request", {
      msg: trigger,
      p: scrollProgress(),
      extra: { y: window.pageYOffset, atTop: atTopForAuto() },
    });
    if (autoMode !== "waiting" || reduce) {
      log("auto_reject", { msg: "mode=" + autoMode });
      return;
    }
    if (!atTopForAuto()) {
      // Already scrolled — free scrub only
      autoMode = "free";
      log("auto_reject", { msg: "not_at_top" });
      return;
    }

    autoMode = "auto";
    virtualP = 0;
    autoStartPerf = performance.now();
    // Remember which human gesture started us — more events in this gesture are NOT take-over
    autoStartGestureId = gestureId;
    section.classList.add("is-autoplaying");
    setIdle(false);
    cancelAuto(null);
    autoToken++;
    var token = autoToken;
    var startT = performance.now();

    // Lock scroll at 0 during virtual play so layout doesn't fight
    forceScrollTop(0);

    log("auto_start", {
      extra: {
        trigger: trigger,
        autoMs: AUTO_MS,
        endY: heroEndScrollY(),
        token: token,
        gestureId: autoStartGestureId,
      },
    });

    function step(now) {
      if (token !== autoToken || autoMode !== "auto") return;

      var t = clamp((now - startT) / AUTO_MS, 0, 1);
      virtualP = easeInOutCubic(t);
      paint(virtualP);

      if (t < 1) {
        autoRaf = requestAnimationFrame(step);
      } else {
        autoRaf = null;
        autoMode = "free";
        section.classList.remove("is-autoplaying");
        finishFilmLayout();
        log("auto_complete", {
          p: 1,
          frame: lastFrameIdx,
          perf: {
            elapsedMs: Math.round(now - startT),
            paints: paintCount,
            finalY: window.pageYOffset,
            sectionH: section.offsetHeight,
            hold: holdEndFrame,
            doneClass: section.classList.contains("is-done"),
          },
        });
      }
    }
    autoRaf = requestAnimationFrame(step);
  }

  function tick(now) {
    if (autoMode !== "auto") {
      var p = filmProgress();
      paint(p);

      if (Math.abs(p - lastLoggedP) >= 0.03) {
        lastLoggedP = p;
        log("scroll", { p: p, frame: lastFrameIdx });
      }

      var y = window.pageYOffset;
      if (Math.abs(y - lastScrollY) > 0.5) {
        lastScrollY = y;
        lastMove = now;
        setIdle(false);
      } else if (
        p < 0.9 &&
        now - lastMove > 1000 &&
        document.body.classList.contains("is-hero-cinematic")
      ) {
        setIdle(true);
      }

      // Back at fully closed box → allow first-scroll auto again
      if (autoMode === "free" && !holdEndFrame && atTopForAuto()) {
        autoMode = "waiting";
        virtualP = 0;
        log("mode", { msg: "reset_waiting" });
      }
    }
    requestAnimationFrame(tick);
  }

  function loadFrames() {
    var i = 0;
    var concurrency = 12;
    var t0load = performance.now();
    log("load_start", { extra: { count: FRAME_COUNT } });

    function worker() {
      if (i >= FRAME_COUNT) return;
      var idx = i++;
      var url = frameUrl(idx);
      fetch(url)
        .then(function (r) {
          return r.blob();
        })
        .then(function (blob) {
          if (typeof createImageBitmap === "function") {
            return createImageBitmap(blob).then(function (bmp) {
              frames[idx] = bmp;
            });
          }
          return new Promise(function (resolve, reject) {
            var img = new Image();
            img.onload = function () {
              frames[idx] = img;
              resolve();
            };
            img.onerror = reject;
            img.src = URL.createObjectURL(blob);
          });
        })
        .catch(function () {
          return new Promise(function (resolve) {
            var img = new Image();
            img.onload = function () {
              frames[idx] = img;
              resolve();
            };
            img.onerror = resolve;
            img.src = url;
          });
        })
        .then(function () {
          loaded++;
          if (loaded === 1 && frames[0]) {
            resizeCanvas();
            paint(0);
            log("first_frame_ready", { frame: 0, perf: { ms: Math.round(performance.now() - t0load) } });
          }
          if (loaded === FRAME_COUNT) {
            log("load_complete", { perf: { ms: Math.round(performance.now() - t0load) } });
          }
          if (i < FRAME_COUNT) worker();
        });
    }
    for (var w = 0; w < concurrency; w++) worker();
  }

  (function hud() {
    if (document.getElementById("lbDebugHud")) return;
    var el = document.createElement("div");
    el.id = "lbDebugHud";
    el.setAttribute(
      "style",
      "position:fixed;left:8px;bottom:8px;z-index:99999;max-width:min(440px,92vw);" +
        "padding:8px 10px;border-radius:10px;font:11px/1.35 ui-monospace,Consolas,monospace;" +
        "color:#d1fae5;background:rgba(0,0,0,.75);border:1px solid rgba(52,211,153,.4);" +
        "white-space:pre-wrap;pointer-events:none;"
    );
    document.body.appendChild(el);
  })();

  log("boot", {
    msg: "v10 gesture-coalesce",
    extra: {
      ua: navigator.userAgent.slice(0, 100),
      sectionH: section.offsetHeight,
      endY: heroEndScrollY(),
      autoMs: AUTO_MS,
      gestureGapMs: GESTURE_GAP_MS,
      disturbGraceMs: DISTURB_GRACE_MS,
    },
  });

  if (!reduce) setCinematic(true);
  if (reduce) {
    section.classList.add("is-end");
    setCinematic(false);
    return;
  }

  loadFrames();
  requestAnimationFrame(tick);

  /*
   * Input model:
   * - One human scroll = many wheel / touchmove events (mouse notch, trackpad inertia, finger fling).
   * - First downward gesture from top → start auto film.
   * - All events in THAT same gesture are swallowed (not take-over).
   * - A NEW gesture after grace can take over; Escape always can.
   */
  window.addEventListener(
    "wheel",
    function (e) {
      var g = noteGesture("wheel");
      log("input_wheel", {
        p: filmProgress(),
        extra: {
          deltaY: e.deltaY,
          atTop: atTopForAuto(),
          mode: autoMode,
          gestureId: g,
          startGesture: autoStartGestureId,
        },
      });

      if (autoMode === "auto") {
        // Always block browser scroll during film; multi-tick same gesture is normal
        e.preventDefault();
        disturb("wheel", g);
        return;
      }

      // Net downward intent (allow trackpad noise as long as overall down)
      if (autoMode === "waiting" && atTopForAuto() && e.deltaY > 0) {
        e.preventDefault();
        startAutoScroll("wheel");
      }
    },
    { passive: false }
  );

  window.addEventListener(
    "touchstart",
    function (e) {
      if (e.touches && e.touches[0]) touchStartY = e.touches[0].clientY;
      // New finger contact often starts a new gesture
      touchGestureId = noteGesture("touchstart");
      log("input_touchstart", { extra: { y: touchStartY, gestureId: touchGestureId } });
    },
    { passive: true }
  );

  window.addEventListener(
    "touchmove",
    function (e) {
      if (!e.touches || !e.touches[0]) return;
      var dy = touchStartY - e.touches[0].clientY; // + = scroll down
      var g = noteGesture("touchmove");
      log("input_touchmove", {
        p: filmProgress(),
        extra: { dy: Math.round(dy), gestureId: g, mode: autoMode },
      });

      if (autoMode === "waiting" && atTopForAuto() && dy > 10) {
        startAutoScroll("touch");
        return;
      }
      if (autoMode === "auto") {
        disturb("touch", g);
      }
    },
    { passive: true }
  );

  window.addEventListener(
    "keydown",
    function (e) {
      if (e.key === "Escape" && autoMode === "auto") {
        e.preventDefault();
        // Force new gesture id so Escape always counts as take-over
        lastInputTime = 0;
        var gEsc = noteGesture("escape");
        disturb("escape", gEsc);
        return;
      }
      var down =
        e.key === "ArrowDown" ||
        e.key === "PageDown" ||
        e.key === " " ||
        e.key === "Spacebar";
      if (!down && e.key !== "ArrowUp" && e.key !== "PageUp") return;

      var g = noteGesture("key");
      log("input_key", { msg: e.key, extra: { down: down, gestureId: g, mode: autoMode } });

      if (autoMode === "waiting" && atTopForAuto() && down) {
        e.preventDefault();
        startAutoScroll("key:" + e.key);
        return;
      }
      if (autoMode === "auto") {
        e.preventDefault();
        disturb("key:" + e.key, g);
      }
    },
    { passive: false }
  );

  window.addEventListener(
    "resize",
    function () {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      lastFrameIdx = -1;
      paint(filmProgress());
    },
    { passive: true }
  );

  window.addEventListener("beforeunload", function () {
    log("unload", { perf: { paints: paintCount, loaded: loaded } });
    flushLogs();
  });

  setInterval(function () {
    log("heartbeat", {
      p: filmProgress(),
      frame: lastFrameIdx,
      perf: { paints: paintCount, loaded: loaded },
    });
  }, 2000);
})();
