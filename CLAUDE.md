# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Music portfolio site for Robot Fantôme (indie / punk / rock, Orlando, FL) at [robotfantome.com](https://robotfantome.com) — plain HTML/CSS/JS with zero build tools and zero dependencies. Everything ships as-is.

**Live site:** [robotfantome.com](https://robotfantome.com)

## Deployment

Pushes to `main` auto-deploy via **GitHub Pages** (Pages source = `main` branch, root path). No build step — the repo root is served as-is. The custom domain `robotfantome.com` is set by the root `CNAME` file; Cloudflare sits in front for DNS/CDN. The `.nojekyll` file keeps GitHub Pages from running Jekyll.

To preview locally, just open `index.html` in a browser, or use any static file server:

```sh
python3 -m http.server 8080
```

## Architecture

Single-page site with one file per concern:

| File | Role |
|---|---|
| `index.html` | All content and structure (single page, 3 tabs; Music Press-Kit is the home tab) |
| `css/style.css` | All styles — GitHub profile layout, cool watercolour cyberpunk |
| `js/main.js` | Tab switching, pinned card clicks, mobile nav toggle, image fade-in |
| `assets/images/` | Photos and artwork (CC BY-NC 4.0 licensed) |
| `assets/icons/` | SVG social media icons |
| `assets/favicon.png` | Site favicon (Absolutely Plausible logo) |
| `VERSION` | Single source of truth for version number (displayed in footer) |

## Design System

Defined entirely via CSS custom properties in `:root` inside `css/style.css`:

- **Brand palette (Absolutely Plausible / Robot Fantôme):** cool watercolour identity — teal → blue → violet, anchored by the AP logo steel-blue. This is the brand standard; never reintroduce the retired orange palette.
  - `--accent` `#3f7d9c` (AP logo steel-blue, primary) · `--accent-mid` `#4b5fa8` (indigo-blue) · `--accent-deep` `#6a4f9e` (violet) · `--accent-teal` `#5cb0ad` (highlight)
  - Background: faint cool paper `#eef0f2` · surfaces `#ffffff`, `#f5f6f9` · text `#1e2238` · muted `#5f6480`
- **Font:** Share Tech Mono throughout — hierarchy via size, letter-spacing, text-transform only
- **Layout:** CSS Grid, max-width 1280px — full-width main by default; the `296px` profile sidebar (`.gh-sidebar`) shows only on the Blog & Story tab, toggled by the `.show-sidebar` class on `.gh-layout`
- **CRT scanlines overlay:** `body::before` pseudo-element, z-index 9999
- **Glow effects:** `--glow-accent` and `--glow-mid` CSS vars used for `text-shadow` / `box-shadow`
- **Motion:** glitch/flicker are occasional, subtle bursts; `prefers-reduced-motion` disables all motion
- **Card shadow:** `--card-shadow` for white cards lifting off the cool paper bg

Content is split into 3 tabs (`.gh-panel`), switched by the top nav and pinned cards: **music press-kit** (home, panel id `music` — hero card, EPK bio, EP player, upcoming shows, streaming links, press photos, live gallery, contact/mailing card, pinned grid), **blog** (Blog & Story — posts, then the merged Absolutely Plausible section with artwork/projects/events timeline, volunteer work, and the full résumé; the profile sidebar shows here), and **mix-tape**. The nav also carries an external link to absolutelyplausible.com — there is no AP panel on this site anymore. Tabs are deep-linkable via URL hash (bare URL = music); legacy hashes `#press`, `#about`, `#volunteer`, `#ap`, `#overview` alias to their new homes in `js/main.js`. **No section titles:** panels and sections carry no heading elements (`.resume-block-title` and `.gh-panel-header` are retired) — context lives in body text and captions; don't add headers back. The footer is the Absolutely Plausible standard: AP logo + "an Absolutely Plausible production" linking to absolutelyplausible.com, above the CC license and version lines.

**Image standard:** every content photo is a `.gallery-item` figure — thumbnail wrapped in `<a class="gallery-link">` linking to the image's own public URL, with a `.gallery-caption` that carries attribution (CC BY-NC 4.0 and/or an Instagram/source link). New photos must follow this pattern. The Absolutely Plausible tab carries the gallery — Artwork / Projects / Events. The Events timeline is sourced from `journey.md` in the `absolutelyplausible-business-plan` repo (one entry per documented Instagram post).

## Constraints

- No npm, no bundlers, no frameworks — keep it that way.
- All images carry CC BY-NC 4.0 licensing; preserve attribution notices in HTML.
- Version number lives in `VERSION` file — update both `VERSION` and the footer `<p class="footer-version">` on every meaningful change.
