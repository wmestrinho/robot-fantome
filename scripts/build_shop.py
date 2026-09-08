#!/usr/bin/env python3
"""Generate the Robot Fantôme shop and keep the site's shared chrome in sync.

This is a *local authoring tool*, not a server build step — it writes plain
static files that ship as-is (keeps the zero-dependency / zero-build ethos).

Reads shop/products.json + VERSION, then:
  1. Writes one crawlable static page per product:  shop/<id>.html
     (own <title>, canonical, Open Graph, Product JSON-LD, shared nav + footer).
  2. Writes js/shop-catalog.js (window.RF_CATALOG) for the cart drawer — display only;
     the checkout Worker re-prices every line server-side.
  3. Splices product cards into index.html:
       Shop tab       → between <!-- shop:cards:start -->    and <!-- shop:cards:end -->
       Home preview   → between <!-- shop:featured:start --> and <!-- shop:featured:end -->
                        (products with "featured": true, in catalog order)
  4. Splices the shared header and footer into index.html, privacy.html, terms.html
     between <!-- chrome:nav:start/end --> and <!-- chrome:footer:start/end --> (the
     product pages get the same chrome inline), stamping `v<VERSION>` into the footer
     so the VERSION file stays the single source of truth.
  5. Writes sitemap.xml — home, legal pages, and every non-draft product page, with
     <lastmod> taken from each file's last git commit (today if the file is modified).

Usage:
    python3 scripts/build_shop.py          # regenerate everything
    python3 scripts/build_shop.py --check  # exit 1 if any output would change (CI/pre-commit)

Stdlib only. Run from anywhere; paths are resolved relative to the repo root.
"""

import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://robotfantome.com"

CARD_START = "<!-- shop:cards:start -->"
CARD_END = "<!-- shop:cards:end -->"
FEATURED_START = "<!-- shop:featured:start -->"
FEATURED_END = "<!-- shop:featured:end -->"
NAV_START = "<!-- chrome:nav:start -->"
NAV_END = "<!-- chrome:nav:end -->"
FOOTER_START = "<!-- chrome:footer:start -->"
FOOTER_END = "<!-- chrome:footer:end -->"

# Pages (besides the generated product pages) whose footer version is kept in sync.
VERSIONED_PAGES = ["index.html", "privacy.html", "terms.html"]

AVAILABILITY = {
    "sold-out": "https://schema.org/SoldOut",
    "made-to-order": "https://schema.org/MadeToOrder",
    "in-stock": "https://schema.org/InStock",
}

LOGO_SVG = (
    '<svg class="gh-nav-logo" viewBox="0 0 16 16" width="20" height="20" aria-hidden="true">'
    '<path fill="currentColor" d="M9.504.43a1.516 1.516 0 0 1 2.437 1.713L10.415 5.5h2.123c1.57 0 '
    '2.346 1.909 1.22 3.004l-7.34 7.142a1.249 1.249 0 0 1-.871.354h-.302a1.25 1.25 0 0 1-1.157-1.723'
    'L5.633 10.5H3.462c-1.57 0-2.346-1.909-1.22-3.004L9.503.429Zm1.047 1.074L3.286 8.571A.25.25 0 0 '
    '0 3.462 9H6.75a.75.75 0 0 1 .694 1.034l-1.713 4.188 6.982-6.793A.25.25 0 0 0 12.538 7H9.25a.75'
    '.75 0 0 1-.683-1.06l2.008-4.418.003-.006a.036.036 0 0 0-.004-.009l-.006-.006-.008-.001c-.003 '
    '0-.006.002-.009.004Z"/></svg>'
)


def e(text):
    """HTML-escape (and keep the result safe inside attributes too)."""
    return html.escape(str(text), quote=True)


def read_version():
    """VERSION file → bare SemVer string (a leading 'v' is tolerated and stripped)."""
    with open(os.path.join(REPO, "VERSION"), encoding="utf-8") as f:
        v = f.read().strip().splitlines()[0].strip()
    return v[1:] if v.startswith("v") else v


def git_lastmod(relpath):
    """ISO date of the file's last commit; today if it has uncommitted changes or git is unavailable."""
    today = datetime.date.today().isoformat()
    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", relpath],
            cwd=REPO, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if dirty:
            return today
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", relpath],
            cwd=REPO, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        return out or today
    except Exception:
        return today


def fmt_usd(v):
    """'$35' for whole dollars, '$34.50' otherwise."""
    if isinstance(v, float) and not v.is_integer():
        return f"${v:.2f}"
    return f"${int(v)}"


def price_spans(p):
    """Sale-aware price markup: optional struck-through compare-at + sale price (+ % off).

    Renders just the price <span>s; the caller wraps them in .product-price /
    .shop-card-price. `compare_at_usd` (optional) is the original price shown struck
    through when it is higher than `price_usd`.
    """
    price = p.get("price_usd")
    if price is None:
        return '<span class="price-now">Price on request</span>'
    now = f'<span class="price-now">{e(fmt_usd(price))}</span>'
    compare = p.get("compare_at_usd")
    if isinstance(compare, (int, float)) and compare > price:
        off = round((compare - price) / compare * 100)
        return (
            f'<span class="price-was">{e(fmt_usd(compare))}</span> {now}'
            f' <span class="price-save">&minus;{off}%</span>'
        )
    return now


def availability(p):
    if p.get("type") == "print-made-to-order":
        return AVAILABILITY["made-to-order"]
    qty = p.get("qty")
    if qty == 0:
        return AVAILABILITY["sold-out"]
    return AVAILABILITY["in-stock"]


def resolve_image(p, prefix=""):
    """Return the image path; fall back to placeholder.svg if the file is missing."""
    img = p.get("image") or ""
    if not img or not os.path.exists(os.path.join(REPO, img)):
        if img:
            print(f"  ! {p['id']}: image '{img}' not found — using placeholder")
        img = "assets/images/shop/placeholder.svg"
    return prefix + img


# ── Shared chrome (nav + footer) ──────────────────────────────────────────────
# `root` is the relative path back to the site root ("../" from /shop/, "./" at root).

def nav_html(root, active=None, tabs=False):
    """Site header. `tabs=True` (index.html) adds data-tab hooks for js/main.js."""
    def link(tab, label):
        href = root if tab == "music" else f"{root}#{tab}"
        attrs = f' data-tab="{tab}"' if tabs else ""
        attrs += ' class="active" aria-current="page"' if tab == active else ""
        return f'        <a href="{href}"{attrs}>{label}</a>'

    return f"""  <header class="gh-nav">
    <div class="gh-nav-inner">
      <a href="{root}" class="gh-nav-brand" aria-label="robot fantôme home">
        {LOGO_SVG}
        <span class="gh-nav-brand-text">robot fant&ocirc;me</span>
      </a>

      <nav class="gh-nav-links" aria-label="Site navigation">
{link("music", "music press-kit")}
{link("shop", "shop")}
{link("blog", "blog")}
{link("mixtape", "mix-tape")}
        <a href="https://absolutelyplausible.com" target="_blank" rel="noopener" class="gh-nav-external">absolutely plausible &nearr;</a>
      </nav>

      <button class="gh-nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>"""


def footer_html(root, version):
    return f"""  <footer>
    <div class="footer-inner">
      <a href="https://absolutelyplausible.com" target="_blank" rel="noopener" class="footer-ap" aria-label="Absolutely Plausible — official site">
        <img src="{root}assets/images/ap-logo.png" width="707" height="706" alt="Absolutely Plausible logo" class="footer-ap-logo" />
        <span>an Absolutely Plausible production</span>
      </a>
      <p class="footer-license">
        Photos &amp; artwork &copy; <span class="footer-year">{datetime.date.today().year}</span> robot fant&ocirc;me &mdash;
        <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener">CC BY-NC 4.0</a>
        &mdash; <a href="{root}privacy.html">privacy</a> &middot; <a href="{root}terms.html">shop terms</a>
      </p>
      <p class="footer-version">v{e(version)}</p>
    </div>
  </footer>"""


# ── Product pages ─────────────────────────────────────────────────────────────

def product_page(p, currency, worker_url, version):
    """Full standalone HTML for one product page (lives at shop/<id>.html)."""
    pid = p["id"]
    name = p["name"]
    tagline = p.get("tagline", "")
    desc = p.get("description", "")
    meta_desc = p.get("meta_description", "")
    price = p.get("price_usd")
    url = f"{SITE}/shop/{pid}.html"
    img_rel = resolve_image(p, prefix="../")          # for <img> on the page
    img_abs = f"{SITE}/{resolve_image(p)}"            # absolute for OG / schema
    avail = availability(p)
    draft = p.get("draft", False)
    badge = p.get("badge")
    local_pickup = p.get("shipping") == "local-pickup"

    # JSON-LD Product schema
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": desc,
        "image": img_abs,
        "brand": {"@type": "Brand", "name": "Robot Fantôme"},
        "url": url,
        "offers": {
            "@type": "Offer",
            "price": f"{price:.2f}" if isinstance(price, (int, float)) else "0.00",
            "priceCurrency": currency,
            "availability": avail,
            "url": url,
            "seller": {"@type": "Organization", "name": "Robot Fantôme"},
        },
    }
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)

    draft_banner = (
        '\n      <p class="product-draft">DRAFT — placeholder data, not for sale yet.</p>'
        if draft else ""
    )
    badge_html = f'<span class="product-badge">{e(badge)}</span>' if badge else ""
    print_note = (
        '\n        <p class="product-buy-note">Archival print only; original artwork stays in the artist archive.</p>'
        if p.get("type") == "print-made-to-order" else ""
    )

    if local_pickup:
        subject = urllib.parse.quote(f"Shop enquiry — {name}")
        buy_html = (
            '<p class="product-pickup">Local pickup / freight only (heavy &amp; oversized). '
            f'<a href="mailto:absolutelyplausible@gmail.com?subject={subject}">'
            'Email to arrange &rarr;</a></p>'
        )
    else:
        price_label = fmt_usd(price) if price is not None else "Buy"
        buy_html = (
            f'<button class="btn-buy" data-product-id="{e(pid)}" data-qty="1">'
            f'Add to cart &mdash; {e(price_label)}</button>\n'
            '        <p class="product-buy-note">No payment is collected on this page.</p>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(name)} — Robot Fantôme shop</title>
  <meta name="description" content="{e(meta_desc or tagline or desc)}" />
  <meta name="robots" content="{'noindex, nofollow' if draft else 'index, follow, max-image-preview:large'}" />
  <link rel="icon" type="image/png" href="../assets/favicon.png" />
  <link rel="apple-touch-icon" href="../assets/favicon.png" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#4b5fa8" />
  <meta property="og:type" content="product" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content="{e(name)} — Robot Fantôme" />
  <meta property="og:description" content="{e(meta_desc or tagline or desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{img_abs}" />
  <meta property="og:image:alt" content="{e(name)}" />
  <meta property="og:site_name" content="Robot Fantôme" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@robotfantome" />
  <meta name="twitter:title" content="{e(name)} — Robot Fantôme" />
  <meta name="twitter:description" content="{e(meta_desc or tagline or desc)}" />
  <meta name="twitter:image" content="{img_abs}" />
  <meta name="shop-worker-url" content="{e(worker_url)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/style.css" />
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
{nav_html("../", active="shop")}

  <main class="gh-main product-page">
    <p class="product-breadcrumb"><a href="../#shop">&larr; back to shop</a></p>
    <article class="product-detail">
      <div class="product-media">
        <img src="{img_rel}" alt="{e(name)}" class="gallery-image" width="800" height="600" loading="eager" decoding="async" />
      </div>
      <div class="product-info">
        {badge_html}
        <h1 class="product-name">{e(name)}</h1>
        <p class="product-tagline">{e(tagline)}</p>
        <p class="product-price">{price_spans(p)}</p>
        <p class="product-description">{e(desc)}</p>{print_note}
        {buy_html}{draft_banner}
      </div>
    </article>
  </main>

{footer_html("../", version)}

  <script src="../js/main.js"></script>
  <script src="../js/shop-catalog.js"></script>
  <script src="../js/cart.js"></script>
</body>
</html>
"""


def card(p):
    """One product card for index.html (root-relative paths)."""
    pid = p["id"]
    name = p["name"]
    tagline = p.get("tagline", "")
    img = resolve_image(p)
    badge = p.get("badge")
    badge_html = f'\n            <span class="product-badge">{e(badge)}</span>' if badge else ""
    draft_html = '\n            <span class="shop-card-draft">draft</span>' if p.get("draft") else ""
    return f"""        <a class="shop-card" href="shop/{e(pid)}.html">
          <img src="{e(img)}" alt="{e(name)}" class="gallery-image" width="800" height="600" loading="lazy" decoding="async" />
          <div class="shop-card-body">{badge_html}{draft_html}
            <span class="shop-card-name">{e(name)}</span>
            <span class="shop-card-tagline">{e(tagline)}</span>
            <span class="shop-card-price">{price_spans(p)}</span>
          </div>
        </a>"""


def catalog_js(products):
    """window.RF_CATALOG used by js/cart.js to render line items (display only).

    Paths are site-absolute so the same file works from the home page (/) and from
    a product page (/shop/<id>.html). The Worker re-prices every line server-side —
    this catalog is never trusted for checkout pricing.
    """
    cat = {}
    for p in products:
        pid = p["id"]
        cat[pid] = {
            "name": p["name"],
            "price": p.get("price_usd"),
            "compare_at": p.get("compare_at_usd"),
            "image": "/" + resolve_image(p),
            "url": f"/shop/{pid}.html",
            "pickup": p.get("shipping") == "local-pickup",
        }
    return "window.RF_CATALOG = " + json.dumps(cat, ensure_ascii=False, indent=2) + ";\n"


def sitemap_xml(products):
    """sitemap.xml: home + legal pages + every non-draft product page."""
    rows = [
        ("", "index.html", "weekly", "1.0"),
        ("privacy.html", "privacy.html", "yearly", "0.3"),
        ("terms.html", "terms.html", "yearly", "0.3"),
    ]
    for p in products:
        if not p.get("draft"):
            rows.append((f"shop/{p['id']}.html", f"shop/{p['id']}.html", "monthly", "0.7"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, path, freq, prio in rows:
        out += [
            "  <url>",
            f"    <loc>{SITE}/{e(loc)}</loc>",
            f"    <lastmod>{git_lastmod(path)}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def splice(text, start, end, block, indent="        "):
    """Replace everything between two marker comments (inclusive) with `block`."""
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        return None
    return pattern.sub(lambda _: f"{start}\n{block}\n{indent}{end}", text)


VERSION_RE = re.compile(r'<p class="footer-version">[^<]*</p>')


def main():
    check = "--check" in sys.argv
    with open(os.path.join(REPO, "shop", "products.json"), encoding="utf-8") as f:
        data = json.load(f)
    currency = data.get("currency", "USD")
    worker_url = data.get("worker_url", "")
    products = data["products"]
    version = read_version()

    changed = []

    def emit(relpath, new):
        path = os.path.join(REPO, relpath)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if new != old:
            changed.append(relpath)
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    # 1. product pages
    for p in products:
        emit(f"shop/{p['id']}.html", product_page(p, currency, worker_url, version))

    # 2. shop catalog for the cart (window.RF_CATALOG)
    emit("js/shop-catalog.js", catalog_js(products))

    # 3. cards spliced into index.html (+ 4. footer version on every versioned page)
    for relpath in VERSIONED_PAGES:
        path = os.path.join(REPO, relpath)
        text = open(path, encoding="utf-8").read()
        new = text
        if relpath == "index.html":
            new = splice(new, CARD_START, CARD_END, "\n".join(card(p) for p in products))
            if new is None:
                print(f"ERROR: card markers not found in index.html — add:\n  {CARD_START}\n  {CARD_END}")
                return 2
            featured = [p for p in products if p.get("featured") and not p.get("draft")]
            spliced = splice(new, FEATURED_START, FEATURED_END, "\n".join(card(p) for p in featured))
            if spliced is None:
                print(f"  ! index.html has no {FEATURED_START} / {FEATURED_END} markers — home preview left as-is")
            else:
                new = spliced
        is_index = relpath == "index.html"
        nav = nav_html("./", active="music" if is_index else None, tabs=is_index)
        for start, end, block in ((NAV_START, NAV_END, nav), (FOOTER_START, FOOTER_END, footer_html("./", version))):
            spliced = splice(new, start, end, block, indent="  ")
            if spliced is None:
                print(f"  ! {relpath}: missing {start} / {end} markers — chrome left as-is")
            else:
                new = spliced
        if not VERSION_RE.search(new):
            print(f"  ! {relpath}: no <p class=\"footer-version\"> to stamp")
        new = VERSION_RE.sub(f'<p class="footer-version">v{e(version)}</p>', new)
        emit(relpath, new)

    # 5. sitemap
    emit("sitemap.xml", sitemap_xml(products))

    if check:
        if changed:
            print("Shop is OUT OF DATE; run `python3 scripts/build_shop.py`. Stale:")
            for c in changed:
                print(f"  - {c}")
            return 1
        print("Shop is up to date.")
        return 0

    if changed:
        print(f"Wrote {len(changed)} file(s):")
        for c in changed:
            print(f"  - {c}")
    else:
        print("No changes — shop already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
