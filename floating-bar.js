/* Floating pill footer bar — shared behavior (Glenn 9/3)
   Active-state toggle, home-aware highlight, Share via Web Share API with clipboard fallback. */
(function () {
  function clearActive() {
    document.querySelectorAll('.footer-btn').forEach(function (b) { b.classList.remove('active'); });
  }
  document.querySelectorAll('.footer-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var isHome = btn.getAttribute('data-home') === '1';
      var isShare = btn.getAttribute('data-share') === '1';

      if (isShare) {
        e.preventDefault();
        clearActive();
        btn.classList.add('active');
        if (navigator.share) {
          navigator.share({ title: document.title, url: location.href }).catch(function () {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(location.href).catch(function () {});
        }
        return;
      }

      // Home icon on the home page = smooth-scroll to top instead of reloading
      if (isHome) {
        var p = location.pathname.split('/').pop() || 'index.html';
        if (p === 'index.html' || p === '') {
          e.preventDefault();
          clearActive();
          btn.classList.add('active');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          return;
        }
      }

      clearActive();
      btn.classList.add('active');
    });
  });

  // Home active on home page
  (function () {
    var p = location.pathname.split('/').pop() || 'index.html';
    if (p === 'index.html' || p === '' || p === '/') {
      var h = document.querySelector('.footer-btn[data-home="1"]');
      if (h) h.classList.add('active');
    }
  })();
})();