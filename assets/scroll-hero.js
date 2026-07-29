/**
 * High-refresh scroll hero (60–120Hz via rAF).
 * Scrubs a preloaded frame sequence on canvas — no video.currentTime seeks
 * (those are why it felt inconsistent / low-fps).
 *
 * First scroll from top → auto-scroll through film; disturb → user owns scroll.
 */
(function () {
  var section = document.getElementById("scrollHero");
  var canvas = document.getElementById("heroCanvas");
  var bar = document.getElementById("heroProgress");
  if (!section || !canvas) return;

  var ctx = canvas.getContext("2d", { alpha: false, desynchronized: true });
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var FRAME_COUNT = 144;
  var FPS = 24;
  var SEQ_PREFIX = "assets/hero-video/seq/f_";
  var SEQ_PAD = 4;
  var SEQ_EXT = ".jpg";

  /** @type {(ImageBitmap|HTMLImageElement)[]} */
  var frames = new Array(FRAME_COUNT);
  var loaded = 0;
  var ready = false;
  var lastFrameIdx = -1;

  /** @type {'waiting'|'auto'|'free'} */
  var autoMode = "waiting";
  var autoRaf = null;
  var autoToken = 0;
  var touchStartY = 0;

  var lastScrollY = window.pageYOffset;
  var lastMove = performance.now();
  var idle = false;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);

  // Auto-scroll length (snappy; content still maps full 0→1)
  var AUTO_MS = 4200;

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
    // files are 1-indexed: f_0001.jpg … f_0144.jpg
    return SEQ_PREFIX + pad(i + 1) + SEQ_EXT;
  }

  function progressFromScroll() {
    var rect = section.getBoundingClientRect();
    var total = Math.max(1, section.offsetHeight - window.innerHeight);
    return clamp(-rect.top, 0, total) / total;
  }

  function heroEndScrollY() {
    var top = section.getBoundingClientRect().top + window.pageYOffset;
    return Math.max(0, top + section.offsetHeight - window.innerHeight);
  }

  function setCinematic(on) {
    document.body.classList.toggle("is-hero-cinematic", on);
  }

  function setPhase(p) {
    section.classList.toggle("is-mid", p > 0.08 && p < 0.88);
    section.classList.toggle("is-end", p >= 0.88);
    if (p <= 0.08) section.classList.remove("is-mid", "is-end");

    var pastHero = section.getBoundingClientRect().bottom <= window.innerHeight * 0.55;
    setCinematic(!pastHero && p < 0.92 && !reduce);
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
      lastFrameIdx = -1; // force redraw
    }
  }

  function drawFrame(idx) {
    idx = clamp(idx | 0, 0, FRAME_COUNT - 1);
    var img = frames[idx];
    if (!img) return;

    var cw = canvas.width;
    var ch = canvas.height;
    var iw = img.width || img.naturalWidth || 1280;
    var ih = img.height || img.naturalHeight || 720;

    // object-fit: cover
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
  }

  function frameIndexFromProgress(p) {
    // Map 0..1 → 0..FRAME_COUNT-1
    return clamp(Math.round(p * (FRAME_COUNT - 1)), 0, FRAME_COUNT - 1);
  }

  function paint(p) {
    resizeCanvas();
    var idx = frameIndexFromProgress(p);
    // Always paint when idle (breathe uses CSS transform on canvas parent)
    // or when frame changes, or first paint
    if (idx !== lastFrameIdx || lastFrameIdx < 0) {
      drawFrame(idx);
    }
  }

  function cancelAutoScroll() {
    if (autoRaf != null) {
      cancelAnimationFrame(autoRaf);
      autoRaf = null;
    }
    autoToken++;
    section.classList.remove("is-autoplaying");
  }

  function disturb() {
    if (autoMode === "auto") {
      cancelAutoScroll();
      autoMode = "free";
      setIdle(false);
      lastMove = performance.now();
    }
  }

  function atTopForAuto() {
    return window.pageYOffset < 40 && progressFromScroll() < 0.05;
  }

  function maybeResetWaiting() {
    if (autoMode === "free" && atTopForAuto() && !autoRaf) {
      autoMode = "waiting";
    }
  }

  function startAutoScroll() {
    if (autoMode !== "waiting" || reduce) {
      if (reduce) autoMode = "free";
      return;
    }
    if (!atTopForAuto() && progressFromScroll() > 0.06) {
      autoMode = "free";
      return;
    }

    autoMode = "auto";
    section.classList.add("is-autoplaying");
    setIdle(false);
    cancelAutoScroll();

    var token = ++autoToken;
    var startY = window.pageYOffset;
    var endY = heroEndScrollY();
    var startT = performance.now();

    function step(now) {
      if (token !== autoToken || autoMode !== "auto") return;

      var t = clamp((now - startT) / AUTO_MS, 0, 1);
      var eased = easeInOutCubic(t);
      var y = startY + (endY - startY) * eased;

      // Instant jump each frame — never native smooth scroll (janky)
      window.scrollTo(0, y);

      lastMove = now;
      lastScrollY = y;

      // Paint immediately from eased progress (don't wait for layout)
      var p = eased;
      setPhase(p);
      if (bar) bar.style.width = (p * 100).toFixed(2) + "%";
      paint(p);

      if (t < 1) {
        autoRaf = requestAnimationFrame(step);
      } else {
        autoRaf = null;
        autoMode = "free";
        section.classList.remove("is-autoplaying");
        window.scrollTo(0, heroEndScrollY());
        paint(1);
        setPhase(1);
        if (bar) bar.style.width = "100%";
      }
    }

    autoRaf = requestAnimationFrame(step);
  }

  function tick(now) {
    var p = progressFromScroll();

    if (autoMode !== "auto") {
      setPhase(p);
      if (bar) bar.style.width = (p * 100).toFixed(2) + "%";
      paint(p);

      var y = window.pageYOffset;
      if (Math.abs(y - lastScrollY) > 0.5) {
        lastScrollY = y;
        lastMove = now;
        setIdle(false);
      } else if (
        p < 0.9 &&
        now - lastMove > 900 &&
        document.body.classList.contains("is-hero-cinematic")
      ) {
        setIdle(true);
      }
      maybeResetWaiting();
    }
    // When auto, step() already paints

    requestAnimationFrame(tick);
  }

  function loadFrames() {
    var i = 0;
    var concurrency = 8;

    function worker() {
      if (i >= FRAME_COUNT) return;
      var idx = i++;
      var url = frameUrl(idx);

      // Prefer createImageBitmap (decode off main thread when possible)
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
            img.decoding = "async";
            img.onload = function () {
              frames[idx] = img;
              resolve();
            };
            img.onerror = reject;
            img.src = URL.createObjectURL(blob);
          });
        })
        .catch(function () {
          // Fallback path via Image src
          return new Promise(function (resolve) {
            var img = new Image();
            img.decoding = "async";
            img.onload = function () {
              frames[idx] = img;
              resolve();
            };
            img.onerror = function () {
              resolve();
            };
            img.src = url;
          });
        })
        .then(function () {
          loaded++;
          if (loaded === 1 && frames[0]) {
            ready = true;
            resizeCanvas();
            paint(0);
          }
          // Progressive: paint if user already scrolled
          if (frames[idx] && idx === frameIndexFromProgress(progressFromScroll())) {
            paint(progressFromScroll());
          }
          if (i < FRAME_COUNT) worker();
        });
    }

    for (var w = 0; w < concurrency; w++) worker();
  }

  // —— Init ——
  if (!reduce) setCinematic(true);

  if (reduce) {
    section.classList.add("is-end");
    setCinematic(false);
    if (bar) bar.style.width = "100%";
    // Load only last frame
    var img = new Image();
    img.onload = function () {
      frames[FRAME_COUNT - 1] = img;
      ready = true;
      resizeCanvas();
      paint(1);
    };
    img.src = frameUrl(FRAME_COUNT - 1);
    return;
  }

  loadFrames();
  requestAnimationFrame(tick);

  window.addEventListener(
    "wheel",
    function (e) {
      if (autoMode === "waiting" && atTopForAuto() && e.deltaY > 0) {
        e.preventDefault();
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") disturb();
    },
    { passive: false }
  );

  window.addEventListener(
    "touchstart",
    function (e) {
      if (e.touches && e.touches[0]) touchStartY = e.touches[0].clientY;
    },
    { passive: true }
  );

  window.addEventListener(
    "touchmove",
    function (e) {
      if (!e.touches || !e.touches[0]) return;
      var dy = touchStartY - e.touches[0].clientY;
      if (autoMode === "waiting" && atTopForAuto() && dy > 10) {
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") disturb();
    },
    { passive: true }
  );

  window.addEventListener(
    "keydown",
    function (e) {
      var down =
        e.key === "ArrowDown" ||
        e.key === "PageDown" ||
        e.key === " " ||
        e.key === "Spacebar";
      if (autoMode === "waiting" && atTopForAuto() && down) {
        e.preventDefault();
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") disturb();
    },
    { passive: false }
  );

  window.addEventListener(
    "resize",
    function () {
      lastFrameIdx = -1;
      resizeCanvas();
      paint(progressFromScroll());
    },
    { passive: true }
  );
})();
