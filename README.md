# Mt Davis HVAC website

Production static website for **Mt Davis HVAC**, powered by the `ben219brown/MtDavisHvac` GitHub repository and deployed through Cloudflare Workers (static assets).

## Site structure
- `index.html`: homepage, project gallery and Google customer review carousel.
- `services/index.html`: all-services directory.
- `services/*/index.html`: targeted, unique service pages for air conditioning, heating and furnaces, mini-splits, heat pumps, and maintenance.
- `service-pages.css`: responsive styles shared by the service pages.
- `hvac-assets/`: self-hosted Mt Davis project images and Bosch/Fujitsu vector logos.
- `favicon.svg`: site icon.
- `robots.txt` and `sitemap.xml`: indexing and sitemap discovery.
- `_redirects`: intended Cloudflare static asset redirects for legacy /services and /contact paths.
- `_headers`: baseline security and file-type headers.
- `SEO_AUDIT.md`: implementation record and outstanding launch tasks.

Do **not** replace the images with links to the old GoDaddy image CDN; earlier direct hotlinks caused broken images.

## Current contact conversion
Customers can reliably **call** either published number:
- Main: (814) 926-6646.
- Additional / emergency: (724) 953-6712.

The demo email-to-quote form was deliberately disabled: its `mtdavishvac@protonmail.com` recipient was never independently confirmed. Before restoring a production online form, obtain an owner-approved inbox and a hosted form endpoint (e.g. a properly configured Cloudflare Worker with spam protection and a verified email-delivery service). Do not place an unverified or nonfunctional HTML form on the live site.

## Deployment verification
Git commits should cause a new Cloudflare deployment **if its GitHub build integration is enabled**. After deployment, verify in an incognito browser:
1. Homepage and every `/services/...` page return HTTP 200 and show the new content.
2. Local images, SVG logos, favicon, `/robots.txt`, and `/sitemap.xml` load.
3. View page source to verify canonical URL and that no `noindex` directive remains.
4. Check `/services` and `/contact` redirects; Cloudflare Workers with static assets supports `_redirects`, but confirm the current build serves those rules.
5. Confirm the Cloudflare **Single Redirect** from `www.mtdavishvac.com` to `https://mtdavishvac.com` (301, preserve path and query string). This is a dashboard configuration; `_redirects` cannot match hostnames.
6. Check mobile layout, phone links, review carousel and gallery.
7. Verify that Microsoft 365/GoDaddy-related email DNS records remain DNS-only and untouched.

## Google setup
1. Verify `mtdavishvac.com` as a **Domain** property in Google Search Console by adding the supplied TXT record in Cloudflare DNS.
2. Submit `https://mtdavishvac.com/sitemap.xml`.
3. Inspect the homepage and main service URLs, request indexing where appropriate, and monitor indexing reports and queries.
4. Update the Google Business Profile website URL and maintain consistent main phone, areas served, services and genuine project photos.
5. Reconfirm copied review excerpts with the owner and check whether the hardcoded 5.0 / 27 rating summary has changed. The site intentionally does **not** use self-serving review-star structured data.

## Photo updates
Have the owner send original work photographs, with approval to publish, through a shared folder or email. Organize high-resolution originals by project and add optimized WebP/JPEG versions and useful captions. The current photos are small files, so replace them when original full-resolution photos are provided. Commit updates to GitHub to publish.

**Never remove or repurpose business email DNS records to support website-only changes.**
