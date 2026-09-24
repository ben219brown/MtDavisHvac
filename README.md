# Mt Davis HVAC — production website

Public static website for Mt Davis HVAC, deployed with **Cloudflare Workers static assets** from the `ben219brown/MtDavisHvac` GitHub repository. Preferred public host: **https://mtdavishvac.com**. The original JobSnapApp demo was not changed by this migration.

## Structure and SEO

- `index.html` — production homepage, authentic installation photo gallery, accessible reviews slider, online quote form.
- `services/index.html` and `services/{air-conditioning,heating-furnaces,mini-splits,heat-pumps,maintenance}/index.html` — locally focused service pages with unique metadata, internal links, breadcrumbs and service structured data.
- `contact/index.html` — local HVAC contact page.
- `privacy/index.html` and `thank-you/index.html` — form privacy disclosure and noindexed form-confirmation page.
- `hvac-assets/` — authentic owner-site installation photographs and Bosch/Fujitsu vector logos. Do not hotlink GoDaddy images.
- `favicon-32.png`, `favicon-192.png`, `favicon.ico`, `apple-touch-icon.png`, `favicon.svg` — browser and mobile icons; PNG/ICO are derived from the user-approved screenshot.
- `social-preview.jpg` — 1200 × 630 sharing image using a real Fujitsu installation photo.
- `robots.txt`, `sitemap.xml`, `_redirects`, `_headers`, `site.webmanifest` — search discovery and static asset routing.
- `scripts/check_site.py` with `.github/workflows/site-qa.yml` — runs on GitHub pushes and PRs, checking SEO metadata, local assets, canonical URLs, sitemap and the form destination.
- `SEO_AUDIT.md` — full review, implemented measures and remaining verification.

## Online quote form — first-use activation required

The homepage form POSTs directly to **FormSubmit** and forwards submissions to the owner-approved email **markoplixo@gmail.com**. It uses a default spam check plus a honeypot and links to a privacy notice. Direct phone/email contact remains available if the form is unavailable.

**The site code alone does not activate email delivery.** After a Cloudflare deployment containing the form:
1. The owner or site manager opens **https://mtdavishvac.com/#quote** and makes a clearly labeled test submission using non-sensitive test details.
2. FormSubmit sends an activation email to **markoplixo@gmail.com**; the inbox owner must open it and approve the form.
3. Submit a **second** clearly labeled test form after activation and verify that its details reach **markoplixo@gmail.com**. Check spam/junk.
4. Verify redirection to **https://mtdavishvac.com/thank-you/** after a normal successful submission.

FormSubmit currently documents a free no-signup backend, a default CAPTCHA, and a 30-day submission archive. This is an external service, not a Cloudflare-native form handler. The owner must agree to that third-party processing. Do not announce the form as operational until step 3 succeeds.

## Cloudflare — required dashboard work

GitHub commits deploy automatically **only if the Worker’s GitHub build integration is still correctly connected and successful**. Check **Workers & Pages → mt-davis-hvac → Deployments** after changes.

Set up a permanent www-to-apex redirect in Cloudflare zone **mtdavishvac.com → Rules → Redirect Rules → Single Redirect**:
- Rule name: `Canonical WWW to apex`.
- Wildcard match: `https://www.mtdavishvac.com/*`.
- Target: `https://mtdavishvac.com/${1}`.
- Type: `301 Permanent Redirect`.
- Preserve query string: **On**.
- Ensure `www` is handled by Cloudflare and remains proxied. Remove no MX/TXT/SRV/CNAME records for email.

Host redirects **cannot** be implemented via the repository’s `_redirects` file: that file only matches URL paths.

## Search Console / business listing — manual ownership steps

1. Sign in to Google Search Console and add **Domain property** `mtdavishvac.com`. Add the **unique TXT verification record** Google gives you to **Cloudflare DNS** (leave Microsoft 365 and GoDaddy email DNS records intact).
2. Submit `https://mtdavishvac.com/sitemap.xml`, inspect the homepage and service pages, check index coverage and monitor Core Web Vitals.
3. Review the existing Google Business Profile (do **not** create a duplicate): website URL, actual hours/emergency availability, main phone, service areas, services and genuine project photos.
4. Approve the five existing review slider excerpts against their source reviews and recheck any displayed star rating or count before marketing the site.
5. Obtain higher-resolution approved installation photographs and regularly add them to the gallery.

## Smoke tests

```powershell
curl.exe -I --http1.1 https://mtdavishvac.com/
curl.exe -I --http1.1 https://mtdavishvac.com/robots.txt
curl.exe -I --http1.1 https://mtdavishvac.com/sitemap.xml
curl.exe -I --http1.1 https://mtdavishvac.com/favicon.ico
curl.exe -I --http1.1 https://mtdavishvac.com/social-preview.jpg
curl.exe -I --http1.1 https://mtdavishvac.com/services/air-conditioning/
curl.exe -I --http1.1 https://mtdavishvac.com/contact/
curl.exe -I --http1.1 https://www.mtdavishvac.com/contact/
```

Confirm normal pages and files return HTTP 200. Verify `www` responds with HTTP 301, preserving paths and query strings. A 200 for a `www` URL means the redirect isn't yet configured. Review mobile photos, logos, headings and the form after deploying; local static checks alone do not prove a live Cloudflare release.

## Photo publishing

The simplest initial workflow is for the owner to send job photos with a short project description and approval to publish. The maintainer optimizes/renames photos, adds them under `hvac-assets/`, creates gallery cards in `index.html` and commits to `main`. All images stay locally hosted. Do not use generic stock images as purported completed projects.
