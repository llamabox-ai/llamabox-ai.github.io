/**
 * Canvas frame-sequence hero + first-scroll autoplay.
 * Gesture-coalesced input (mouse/trackpad/touch multi-events = one human scroll).
 * Reverse scrub after auto: park at end of tall track, scroll up to close the box.
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
  var DISTURB_GRACE_MS = 500;
  var GESTURE_GAP_MS = 200;

  var frames = new Array(FRAME_COUNT);
  var loaded = 0;
  var lastFrameIdx = -1;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);

  /** @type {'waiting'|'auto'|'free'} */
  var autoMode = "waiting";
  var autoRaf = null;
  var autoToken = 0;
  var autoStartPerf = 0;
  var virtualP = 0;

  var touchStartY = 0;
  var lastScrollY = window.pageYOffset;
  var lastMove = performance.now();
  var idle = false;
  var holdEndFrame = false;

  var lastInputTime = 0;
  var gestureId = 0;
  var autoStartGestureId = -1;

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

  function filmProgress() {
    if (autoMode === "auto") return virtualP;
    if (holdEndFrame) {
      var sp = scrollProgress();
      var y = window.pageYOffset;
      var endY = heroEndScrollY();
      if (sp >= 0.97 || y >= endY - 8) {
        holdEndFrame = false;
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

      if (ok || tries >= 16) {
        holdEndFrame = false;
        paint(Math.max(scrollProgress(), ok ? 1 : scrollProgress()));
        if (!ok && y < 24) {
          holdEndFrame = true;
          paint(1);
        }
        return;
      }
      requestAnimationFrame(settle);
    }
    requestAnimationFrame(settle);
  }

  function setCinematic(on) {
    document.body.classList.toggle("is-hero-cinematic", on);
  }

  function setPhase(p) {
    section.classList.toggle("is-mid", p > 0.08 && p < 0.88);
    section.classList.toggle("is-end", p >= 0.88);
    if (p <= 0.08) section.classList.remove("is-mid", "is-end");
    var pastHero = section.getBoundingClientRect().bottom <= window.innerHeight * 0.55;
    if (autoMode === "auto") setCinematic(true);
    else setCinematic(!pastHero && p < 0.92 && !reduce);
  }

  function setIdle(on) {
    if (idle === on) return;
    idle = on;
    section.classList.toggle("is-idle", on);
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
      drawFrame(idx);
    }
    if (bar) bar.style.width = (p * 100).toFixed(2) + "%";
    setPhase(p);
  }

  function cancelAuto() {
    if (autoRaf != null) {
      cancelAnimationFrame(autoRaf);
      autoRaf = null;
    }
    autoToken++;
    section.classList.remove("is-autoplaying");
  }

  function noteGesture() {
    var now = performance.now();
    if (now - lastInputTime > GESTURE_GAP_MS) {
      gestureId++;
    }
    lastInputTime = now;
    return gestureId;
  }

  function disturb(gId) {
    if (autoMode !== "auto") return;
    var age = performance.now() - autoStartPerf;
    if (gId != null && gId === autoStartGestureId) return;
    if (age < DISTURB_GRACE_MS) return;

    cancelAuto();
    autoMode = "free";
    setIdle(false);
    forceScrollTop(virtualP * heroEndScrollY());
  }

  function atTopForAuto() {
    return window.pageYOffset < 24 && scrollProgress() < 0.03;
  }

  function startAutoScroll() {
    if (autoMode !== "waiting" || reduce) return;
    if (!atTopForAuto()) {
      autoMode = "free";
      return;
    }

    autoMode = "auto";
    virtualP = 0;
    autoStartPerf = performance.now();
    autoStartGestureId = gestureId;
    section.classList.add("is-autoplaying");
    setIdle(false);
    cancelAuto();
    autoToken++;
    var token = autoToken;
    var startT = performance.now();

    forceScrollTop(0);

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
      }
    }
    autoRaf = requestAnimationFrame(step);
  }

  function tick(now) {
    if (autoMode !== "auto") {
      paint(filmProgress());

      var y = window.pageYOffset;
      if (Math.abs(y - lastScrollY) > 0.5) {
        lastScrollY = y;
        lastMove = now;
        setIdle(false);
      } else if (
        filmProgress() < 0.9 &&
        now - lastMove > 1000 &&
        document.body.classList.contains("is-hero-cinematic")
      ) {
        setIdle(true);
      }

      if (autoMode === "free" && !holdEndFrame && atTopForAuto()) {
        autoMode = "waiting";
        virtualP = 0;
      }
    }
    requestAnimationFrame(tick);
  }

  function loadFrames() {
    var i = 0;
    var concurrency = 12;

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
          }
          if (i < FRAME_COUNT) worker();
        });
    }
    for (var w = 0; w < concurrency; w++) worker();
  }

  if (!reduce) setCinematic(true);
  if (reduce) {
    section.classList.add("is-end");
    setCinematic(false);
    return;
  }

  loadFrames();
  requestAnimationFrame(tick);

  window.addEventListener(
    "wheel",
    function (e) {
      var g = noteGesture();

      if (autoMode === "auto") {
        e.preventDefault();
        disturb(g);
        return;
      }

      if (autoMode === "waiting" && atTopForAuto() && e.deltaY > 0) {
        e.preventDefault();
        startAutoScroll();
      }
    },
    { passive: false }
  );

  window.addEventListener(
    "touchstart",
    function (e) {
      if (e.touches && e.touches[0]) touchStartY = e.touches[0].clientY;
      noteGesture();
    },
    { passive: true }
  );

  window.addEventListener(
    "touchmove",
    function (e) {
      if (!e.touches || !e.touches[0]) return;
      var dy = touchStartY - e.touches[0].clientY;
      var g = noteGesture();

      if (autoMode === "waiting" && atTopForAuto() && dy > 10) {
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") {
        disturb(g);
      }
    },
    { passive: true }
  );

  window.addEventListener(
    "keydown",
    function (e) {
      if (e.key === "Escape" && autoMode === "auto") {
        e.preventDefault();
        lastInputTime = 0;
        disturb(noteGesture());
        return;
      }
      var down =
        e.key === "ArrowDown" ||
        e.key === "PageDown" ||
        e.key === " " ||
        e.key === "Spacebar";
      if (!down && e.key !== "ArrowUp" && e.key !== "PageUp") return;

      var g = noteGesture();

      if (autoMode === "waiting" && atTopForAuto() && down) {
        e.preventDefault();
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") {
        e.preventDefault();
        disturb(g);
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
})();
