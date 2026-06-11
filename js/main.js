/* robot fantôme — main.js */

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

  // ── Tab switching ───────────────────────────────────────────
  var navLinks = document.querySelectorAll('.gh-nav-links a[data-tab]');
  var panels   = document.querySelectorAll('.gh-panel');

  var layout = document.querySelector('.gh-layout');

  function activateTab(target, push) {
    navLinks.forEach(function (a) {
      var on = a.dataset.tab === target;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.id === target);
    });
    // Profile sidebar is only shown on the About tab
    if (layout) layout.classList.toggle('show-sidebar', target === 'about');
    // Keep the URL shareable (#blog, #mixtape, …) and the back button working
    var newHash = target === 'overview' ? '' : '#' + target;
    if (push !== false && history.pushState && window.location.hash !== newHash) {
      history.pushState(null, '', newHash || window.location.pathname);
    }
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  // ── Deep links: open the tab named in the URL hash ─────────
  function tabFromHash() {
    var id = window.location.hash.slice(1);
    var el = id && document.getElementById(id);
    return el && el.classList.contains('gh-panel') ? id : null;
  }

  var initialTab = tabFromHash();
  if (initialTab) activateTab(initialTab, false);

  // Back/forward buttons and in-page #links walk the tab history
  window.addEventListener('popstate', function () {
    activateTab(tabFromHash() || 'overview', false);
  });
  window.addEventListener('hashchange', function () {
    var tab = tabFromHash();
    if (tab) activateTab(tab, false);
  });

  // ── Pinned cards → switch to their tab ─────────────────────
  document.querySelectorAll('.gh-pinned-card').forEach(function (card) {
    card.addEventListener('click', function () {
      activateTab(card.dataset.tab);
    });
  });

  // ── Nav links → switch to their tab ────────────────────────
  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      activateTab(link.dataset.tab);
      // close mobile menu
      var navEl  = document.querySelector('.gh-nav-links');
      var toggle = document.querySelector('.gh-nav-toggle');
      if (navEl)   navEl.classList.remove('open');
      if (toggle)  toggle.setAttribute('aria-expanded', 'false');
    });
  });

  // ── Mobile nav toggle ───────────────────────────────────────
  var toggle = document.querySelector('.gh-nav-toggle');
  var navEl  = document.querySelector('.gh-nav-links');

  if (toggle && navEl) {
    toggle.addEventListener('click', function () {
      var open = navEl.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ── Brand logo → return to overview ────────────────────────
  var brand = document.querySelector('.gh-nav-brand');
  if (brand) {
    brand.addEventListener('click', function (e) {
      e.preventDefault();
      activateTab('overview');
    });
  }

})();
