# Copilot instructions — Robot Fantôme

Authoritative agent guidance for this repo lives in [`CLAUDE.md`](../CLAUDE.md).
This file mirrors the key rules so Copilot's inline help stays aligned.

## What this repo is
Music portfolio site for Robot Fantôme (indie/punk/rock, Orlando FL) at
`robotfantome.com`. Plain HTML/CSS/JS, **zero build tools, zero dependencies** —
ships as-is. Auto-deploys via GitHub Pages on push to `main` (root path, custom
domain via `CNAME`, `.nojekyll` present).

## Rules that matter
- **Version:** `VERSION` file is the single source of truth, shown in the footer
  (`<p class="footer-version">`). Update both on every meaningful change.
- **Single-page, 3 tabs** (`.gh-panel`): music press-kit (home), blog, mix-tape;
  switched in `js/main.js`, deep-linkable via URL hash.
- **No section titles:** panels/sections carry no heading elements
  (`.resume-block-title`, `.gh-panel-header` are retired) — don't add headers back.
- **Brand palette:** cool watercolour (teal → blue → violet, AP steel-blue
  `--accent #3f7d9c`). Never reintroduce the retired orange palette.
- **Images:** every content photo is a `.gallery-item` with a `.gallery-caption`
  carrying CC BY-NC 4.0 attribution — follow the pattern, preserve notices.
- **No npm/bundlers/frameworks.**

## Paired sources of truth — never auto-edit without review
- `VERSION` ↔ footer `<p class="footer-version">`.

## Division of labor
Copilot: inline completions in `js/main.js` and CSS, in-editor explanations.
Leave deploys and content/brand/layout decisions to Claude Code.

## Commits
Convention: `type(scope): subject`.
