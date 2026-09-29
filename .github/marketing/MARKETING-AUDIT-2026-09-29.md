# Marketing audit — robotfantome.com (2026-09-29)

Scope: the public site https://robotfantome.com (music press-kit, shop, blog,
mix-tape, legal pages) as served on 2026-09-29, plus its public search/social
footprint. Read-only research. No forms submitted, no checkout started. The
live HTML matched `origin/main` at `01e3d77` byte for byte (`diff` of the
fetched `/` against `index.html` was empty), so file:line references in this
audit point at that commit.

> **Where this file lives, and why.** GitHub Pages serves this repo's root
> as-is (`.nojekyll`). Dot-directories are served too:
> `curl -sI https://robotfantome.com/.github/copilot-instructions.md` returned
> **200** (`text/markdown`), as did `/.github/workflows/version-check.yml`, `/.gitignore`,
> `/AGENTS.md`, `/CLAUDE.md`, `/ECOMMERCE_BRIEF.md` and `/scripts/build_shop.py`.
> **No path on `main` is unserved.** This file sits under `.github/` because
> `robots.txt` blocks it from crawlers twice (`Disallow: /.github/` and
> `Disallow: /*.md$`), and because the repo is already public on GitHub. It holds
> only observations of public pages and recommendations. If it is merged, it
> can be fetched at `https://robotfantome.com/.github/marketing/MARKETING-AUDIT-2026-09-29.md`.

---

## 1. Summary

Robot Fantôme reads clearly as an **indie / punk / rock artist from Orlando**.
The H1 `Robot Fantôme` with `Indie / Punk / Rock — Orlando, FL` beneath it
(`index.html:175-176`) passes the 5-second test. The technical base is solid:
HTTPS with www/http → apex 301s, canonical tags, full OG and Twitter card sets,
MusicGroup and Product JSON-LD, a valid sitemap covering all 12 pages, no
broken internal links, honest privacy and terms pages, a working mailing list,
and a Stripe-hosted checkout.

The weak spots are outside the markup. **The site is effectively invisible in
search.** It does not show up for its own name, and `site:robotfantome.com`
returns only the GitHub repo. **The press kit is thin for bookers:** there is
one photo at 886 px, no downloadable assets, no stage plot, no quotes, and
"next date TBA". **Nothing is measured**, since there is no analytics of any
kind. **Shipping cost stays hidden until Stripe's page.** The music identity is
**split across names and releases**: Robot Fantôme, Robô Fantasma,
`robofantasma` and `robotfantme`, with EP titles that don't match the streaming
platforms. The home tab also shares the site with a full job résumé and
certificates, which dilutes the artist positioning.

### Top 5 priorities

1. **MKT-01 (P1)**: get indexed. Verify the site in Google Search Console and Bing Webmaster Tools and submit the sitemap. *(Tier 3)*
2. **MKT-02 (P1)**: turn the press kit into something a booker can use: a downloadable hi-res photo pack, one-line/short/long bios, stage plot or tech rider, live video, press quotes, and a shows widget. *(Tier 2, with assets from Luiz)*
3. **MKT-03 (P1)**: show shipping cost before checkout, on product pages and in the cart. *(Tier 3 decides the rates, then Tier 2 copy)*
4. **MKT-04 (P1)**: add privacy-respecting analytics plus a purchase-success event. There is currently zero measurement. *(Tier 3 account, then Tier 1 code, then Tier 2 privacy text)*
5. **MKT-05 (P1)**: settle one music identity. Use one release name that matches the streaming platforms, stop calling the 2022 EP the "debut" when Bandcamp has 2019 releases, and link the unlinked `fantasma/robô` release. *(Tier 2)*

Findings by severity: **P0: 0 · P1: 6 · P2: 10 · P3: 5** (21 total).

---

## 2. Scorecard

| Area | Grade | Reason |
|---|---|---|
| Positioning & messaging | B− | The 5-second test passes, and the bio is vivid. The home tab mixes artist, studio, developer résumé and volunteer history, and release naming is inconsistent. |
| Press kit (EPK) | D | Bio and gallery exist. There is no hi-res download, rider, quotes, video, shows or booking-specific contact. |
| Conversion: music | B | Spotify embed plus 6 platform links. No pre-save or follow CTA, and Instagram points to the studio account. |
| Conversion: shop | C+ | Clean product pages, prices, sale badges and clear terms. Shipping cost is unknown until Stripe, and stock status is static. |
| Fan capture | B | A mailing list with a no-JS fallback and a privacy note. It only appears once, low on the home tab. |
| On-page SEO | B | Titles, descriptions, canonicals, OG and JSON-LD are all present. Some descriptions are too long or too short, and the sticker OG image is a portrait transparent PNG. |
| Structured data | B− | MusicGroup and Product are present. The album name doesn't match the platforms, and Product lacks return and shipping details. |
| Technical | B+ | Redirects, sitemap and robots are good, with no broken internal links. The 404 is GitHub's default page, internal files are served, and there is no WebP. |
| Measurement | F | No analytics, no conversion tracking, and no Search Console evidence. |
| Search presence | F | Not found for its own name. Collisions with a Scratch user and French "robots fantômes" results. |
| Legal / trust | A− | Plain-language privacy, terms and returns. The privacy text says "Cloudflare in front", but the apex is served straight from GitHub. |

---

## 3. Findings

Severity: **P0** means broken or losing customers now. **P1** means high. **P2** means improvement. **P3** means nice to have.
Tier: **1** means an agent can ship it (a verifiable technical fix). **2** means public copy, visuals or identity, which needs a branch and Luiz's review. **3** means Luiz only (accounts, pricing, credentials, Stripe or shop-api config).

### MKT-01 — Site not found in search for its own name · P1 · Tier 3
- **Evidence:** a WebSearch for `"Robot Fantôme"` returned only French books and art projects. `"Robot Fantome" band Orlando` returned Lovestruck Robot and Captured! By Robots. `robotfantome` returned an unrelated Scratch user (`scratch.mit.edu/users/robotfantome`). `site:robotfantome.com` returned only `github.com/wmestrinho/robot-fantome/pull/5`. Only the Bandcamp album surfaced, for the query `"Stolen ghost Recordings"`.
- **Why:** bookers, press and fans who hear the name can't find the site, and the name collides with generic French phrases.
- **Fix:** verify the domain in Google Search Console (DNS TXT via Cloudflare) and Bing Webmaster Tools, submit `https://robotfantome.com/sitemap.xml`, and request indexing of `/` and each `/shop/*.html`. Then have every profile (Spotify for Artists bio, Bandcamp, YouTube, TikTok, X, Facebook) link back to robotfantome.com to build entity signals.
- **Caveat:** the WebSearch tool's index is not Google's own. Confirm the result in Search Console.

### MKT-02 — Press kit is not booker-ready · P1 · Tier 2
- **Evidence:** the music tab (`index.html:168-353`) has one press photo, `assets/images/press-profile.jpg` at 886×886 and 82 KB, which is not print-grade. It has a two-paragraph bio, a gallery with a maximum width of 1182 px, no downloadable ZIP, no stage plot or tech rider, no press quotes, no live video embed (YouTube is linked, not embedded), and `Upcoming shows: next date TBA` (`index.html:230`). The booking contact is a shared studio Gmail (`index.html:312`).
- **Comparison:** a peer EPK such as `officialstayout.com/epk/` offers a downloadable ZIP (photos, logos, stage plot), a press archive, radio stats, manager contact, Bandsintown dates and endorsements.
- **Fix:** add a press-kit block with (a) one-line, 50-word and 150-word bios; (b) a ZIP of 3–5 photos at 3000 px or more, the logo and both mascots; (c) a stage plot and input list; (d) 2–3 quotes or notable bills (CityArts Third Thursdays and the Zora Neale Hurston Festival already qualify); (e) one embedded live clip; (f) a Bandsintown or Songkick artist profile and widget. Luiz supplies the assets. Given the "no section titles" rule, keep it headless.

### MKT-03 — Shipping cost is unknown until Stripe's page · P1 · Tier 3 → Tier 2
- **Evidence:** the cart says `Cart total excludes shipping and taxes.` (`js/cart.js:107`). The product pages show price only (for example `shop/sticker-pack-01.html`, the `.product-price` line). `terms.html` states US-only shipping and "typically within 5 business days" but gives no rate. `ECOMMERCE_BRIEF.md` open question 1 (shipping model) has no recorded answer in the repo.
- **Why:** surprise shipping costs are the most common reason carts are abandoned, and a $7 sticker pack is especially sensitive.
- **Fix:** Luiz decides the rates (for example flat per type, or free over $X), and the shop-api config must match. Then show one line per product ("Ships US · $X flat" or "Local pickup, Orlando") and a matching cart note.

### MKT-04 — No analytics or conversion measurement at all · P1 · Tier 3 → 1 → 2
- **Evidence:** a grep across `*.html` and `js/*` for `gtag|analytics|plausible.io|umami|goatcounter|cloudflareinsights` found nothing. `privacy.html` states "no analytics". The Stripe return is handled only as a toast (`js/cart.js:229-248`) and nothing is recorded.
- **Why:** there is no way to know traffic, referrers (for example which social posts drive visits), shop conversion, or mailing-list sign-up rate.
- **Fix:** use a cookieless tool so no consent banner is needed. Candidates are Cloudflare Web Analytics (a JS beacon works even though the apex is DNS-only) or GoatCounter or Plausible. Fire custom events for `add_to_cart`, `begin_checkout`, `purchase` (on `?order=success`), `subscribe` and outbound streaming clicks. Luiz creates the account (Tier 3). An agent adds the snippet and events, bumping `VERSION` (Tier 1). The privacy page's "no analytics" sentence must change first (Tier 2), because the page promises that.

### MKT-05 — Release and artist naming is inconsistent · P1 · Tier 2
- **Evidence:**
  - The site says "the debut EP *stolenghost recordings* (2022)" (`index.html:192`), and the JSON-LD album is `"stolenghost recordings"` (`index.html:51`).
  - Apple Music redirects to the title **"Final Project (draft) Stolen ghost Recordings — EP"**. The Spotify embed metadata uses the same name. The DistroKid HyperFollow title matches as well.
  - Bandcamp lists **"Final Project (draft)"**, released May 1, 2019, with 5 tracks, and **"fantasma/robô"**, released December 9, 2019, with 4 tracks. The Bandcamp root redirects to that second release, and it is linked nowhere on the site. Calling the 2022 EP the "debut" contradicts both.
  - Handles vary: the Bandcamp subdomain is `robofantasma`, the HyperFollow slug is `robotfantme` (a typo on DistroKid's side), the Instagram link is the studio's `absolutelyplausible`, and the YouTube channel appears under two different URLs (`index.html:144` and `:223`, both resolving to the same channel).
- **Why:** press and fans search for the exact title. Mismatches split search results and look careless.
- **Fix:** pick the canonical release title and year, use it in the copy and in `MusicGroup.album` (making it an array of both releases), add the `fantasma/robô` Bandcamp link, and use one YouTube URL. Longer term (Tier 3): a band Instagram handle, or explicitly present `@absolutelyplausible` as the band's account.

### MKT-06 — Home positioning diluted by résumé, certificates and dev content · P1 · Tier 2
- **Evidence:** the blog tab carries 40 `timeline-entry` items, including hotel and legal jobs (`index.html:906-1130`), a high-school diploma, Pathlight Kitchen certificate images and PDFs (`index.html:1075-1090`), and a skills list ("AngularJS", "Hotel Management"). Blog posts are Ethereum tooling links (`index.html:526-537`). The meta description mixes "open source" with the artist pitch (`index.html:7`).
- **Why:** bookers and fans landing on the artist domain meet a job CV. The personal documents also add little for the music audience.
- **Fix:** move the résumé, certificates and dev links to absolutelyplausible.com (or LinkedIn), and keep the blog to music and art posts such as show recaps, release notes and build logs. This is Luiz's positioning call.

### MKT-07 — Internal repo files are publicly served on the brand domain · P2 · Tier 3
- **Evidence:** 200 responses for `/AGENTS.md`, `/CLAUDE.md`, `/ECOMMERCE_BRIEF.md` (which includes "Open questions for Luiz"), `/README.md`, `/CHANGELOG.md`, `/VERSION`, `/LICENSE`, `/CNAME`, `/.gitignore`, `/.nojekyll`, `/.github/copilot-instructions.md`, `/.github/workflows/version-check.yml` and `/scripts/*.py`. `robots.txt` blocks `*.md`, `/scripts/` and `/.github/` from crawling, but not access. There is also no `X-Robots-Tag` header (GitHub Pages can't set one).
- **Why:** low confidentiality risk, since the repo is public anyway. It is still unprofessional, and agent and brief docs on the brand domain can leak into previews.
- **Fix:** deploy via a GitHub Actions Pages workflow that uploads only site files (`index.html`, `privacy.html`, `terms.html`, `robots.txt`, `sitemap.xml`, `CNAME`, `assets/`, `css/`, `js/`, `shop/*.html`, and `shop/products.json` if still needed client-side), or move the site into `/docs`. This changes the deploy pipeline and Pages settings, so Luiz must sign off. Remove the dead `qa-comparison.png` mention from future checklists; it already returns 404.

### MKT-08 — 404 page is GitHub's generic page · P2 · Tier 1
- **Evidence:** `curl https://robotfantome.com/nonexistent-xyz` returns 404 with `<title>Page not found · GitHub Pages`. Old links to `/shop/`, which returns 404, land there too.
- **Fix:** add a branded `404.html` with the site nav and footer, links to the music, shop and mailing list, and `noindex`. Generate it with `build_shop.py` so the chrome and version stay in sync, and bump `VERSION` with a CHANGELOG entry. Optionally add a `shop/index.html` that redirects to `/#shop`.

### MKT-09 — Product JSON-LD lacks return and shipping details, and stock status is static · P2 · Tier 1 (returns) / Tier 3 (shipping)
- **Evidence:** the `Offer` in `shop/*.html` (for example `shop/sticker-pack-01.html:44-54`) has no `hasMerchantReturnPolicy` or `shippingDetails`, which triggers Google merchant-listing warnings. `availability` comes from the static `qty` in `products.json` (`scripts/build_shop.py:120-126`), while real stock is decremented in the Worker's KV. A sold one-of-one item keeps saying `InStock` until someone edits the JSON and rebuilds.
- **Fix:** Tier 1: emit `hasMerchantReturnPolicy` mirroring `terms.html` (final sale, with 14-day damaged or lost exceptions: `MerchantReturnNotPermitted` plus a policy URL), and `shippingDetails.shippingDestination: US`. Tier 3: add shipping rates once MKT-03 is decided, and a process or webhook to mark sold uniques `qty: 0` in `products.json`.

### MKT-10 — Sticker-pack share image is a portrait transparent PNG · P2 · Tier 1
- **Evidence:** `shop/sticker-pack-01.html` `og:image` is `robot-ghost-rising.png` (374×600, transparent, 187 KB) while the page declares `twitter:card=summary_large_image`, which expects about 1.91:1. Transparent PNGs render on black or grey in several apps.
- **Fix:** generate a 1200×630 JPEG card (both stickers on the paper background) and point the product's OG and Twitter image at it. Add `og:image:width/height` site-wide. The home card `live-cityarts-wide.jpg` is 1024×768 (4:3). A 1200×630 crop is better.

### MKT-11 — Meta descriptions outside 150–160 characters · P2 · Tier 2
- **Evidence (bytes, including multi-byte characters):** home 169. Sticker pack 173, Nirvana shirt 172, pallet cubby 164. Disruptive by Design 105, Robot & monkey 113, Leading Ladies 118. `PROJECT-RULES.md` §7 asks for unique descriptions of 150–160 characters.
- **Fix:** rewrite in `shop/products.json` `meta_description` and rebuild. Rewrite the home one in `index.html:7` and lead with the music ("Indie / punk / rock from Orlando — stream the EP, see shows, shop handmade merch").

### MKT-12 — No streaming or fan call to action above the fold · P2 · Tier 2
- **Evidence:** the hero (`index.html:171-180`) has title and genre only. The Spotify embed and platform links come after the bio. The mailing list sits near the bottom of the tab (`index.html:314`).
- **Fix:** add a single hero line with the primary actions ("Listen on Spotify · Bandcamp · Join the list"). Consider a Spotify "Follow" link and a Bandcamp follow link.

### MKT-13 — `sameAs` and social set incomplete or inconsistent · P2 · Tier 1 (after MKT-05)
- **Evidence:** JSON-LD `sameAs` (`index.html:55-64`) omits the Bandcamp artist root, Amazon Music, LinkedIn and Pinterest (though the latter two are personal or studio accounts, so omitting them may be right), and includes the studio Instagram. The Facebook link is `profile.php?id=…` (a personal-profile URL, not a page); curl got HTTP 400 on it (bot-blocked), so unverified.
- **Fix:** once MKT-05 settles the handles, make `sameAs` list only band-owned profiles: Spotify, Apple, Bandcamp root, YouTube, TikTok, X, and a band IG or FB if one exists.

### MKT-14 — Images are JPEG/PNG only, with no WebP or AVIF · P2 · Tier 1
- **Evidence:** 32 unique images are referenced by `index.html`, about 5.6 MB in total (mostly lazy). Eager above-the-fold images are `robot-ghost-rising.png` (187 KB), `robot-ghost-standing.png` and `press-profile.jpg` (80 KB). No `webp` anywhere. `PROJECT-RULES.md` §7 asks for compressed/WebP.
- **Fix:** add `<picture>` with WebP sources for the mascots and gallery (keeping the originals untouched, per the sticker rule), and emit it from the generator for shop cards. Bump `VERSION`.

### MKT-15 — Shows section is a dead end · P2 · Tier 2 / Tier 3
- **Evidence:** "Upcoming shows: next date TBA — announcements land on Instagram first" (`index.html:230-232`), with no `Event` schema and no Bandsintown or Songkick link.
- **Fix:** Luiz claims a Bandsintown artist profile (Tier 3). Link or embed it, and emit `MusicEvent` JSON-LD when dates exist. Otherwise, point the TBA line at the mailing list ("get the next date by email").

### MKT-16 — Blog posts are few, off-topic and share one date · P2 · Tier 2
- **Evidence:** 2 posts, both `2026-06-11`: Ethereum tools and a sustainability reading list (`index.html:519-557`). The blog is a hash tab, not a crawlable URL per post.
- **Fix:** post show recaps, build logs (the DJ pallet table in July 2026 is ready-made) and release notes. If the blog becomes a traffic channel, per-post pages would be a separate zero-build decision.

### MKT-17 — Privacy page says Cloudflare is in front, but the apex is served directly by GitHub · P3 · Tier 2
- **Evidence:** `privacy.html` says "served by GitHub Pages with Cloudflare in front". `nslookup robotfantome.com` returns the GitHub Pages IPs `185.199.108-111.153`, and the response headers show `Server: GitHub.com` with Fastly and no `cf-ray`. Only `shop-api.robotfantome.com` resolves to Cloudflare (`104.21.15.253`, `172.67.165.157`). `CLAUDE.md` and `README.md` repeat the "CDN in front" claim.
- **Fix:** reword to "DNS by Cloudflare; pages served by GitHub Pages". Legal text, so Luiz reviews.

### MKT-18 — Mix-tape and outbound links: two unverifiable destinations · P3 · Tier 1
- **Evidence:** a check of all 150 unique links found no internal failures. External non-200 results were `beacons.ai/laghima` 403, `facebook.com/profile.php?id=…` 400 and `linkedin.com/in/mestrinho` 999, all bot-blocking typical of those hosts. `remix-project.org` timed out once (000). `docs.ethers.io` now redirects to `docs.ethers.org/v6/`, and `web3js…/en/1.0/` redirects to v1.10.0 (the web3.js docs are deprecated).
- **Fix:** re-check these four in a real browser, and update the ethers and web3 URLs (or drop that post per MKT-06).

### MKT-19 — Sitemap `lastmod` lags real edits · P3 · Tier 1
- **Evidence:** every `<lastmod>` is `2026-09-11`, and the last commit touching `index.html` is also 2026-09-11. The generator takes each file's last git commit (`scripts/build_shop.py:73`), so this is correct today. It only drifts if files change without a rebuild.
- **Fix:** none needed beyond running `build_shop.py` on every content change, which is already the rule.

### MKT-20 — Cart and checkout UX not verified end-to-end · P3 · Tier 3
- **Evidence:** no checkout was started, by design. Only the CORS preflight was checked: `OPTIONS https://shop-api.robotfantome.com/checkout` returned 204 with `Access-Control-Allow-Origin: https://robotfantome.com`. `GET /` on shop-api returned 404.
- **Fix:** Luiz, or an agent with his go-ahead, runs a Stripe test-mode purchase and a cancel to confirm the redirects to `/?order=success|cancel`, the receipt email, and the shipping-address collection.

### MKT-21 — Favicon is a single PNG · P3 · Tier 1
- **Evidence:** `assets/favicon.png` (922 bytes) serves as both `icon` and `apple-touch-icon` (`index.html:9-10`). It has no 180×180 touch icon, no SVG icon and no `site.webmanifest`.
- **Fix:** add a 180×180 apple-touch-icon and a 32×32 or SVG icon generated from the standing mascot, and bump `VERSION`.

---

## 4. Checklist

### Tier 1 — an agent can ship (branch, `VERSION` bump plus CHANGELOG for site files, `build_shop.py --check`)
- [ ] MKT-08 Branded `404.html` (noindex), generated with the shared chrome
- [ ] MKT-09 `hasMerchantReturnPolicy` + `shippingDetails.shippingDestination` in Product JSON-LD (generator)
- [ ] MKT-10 1200×630 share card for the sticker pack, plus `og:image:width/height` site-wide
- [ ] MKT-13 Clean `sameAs` (after MKT-05 decides the handles)
- [ ] MKT-14 WebP `<picture>` sources for mascots, gallery and shop cards (originals untouched)
- [ ] MKT-18 Re-check the four blocked links and update the ethers and web3 URLs
- [ ] MKT-19 Keep running `build_shop.py` so `lastmod` stays true (no code change)
- [ ] MKT-21 180×180 touch icon + SVG favicon
- [ ] MKT-04 (code half) Analytics snippet + events, **only after** the Tier 3 account and the Tier 2 privacy wording

### Tier 2 — public copy, visuals or identity (branch, then Luiz reviews)
- [ ] MKT-02 Booker-ready press-kit block (bios, ZIP, rider, video, quotes)
- [ ] MKT-05 One canonical release name and year, drop "debut", link `fantasma/robô`
- [ ] MKT-06 Move résumé, certificates and dev links off the artist site
- [ ] MKT-11 Meta descriptions of 150–160 characters
- [ ] MKT-12 Hero CTA line (listen and join)
- [ ] MKT-15 Shows line pointing to the list or Bandsintown, `MusicEvent` schema when dates exist
- [ ] MKT-16 Music and art blog posts
- [ ] MKT-17 Privacy wording on Cloudflare vs GitHub (and the analytics sentence for MKT-04)
- [ ] MKT-03 (copy half) Shipping line on product pages and in the cart

### Tier 3 — Luiz only
- [ ] MKT-01 Google Search Console + Bing Webmaster verification, submit the sitemap
- [ ] MKT-03 Decide shipping rates, configure shop-api and Stripe to match
- [ ] MKT-04 Create the analytics account (a cookieless tool)
- [ ] MKT-05 Band Instagram or other handle decision
- [ ] MKT-07 Pages deploy that publishes only site files (Actions workflow or `/docs`)
- [ ] MKT-09 Process for marking sold one-of-one items `qty: 0`
- [ ] MKT-15 Claim a Bandsintown or Songkick artist profile
- [ ] MKT-20 Stripe test-mode purchase and cancel walkthrough
- [ ] MKT-02 Supply the hi-res photos, rider and quotes

---

## 5. Re-check commands

```sh
UA='Mozilla/5.0'
# Internal files still served? (MKT-07). Expect 404 once fixed.
for p in /AGENTS.md /CLAUDE.md /ECOMMERCE_BRIEF.md /.gitignore /.github/copilot-instructions.md /scripts/build_shop.py; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' -A "$UA" https://robotfantome.com$p) $p"; done
# Branded 404 (MKT-08). Expect a title other than "GitHub Pages".
curl -s -A "$UA" https://robotfantome.com/nonexistent-xyz | grep -o '<title>[^<]*'
# Redirects
for u in http://robotfantome.com/ https://www.robotfantome.com/ http://www.robotfantome.com/; do curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' "$u"; done
# Internal link check (run from repo root)
grep -ohE '(href|src)="[^"]+"' index.html privacy.html terms.html shop/*.html | sed -E 's/^(href|src)="//;s/"$//' \
  | grep -vE '^(https?:|mailto:|#)' | sed -E 's#^\.\./##;s#^\./##;s#\?.*##' | sort -u \
  | while read p; do c=$(curl -s -o /dev/null -w '%{http_code}' https://robotfantome.com/$p); [ "$c" != 200 ] && echo "$c $p"; done
# Meta description lengths (MKT-11)
for f in index.html shop/*.html; do echo "$(grep -oE 'name="description" content="[^"]*' $f | sed 's/.*content="//' | wc -m) $f"; done
# Analytics present? (MKT-04)
grep -rlE 'cloudflareinsights|goatcounter|plausible\.io|umami|gtag' --include=*.html --include=*.js .
# Product JSON-LD return policy (MKT-09)
grep -c hasMerchantReturnPolicy shop/*.html
# Checkout CORS preflight (no purchase)
curl -s -X OPTIONS -D - -o /dev/null -H 'Origin: https://robotfantome.com' -H 'Access-Control-Request-Method: POST' https://shop-api.robotfantome.com/checkout | grep -iE '^HTTP|allow-origin'
# Repo validation
python3 scripts/validate_agent_baseline.py && python3 scripts/build_shop.py --check
```
