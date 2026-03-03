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
| `index.html` | All content and structure (single page, 7 tabs) |
| `css/style.css` | All styles — GitHub profile layout, warm off-white + amber cyberpunk |
| `js/main.js` | Tab switching, pinned card clicks, mobile nav toggle, image fade-in |
| `assets/images/` | Photos and artwork (CC BY-NC 4.0 licensed) |
| `assets/icons/` | SVG social media icons |
| `assets/favicon.png` | Site favicon (Absolutely Plausible logo) |
| `VERSION` | Single source of truth for version number (displayed in footer) |

## Design System

Defined entirely via CSS custom properties in `:root` inside `css/style.css`:

- **Palette:** Warm off-white bg (`#f0eeeb`) · card surfaces (`#ffffff`, `#f8f6f3`) · amber accent (`#d4621a`) · copper (`#9c5220`) · rust (`#6b3310`)
- **Font:** Share Tech Mono throughout — hierarchy via size, letter-spacing, text-transform only
- **Layout:** CSS Grid `296px 1fr` (sidebar + main), max-width 1280px
- **CRT scanlines overlay:** `body::before` pseudo-element, z-index 9999
- **Glow effects:** `--glow-orange` and `--glow-copper` CSS vars used for `text-shadow` / `box-shadow`
- **Card shadow:** `--card-shadow` for white cards lifting off warm bg

Section structure in HTML uses `module_01` through `module_06` labels, rendered as tabs via `.gh-tab` / `.gh-panel`.

## Constraints

- No npm, no bundlers, no frameworks — keep it that way.
- All images carry CC BY-NC 4.0 licensing; preserve attribution notices in HTML.
- Version number lives in `VERSION` file — update both `VERSION` and the footer `<p class="footer-version">` on every meaningful change.
