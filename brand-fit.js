/* SlamDunk brand-fit — scales the SLAMDUNK TECHNOLOGIES wordmark so it spans
   from the icon's left edge toward the nav's right padding edge, then adds
   30% per Glenn 9/4 and may grow all the way to the right edge of the screen,
   but never past it. Works on inner pages (.page-nav) and the homepage
   (.hero-copy fallback). */
(function () {
  function fit() {
    var nav = document.querySelector(".page-nav") ||
              document.querySelector(".hero-copy") ||
              document.querySelector(".page");
    var title = document.querySelector(".brand-title") || document.querySelector(".brand-text h1");
    if (!nav || !title) return;
    var brand = title.closest(".brand");
    var icon = document.querySelector(".brand-mark");
    if (!brand || !icon) return;

    var navStyle = getComputedStyle(nav);
    var padL = parseFloat(navStyle.paddingLeft) || 0;
    var padR = parseFloat(navStyle.paddingRight) || 0;

    // available width: container inner width - icon - gap between icon and text
    var navW = nav.clientWidth - padL - padR;
    var iconW = icon.getBoundingClientRect().width;
    var gap = parseFloat(getComputedStyle(brand).gap) || 0;
    var target = navW - iconW - gap;
    if (target < 60) return;

    title.style.whiteSpace = "nowrap";
    title.style.width = "auto";

    var base = parseFloat(getComputedStyle(title).fontSize);
    // measure current rendered width at current font-size
    var w = title.scrollWidth;
    if (!w) return;

    // Glenn 9/4: make it 30% larger than the exact span, and let it grow
    // right up to the edge of the screen, but no further.
    var fitted = base * ((target * 1.3) / w);
    var left = title.getBoundingClientRect().left;
    var maxFit = base * ((window.innerWidth - left - 8) / w);
    fitted = Math.min(fitted, maxFit);

    // sensible bounds: never tiny, never absurd
    var min = 14, max = 64;
    fitted = Math.max(min, Math.min(max, fitted));
    title.style.fontSize = fitted.toFixed(2) + "px";
  }

  function run() {
    fit();
    // re-run once web fonts finish loading (metrics change)
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
  window.addEventListener("resize", function () {
    clearTimeout(window.__sdFitT);
    window.__sdFitT = setTimeout(fit, 150);
  });
})();