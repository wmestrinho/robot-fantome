# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Music portfolio + small shop for Robot Fantôme (indie / punk / rock, Orlando, FL) at [robotfantome.com](https://robotfantome.com) — plain HTML/CSS/JS with zero build tools and zero dependencies. Everything ships as-is.

**Live site:** [robotfantome.com](https://robotfantome.com)

## Deployment

Pushes to `main` auto-deploy via **GitHub Pages** (Pages source = `main` branch, root path). No build step — the repo root is served as-is. The custom domain `robotfantome.com` is set by the root `CNAME` file; Cloudflare sits in front for DNS/CDN. The `.nojekyll` file keeps GitHub Pages from running Jekyll.

To preview locally, just open `index.html` in a browser, or use any static file server:

```sh
python3 -m http.server 8080
```

## Files

| Path | Role |
|---|---|
| `index.html` | The single-page site: 4 tabs (`.gh-panel`) + sidebar + footer. Two blocks are **generated** (see below). |
| `shop/<id>.html` | One static page per product — **generated**, never hand-edit. |
| `shop/products.json` | Source of truth for the shop (prices, stock, copy, `featured`, `draft`). |
| `scripts/build_shop.py` | Local authoring tool (stdlib only). Regenerates product pages, `js/shop-catalog.js`, the two card blocks in `index.html`, the footer version on every page, and `sitemap.xml`. `--check` exits 1 if anything is stale. |
| `privacy.html`, `terms.html` | Legal pages; share the nav/footer chrome with the product pages. |
| `css/style.css` | All styles. Tokens in `:root`; DIY product-page layout (hard borders, offset shadows). |
| `js/main.js` | Every page: image fade-in, mobile nav toggle, footer year, mailing-list form → Worker `/subscribe`. Tab switching only runs when `.gh-panel`s exist (index). |
| `js/cart.js` | localStorage cart drawer + nav button; POSTs `{items}` to the Worker `/checkout`. Display-only — the Worker re-prices. |
| `js/shop-catalog.js` | `window.RF_CATALOG` — **generated**. |
| `VERSION` | Single source of truth for the version (bare SemVer, e.g. `4.9.0-beta.1`). |
| `assets/images/`, `assets/icons/` | Photos/artwork (CC BY-NC 4.0) and monochrome SVG social icons. |

**Shop edit loop:** edit `shop/products.json` → `python3 scripts/build_shop.py` → commit everything it wrote. Checkout backend is the separate `shop-api` Worker repo (`https://shop-api.robotfantome.com`); this repo never holds secrets.

## Design System

Defined via CSS custom properties in `:root` inside `css/style.css`:

- **Brand palette (Robot Fantôme sticker theme, requested by Luiz 2026-09-11):** black ink, white paper, and golden watercolour drawn from both original Robô Fantasma stickers. This project-specific theme supersedes the previous indigo/teal appearance.
  - `--sticker-gold` is the button/active-tab surface; `--accent` is dark ochre for readable links; `--color-text` is ink. All component colours use the tokens in `css/style.css`.
  - Originals: `assets/images/shop/robot-ghost-rising.png` (374×600) and `robot-ghost-standing.png` (340×600). Preserve transparency, white die-cut borders, lettering, artist signatures, and proportions. Do not redraw or recolour them.
- **Font:** Share Tech Mono throughout — hierarchy via size, letter-spacing, text-transform only
- **Layout:** CSS Grid, max-width 960px. Preserve the current tab structure, content order, sidebar, galleries, music player, and checkout. Paper cards use ink borders, modest rounded corners, offset shadows, and pressed controls. Both mascots frame the existing home title; smaller appearances have reserved space in tab introductions and the shared footer. The profile sidebar shows only on Blog & Story.
- **Effects:** no CRT scanlines, glow, or glitch animations (retired — don't add them back). Motion is limited to functional hover/press feedback and respects `prefers-reduced-motion`.
- **Stylesheet structure:** one base layer, plus a short `SHARED STICKER SURFACES` section holding group-selector treatments. Edit base rules instead of stacking same-selector overrides.

## Content structure

Four tabs (`.gh-panel`), switched by the top nav and pinned cards, deep-linkable via URL hash (bare URL = music):

- **music press-kit** (home, panel id `music`) — hero card, EPK bio, EP player, streaming links, upcoming shows, live gallery, shop preview (generated from products with `"featured": true`), contact/mailing card, pinned grid.
- **shop** (`shop`) — intro line + the full product grid (generated).
- **blog** (`blog`) — posts, then the Absolutely Plausible block with artwork/projects/events timeline, volunteer work, and the full résumé; the profile sidebar shows here.
- **mix-tape** (`mixtape`) — artists we love.

Legacy hashes `#press`, `#about`, `#volunteer`, `#ap`, `#overview` alias to their new homes in `js/main.js`. The nav also carries an external link to absolutelyplausible.com — there is no AP panel.

**No section titles:** panels and sections carry no heading elements — context lives in body text and captions; don't add headers back.

**Footer** (identical on every page, emitted by the generator for product pages): AP logo + "an Absolutely Plausible production" linking to absolutelyplausible.com, then the `Photos & artwork © <year> robot fantôme — CC BY-NC 4.0 — privacy · shop terms` line, then `.footer-version` last.

**Image standard:** every content photo is a `.gallery-item` figure — thumbnail wrapped in `<a class="gallery-link">` linking to the image's own public URL, with a `.gallery-caption` that carries attribution (CC BY-NC 4.0 and/or an Instagram/source link). New photos must follow this pattern. The Events timeline is sourced from `journey.md` in the `absolutelyplausible-business-plan` repo (one entry per documented Instagram post).

## Constraints

- No npm, no bundlers, no frameworks — keep it that way.
- Photos and artwork are CC BY-NC 4.0; preserve attribution notices in HTML. Source code is under the repo `LICENSE` (all rights reserved) — don't describe the code as CC.
- Never hand-edit generated output (`shop/*.html`, `js/shop-catalog.js`, the marker blocks in `index.html`, `sitemap.xml`, footer version strings). Change the source and rerun `scripts/build_shop.py`.
- **Version:** bump `VERSION` on every behaviour/UI change, add a CHANGELOG entry, then run `python3 scripts/build_shop.py` to stamp the footers. Conventions: see `ap-ops-workspace/PROJECT-RULES.md`.
- Before committing: `python3 scripts/validate_agent_baseline.py && python3 scripts/build_shop.py --check`.
