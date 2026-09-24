# Mt Davis HVAC — full SEO audit
**Audit date:** 2026-09-24  
**Primary domain:** https://mtdavishvac.com/  
**Repository:** ben219brown/MtDavisHvac  
**Scope:** production HTML/CSS, on-page SEO, local-business data, technical crawlability, site migration, images, content architecture, UX/conversion and measurement.

This is a source-code/content and publicly available listing review. **It is not a completed live Core Web Vitals measurement or a Google Search Console crawl audit.** Cloudflare deployment, redirect responses and actual search-indexing status must be verified separately.

## Findings and implementation

| Priority | Finding | Work in this repository | Remaining verification |
|---|---|---|---|
| Critical | Homepage carried `noindex,nofollow` from the demo. | Removed; set index/follow. | Check live page source and HTTP `X-Robots-Tag` after Cloudflare deploy, then inspect in Search Console. |
| Critical | Quote form opened an unverified `mtdavishvac@protonmail.com` mailbox via `mailto:`; there was no actual form backend. | Removed unreliable submission and replaced with published click-to-call choices. | Business owner supplies and approves a destination inbox; configure secure form delivery and anti-spam before reintroducing the form. |
| High | No explicit canonical or social preview metadata. | Added canonical, unique homepage title/description, Open Graph/Twitter metadata and favicon. Added unique metadata to service pages. | Inspect rendered metadata and social-preview tests; obtain a higher-resolution project image for social sharing. |
| High | No accessible sitemap or robots asset was present in the migrated repo. | Added `robots.txt` and `sitemap.xml` listing 7 intentional indexable URLs and genuine project images. | Verify they return HTTP 200, then submit sitemap in Google Search Console. |
| High | Existing homepage tried to cover all services on a single URL. | Added one service hub plus five distinct service pages: AC, heating/furnaces, mini-splits, heat pumps and maintenance. Linked from the homepage and to one another. | Confirm pages are live; expand details using information verified by the business owner and actual project-specific photos. |
| High | No business-identity markup. | Added `HVACBusiness` JSON-LD on homepage with verified main phone, city/region, service area, service catalog and Google Maps lookup. Added Service/Breadcrumb markup on each service page. | Test markup using Google Rich Results Test and Schema.org validator after deploy. Add complete business address ONLY if owner approves public publication. |
| High | Legacy GoDaddy `/services` page may have backlinks or be indexed. | Added intended Cloudflare static asset redirect `/services -> /services/`; mapped potential `/contact` redirect to homepage contact section. | Test HTTP 301 in the actual Worker deployment. Check Search Console old URL reports for additional historic paths. |
| High | Both `www` and apex may serve the same content. | Every page has one apex canonical URL. | In Cloudflare zone Rules -> Redirect Rules, make `www` permanently redirect to apex, preserving path and query. Confirm no loops. |
| Medium | Public photo gallery contains just 3 distinct project photographs; 2 of these are reused on multiple pages. | Retained authentic, locally hosted project photos (not stock) and descriptive ALT/captions. Homepage hero has fetch priority high; below-fold photos use lazy loading and async decode. | Get originals at >=1200px wide; optimize in WebP; add approved project descriptions and more job photographs. |
| Medium | Rating summary and excerpts are hardcoded. | Verified public business listing at audit time displayed 5.0 / 27 reviews; retained slider and added a direct Maps reviews link. **No review/aggregateRating JSON-LD** was added because Google disallows self-serving business review-star markup. | Owner verifies permission/accuracy of copied excerpts; recheck summary periodically and correct it as review count changes. |
| Medium | Local listing details could conflict after site migration. | Used the published main line `814-926-6646` and published additional line `724-953-6712` consistently. Service-area language stays at Meyersdale/Somerset County. | Update Google Business Profile's website to the new canonical domain; confirm categories, hours, service areas, phone priority and business name; maintain consistency on other directories. |
| Medium | Search ranking/performance reporting unknown. | Added necessary site discovery files and page structure. | Verify Search Console Domain property with Cloudflare TXT record. Submit sitemap; check indexing, query impressions and coverage. Performance baseline is not available until live tests run. |
| Medium | Mobile visual overlays and sticky call treatment previously caused problems. | Prior mobile layout changes now stack hero/About information below photos. New subpages use responsive layouts. | Perform hands-on 360px / 390px / tablet testing and PageSpeed Insights mobile/desktop tests on the deployed version. |
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
1. **Which email inbox should receive quote requests?** Previous demo's Proton address was never confirmed. Choose whether online requests should use a hosted service or a Cloudflare Worker backend with spam protection and verified delivery.
2. Confirm advertised 24/7 emergency dispatch vs office hours and the exact geographical boundaries.
3. Supply full-resolution versions of actual jobs and written consent for web publication.
4. Approve the excerpts in the review slider and confirm any phone or branding corrections.
5. Approve whether to expose a physical address; do not publish a private home address automatically.

## External reference documentation
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google local-business structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google self-serving review markup limits: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Google Search Console: https://search.google.com/search-console
- Cloudflare WWW-to-apex rule example: https://developers.cloudflare.com/rules/url-forwarding/examples/redirect-www-to-root/
- Cloudflare Worker static-asset redirects: https://developers.cloudflare.com/workers/static-assets/redirects/
