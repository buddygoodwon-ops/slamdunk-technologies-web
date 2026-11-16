/* see-like-ai.js -- "See Like AI Sees" view for SlamDunk Technologies (v1, client-side)
 * Wired to the "That's a SlamDunk!" element on the site's first pages.
 * Clicking it flips the page to the way an AI agent / MCP client reads it.
 * Deep link: ?view=ai   Persist: localStorage 'slai'   Exit: Esc or "Human view".
 * NOTE: this file is intentionally ASCII-only (unicode via escapes) so it can be
 * served without a charset header and still render correctly. */
(function () {
  'use strict';
  var KEY = 'slai';
  var ROBOT = '\uD83E\uDD16';   // 🤖
  var EYE = '\uD83D\uDC41';     // 👁
  var EMDASH = '\u2014';        // —
  var MIDDOT = '\u00B7';        // ·
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function esc(s) { return String(s == null ? '' : s); }
  function clean(s) { return (s || '').replace(/\s+/g, ' ').trim(); }
  function textOf(node) { var t = (node && node.innerText != null) ? node.innerText : (node ? node.textContent : ''); return clean(t); }

  function collect() {
    var title = (document.title || '').replace(/\s*\|\s*SlamDunk Technologies\s*$/i, '').trim();
    var meta = document.querySelector('meta[name="description"]');
    var desc = clean(meta ? meta.getAttribute('content') : '');

    var jsonLd = [];
    Array.prototype.forEach.call(document.querySelectorAll('script[type="application/ld+json"]'), function (s) {
      try { jsonLd.push(JSON.parse(s.textContent)); } catch (e) { /* ignore bad JSON-LD */ }
    });

    var outline = [];
    Array.prototype.forEach.call(document.querySelectorAll('h1, h2, h3'), function (h) {
      if (h.closest('.slai-overlay')) return;
      var t = textOf(h);
      if (t) outline.push({ lvl: h.tagName.toLowerCase(), t: t });
    });

    var actions = [], seenAct = {};
    Array.prototype.forEach.call(document.querySelectorAll('a[href],button'), function (a) {
      if (a.closest('.slai-overlay')) return;
      var href = a.getAttribute('href') || '';
      var label = textOf(a) || a.getAttribute('aria-label') || '';
      var kind = null, id = null;
      if (/^tel:/i.test(href)) { kind = 'phone'; id = 'call'; }
      else if (/^sms:/i.test(href)) { kind = 'sms'; id = 'text'; }
      else if (/^mailto:/i.test(href)) { kind = 'email'; id = 'email'; }
      else if (/calendly|book-a-demo/i.test(href)) { kind = 'book'; id = 'book_demo'; }
      if (kind && !seenAct[id]) { seenAct[id] = 1; actions.push({ id: id, kind: kind, label: label, href: href }); }
    });

    var links = [], seenLink = {};
    Array.prototype.forEach.call(document.querySelectorAll('a[href]'), function (a) {
      if (a.closest('.slai-overlay') || a.classList.contains('slamdunk-link')) return;
      var href = a.getAttribute('href') || '';
      if (/^(tel:|sms:|mailto:|#|javascript:)/i.test(href)) return;
      var t = textOf(a);
      if (!t || t.length > 48) return;
      var k = t + '|' + href;
      if (seenLink[k]) return; seenLink[k] = 1;
      links.push({ text: t, href: href, rel: /^https?:/i.test(href) ? 'external' : 'internal' });
    });

    var lead = '';
    var cands = document.querySelectorAll('.page-lede, .hero-copy p, main p');
    for (var i = 0; i < cands.length; i++) { var tx = textOf(cands[i]); if (tx.length > 60) { lead = tx; break; } }

    var imgs = document.querySelectorAll('img'), imgsNoAlt = 0;
    Array.prototype.forEach.call(imgs, function (i) { if (!i.getAttribute('alt')) imgsNoAlt++; });

    return { title: title, desc: desc, lead: lead, jsonLd: jsonLd, outline: outline, actions: actions,
             links: links, imgsTotal: imgs.length, imgsNoAlt: imgsNoAlt, h1count: document.querySelectorAll('h1').length };
  }

  function score(d) {
    var s = 0, issues = [];
    if (d.jsonLd.length) { s += 25; issues.push(['ok', 'Structured data', 'JSON-LD present (' + d.jsonLd.length + ' block' + (d.jsonLd.length > 1 ? 's' : '') + ').']); }
    else { issues.push(['warn', 'Structured data', 'No JSON-LD found ' + EMDASH + ' add Organization/Offer schema.']); }
    if (d.h1count >= 1) { s += 20; issues.push(['ok', 'Semantic H1', 'Page exposes a primary heading.']); }
    else { issues.push(['warn', 'Semantic H1', 'No H1 on the page.']); }
    if ((d.desc && d.desc.length > 40) || d.lead) { s += 10; } else { issues.push(['warn', 'Summary text', 'Meta description missing or too short.']); }
    if (d.actions.length) { s += 15; issues.push(['ok', 'Machine actions', d.actions.length + ' actionable endpoint(s) exposed for AI to call/text/email/book.']); }
    else { issues.push(['issue', 'Machine actions', 'No call/email/booking endpoints found.']); }
    if (d.imgsNoAlt === 0) { s += 10; } else { issues.push(['warn', 'Image alt text', d.imgsNoAlt + ' image(s) missing alt text.']); }
    if (d.outline.length >= 3) { s += 10; issues.push(['ok', 'Content extractability', 'Clear heading structure for extraction.']); }
    else { issues.push(['warn', 'Content extractability', 'Thin heading structure.']); }
    if (d.links.length >= 3) { s += 10; } else { issues.push(['warn', 'Internal links', 'Few navigable links exposed.']); }
    return { score: Math.max(0, Math.min(100, s)), issues: issues };
  }

  function chip(k, v) { var c = el('div', 'slai-chip'); c.appendChild(el('b', null, k + ': ')); c.appendChild(document.createTextNode(v || '')); return c; }

  function render(d, sc) {
    var ov = el('div', 'slai-overlay');
    ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', 'See Like AI Sees');
    var wrap = el('div', 'slai-wrap');

    var head = el('div', 'slai-head');
    var tt = el('div');
    var h1 = el('h1', 'slai-title');
    var titleLogo = document.createElement('img');
    titleLogo.src = 'assets/buddyfetch-robot-logo.png';
    titleLogo.alt = 'BuddyFetch AI';
    titleLogo.className = 'slai-logo';
    h1.appendChild(titleLogo);
    h1.appendChild(document.createTextNode('See Like AI Sees'));
    tt.appendChild(h1);
    tt.appendChild(el('p', 'slai-sub', 'The AI\u2019s-eye view of this page ' + EMDASH + ' ' + (location.pathname === '/' ? '/index.html' : location.pathname)));
    head.appendChild(tt); head.appendChild(el('div', 'slai-spacer'));
    var close = el('button', 'cta-button slai-close');
    close.type = 'button';
    close.setAttribute('aria-label', 'Back to Human View');
    var closeLogo = document.createElement('img');
    closeLogo.src = 'assets/slamdunk-dog-icon.png';
    closeLogo.alt = 'SlamDunk';
    closeLogo.className = 'slai-close-logo';
    close.appendChild(closeLogo);
    close.appendChild(document.createTextNode('Back to Human View'));
    close.addEventListener('click', function () { toggle(false); });
    head.appendChild(close);
    wrap.appendChild(head);

    var scoreCard = el('div', 'slai-score');
    var dial = el('div', 'slai-dial'); dial.style.setProperty('--p', String(sc.score));
    dial.appendChild(el('span', null, String(sc.score)));
    scoreCard.appendChild(dial);
    var sp = el('p');
    sp.appendChild(el('strong', null, 'AI-readability: ' + sc.score + '/100. '));
    sp.appendChild(document.createTextNode(sc.score >= 80 ? 'Strong ' + EMDASH + ' AI can readily cite this page.' : sc.score >= 60 ? 'Fair ' + EMDASH + ' a few fixes will sharpen AI citation.' : 'Needs work ' + EMDASH + ' several gaps block AI from reading this page.'));
    scoreCard.appendChild(sp);
    wrap.appendChild(scoreCard);

    var grid = el('div', 'slai-grid');

    var cSum = el('div', 'slai-card span');
    cSum.appendChild(el('h3', null, 'Summary'));
    cSum.appendChild(el('p', 'slai-summary', d.lead || d.desc || (d.outline[0] ? d.outline[0].t : d.title)));
    grid.appendChild(cSum);

    var cEnt = el('div', 'slai-card');
    cEnt.appendChild(el('h3', null, 'Entities & structure'));
    var chips = el('div', 'slai-chips');
    chips.appendChild(chip('Title', d.title));
    d.jsonLd.forEach(function (j) {
      var types = [].concat(j['@type'] || j.type || []).join(', ');
      if (types) chips.appendChild(chip('schema:' + types, j.name || j.headline || ''));
    });
    chips.appendChild(chip('headings', String(d.outline.length)));
    chips.appendChild(chip('links', String(d.links.length)));
    cEnt.appendChild(chips);
    grid.appendChild(cEnt);

    var cAct = el('div', 'slai-card');
    cAct.appendChild(el('h3', null, 'Actions an AI can take'));
    var acts = el('div', 'slai-actions');
    if (!d.actions.length) acts.appendChild(el('p', 'slai-summary', 'None detected.'));
    d.actions.forEach(function (a) {
      var row = el('a', 'slai-action'); row.href = a.href;
      row.appendChild(el('span', 'k', a.kind));
      row.appendChild(el('span', null, a.label || a.id));
      row.appendChild(el('span', 'h', a.href));
      acts.appendChild(row);
    });
    cAct.appendChild(acts);
    grid.appendChild(cAct);

    var cOut = el('div', 'slai-card');
    cOut.appendChild(el('h3', null, 'Heading outline'));
    var ul = el('ul', 'slai-outline');
    d.outline.slice(0, 14).forEach(function (h) { ul.appendChild(el('li', h.lvl, h.t)); });
    cOut.appendChild(ul);
    grid.appendChild(cOut);

    var cLnk = el('div', 'slai-card');
    cLnk.appendChild(el('h3', null, 'Links exposed'));
    var lw = el('div', 'slai-links');
    if (!d.links.length) lw.appendChild(el('p', 'slai-summary', 'None found.'));
    d.links.slice(0, 24).forEach(function (l) { var a = el('a', null, l.text); a.href = l.href; lw.appendChild(a); });
    cLnk.appendChild(lw);
    grid.appendChild(cLnk);

    if (d.jsonLd.length) {
      var cJson = el('div', 'slai-card span');
      cJson.appendChild(el('h3', null, 'Structured data (JSON-LD)'));
      cJson.appendChild(el('pre', 'slai-json', JSON.stringify(d.jsonLd.length === 1 ? d.jsonLd[0] : d.jsonLd, null, 2)));
      grid.appendChild(cJson);
    }

    var cIss = el('div', 'slai-card span');
    cIss.appendChild(el('h3', null, 'AI-readability checks'));
    var il = el('ul', 'slai-issues');
    sc.issues.forEach(function (it) {
      var li = el('li', it[0]);
      li.appendChild(el('span', 'tag', it[0] === 'ok' ? 'pass' : it[0] === 'warn' ? 'warn' : 'fix'));
      var s2 = el('span'); s2.appendChild(el('strong', null, esc(it[1]) + '. ')); s2.appendChild(document.createTextNode(esc(it[2])));
      li.appendChild(s2);
      il.appendChild(li);
    });
    cIss.appendChild(il); grid.appendChild(cIss);

    wrap.appendChild(grid);
    wrap.appendChild(el('p', 'slai-foot', 'SlamDunk Technologies ' + MIDDOT + ' MCP Server Mode ' + EMDASH + ' how ChatGPT, Claude, Perplexity & Gemini ingest your site.'));
    ov.appendChild(wrap);
    return ov;
  }

  var current = null;
  function toggle(on) {
    var want = (on == null) ? !document.body.classList.contains('slai-on') : !!on;
    if (want === document.body.classList.contains('slai-on')) return;
    if (want) {
      var d = collect(), sc = score(d);
      current = render(d, sc);
      document.body.appendChild(current);
      document.body.classList.add('slai-on');
      try { localStorage.setItem(KEY, '1'); } catch (e) {}
      try { var u = new URL(location.href); u.searchParams.set('view', 'ai'); history.replaceState(null, '', u.toString()); } catch (e) {}
      var btn = current.querySelector('.slai-close'); if (btn && btn.focus) btn.focus();
    } else {
      if (current && current.parentNode) current.parentNode.removeChild(current);
      current = null;
      document.body.classList.remove('slai-on');
      try { localStorage.setItem(KEY, '0'); } catch (e) {}
      try { var v = new URL(location.href); v.searchParams.delete('view'); history.replaceState(null, '', v.pathname + v.search + v.hash); } catch (e) {}
    }
  }
  window.SLAI = { toggle: toggle };
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') toggle(false); });

  function init() {
    // "That's a SlamDunk!" still opens the AI view.
    Array.prototype.forEach.call(document.querySelectorAll('a.slamdunk-link'), function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); toggle(true); });
    });
    // Add the "See Like an AI MCP" button ONLY on pages that do NOT already have
    // the "Say Hi to Buddy" button. It mirrors that button's format and color.
    var hasSayHi = document.querySelector('a.cta-button[href*="buddyfetch.ai"], a.cta-button[href*="buddyfetch"]');
    if (!hasSayHi && !document.querySelector('.slai-btn')) {
      var row = document.querySelector('.cta-row');
      var text = document.querySelector('.cta-text');
      var host = (text && row && text.parentNode === row) ? row : (text || row);
      if (host) {
        var btn = el('button', 'cta-button slai-btn', 'See Like an AI MCP');
        btn.type = 'button';
        btn.setAttribute('aria-label', 'See Like an AI MCP');
        btn.addEventListener('click', function (e) { e.stopPropagation(); toggle(true); });
        if (host === row && text) row.appendChild(btn);
        else host.parentNode.insertBefore(btn, host.nextSibling);
      }
    }
    var openByLink = /(?:[?&])view=ai\b/.test(location.search) || location.hash === '#ai';
    var remember = false; try { remember = localStorage.getItem(KEY) === '1'; } catch (e) {}
    if (openByLink || remember) toggle(true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
