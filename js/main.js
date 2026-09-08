/* robot fantôme — main.js
   Loaded by every page (index, product pages, privacy, terms).
   Shared: image fade-in, mobile nav toggle, footer year.
   Tab switching only wires up when the page has .gh-panel tabs (index.html). */

(function () {
  'use strict';

  // ── Fade images in once loaded ──────────────────────────────
  document.querySelectorAll('img').forEach(function (img) {
    if (img.complete) {
      img.classList.add('loaded');
    } else {
      img.addEventListener('load', function () {
        img.classList.add('loaded');
      });
    }
  });

  // ── Footer © year ───────────────────────────────────────────
  document.querySelectorAll('.footer-year').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // ── Mobile nav toggle ───────────────────────────────────────
  var toggle = document.querySelector('.gh-nav-toggle');
  var navEl  = document.querySelector('.gh-nav-links');

  function closeMenu() {
    if (navEl)  navEl.classList.remove('open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }

  if (toggle && navEl) {
    toggle.addEventListener('click', function () {
      var open = navEl.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // ── Tabs (index.html only) ──────────────────────────────────
  var panels = document.querySelectorAll('.gh-panel');
  if (!panels.length) return;

  var navLinks = document.querySelectorAll('.gh-nav-links a[data-tab]');
  var layout   = document.querySelector('.gh-layout');

  function activateTab(target, push) {
    navLinks.forEach(function (a) {
      var on = a.dataset.tab === target;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    panels.forEach(function (p) {
      var on = p.id === target;
      p.classList.toggle('active', on);
      // Lazy images inside a hidden panel only start loading a few seconds after it
      // becomes visible; switch them to eager the moment the tab opens.
      if (on) {
        p.querySelectorAll('img[loading="lazy"]').forEach(function (img) { img.loading = 'eager'; });
      }
    });
    // Profile sidebar is only shown on the Blog & Story tab
    if (layout) layout.classList.toggle('show-sidebar', target === 'blog');
    // Keep the URL shareable (#blog, #mixtape, …) and the back button working
    var newHash = target === 'music' ? '' : '#' + target;
    if (push !== false && history.pushState && window.location.hash !== newHash) {
      history.pushState(null, '', newHash || window.location.pathname);
    }
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  // ── Deep links: open the tab named in the URL hash ─────────
  // Legacy hashes from retired tabs keep working
  var hashAliases = { about: 'blog', volunteer: 'blog', ap: 'blog', overview: 'music', press: 'music' };

  function tabFromHash() {
    var id = window.location.hash.slice(1);
    if (hashAliases[id]) id = hashAliases[id];
    var el = id && document.getElementById(id);
    return el && el.classList.contains('gh-panel') ? id : null;
  }

  var initialTab = tabFromHash();
  if (initialTab) activateTab(initialTab, false);

  // Back/forward buttons and in-page #links walk the tab history
  window.addEventListener('popstate', function () {
    activateTab(tabFromHash() || 'music', false);
  });
  window.addEventListener('hashchange', function () {
    var tab = tabFromHash();
    if (tab) activateTab(tab, false);
  });

  // ── Pinned cards → switch to their tab ─────────────────────
  document.querySelectorAll('.gh-pinned-card[data-tab]').forEach(function (card) {
    card.addEventListener('click', function () {
      activateTab(card.dataset.tab);
    });
  });

  // ── Nav links → switch to their tab ────────────────────────
  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      activateTab(link.dataset.tab);
      closeMenu();
    });
  });

  // ── Brand logo → return home (music) ───────────────────────
  var brand = document.querySelector('.gh-nav-brand');
  if (brand) {
    brand.addEventListener('click', function (e) {
      e.preventDefault();
      activateTab('music');
      closeMenu();
    });
  }

})();
