#!/usr/bin/env python3
"""Generate the Robot Fantôme shop from shop/products.json.

This is a *local authoring tool*, not a server build step — it writes plain
static HTML that ships as-is (keeps the zero-dependency / zero-build ethos).

It does two things:
  1. Writes one crawlable static page per product:  shop/<id>.html
     (own <title>, canonical, Open Graph, and Product JSON-LD for SEO).
  2. Splices the Shop-tab product cards into index.html, between the markers
     <!-- shop:cards:start --> and <!-- shop:cards:end -->.

Usage:
    python3 scripts/build_shop.py          # regenerate everything
    python3 scripts/build_shop.py --check  # fail if output would change (CI/pre-commit)

Stdlib only. Run from anywhere; paths are resolved relative to the repo root.
"""

import html
import json
import os
import re
import sys
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://robotfantome.com"

CARD_START = "<!-- shop:cards:start -->"
CARD_END = "<!-- shop:cards:end -->"

AVAILABILITY = {
    "sold-out": "https://schema.org/SoldOut",
    "made-to-order": "https://schema.org/MadeToOrder",
    "in-stock": "https://schema.org/InStock",
}


def e(text):
    """HTML-escape (and keep the result safe inside attributes too)."""
    return html.escape(str(text), quote=True)


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


def product_page(p, currency, worker_url):
    """Full standalone HTML for one product page (lives at shop/<id>.html)."""
    pid = p["id"]
    name = p["name"]
    tagline = p.get("tagline", "")
    desc = p.get("description", "")
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

    if local_pickup:
        subject = urllib.parse.quote(f"Shop enquiry — {name}")
        buy_html = (
            '<p class="product-pickup">Local pickup / freight only (heavy &amp; oversized). '
            f'<a href="mailto:absolutelyplausible@gmail.com?subject={subject}">'
            'Email to arrange &rarr;</a></p>'
        )
    else:
        price_label = f"${price}" if price is not None else "Buy"
        buy_html = (
            f'<button class="btn-buy" data-product-id="{e(pid)}" data-qty="1">'
            f'Buy &mdash; {e(price_label)}</button>\n'
            '        <p class="product-buy-note">Secure checkout via Stripe. '
            'Card details never touch this site.</p>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(name)} — Robot Fantôme shop</title>
  <meta name="description" content="{e(tagline or desc)}" />
  <meta name="robots" content="{'noindex, nofollow' if draft else 'index, follow, max-image-preview:large'}" />
  <link rel="icon" type="image/png" href="../assets/favicon.png" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#3f7d9c" />
  <meta property="og:type" content="product" />
  <meta property="og:title" content="{e(name)} — Robot Fantôme" />
  <meta property="og:description" content="{e(tagline or desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{img_abs}" />
  <meta property="og:site_name" content="Robot Fantôme" />
  <meta name="twitter:card" content="summary_large_image" />
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
  <header class="gh-nav">
    <div class="gh-nav-inner">
      <a href="../" class="gh-nav-brand" aria-label="robot fantôme home">
        <span class="gh-nav-brand-text">robot fant&ocirc;me</span>
      </a>
      <nav class="gh-nav-links" aria-label="Site navigation">
        <a href="../">music press-kit</a>
        <a href="../#shop">shop</a>
        <a href="../#blog">blog</a>
        <a href="../#mixtape">mix-tape</a>
      </nav>
    </div>
  </header>

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
        <p class="product-price">${e(price)}</p>
        <p class="product-description">{e(desc)}</p>
        {buy_html}{draft_banner}
      </div>
    </article>
  </main>

  <footer>
    <div class="footer-inner">
      <a href="https://absolutelyplausible.com" target="_blank" rel="noopener" class="footer-ap" aria-label="Absolutely Plausible — official site">
        <img src="../assets/images/ap-logo.png" width="707" height="706" alt="Absolutely Plausible logo" class="footer-ap-logo" />
        <span>an Absolutely Plausible production</span>
      </a>
      <p class="footer-license">
        Website Design &copy; 2026 by robot fant&ocirc;me &mdash;
        <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener">CC BY-NC 4.0</a>
      </p>
    </div>
  </footer>

  <script src="../js/shop.js"></script>
</body>
</html>
"""


def card(p):
    """One product card for the Shop tab in index.html (root-relative paths)."""
    pid = p["id"]
    name = p["name"]
    tagline = p.get("tagline", "")
    price = p.get("price_usd")
    img = resolve_image(p)
    badge = p.get("badge")
    badge_html = f'\n        <span class="product-badge">{e(badge)}</span>' if badge else ""
    draft_html = '\n        <span class="shop-card-draft">draft</span>' if p.get("draft") else ""
    return f"""        <a class="shop-card" href="shop/{e(pid)}.html">
          <img src="{e(img)}" alt="{e(name)}" class="gallery-image" width="800" height="600" loading="lazy" decoding="async" />
          <div class="shop-card-body">{badge_html}{draft_html}
            <span class="shop-card-name">{e(name)}</span>
            <span class="shop-card-tagline">{e(tagline)}</span>
            <span class="shop-card-price">${e(price)}</span>
          </div>
        </a>"""


def main():
    check = "--check" in sys.argv
    with open(os.path.join(REPO, "shop", "products.json"), encoding="utf-8") as f:
        data = json.load(f)
    currency = data.get("currency", "USD")
    worker_url = data.get("worker_url", "")
    products = data["products"]

    changed = []

    # 1. product pages
    for p in products:
        path = os.path.join(REPO, "shop", f"{p['id']}.html")
        new = product_page(p, currency, worker_url)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if new != old:
            changed.append(os.path.relpath(path, REPO))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    # 2. splice cards into index.html
    index_path = os.path.join(REPO, "index.html")
    index = open(index_path, encoding="utf-8").read()
    cards = "\n".join(card(p) for p in products)
    block = f"{CARD_START}\n{cards}\n        {CARD_END}"
    pattern = re.compile(re.escape(CARD_START) + r".*?" + re.escape(CARD_END), re.DOTALL)
    if not pattern.search(index):
        print(f"ERROR: card markers not found in index.html — add:\n  {CARD_START}\n  {CARD_END}")
        return 2
    new_index = pattern.sub(lambda _: block, index)
    if new_index != index:
        changed.append("index.html")
        if not check:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_index)

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
