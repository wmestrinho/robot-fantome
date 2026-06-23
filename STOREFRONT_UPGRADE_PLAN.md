# STOREFRONT_UPGRADE_PLAN.md — Robot Fantôme

> Companion to `ECOMMERCE_BRIEF.md`. Captures the storefront/UX upgrade modelled on
> [anthonymarinellimusic.com](https://anthonymarinellimusic.com) and the plan to extract
> the result into a reusable template. Same baseline rules apply (CLAUDE.md, AGENTS.md):
> zero build on the live static site, preserve the watercolour-cyberpunk design system,
> bump VERSION + footer on every meaningful change.

## Context — why this work

Wagner reviewed anthonymarinellimusic.com as a reference for "what we should have and how
it's placed in our UI." That site is **Shopify** (courses business): full cart, accounts,
search, sale pricing, hosted checkout, clean black/white minimalist skin. We are **not**
adopting its stack (we keep Stripe Checkout + Cloudflare Worker per `ECOMMERCE_BRIEF.md`)
and **not** its visual language (we keep the cyberpunk brand). We are adopting its
**commerce UX structure and placement patterns**, rendered in our own skin.

## Decisions (confirmed by Wagner, 2026-06-23)

1. **Aesthetic:** keep the cyberpunk brand; lean *more minimalist / less fluff* within it
   (consistent with the "minimalist trim" already wanted). No shift toward the clean look.
2. **Checkout:** add a **multi-item cart** (Marinelli-style). localStorage-backed because the
   shop spans per-product static pages; one Stripe Checkout via the Worker's existing
   `POST /checkout {items:[{id,qty}]}` contract (already multi-item — no contract change).
3. **Patterns to adopt (all four):** sale/compare-at pricing · press/testimonial strip ·
   stronger (incentivized) mailing-list signup · footer trust / payment badges.
4. **Template:** build & verify on Robot Fantôme **first**, then extract into a **separate
   new repo** (`storefront-template`), **token-driven** (existing `:root` CSS custom
   properties + a `site-config` + `products.json`) so a new project reskins by editing
   config, not markup. RF stays the default reference skin.

## Reference → our implementation (mapping)

| Marinelli pattern | Our version (in-brand, static) |
|---|---|
| Shopify cart + qty + multi-item checkout | localStorage cart drawer + qty steppers → Worker `/checkout` |
| Regular price struck-through + sale price (30% off) | `compare_at_usd` in `products.json`; struck-through + sale in cards, product pages, JSON-LD |
| Testimonials carousel (industry quotes + headshots) | Press/testimonial strip on the Music tab (quotes + source credit), cyberpunk cards |
| Incentivized mailing-list ("discounts & announcements") | Upgrade the "Get in touch" card → early-drops/subscriber-discount hook (mailto now; Worker `/subscribe` later) |
| Footer payment icons + "secure checkout" trust | "Secure checkout via Stripe" + payment-mark SVGs near buy + footer |
| Banner + `Home / Courses` breadcrumb | Keep our no-headings rule; product pages already have a breadcrumb — light shop-landing polish only |

## Build order (RF first; each step ships + verifies independently)

All product-page/card output is **generated** — edit `shop/products.json` then run
`python3 scripts/build_shop.py` (idempotent, `--check` for CI). Never hand-edit
`shop/<id>.html` or the spliced cards in `index.html`.

1. **Sale / compare-at pricing** (foundation, no JS).
   - `shop/products.json`: add optional `compare_at_usd`.
   - `scripts/build_shop.py`: `card()` + `product_page()` render `<span class="price-was">`
     (struck-through `compare_at`) + `<span class="price-now">`; JSON-LD `Offer.price` = sale
     price, add `priceValidUntil`/`highPrice` only if needed. New `.price-was/.price-now` CSS.
   - Regenerate; `--check` must pass.

2. **Footer trust / payment badges** (CSS + markup + small SVGs).
   - Add `assets/icons/pay-*.svg` (Visa/MC/Amex/Stripe marks, monochrome to suit brand).
   - Add a `.trust-badges` row: in `index.html` footer + emitted into each product page by
     `product_page()`. Strengthen the existing `.product-buy-note` ("Card details never touch
     this site").

3. **Stronger mailing-list** (copy/markup + CSS).
   - Upgrade the "Get in touch" card (`index.html:298-306`): incentive copy
     (early access to drops + subscriber-only discounts), clearer CTA. Keep `mailto:` now;
     leave a `data-` hook + config slot for a real Worker `/subscribe` endpoint later.

4. **Press / testimonial strip** (new Music-tab section).
   - New `.press-quotes` block (quote + attribution/source link), in-brand cards.
   - No section-title heading (site rule) — context in body/caption.

5. **Multi-item cart** (the big one; spans front-end only).
   - `scripts/build_shop.py` emits `js/shop-catalog.js` → `window.RF_CATALOG` (id → {name,
     price, sale, image, url}) so the cart renders line items with zero fetch.
   - New `js/cart.js` (vanilla, IIFE like `main.js`/`shop.js`): localStorage key `rf_cart`,
     add/remove/setQty, subtotal, render a slide-in **cart drawer** + a nav cart button with
     count. "Buy" buttons become **Add to cart**; drawer "Checkout" POSTs `items:[{id,qty}]`
     to the Worker `/checkout` and redirects to Stripe (reuse `shop.js` fetch/fail-soft logic).
   - Inject the drawer markup + nav cart button + `<script src="../js/cart.js">` into every
     product page via `product_page()`, and into `index.html` (nav + drawer + script).
   - Browser cart is **display-only**; Worker re-prices from catalog (price integrity).

6. **Minimalist trim pass** (light) — tighten shop copy/whitespace per decision #1.

## Phase 2 — extract `storefront-template` (separate repo)

After RF features are verified:

- New repo `storefront-template`: generalized copy of the storefront subsystem
  (`shop/`, `scripts/build_shop.py`, shop CSS partials, `js/{cart,shop}.js`, the Worker
  contract doc), **not** the music-specific tabs/content.
- **Tokenization:** brand entirely via the existing `:root` CSS custom properties +
  a new `site.config.json` (site name, domain, colors→token overrides, fonts, socials,
  worker URL, currency). `build_shop.py` reads `site.config.json` for `SITE`/worker URL/
  footer instead of the hardcoded constants it has today.
- Ship a neutral placeholder skin + RF as the documented example reskin; a README with the
  "edit config + tokens + products.json, run the generator" workflow.
- The checkout **Worker** repo (ECOMMERCE_BRIEF track #4) is a sibling, referenced by URL.

## Files touched (RF phase)

- `shop/products.json` — `compare_at_usd`; (later) catalog feeds `shop-catalog.js`.
- `scripts/build_shop.py` — pricing render, trust badges, catalog emit, cart-drawer/nav inject.
- `css/style.css` — `.price-was/.price-now`, `.trust-badges`, `.press-quotes`, cart drawer/nav.
- `index.html` — mailing-list upgrade, press strip, footer badges, nav cart button, drawer, script.
- `js/cart.js` (new), `js/shop-catalog.js` (generated), `assets/icons/pay-*.svg` (new).
- `VERSION` + footer `<p class="footer-version">` — bump per change.
- `CLAUDE.md` — note cart + the four patterns when shop ships (also "3 tabs" → 4, already pending).

## Verification

- `python3 scripts/build_shop.py && python3 scripts/build_shop.py --check` → "up to date", exit 0
  (output stays in sync; CI-safe).
- Local: `python3 -m http.server 8080`, open `index.html` → Shop tab; open a product page;
  add multiple items, change qty, remove, see subtotal; Checkout fails *soft* (Worker offline)
  with the "coming soon" message; cart persists across page loads (localStorage).
- Sale pricing: struck-through `was` + `now` render on card + product page; JSON-LD `Offer.price`
  equals the sale price; draft products still emit `noindex,nofollow`.
- `prefers-reduced-motion` disables drawer/strip motion; keyboard-operable cart + drawer.
