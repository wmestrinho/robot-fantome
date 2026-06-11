# robot fantôme — robotfantome.com

Music portfolio and creative home of Robot Fantôme / Absolutely Plausible,
in plain HTML/CSS/JS. No Canva. No build tools. No dependencies. Just our code.

**Live:** [robotfantome.com](https://robotfantome.com)

To preview locally:

```sh
python3 -m http.server 8080
```

## Deployment

**GitHub Pages**, from the `main` branch, root path. Every push to `main`
auto-deploys — there is no build step; the repo root is served as-is.

- `CNAME` sets the custom domain (`robotfantome.com`)
- Cloudflare sits in front for DNS/CDN only
- `.nojekyll` keeps GitHub Pages from running Jekyll

> Historical note: the site once deployed via Cloudflare Workers/Pages with
> Wrangler. That path is retired — `wrangler.jsonc` was removed 2026-06-11,
> and none should be added back without changing this section first.

## Version

Single source of truth: the `VERSION` file. The same string is displayed in
the site footer (`<p class="footer-version">` in `index.html`). Bump both on
every meaningful change. Do not trust hardcoded version strings in docs.

## Validation

```sh
python3 scripts/validate_agent_baseline.py
```

---

*absolutely plausible by robot fantôme*

---

## AI Agent Handoff

Canonical local path:

- `/Users/wmestrinho/Workspace/Projects/robot-fantome`

Before editing:

- Read `AGENTS.md` and `CLAUDE.md`.
- Check `git status --short --branch`.
- Run the validation script before committing.
