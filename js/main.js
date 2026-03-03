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

  function activateTab(target) {
    navLinks.forEach(function (a) {
      a.classList.toggle('active', a.dataset.tab === target);
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.id === target);
    });
  }

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

})();
