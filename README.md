# Mt Davis HVAC website

**Live website:** https://mtdavishvac.com/  
**Source:** ben219brown/MtDavisHvac (`main`)  
**Hosting:** Cloudflare Worker static assets with GitHub integration

## Production implementation (24 September 2026)
- Indexed homepage with canonical URL, title and meta description, Open Graph and branded social-sharing preview.
- Five unique HVAC service pages, a services hub, contact page, privacy notice and noindex submission confirmation page.
- Local HVACBusiness, Service, ContactPage and breadcrumb JSON-LD, without self-serving review-star markup.
- `robots.txt` and a complete XML sitemap.
- **Approved mountain-icon favicons:** ICO, 32px PNG, 192px PNG, Apple touch icon and web manifest.
- Genuine project images locally stored under `hvac-assets/`, not hotlinked to the old GoDaddy website.
- Real quote form configured to post to FormSubmit for **mark@mtdavishvac.com**. Fields include consent and an anti-spam honeypot. Confirmation redirects to `/thank-you/`.

**ACTION REQUIRED:** The business mailbox owner must submit a test through the website and click FormSubmit's one-time activation link when it arrives. Until then, there is no confirmation the owner receives form submissions. FormSubmit is a third-party service. Test delivery after activation. For emergency inquiries, visitors should call the published phone number.

## Website assistant (staged)

A responsive guided lead-intake assistant is available in this branch across the homepage, contact and service pages. It asks structured HVAC intake questions, offers an explicitly opt-in AI-generated follow-up when the separate Cloudflare Worker is configured, and submits reviewed/consented requests with transcript to the same FormSubmit business mailbox. If AI is unavailable, the rest of the assistant works using a standard follow-up question. The original quote form remains unchanged.

**Before promoting this feature:** follow [chat-worker/README.md](chat-worker/README.md) to deploy the separate Worker and store the OpenAI API key as a Cloudflare secret, set an API spend limit, secure the endpoint, confirm mailbox activation and run a complete email-delivery test. Do not change the root website Worker or Microsoft 365 DNS records as part of chatbot deployment.

## Domain and DNS
- Preferred public URL: `https://mtdavishvac.com/`.
- On 24 September 2026 an external GitHub-hosted network test verified the root site returned 200, displayed the new form, had no homepage noindex, and served favicon.ico, favicon PNGs, robots.txt, sitemap.xml, branded social preview and contact/services pages.
- **Outstanding:** `https://www.mtdavishvac.com/` still returned 200 rather than 301 in that test. Configure a Cloudflare *zone redirect rule* from WWW to the root host, retaining path and query string. GitHub `_redirects` cannot implement host-to-host redirects.
- Do **not** change Microsoft 365 or GoDaddy email DNS records.

## Google SEO setup (requires account access)
1. Open Google Search Console using an owner-controlled account and add **Domain property** `mtdavishvac.com`.
2. Add Google's TXT verification record in Cloudflare DNS. **Do not alter the business-email TXT/MX/SRV/CNAME records.**
3. Submit `https://mtdavishvac.com/sitemap.xml`; inspect the homepage and service pages.
4. Update the existing Google Business Profile's **website URL** to `https://mtdavishvac.com/` without creating a duplicate listing.
5. Confirm service areas, listed business hours/emergency availability, photo publication permission and the five existing review quotes/summary. These require business-owner approval and current verification.

## Content operations
Real work photos can be supplied via email or a shared folder. Optimize each image and add an appropriately labeled gallery card with `data-category`. Avoid unapproved or stock work imagery.

The site has an automated GitHub Action at `.github/workflows/site-qa.yml`, which checks the site's SEO tags, sitemap consistency, local assets and quote-form configuration on every commit.

For the detailed audit, see `SEO_AUDIT.md`.
