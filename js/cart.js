/* robot fantôme — cart.js
   localStorage-backed multi-item cart with a slide-in drawer and a nav button.
   Self-contained: builds its own nav button + drawer DOM, so a page only needs
   <script src="…/shop-catalog.js"> (window.RF_CATALOG) then <script src="…/cart.js">.

   "Add to cart" buttons are any `.btn-buy[data-product-id]` on the page (the product
   pages). Checkout POSTs { items: [{ id, qty }] } to the Worker's /checkout and
   redirects to Stripe. The browser cart is DISPLAY-ONLY — the Worker re-prices every
   line from the catalog, so the browser is never trusted on price. No card handling
   ever happens here. Until the Worker is live, checkout fails gracefully. */

(function () {
  'use strict';

  var CATALOG = window.RF_CATALOG || {};
  var KEY = 'rf_cart';
  var meta = document.querySelector('meta[name="shop-worker-url"]');
  var WORKER_URL = (meta && meta.content) || '';

  // ── state ──────────────────────────────────────────────────
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch (e) { return {}; }
  }
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) { /* private mode */ }
  }
  var cart = load();
  // drop any stored ids that are no longer in the catalog (loads before this script)
  Object.keys(cart).forEach(function (id) { if (!CATALOG[id]) delete cart[id]; });
  persist();

  function count() {
    return Object.keys(cart).reduce(function (n, id) { return n + cart[id]; }, 0);
  }
  function subtotal() {
    return Object.keys(cart).reduce(function (s, id) {
      var p = CATALOG[id];
      return s + (p && typeof p.price === 'number' ? p.price * cart[id] : 0);
    }, 0);
  }
  function fmt(n) {
    return '$' + (Math.round(n * 100) % 100 === 0 ? n.toFixed(0) : n.toFixed(2));
  }
  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s == null ? '' : String(s);
    return d.innerHTML;
  }

  function setQty(id, qty) {
    qty = Math.max(0, qty | 0);
    if (qty === 0) { delete cart[id]; } else { cart[id] = qty; }
    persist();
    render();
  }
  function add(id, qty) {
    if (!CATALOG[id]) return;
    cart[id] = (cart[id] || 0) + (qty > 0 ? qty : 1);
    persist();
    render();
    openDrawer();
  }

  // ── DOM ────────────────────────────────────────────────────
  var navBtn, badge, drawer, overlay, listEl, subEl, checkoutBtn, msgEl;

  var CART_ICON =
    '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18">' +
    '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" ' +
    'd="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>' +
    '<path fill="none" stroke="currentColor" stroke-width="2" d="M3 6h18"/>' +
    '<path fill="none" stroke="currentColor" stroke-width="2" d="M16 10a4 4 0 0 1-8 0"/></svg>';

  function buildUI() {
    var navInner = document.querySelector('.gh-nav-inner');
    if (navInner) {
      navBtn = document.createElement('button');
      navBtn.className = 'cart-nav-btn';
      navBtn.type = 'button';
      navBtn.setAttribute('aria-label', 'Open cart');
      navBtn.innerHTML = CART_ICON + '<span class="cart-count" hidden>0</span>';
      navBtn.addEventListener('click', openDrawer);
      navInner.appendChild(navBtn);
      badge = navBtn.querySelector('.cart-count');
    }

    overlay = document.createElement('div');
    overlay.className = 'cart-overlay';
    overlay.hidden = true;
    overlay.addEventListener('click', closeDrawer);

    drawer = document.createElement('aside');
    drawer.className = 'cart-drawer';
    drawer.setAttribute('aria-label', 'Shopping cart');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML =
      '<div class="cart-head">' +
        '<span class="cart-title">Cart</span>' +
        '<button class="cart-close" type="button" aria-label="Close cart">&times;</button>' +
      '</div>' +
      '<div class="cart-body"></div>' +
      '<div class="cart-foot">' +
        '<div class="cart-subtotal"><span>Subtotal</span><span class="cart-subtotal-val">$0</span></div>' +
        '<p class="cart-note">Cart total excludes shipping and taxes.</p>' +
        '<button class="btn-buy cart-checkout" type="button" disabled>Checkout</button>' +
        '<p class="cart-msg" role="status"></p>' +
      '</div>';

    document.body.appendChild(overlay);
    document.body.appendChild(drawer);

    listEl = drawer.querySelector('.cart-body');
    subEl = drawer.querySelector('.cart-subtotal-val');
    checkoutBtn = drawer.querySelector('.cart-checkout');
    msgEl = drawer.querySelector('.cart-msg');

    drawer.querySelector('.cart-close').addEventListener('click', closeDrawer);
    checkoutBtn.addEventListener('click', checkout);
    listEl.addEventListener('click', onListClick);
  }

  function onListClick(e) {
    var t = e.target;
    var id = t.getAttribute && t.getAttribute('data-id');
    if (!id) return;
    if (t.classList.contains('cart-inc')) setQty(id, (cart[id] || 0) + 1);
    else if (t.classList.contains('cart-dec')) setQty(id, (cart[id] || 0) - 1);
    else if (t.classList.contains('cart-remove')) setQty(id, 0);
  }

  function render() {
    var n = count();
    if (badge) { badge.textContent = n; badge.hidden = n === 0; }
    if (!listEl) return;

    var ids = Object.keys(cart);
    if (!ids.length) {
      listEl.innerHTML = '<p class="cart-empty">Your cart is empty.</p>';
    } else {
      listEl.innerHTML = ids.map(function (id) {
        var p = CATALOG[id] || {};
        var line = (typeof p.price === 'number' ? p.price : 0) * cart[id];
        return '<div class="cart-line">' +
          '<img class="cart-line-img" src="' + esc(p.image || '') + '" alt="" width="64" height="48" loading="lazy" />' +
          '<div class="cart-line-info">' +
            '<a class="cart-line-name" href="' + esc(p.url || '#') + '">' + esc(p.name || id) + '</a>' +
            '<div class="cart-qty">' +
              '<button class="cart-dec" type="button" data-id="' + esc(id) + '" aria-label="Decrease quantity">&minus;</button>' +
              '<span class="cart-qty-val">' + cart[id] + '</span>' +
              '<button class="cart-inc" type="button" data-id="' + esc(id) + '" aria-label="Increase quantity">+</button>' +
              '<button class="cart-remove" type="button" data-id="' + esc(id) + '">remove</button>' +
            '</div>' +
          '</div>' +
          '<span class="cart-line-price">' + fmt(line) + '</span>' +
        '</div>';
      }).join('');
    }

    if (subEl) subEl.textContent = fmt(subtotal());
    if (checkoutBtn) checkoutBtn.disabled = n === 0;
  }

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    overlay.hidden = false;
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    overlay.hidden = true;
  }

  function checkout() {
    var items = Object.keys(cart).map(function (id) { return { id: id, qty: cart[id] }; });
    if (!items.length) return;
    checkoutBtn.disabled = true;
    var original = checkoutBtn.textContent;
    checkoutBtn.textContent = 'Starting checkout…';
    if (msgEl) msgEl.textContent = '';

    fetch(WORKER_URL + '/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: items })
    })
      .then(function (r) {
        if (!r.ok) throw new Error('checkout ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (data && data.url) { window.location.href = data.url; }
        else { throw new Error('no checkout url'); }
      })
      .catch(function () {
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = original;
        if (msgEl) msgEl.textContent = 'Online checkout is unavailable right now — email absolutelyplausible@gmail.com to buy.';
      });
  }

  // ── Post-checkout return (Stripe redirects to /?order=success|cancel) ──
  function showToast(title, body) {
    var el = document.createElement('div');
    el.className = 'order-toast';
    el.setAttribute('role', 'status');
    el.innerHTML =
      '<div class="order-toast-text"><strong>' + esc(title) + '</strong>' + esc(body) + '</div>' +
      '<button class="order-toast-close" type="button" aria-label="Dismiss">&times;</button>';
    document.body.appendChild(el);
    function dismiss() { if (el.parentNode) el.parentNode.removeChild(el); }
    el.querySelector('.order-toast-close').addEventListener('click', dismiss);
    setTimeout(dismiss, 9000);
  }

  function handleOrderReturn() {
    var params;
    try { params = new URLSearchParams(window.location.search); } catch (e) { return; }
    var order = params.get('order');
    if (!order) return;

    if (order === 'success') {
      cart = {};
      persist();
      render();
      showToast('Thank you!', 'Your order is confirmed — a receipt is on its way to your email.');
    } else if (order === 'cancel') {
      showToast('Checkout canceled', 'No charge was made — your cart is still here when you’re ready.');
    }

    // Strip the order params so a refresh or shared link doesn't re-fire the toast.
    params.delete('order');
    params.delete('session_id');
    var qs = params.toString();
    var url = window.location.pathname + (qs ? '?' + qs : '') + window.location.hash;
    try { window.history.replaceState({}, document.title, url); } catch (e) { /* no-op */ }
  }

  // ── Add-to-cart buttons (product pages) ────────────────────
  function wireButtons() {
    document.querySelectorAll('.btn-buy[data-product-id]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.dataset.productId;
        var qty = parseInt(btn.dataset.qty, 10) || 1;
        if (id) add(id, qty);
      });
    });
  }

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });

  buildUI();
  wireButtons();
  render();
  handleOrderReturn();
})();
