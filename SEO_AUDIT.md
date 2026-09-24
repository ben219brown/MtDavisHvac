# Mt Davis HVAC — full SEO audit
**Audit date:** 2026-09-24  
**Primary domain:** https://mtdavishvac.com/  
**Repository:** ben219brown/MtDavisHvac  
**Scope:** production HTML/CSS, on-page SEO, local-business data, technical crawlability, site migration, images, content architecture, UX/conversion and measurement.

## Measured production optimization results (24 September 2026)

After enlarging the Google review carousel touch targets and preloading the real Oswald and Manrope font resources identified by Lighthouse, a fresh Lighthouse run against the **live public homepage** reported:

| Lighthouse category / metric | Mobile | Desktop |
|---|---:|---:|
| Performance | **97** | **100** |
| Accessibility | **100** | **100** |
| Best Practices | **100** | **100** |
| SEO | **100** | **100** |
| First Contentful Paint | 1.9 s | 0.6 s |
| Largest Contentful Paint | 2.2 s | 0.7 s |
| Cumulative Layout Shift | **0** | **0** |
| Total Blocking Time | 70 ms | 0 ms |

Source: GitHub Actions Lighthouse Production Audit run **36003981494** (2026-09-24, mobile and desktop). This is an individual simulated lab test; scores may vary with network conditions, and actual user Core Web Vitals require field data in Search Console or compatible monitoring. Lighthouse SEO 100 means the tested page passed its automated checks, **not** that search engines have indexed the page or that it ranks for particular searches.

## Live Lighthouse baseline (24 September 2026)
A real headless Chrome Lighthouse run against the public HTTPS homepage completed successfully from a GitHub Actions runner. This is **one laboratory run**, not a field-data Core Web Vitals report and not a search-ranking forecast.

| Lighthouse category | Mobile | Desktop |
|---|---:|---:|
| SEO | **100** | **100** |
| Best Practices | **100** | **100** |
| Accessibility | **96** | **96** |
| Performance | **86** | **99** |
| Largest Contentful Paint | 2.9 seconds | 0.8 seconds |
| First Contentful Paint | 2.7 seconds | 0.8 seconds |
| Cumulative Layout Shift | 0.123 | 0.004 |
| Total Blocking Time | 0 ms | 0 ms |

**Resolved:** those initial mobile paint and layout-shift findings prompted touch-target and font-preload updates. See the follow-up live run and results above. Keep the baseline for before/after comparison.

> **Production implementation update — 24 September 2026:** The homepage indexing block was removed, real approved mountain-icon favicons (PNG/ICO/Apple), branded social preview, robots.txt, sitemap.xml, six service URLs, contact page and privacy page were deployed. The quote form now posts to FormSubmit for the confirmed address **mark@mtdavishvac.com** and includes an anti-spam honeypot and thank-you page. **Delivery requires the owner to complete FormSubmit's activation email** after a test submission. An external GitHub Actions smoke test verified 200 responses for homepage, sitemap, robots, favicons, contact and service hub, and checked that the live homepage contains the new form and no `noindex`. The `www` hostname currently returns 200 rather than the desired 301: finish its redirect in the Cloudflare dashboard. Search Console ownership, live indexing measurements and approval of review quotations are still pending.


This is a repository/content and publicly available listing review. **It is not a completed live Core Web Vitals measurement, a verified production form-delivery test, or a Google Search Console crawl audit.** Cloudflare deployment, redirect responses, form activation and actual search-indexing status must be verified separately. GitHub Actions now runs `scripts/check_site.py` on every push and pull request for offline regression checks.


## Final implementation status (2026-09-24)

**Implemented in the GitHub repository:** public indexing directive, unique metadata and canonicals, HVACBusiness/Service/ContactPage structured data, 9-URL sitemap, robots.txt, homepage + five unique service pages + contact and privacy pages, real-photo branded social card, supplied mountain icon in PNG/ICO/Apple formats, live-POST form markup to `mark@mtdavishvac.com`, page-level phone fallback, noindexed confirmation page, accessible reviews pause and local-asset quality checks. This is not an assertion that the latest revision has already deployed or that third-party email delivery has already been activated.

**Requires action in external accounts:** approve FormSubmit first-use confirmation and verify a second delivery; create Cloudflare zone 301 redirect from www to apex with path/query preserved; verify Google Search Console ownership and submit sitemap; verify Google Business Profile review excerpts/details. Live HTTP and Lighthouse checks were completed and reported above.

## Findings and implementation

| Priority | Finding | Work in this repository | Remaining verification |
|---|---|---|---|
| Critical | Homepage carried `noindex,nofollow` from the demo. | Removed; set index/follow. | Check live page source and HTTP `X-Robots-Tag` after Cloudflare deploy, then inspect in Search Console. |
| Critical | Demo quote form opened an unverified email address and did not submit online. | Replaced with a FormSubmit POST to the user-approved `mark@mtdavishvac.com`, spam check, honeypot, privacy notice and confirmation page; phone fallback remains. | **Activation required:** owner must submit a test, confirm the activation email, then submit and receive a second test. |
| High | No explicit canonical or social preview metadata. | Added canonicals, unique page titles/descriptions, OG/Twitter tags, exact user-provided browser icons, and a 1200×630 branded sharing image using a real project photograph. | Inspect the LIVE page source and test sharing with a social debugger after Cloudflare deployment. |
| High | No accessible sitemap or robots asset was present in the migrated repo. | Added `robots.txt` and `sitemap.xml` listing 9 intentional indexable URLs (homepage, service hub, 5 services, contact, privacy) and genuine project images. | Confirm live HTTP 200 and submit sitemap in Google Search Console; the noindexed confirmation page is not listed. |
| High | Existing homepage tried to cover all services on a single URL. | Added one service hub plus five distinct service pages: AC, heating/furnaces, mini-splits, heat pumps and maintenance. Linked from the homepage and to one another. | Confirm pages are live; expand details using information verified by the business owner and actual project-specific photos. |
| High | No business-identity markup. | Added `HVACBusiness` JSON-LD with contact email, main phone, city/region, service area and service catalog; Service/Breadcrumb markup on each service page and ContactPage/Breadcrumb markup on contact page. Removed unverified Google Maps place identifier. | Test deployed markup using Google Rich Results Test and Schema.org validator; don't publish a private street address without owner approval. |
| High | Legacy GoDaddy `/services` or contact URLs may have backlinks or be indexed. | Added intended static redirects `/services -> /services/`, `/contact -> /contact/`, `/contact-us -> /contact/`. | Verify HTTP 301 on the actual Worker deployment and add additional historic paths identified in Search Console. |
| High | Both `www` and apex may serve the same content. | Every page has one apex canonical URL. | In Cloudflare zone Rules -> Redirect Rules, make `www` permanently redirect to apex, preserving path and query. Confirm no loops. |
| Medium | Public photo gallery contains just 3 distinct project photographs; 2 of these are reused on multiple pages. | Retained authentic, locally hosted project photos (not stock) and descriptive ALT/captions. Homepage hero has fetch priority high; below-fold photos use lazy loading and async decode. | Get originals at >=1200px wide; optimize in WebP; add approved project descriptions and more job photographs. |
| Medium | Rating summary and review excerpts are hardcoded and may become stale. | Retained the slider, added a pause/resume control, disabled automatic rotation by default for reduced-motion users, and linked to a Google Maps lookup. No self-serving review-star structured data added. | Owner must validate actual quoted review wording and the current rating/count and provide a verified direct review-profile URL. |
| Medium | Local listing details could conflict after site migration. | Used the published main line `814-926-6646` and published additional line `724-953-6712` consistently. Service-area language stays at Meyersdale/Somerset County. | Update Google Business Profile's website to the new canonical domain; confirm categories, hours, service areas, phone priority and business name; maintain consistency on other directories. |
| Medium | Search ranking/performance reporting unknown. | Added necessary site discovery files and page structure. | Verify Search Console Domain property with Cloudflare TXT record. Submit sitemap; check indexing, query impressions and coverage. Performance baseline is not available until live tests run. |
| Medium | Mobile overlays, automatic slider movement and sticky call treatment may impair user experience. | Earlier changes stacked hero/About information below photos; added accessible pause and reduced-motion support to review carousel. New subpages are responsive. | Perform live 360px/390px and tablet checks and measure Core Web Vitals on the deployment. |
| Low | External font loading and inline homepage CSS. | Current Google Fonts have preconnect and display swap; added image priority controls for hero. | Consider system-font fallback or self-hosting if measured LCP/CLS indicate a problem; do not change blindly. |

## Local search priorities

### Search intent, pages and keyword themes
Target useful, geographically honest language—avoid naming towns not actually served.

| Page | User intent / theme |
|---|---|
| `/` | HVAC contractor in Meyersdale, PA; heating and cooling near Somerset County |
| `/services/` | HVAC repair, replacement and maintenance in Meyersdale |
| `/services/air-conditioning/` | AC repair and installation; cooling service |
| `/services/heating-furnaces/` | Furnace repair; heating replacement; oil-furnace seasonal maintenance |
| `/services/mini-splits/` | Ductless mini-split consultation and installation |
| `/services/heat-pumps/` | Heat pump heating/cooling consultations and service |
| `/services/maintenance/` | HVAC preseason checks and repair |

The new pages are written with distinct factual subject matter. Before expanding beyond these pages, gather specific owner-supplied service details and real completed jobs to avoid boilerplate city/service doorway pages.

### Google Business Profile
- Log into the owner's actual Business Profile and update **Website** to `https://mtdavishvac.com/` (do not create a duplicate listing).
- Verify the displayed main and emergency phone numbers, categories, actual public hours vs emergency availability, and where the owner truly serves.
- Upload owner-approved original photos of real work, labeled meaningfully.
- Request additional authentic Google customer reviews in accordance with Google's review policies. Do not purchase or fabricate them.
- Link directly to the Google listing/reviews from the website; the current button uses a Maps search with the verified place identifier.
- If the business is a service-area business and the address is private, do not publish its street address in site schema or on the site without owner approval.

### Indexation and ownership
1. Open Google Search Console and create a **Domain** property for `mtdavishvac.com` (not a temporary workers.dev property).
2. Add Google's verification TXT record in **Cloudflare DNS**; it is separate from the Microsoft 365 TXT records. Leave email TXT/MX/CNAME/SRV records untouched.
3. Submit `https://mtdavishvac.com/sitemap.xml`, inspect homepage and service pages, request indexing if appropriate.
4. After the migration, monitor redirects, old indexed GoDaddy URLs, Core Web Vitals, and Search Performance queries.
5. Optionally verify the domain with Bing Webmaster Tools.

### Canonical and redirect checks
- Preferred host is **https://mtdavishvac.com**.
- In Cloudflare zone **Rules -> Redirect Rules**, create a wildcard 301:
  - Request: `https://www.mtdavishvac.com/*`
  - Target: `https://mtdavishvac.com/${1}`
  - Preserve query strings: ON
- Ensure the `www` hostname is proxied/routed to Cloudflare so rules run.
- Check `http://` is upgraded via Cloudflare HTTPS settings.
- Test `/services` legacy redirect and any additional historic paths found in GoDaddy/Google search results.
- Keep Cloudflare Worker static assets connected to the correct GitHub production branch.

### Production smoke-test commands (Windows PowerShell)
```powershell
curl.exe -I --http1.1 https://mtdavishvac.com/
curl.exe -I --http1.1 https://mtdavishvac.com/robots.txt
curl.exe -I --http1.1 https://mtdavishvac.com/sitemap.xml
curl.exe -I --http1.1 https://mtdavishvac.com/services/air-conditioning/
curl.exe -I --http1.1 https://mtdavishvac.com/services/
curl.exe -I --http1.1 https://mtdavishvac.com/services
curl.exe -I --http1.1 https://www.mtdavishvac.com/services/mini-splits/
```
Check first four return **200**, and expected redirects return **301** where configured. Use `View Source` to verify live canonical and lack of `noindex`. Check the pages visually on mobile; a 200 status by itself does not prove correct HTML or images.

## Pending owner details — essential before calling the conversion workflow complete
1. **Activate the approved quote inbox:** user confirmed `mark@mtdavishvac.com`; FormSubmit must send a first-use activation email and the owner must approve it. Then submit a second test and verify receipt before promoting online quote submissions.
2. Confirm advertised 24/7 emergency dispatch vs office hours and the exact geographical boundaries.
3. Supply full-resolution versions of actual jobs and written consent for web publication.
4. Approve and verify the exact original Google review excerpts and current rating/count; supply a verified direct Google review-profile link if available.
5. Approve whether to expose a physical address; do not publish a private home address automatically.

## External reference documentation
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google local-business structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google self-serving review markup limits: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Google Search Console: https://search.google.com/search-console
- Cloudflare WWW-to-apex rule example: https://developers.cloudflare.com/rules/url-forwarding/examples/redirect-www-to-root/
- Cloudflare Worker static-asset redirects: https://developers.cloudflare.com/workers/static-assets/redirects/
