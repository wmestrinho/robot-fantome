# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [4.10.1-beta.1] - 2026-09-08
### Fixed
- Mailing-list form now actually disappears after a successful signup (the flex rule was overriding the `hidden` attribute).

## [4.10.0-beta.1] - 2026-09-08
### Added
- Mailing-list signup form on the home tab, posting to the Worker's new `POST /subscribe` (honeypot + rate cap on the Worker side). Falls back to a mailto: form without JavaScript.

### Changed
- Privacy notice: mailing-list section now describes the subscriber list we keep (Cloudflare KV) and how to leave; effective date moved to 2026-09-08.
- Events timeline: DJ Pallet Table dated July 2026 (no longer "in progress").

## [4.9.2-beta.1] - 2026-09-08
### Changed
- Switching to a tab now loads that tab's images immediately instead of waiting on the browser's lazy-load timer (other tabs stay lazy).
- EPK lead photo is the press portrait (`press-profile.jpg`) again; the wide CityArts live shot opens the live gallery and stays the social-card image.
- Shop hero photos capped at 1200px / JPEG q80 (35–45% smaller); sticker and “Art is Local” photos converted from PNG to JPEG (75% smaller). Tracked assets 11.1 MB → 6.4 MB.

### Removed
- 11 unreferenced photos under `assets/images/` (kept in git history).

## [4.9.1-beta.1] - 2026-09-08
### Changed
- One source for the site chrome: `scripts/build_shop.py` now splices the header and footer into `index.html`, `privacy.html`, and `terms.html` (`<!-- chrome:nav -->` / `<!-- chrome:footer -->` markers) as well as the product pages.
- `css/style.css`: the DIY override layer is folded into the base rules where selectors match (1606 → 1473 lines); verified by computed-style diff on every page. Only group-selector overrides remain in the DIY section.
- Blog & Story: artwork and project captions link to the matching shop prints instead of repeating them; stale "11+ years running" dropped; pinned-card teasers no longer repeat the nav and Shop intro word for word.
- `robots.txt` disallows crawling of repo housekeeping (`/scripts/`, `/.github/`, `*.md`, `*.py`).

### Removed
- `design-qa.md` and `STOREFRONT_UPGRADE_PLAN.md` (completed; history stays in git and this changelog).

## [4.9.0-beta.1] - 2026-09-08
### Added
- Pathlight Kitchen certificates (Culinary Program, Dining Room & Service Skills) shown in the résumé with downloadable PDFs.
- Mobile nav toggle and the Absolutely Plausible link on product, privacy, and terms pages (previously those pages had no navigation below 1000px).
- Footer version + privacy / shop-terms links on every page; footer © year set by JS.
- `sitemap.xml` now generated with every live product page; `lastmod` from git.
- Home-tab shop preview generated from `shop/products.json` (`"featured": true`).
- Cart drawer: `role="dialog"`, focus moves to Close on open and back on close.

### Fixed
- Sidebar social icons were mislabeled files (Instagram showed the TikTok glyph, LinkedIn a Twitter bird, Facebook a YouTube button, TikTok the LinkedIn mark, Twitter a Discord controller, YouTube a paper plane). Replaced with accurate monochrome glyphs (Simple Icons, CC0); unused `discord.svg` removed.

### Changed
- `scripts/build_shop.py` owns the shared nav/footer chrome, stamps `VERSION` into every footer, and regenerates the sitemap; `--check` covers all of it.
- `js/main.js` runs on every page; tab logic only activates on `index.html`.
- Nav links carry real hashes (`#shop`, `#blog`, `#mixtape`) instead of `#`.
- Footer license line reads “Photos & artwork © … CC BY-NC 4.0” (code is under `LICENSE`).
- Legal pages: theme-color matches the site; inline styles replaced by classes.

### Removed
- ~390 lines of dead CSS (retired GitHub-profile / press-strip / trust-badge / avatar rules, CRT scanline, glitch + flicker + scan keyframes); DIY token overrides merged into `:root`.

## [4.8.6-beta.1] - 2026-09-05
### Added
- Initial changelog baseline.
