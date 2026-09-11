# robot fantôme — robotfantome.com

Music portfolio and creative home of Robot Fantôme / Absolutely Plausible,
in plain HTML/CSS/JS. No Canva. No build tools. No dependencies. Just our code.

The visual system follows the two original Robô Fantasma stickers: black ink,
white paper, golden watercolour accents, die-cut edges, and pressed controls.
The existing four-tab layout, content order, sidebar, galleries, and shop stay
intact. Theme tokens live in `css/style.css`; both transparent originals are
`assets/images/shop/robot-ghost-rising.png` and `robot-ghost-standing.png`.

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

Single source of truth: the `VERSION` file (bare SemVer, e.g. `4.9.0-beta.1`).
`scripts/build_shop.py` stamps `v<VERSION>` into the footer of every page
(`index.html`, `privacy.html`, `terms.html`, and each `shop/*.html`), so bump
`VERSION`, add a CHANGELOG entry, and rerun the generator. Do not trust
hardcoded version strings in docs.

## Shop & generated files

`shop/products.json` is the source of truth for the shop. After editing it (or
`VERSION`), run:

```sh
python3 scripts/build_shop.py
```

It rewrites `shop/<id>.html`, `js/shop-catalog.js`, the product-card blocks in
`index.html`, every footer version, and `sitemap.xml`. Never hand-edit those.
Checkout is handled by the separate `shop-api` Cloudflare Worker.

The sticker pack's optional `images` list supplies both original artworks
(path, alt text, and real dimensions) to its existing card/detail media slot.
Other products keep their single `image`. Decorative mascot appearances reuse
the same originals; preserve their white borders, signatures, and proportions.

## Validation

```sh
python3 scripts/validate_agent_baseline.py
python3 scripts/build_shop.py --check   # exit 1 if generated files are stale
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
