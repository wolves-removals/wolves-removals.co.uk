# Wolves Removals — Static Rebuild

Static SEO rebuild of **wolves-removals.co.uk** (Sussex/Surrey/Kent/Hampshire removals).
Replaces the WordPress (Elementor + ACF) site with a fast, secure, free-to-host static build.

## Architecture decision

- **Design / UI / UX:** faithful reproduction of the *current* live site. We reuse the
  original `wolvesremovals` theme's compiled stylesheet (`css/site.min.css`, Tailwind),
  the Barlow webfonts, the logo + icon sprite, and replicate the rendered markup/classes.
  The rendered live HTML in `_source/live/` is the pixel-exact reference.
- **Build engine:** NSR-style Python generators (`tools/nsr-render-*.py` → adapted to
  `render-pages.py` / `render-areas.py` / `render-blog.py`) driven by data files in `data/`.
- **SEO standard ("the Bible"):** Mark Ratcliffe Moving toolchain — `tools/mrm-audit.py`
  (~110 checks / 40-rule mapping), `mrm-build-schema.py`, `mrm-build-llms-txt.py`,
  `mrm-build-sitemap.py`, `mrm-build-blog-index.py`. All pages must pass the audit.
- **Content rule:** on every page, **keep the full existing live copy, then ADD to it**
  to meet the bible (≥1500-word location pages, ≥2000-word blogs, E-E-A-T signals, ≥4 FAQs +
  FAQPage schema, ≥10 in-body internal links, unique title/H1/meta, alt text, etc.).
  Never discard existing content; never fabricate facts, reviews, or accreditations.
- **Hosting:** Cloudflare Pages (`_headers`, `_redirects`, `CNAME`). Forms via
  Cloudflare Worker → Resend (needs domain Resend API key + verified sender — TODO).

## Deploy (push = auto-deploy)

Cloudflare Pages is connected to this GitHub repo via **Git integration** (configured in
the Cloudflare dashboard → *Pages → wolves-removals → Settings → Builds & deployments*).
Every push to the **`main`** branch automatically triggers a production deploy — usually
live within 1–3 minutes. No `wrangler` command, drag-drop, or CI workflow is involved.

The repo commits **pre-built output** (generated HTML + `css/site.min.css`), and Cloudflare
serves those committed files. So a deploy is only as fresh as what you commit. The workflow:

1. Make source changes (edit `tools/*.py` generators, data files, or CSS input).
2. **Build before pushing:** `npm run build` (= `npm run build:css && python3 tools/build.py`).
   Run `build:css` only when CSS changed; `build.py` regenerates all HTML + sitemap + llms.txt.
3. `git add -A && git commit && git push origin main` → Pages auto-builds and deploys.

Notes:
- Pushes to **other branches** create isolated **preview** deployments (`*.pages.dev`), not
  production — safe for testing.
- HTML is served `cf-cache-status: DYNAMIC` (not edge-cached), so page changes appear
  immediately; CSS/JS/images use `?v=` cache-busters, so those refresh cleanly too.
- Watch a deploy: Cloudflare dashboard → **Pages → wolves-removals → Deployments** (each
  push shows as a build with its commit hash + status).

## Brand tokens (from theme `tailwind.config.js`)

| Token | Hex | Use |
|---|---|---|
| black | `#262626` | body text |
| blue | `#678096` | muted blue accent |
| darkgrey | `#697783` | top contact bar bg |
| lightgrey | `#F9F8F6` | section background |
| beige | `#E8E6DA` | header bar bg |
| darkgreen | `#456A54` | secondary |
| **orange** | `#FC9700` | **primary CTA / action** |
| star | `#F6BB06` | review stars |
| border | `#E7E7E7` | borders |

Font: **Barlow** (Regular/Medium/Semibold/Bold woff2 in `fonts/`). Container centred,
responsive padding 1rem/2rem/3rem. Uses Alpine.js for the mobile off-canvas menu.

## Real business facts (do not change)

- Wolves Removals, Doryln House, London Road, Ashington, West Sussex, RH20 3JT
- Tel 01903 893731 · Mob 07789 390421 · contact@wolves-removals.co.uk
- Accreditations: **LAPADA**, **Checkatrade**, fully insured (NOT BAR)
- Trusted by Fine & Country, Leaders, Mansell McTaggart estate agents
- 100+ years combined team experience

## Scale (from live sitemaps) — ~173 URLs

- **114 pages:** ~25 services, ~62 locations, + core (home, about, contact, pricing, FAQ,
  testimonials, gallery, leave-a-review, job-vacancies, get-a-quote, storage-calculator,
  privacy, terms, helpful-tips hub + 7 tips)
- **59 blog posts** (root-level URLs + /blog/ index)

See `data/urls-pages.txt` and `data/urls-posts.txt` for the exact URL map (kept identical).

## Build phases

1. ✅ Scaffold: skeleton, staged source (theme + 15 live pages), design assets, toolchain.
2. ⬜ Adapt engine: header/footer/section templates reproducing the live chrome + components.
3. ⬜ Adapt `mrm-audit.py` config (domain, URL map, accreditation rules) → `audit.py`.
4. ⬜ Data files: `site.json`, `services.json`, `locations.json`, `blog/` content.
5. ⬜ Generate + bible-expand: core pages → services → locations → blog (batched).
6. ⬜ Build sitemap / schema / llms.txt; run audit to zero failures; `_headers`/`_redirects`.

## `_source/` is git-ignored

Reference only (original theme + captured live HTML). Not deployed.
