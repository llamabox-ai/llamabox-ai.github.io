/**
 * Cinematic scroll-scrub hero (first 6s).
 *
 * First scroll intent from the top → smooth auto-scroll through the full
 * film until the animation ends. If the user disturbs mid-flight (wheel /
 * touch / keys), auto-scroll cancels and they own the scroll.
 */
(function () {
  var section = document.getElementById("scrollHero");
  var video = document.getElementById("heroVideo");
  var bar = document.getElementById("heroProgress");
  if (!section || !video) return;

  var CAP = 6;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ready = false;
  var duration = CAP;
  var lastDrawn = -1;
  var lastScrollY = window.scrollY;
  var lastMove = performance.now();
  var idle = false;
  var ticking = false;

  /** @type {'waiting'|'auto'|'free'} */
  var autoMode = "waiting";
  var autoRaf = null;
  var autoToken = 0;
  var touchStartY = 0;

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function progressFromScroll() {
    var rect = section.getBoundingClientRect();
    var total = Math.max(1, section.offsetHeight - window.innerHeight);
    var scrolled = clamp(-rect.top, 0, total);
    return scrolled / total;
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

  function seek(t) {
    if (!ready || reduce) return;
    t = clamp(t, 0, Math.min(duration, CAP) - 0.001);
    if (Math.abs(t - lastDrawn) < 0.018) return;
    if (video.seeking) return;
    try {
      if (typeof video.fastSeek === "function") {
        try {
          video.fastSeek(t);
        } catch (e) {
          video.currentTime = t;
        }
      } else {
        video.currentTime = t;
      }
      lastDrawn = t;
    } catch (e) {}
  }

  function cancelAutoScroll() {
    if (autoRaf != null) {
      cancelAnimationFrame(autoRaf);
      autoRaf = null;
    }
    autoToken++;
    section.classList.remove("is-autoplaying");
  }

  /** User takes over — cancel auto and stay where we are. */
  function disturb() {
    if (autoMode === "auto") {
      cancelAutoScroll();
      autoMode = "free";
      setIdle(false);
      lastMove = performance.now();
    }
  }

  /**
   * Smoothly drive scrollY from current → end of hero track.
   * Duration ≈ film length so scrub feels 1:1 with the 6s cut.
   */
  function startAutoScroll() {
    if (autoMode !== "waiting") return;
    if (reduce) {
      autoMode = "free";
      return;
    }

    var p0 = progressFromScroll();
    // Already mid-film — don't hijack
    if (p0 > 0.06 || window.pageYOffset > 48) {
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
    // Slightly longer than 6s so eases don't feel rushed
    var dur = 6200;

    function step(now) {
      if (token !== autoToken || autoMode !== "auto") return;

      var t = clamp((now - startT) / dur, 0, 1);
      var y = startY + (endY - startY) * easeInOutCubic(t);
      window.scrollTo(0, y);
      // scrub updates via main rAF loop reading scroll position
      lastMove = now;
      lastScrollY = y;

      if (t < 1) {
        autoRaf = requestAnimationFrame(step);
      } else {
        autoRaf = null;
        autoMode = "free";
        section.classList.remove("is-autoplaying");
        // Snap cleanly to end of track
        window.scrollTo(0, heroEndScrollY());
      }
    }

    autoRaf = requestAnimationFrame(step);
  }

  function atTopForAuto() {
    return window.pageYOffset < 40 && progressFromScroll() < 0.05;
  }

  function maybeResetWaiting() {
    // Back at the top → first scroll can trigger auto again
    if (autoMode === "free" && atTopForAuto() && !autoRaf) {
      autoMode = "waiting";
    }
  }

  function draw() {
    ticking = false;
    var p = progressFromScroll();
    setPhase(p);
    if (bar) bar.style.width = (p * 100).toFixed(2) + "%";

    seek(p * Math.min(duration, CAP));

    var now = performance.now();
    var y = window.pageYOffset;

    // During auto, ignore idle; scroll is programmatic
    if (autoMode === "auto") {
      setIdle(false);
      lastScrollY = y;
      lastMove = now;
      return;
    }

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

  function requestDraw() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(draw);
    }
  }

  function onReady() {
    var d = video.duration;
    duration = d && isFinite(d) && d > 0 ? Math.min(d, CAP) : CAP;
    ready = true;
    video.pause();
    try {
      video.currentTime = 0.001;
      lastDrawn = 0;
    } catch (e) {}
    requestDraw();
  }

  if (!reduce) setCinematic(true);

  if (reduce) {
    section.classList.add("is-end");
    setCinematic(false);
    if (bar) bar.style.width = "100%";
    video.addEventListener(
      "loadeddata",
      function () {
        try {
          video.currentTime = Math.min(video.duration || CAP, CAP) * 0.98;
        } catch (e) {}
      },
      { once: true }
    );
    return;
  }

  video.muted = true;
  video.playsInline = true;
  video.preload = "auto";
  video.setAttribute("playsinline", "");
  video.setAttribute("webkit-playsinline", "");
  video.pause();
  video.disablePictureInPicture = true;

  if (video.readyState >= 1) onReady();
  else {
    video.addEventListener("loadedmetadata", onReady, { once: true });
    video.addEventListener("loadeddata", onReady, { once: true });
  }

  // —— Intent: first scroll from top starts auto; later input disturbs ——
  window.addEventListener(
    "wheel",
    function (e) {
      // Only care about scrolling down into the film from the top
      if (autoMode === "waiting" && atTopForAuto() && e.deltaY > 0) {
        e.preventDefault();
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") {
        // User grabs the wheel → cancel auto, keep current place
        disturb();
      }
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
      var dy = touchStartY - e.touches[0].clientY; // positive = finger up = scroll down
      if (autoMode === "waiting" && atTopForAuto() && dy > 10) {
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") {
        disturb();
      }
    },
    { passive: true }
  );

  window.addEventListener(
    "keydown",
    function (e) {
      var keys = ["ArrowDown", "PageDown", " ", "Spacebar", "ArrowUp", "PageUp"];
      if (keys.indexOf(e.key) === -1) return;

      var down = e.key === "ArrowDown" || e.key === "PageDown" || e.key === " " || e.key === "Spacebar";

      if (autoMode === "waiting" && atTopForAuto() && down) {
        e.preventDefault();
        startAutoScroll();
        return;
      }
      if (autoMode === "auto") {
        disturb();
      }
    },
    { passive: false }
  );

  // Trackpad gesture / scrollbar drag during auto
  window.addEventListener(
    "scroll",
    function () {
      // If scroll jumps away from the auto path while autoplaying,
      // a direct scrollbar drag counts as disturb (except our own scrollTo).
      // We can't perfectly detect programmatic vs user scroll, so we only
      // disturb when the user is also generating pointer/wheel (handled above).
      requestDraw();
    },
    { passive: true }
  );

  window.addEventListener("resize", requestDraw, { passive: true });

  (function loop() {
    var rect = section.getBoundingClientRect();
    var near = rect.bottom > 0 && rect.top < window.innerHeight * 1.2;
    if (near || autoMode === "auto") draw();
    requestAnimationFrame(loop);
  })();
})();
