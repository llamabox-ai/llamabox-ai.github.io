/**
 * Cinematic scroll-scrub hero (first 6s).
 * - Nav hidden until film completes (body.is-hero-cinematic)
 * - No layout jump: nav is fixed; hero owns pure 100dvh black
 * - Idle: gentle breathe + RGB glow when user stops scrolling
 * - rAF scrub for smooth seeks
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

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function progressFromScroll() {
    var rect = section.getBoundingClientRect();
    var total = Math.max(1, section.offsetHeight - window.innerHeight);
    // When section top is at viewport top, progress 0
    var scrolled = clamp(-rect.top, 0, total);
    return scrolled / total;
  }

  function setCinematic(on) {
    document.body.classList.toggle("is-hero-cinematic", on);
  }

  function setPhase(p) {
    section.classList.toggle("is-mid", p > 0.08 && p < 0.88);
    section.classList.toggle("is-end", p >= 0.88);
    if (p <= 0.08) section.classList.remove("is-mid", "is-end");

    // Hide nav for almost entire film; show when nearly done or past hero
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
    // ~half frame at 24fps
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

  function draw() {
    ticking = false;
    var p = progressFromScroll();
    setPhase(p);
    if (bar) bar.style.width = (p * 100).toFixed(2) + "%";

    var t = p * Math.min(duration, CAP);
    seek(t);

    // Idle detection: only while still in cinematic hero and not at end
    var now = performance.now();
    var y = window.scrollY;
    if (Math.abs(y - lastScrollY) > 0.5) {
      lastScrollY = y;
      lastMove = now;
      setIdle(false);
    } else if (p < 0.9 && now - lastMove > 900 && document.body.classList.contains("is-hero-cinematic")) {
      setIdle(true);
    }
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
    // Pin first frame immediately — no flash of wrong frame
    try {
      video.currentTime = 0.001;
      lastDrawn = 0;
    } catch (e) {}
    requestDraw();
  }

  // Start cinematic immediately so first paint has no nav gap
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

  // Kill default video chrome / picture-in-picture quirks
  video.disablePictureInPicture = true;

  if (video.readyState >= 1) onReady();
  else {
    video.addEventListener("loadedmetadata", onReady, { once: true });
    video.addEventListener("loadeddata", onReady, { once: true });
  }

  window.addEventListener("scroll", requestDraw, { passive: true });
  window.addEventListener("resize", requestDraw, { passive: true });
  window.addEventListener(
    "wheel",
    function () {
      lastMove = performance.now();
      setIdle(false);
    },
    { passive: true }
  );
  window.addEventListener(
    "touchmove",
    function () {
      lastMove = performance.now();
      setIdle(false);
    },
    { passive: true }
  );

  // Continuous rAF while near hero for buttery trackpad scrub + idle
  (function loop() {
    var rect = section.getBoundingClientRect();
    var near = rect.bottom > 0 && rect.top < window.innerHeight * 1.2;
    if (near) draw();
    requestAnimationFrame(loop);
  })();
})();
