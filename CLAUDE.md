# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static portfolio site for [robotfantome.com](https://robotfantome.com) — rebuilt in plain HTML/CSS/JS with zero build tools and zero dependencies. Everything ships as-is.

**Live site:** [robotfantome.com](https://robotfantome.com)

## Deployment

Pushes to `main` auto-deploy via **Cloudflare Pages** (connected directly to this GitHub repo). No build step — the repo root is served directly. No GitHub Actions workflow needed.

To preview locally, just open `index.html` in a browser, or use any static file server:

```sh
python3 -m http.server 8080
```

## Architecture

Single-page site with one file per concern:

| File | Role |
|---|---|
| `index.html` | All content and structure (single page, 8 tabs) |
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
- **Layout:** CSS Grid `296px 1fr` (sidebar + main), max-width 1280px
- **CRT scanlines overlay:** `body::before` pseudo-element, z-index 9999
- **Glow effects:** `--glow-accent` and `--glow-mid` CSS vars used for `text-shadow` / `box-shadow`
- **Motion:** glitch/flicker are occasional, subtle bursts; `prefers-reduced-motion` disables all motion
- **Card shadow:** `--card-shadow` for white cards lifting off the cool paper bg

Content is split into tabs (`.gh-panel`), switched by the top nav and Overview pinned cards: overview, gallery, opensource, mix-tape, sustainability, about, volunteer, absolutely plausible. The Gallery tab groups visual work into Artwork / Projects / Events sections.

## Constraints

- No npm, no bundlers, no frameworks — keep it that way.
- All images carry CC BY-NC 4.0 licensing; preserve attribution notices in HTML.
- Version number lives in `VERSION` file — update both `VERSION` and the footer `<p class="footer-version">` on every meaningful change.
