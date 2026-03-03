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
  var tabs   = document.querySelectorAll('.gh-tab');
  var panels = document.querySelectorAll('.gh-panel');

  function activateTab(target) {
    tabs.forEach(function (t) {
      var active = t.dataset.target === target;
      t.classList.toggle('active', active);
      t.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.id === target);
    });
    // Scroll main content into view on mobile
    var panel = document.getElementById(target);
    if (panel) {
      var tabs_el = document.querySelector('.gh-tabs');
      if (tabs_el) {
        var offset = tabs_el.getBoundingClientRect().top + window.scrollY - 70;
        window.scrollTo({ top: offset, behavior: 'smooth' });
      }
    }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      activateTab(tab.dataset.target);
    });
  });

  // ── Pinned cards → switch to their tab ─────────────────────
  document.querySelectorAll('.gh-pinned-card').forEach(function (card) {
    card.addEventListener('click', function () {
      activateTab(card.dataset.tab);
    });
  });

  // ── Nav links → switch to their tab ────────────────────────
  document.querySelectorAll('.gh-nav-links a[data-tab]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      activateTab(link.dataset.tab);
      // close mobile menu
      var navLinks = document.querySelector('.gh-nav-links');
      var toggle   = document.querySelector('.gh-nav-toggle');
      if (navLinks) navLinks.classList.remove('open');
      if (toggle)   toggle.setAttribute('aria-expanded', 'false');
    });
  });

  // ── Mobile nav toggle ───────────────────────────────────────
  var toggle   = document.querySelector('.gh-nav-toggle');
  var navLinks = document.querySelector('.gh-nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

})();
