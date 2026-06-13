# ECOMMERCE_BRIEF.md — Robot Fantôme Shop

> Handoff spec for the agent building the store. Read `AGENTS.md` and `CLAUDE.md`
> first — the same baseline rules apply (version bump, no build step on the static
> site, preserve the design system). This brief defines **what to build and the
> contract between the two halves**; it does not prescribe every line.

## Decision (already made by Luiz)

- **Platform:** Stripe Checkout fronted by a thin **Cloudflare Worker**. Not Shopify,
  not Big Cartel. We own the checkout; the marketing site stays a static GitHub Pages site.
- **Placement:** the store is its **own "Shop" tab** in the existing nav
  (`music press-kit · shop · blog · mix-tape · absolutely plausible ↗`).
- **Why this stack:** zero monthly fees (Stripe ~2.9% + 30¢ only), full UX control,
  Cloudflare is already in front of the domain, and it matches the site's
  DIY / zero-dependency ethos.

## Two repos / two responsibilities

| Half | Lives where | Owns |
|---|---|---|
| **Storefront** | THIS repo (`robot-fantome`, static) | Shop tab UI, product catalog JSON, product images, "Buy" buttons that call the Worker |
| **Checkout backend** | NEW separate repo (a Cloudflare Worker) | Stripe session creation, webhook handling, inventory, order-notification email. Holds ALL secrets. |

**Hard security rule:** no Stripe secret key, webhook secret, or any credential ever
goes into this static repo. The static site only knows the Worker's public URL and
(optionally) the Stripe **publishable** key. All card handling happens on Stripe's
hosted Checkout page — never build a card form on the static site (keeps us out of PCI scope).

## Architecture / flow

```
robotfantome.com (static, this repo)
  Shop tab renders products from shop/products.json
  "Buy" button  ──POST {items:[{id, qty}]}──►  Worker /checkout
                                                  └─ looks up price + stock
                                                  └─ creates Stripe Checkout Session (server-side, secret key)
                                                  └─ returns { url }
  browser redirects to Stripe-hosted Checkout (card, shipping address, receipt)
                                                  Stripe ──webhook checkout.session.completed──► Worker /webhook
                                                                                                  └─ verify signature
                                                                                                  └─ decrement inventory (KV/D1)
                                                                                                  └─ email order to absolutelyplausible@gmail.com
  Stripe redirects buyer back to robotfantome.com/?order=success
```

## Worker endpoints

- `POST /checkout` — body `{ items: [{ id, qty }] }`. Validate against catalog + stock,
  build line items, create Stripe Checkout Session (`mode: payment`,
  `shipping_address_collection` for physical goods), return `{ url }`.
  CORS: allow origin `https://robotfantome.com` only.
- `POST /webhook` — verify `Stripe-Signature` with `STRIPE_WEBHOOK_SECRET` (mandatory).
  On `checkout.session.completed`: decrement/mark sold inventory, send order email.
- Worker secrets (via `wrangler secret put`): `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.
- Inventory store: Cloudflare **KV** keyed by product `id` is enough to start
  (one-of-a-kind items are qty 1 → flip to sold-out on purchase). Move to **D1** only
  if order history/reporting is needed.
- Email: Cloudflare Email Routing/Email Service or Resend. See the `cloudflare-email-service` skill.

> Relevant skills for the build agent: **cloudflare**, **wrangler**,
> **workers-best-practices**, **cloudflare-email-service**.

## Product data contract (this is what the Shop tab renders)

Create `shop/products.json` in this repo. The Worker reads the same shape (or a copy)
as the source of truth for price/stock so the browser is never trusted on price.

```json
[
  {
    "id": "tee-nirvana-washed-01",
    "name": "Upcycled tee — washed Nirvana",
    "type": "physical-unique",
    "price_usd": 35,
    "qty": 1,
    "image": "assets/images/shop/tee-nirvana-washed-01.jpg",
    "description": "One-of-a-kind upcycled shirt. Size M. Ships from Orlando, FL.",
    "shipping": "us",
    "stripe_price_id": null
  }
]
```

`type` values and how each behaves:

| `type` | Examples | Inventory | Shipping |
|---|---|---|---|
| `physical-unique` | upcycled shirts, pallet items | qty 1, sold-out after purchase | `us` for shirts; **pallet items = `local-pickup` or freight only** (heavy/oversized) |
| `physical-stock` | stickers, sticker packs | tracked count | flat-rate or free over $X |
| `print-made-to-order` | collage prints | made on demand (or print-on-demand via Printful/Printify) | per print |
| `digital` | future: download codes | unlimited | none |

## Product scope at launch

- **In scope now:** upcycled shirts (unique), stickers, pallet items (local pickup/freight),
  collage prints (made-to-order or POD).
- **Out of scope for now:** **albums.** Once signed to a label, album sales/distribution
  are usually the label's job. Until then, point album buyers to the existing **Bandcamp**
  link. Don't build album SKUs yet.

## Storefront (this repo) — design constraints

- New `<div class="gh-panel" id="shop">` mirroring the existing panels; add the
  `shop` nav link. Tab switching, hash routing, and legacy-hash aliasing already live
  in `js/main.js` — extend, don't replace.
- Reuse the existing `.gallery-grid` / `.gallery-item` card pattern for product cards
  so the Shop tab inherits the watercolour-cyberpunk look. **No new framework, no build step.**
- Product images follow the existing image standard (see `CLAUDE.md`): real dimensions,
  `loading="lazy"`. Put them in `assets/images/shop/`.
- **No section-title headings** (site rule) — product context lives in card body/captions.
- Bump `VERSION` + footer `<p class="footer-version">` when the Shop tab ships.
- Add `https://robotfantome.com/` Shop view is still one URL; if individual product
  pages are ever wanted for SEO, that's a separate decision (would break zero-build).

## Open questions for Luiz (the build agent should confirm)

1. **Shipping:** flat US rate, free-over-threshold, or live rates? Pallet items pickup-only?
2. **Tax:** enable Stripe Tax, or out-of-scope at launch (FL only)?
3. **Prints:** hold stock, make-to-order by hand, or print-on-demand (Printful/Printify)?
4. **Worker hosting:** new GitHub repo name + Cloudflare account/zone to deploy under.
5. **Email:** order notifications to `absolutelyplausible@gmail.com` only, or also buyer confirmation (Stripe already emails receipts)?
