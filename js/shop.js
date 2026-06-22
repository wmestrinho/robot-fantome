/* robot fantôme — shop.js
   Buy buttons → POST to the checkout Worker, redirect to Stripe Checkout.
   The Worker itself is a separate repo (track #4); until it is live this
   fails gracefully with a "checkout coming soon" message. No card handling
   ever happens here — Stripe's hosted page does that. */

(function () {
  'use strict';

  var meta = document.querySelector('meta[name="shop-worker-url"]');
  var WORKER_URL = (meta && meta.content) || '';

  function setMsg(btn, text) {
    var note = btn.parentNode.querySelector('.product-buy-note');
    if (note) note.textContent = text;
  }

  document.querySelectorAll('.btn-buy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.dataset.productId;
      var qty = parseInt(btn.dataset.qty, 10) || 1;
      if (!id) return;

      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Starting checkout…';

      fetch(WORKER_URL + '/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: [{ id: id, qty: qty }] })
      })
        .then(function (r) {
          if (!r.ok) throw new Error('checkout ' + r.status);
          return r.json();
        })
        .then(function (data) {
          if (data && data.url) {
            window.location.href = data.url;
          } else {
            throw new Error('no checkout url');
          }
        })
        .catch(function () {
          btn.disabled = false;
          btn.textContent = original;
          setMsg(btn, 'Checkout is coming soon — email absolutelyplausible@gmail.com to buy now.');
        });
    });
  });
})();
