/**
 * Scroll-scrubbed hero video (first 6s).
 * Maps section scroll progress → video.currentTime with rAF for ~60fps.
 * After progress hits 1, page content continues below.
 */
(function () {
  var section = document.getElementById("scrollHero");
  var video = document.getElementById("heroVideo");
  var bar = document.getElementById("heroProgress");
  if (!section || !video) return;

  var CAP = 6;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ticking = false;
  var targetTime = 0;
  var lastDrawn = -1;
  var duration = CAP;
  var ready = false;

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function progressFromScroll() {
    var rect = section.getBoundingClientRect();
    var total = section.offsetHeight - window.innerHeight;
    if (total <= 0) return 1;
    var scrolled = clamp(-rect.top, 0, total);
    return scrolled / total;
  }

  function setPhase(p) {
    section.classList.toggle("is-mid", p > 0.22 && p < 0.78);
    section.classList.toggle("is-end", p >= 0.78);
    if (p <= 0.22) {
      section.classList.remove("is-mid", "is-end");
    }
  }

  function draw() {
    ticking = false;
    var p = progressFromScroll();
    setPhase(p);
    if (bar) bar.style.width = (p * 100).toFixed(2) + "%";

    if (reduce || !ready) return;

    targetTime = p * Math.min(duration, CAP);
    // Only seek when change is meaningful (~1 frame at 24fps ≈ 0.042s)
    if (Math.abs(targetTime - lastDrawn) < 0.02) return;
    try {
      // Avoid thrashing while seeking
      if (video.seeking) return;
      video.currentTime = targetTime;
      lastDrawn = targetTime;
    } catch (e) {
      /* ignore seek errors on incomplete metadata */
    }
  }

  function onScrollOrResize() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(draw);
    }
  }

  function onReady() {
    duration = video.duration && isFinite(video.duration) ? video.duration : CAP;
    // Hard-cap scrub window to first 6s even if file is longer
    duration = Math.min(duration, CAP);
    ready = true;
    video.pause();
    video.currentTime = 0;
    draw();
  }

  if (reduce) {
    section.classList.add("is-end");
    if (bar) bar.style.width = "100%";
    // Show end frame poster path; attempt to jump to end
    video.addEventListener(
      "loadeddata",
      function () {
        try {
          video.currentTime = Math.min(video.duration || CAP, CAP) * 0.99;
        } catch (e) {}
      },
      { once: true }
    );
  } else {
    video.preload = "auto";
    video.muted = true;
    video.playsInline = true;
    video.pause();

    if (video.readyState >= 1) onReady();
    else video.addEventListener("loadedmetadata", onReady, { once: true });

    // Some browsers only allow seeking after canplay
    video.addEventListener(
      "canplay",
      function () {
        ready = true;
        draw();
      },
      { once: true }
    );

    window.addEventListener("scroll", onScrollOrResize, { passive: true });
    window.addEventListener("resize", onScrollOrResize, { passive: true });
    // Continuous rAF while section is in view for buttery scrub on trackpads
    var io = "IntersectionObserver" in window
      ? new IntersectionObserver(
          function (entries) {
            entries.forEach(function (en) {
              section._inView = en.isIntersecting;
            });
          },
          { threshold: 0 }
        )
      : null;
    if (io) io.observe(section);

    (function loop() {
      if (section._inView !== false) draw();
      requestAnimationFrame(loop);
    })();
  }
})();
