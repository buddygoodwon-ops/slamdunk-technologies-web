/* SlamDunk brand-fit — scales the SLAMDUNK TECHNOLOGIES wordmark so it spans
   exactly from the icon's left edge to the nav's right padding edge
   (symmetric gaps: icon-to-screen-edge == last letter-to-screen-edge). */
(function () {
  function fit() {
    var nav = document.querySelector(".page-nav");
    var title = document.querySelector(".brand-title") || document.querySelector(".brand-text h1");
    if (!nav || !title) return;
    var brand = title.closest(".brand") || title.closest(".brand-text") && title.closest(".brand-text").parentElement;
    var icon = document.querySelector(".brand-mark");
    if (!brand || !icon) return;

    var navStyle = getComputedStyle(nav);
    var padL = parseFloat(navStyle.paddingLeft) || 0;
    var padR = parseFloat(navStyle.paddingRight) || 0;

    // available width: nav inner width - icon - gap between icon and text
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
    var fitted = base * (target / w);

    // sensible bounds: never smaller than 60% of design size, never bigger than 44px
    var min = base * 0.6, max = 44;
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