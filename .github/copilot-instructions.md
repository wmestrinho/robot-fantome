# Copilot instructions — Robot Fantôme

**Canonical agent guidance lives in [`CLAUDE.md`](../CLAUDE.md). Read it first
and treat it as authoritative — this file only orients Copilot, it does not
restate the rules.**

Music portfolio site for Robot Fantôme at `robotfantome.com`: plain HTML/CSS/JS,
zero build tools, zero dependencies, auto-deployed via GitHub Pages on push to
`main`. See `CLAUDE.md` for the design system, tab structure, brand palette,
image/attribution standard, and version-bump rule (`VERSION` ↔ footer).

## Division of labor
Copilot: inline completions in `js/main.js` and CSS, in-editor explanations.
Leave deploys and content/brand/layout decisions to Claude Code.

## Commits
Convention: `type(scope): subject`.
