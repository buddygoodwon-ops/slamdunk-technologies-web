/* SlamDunk swipe navigation — app-style page flipping (Glenn 9/3)
   Swipe left = next page, swipe right = previous page. */
(function () {
  var ORDER = [
    "index.html",
    "workflows.html",
    "agents.html",
    "marketing.html",
    "smart.html",
    "future.html",
    "company-brain.html",
    "distribution.html",
    "virtual-mascot.html",
    "avatar-app.html",
    "mcp-server.html"
  ];

  function currentPage() {
    var p = location.pathname.split("/").pop();
    if (!p || p === "" || p === "/") return "index.html";
    return p;
  }

  function go(delta) {
    var cur = currentPage();
    var i = ORDER.indexOf(cur);
    if (i === -1) return;
    var next = ORDER[i + delta];
    if (next && next !== cur) {
      // little slide feedback then navigate
      document.body.style.transition = "transform .18s ease, opacity .18s ease";
      document.body.style.transform = "translateX(" + (delta > 0 ? "-18%" : "18%") + ")";
      document.body.style.opacity = "0.6";
      setTimeout(function () { location.href = next; }, 160);
    }
  }

  var sx = 0, sy = 0, st = 0, tracking = false;

  document.addEventListener("touchstart", function (e) {
    if (e.touches.length !== 1) return;
    sx = e.touches[0].clientX;
    sy = e.touches[0].clientY;
    st = Date.now();
  }, { passive: true });

  document.addEventListener("touchend", function (e) {
    if (e.changedTouches.length !== 1) return;
    var dx = e.changedTouches[0].clientX - sx;
    var dy = e.changedTouches[0].clientY - sy;
    var dt = Date.now() - st;
    // horizontal, fast enough, long enough, and mostly horizontal
    if (Math.abs(dx) > 70 && Math.abs(dx) > Math.abs(dy) * 1.8 && dt < 800) {
      go(dx < 0 ? 1 : -1);
    }
  }, { passive: true });

  /* one-time swipe hint pill (phone only) */
  if (window.matchMedia("(max-width: 820px)").matches && !localStorage.getItem("sd_swipe_hint")) {
    var pill = document.createElement("div");
    pill.textContent = "Swipe ← → to explore";
    pill.style.cssText = "position:fixed;left:50%;bottom:26px;transform:translateX(-50%);" +
      "background:linear-gradient(90deg,#8b6cf0,#4f8ef7);color:#fff;font:600 13px Inter,sans-serif;" +
      "padding:9px 16px;border-radius:999px;z-index:9999;box-shadow:0 8px 24px rgba(107,90,240,.45);" +
      "transition:opacity .6s ease;pointer-events:none;opacity:.96;";
    document.addEventListener("DOMContentLoaded", function () {
      document.body.appendChild(pill);
      setTimeout(function () { pill.style.opacity = "0"; }, 3200);
      setTimeout(function () { pill.remove(); }, 4000);
    });
    try { localStorage.setItem("sd_swipe_hint", "1"); } catch (e) {}
  }
})();
