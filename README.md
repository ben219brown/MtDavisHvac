# Mt Davis HVAC — website

Static website for Mt Davis HVAC, prepared for Cloudflare Pages.

## Files
- `index.html` — homepage, service cards, responsive photo gallery, and review carousel.
- `hvac-assets/` — copies of the approved Mt Davis installation photographs and vector Bosch/Fujitsu logos. These are locally hosted; do **not** hotlink the old GoDaddy image URLs.
- The previous demo remains unchanged in the JobSnapAppSite repository until this site is approved and live.

## Cloudflare Pages setup
1. Create a **Pages** project connected to `ben219brown/MtDavisHvac`.
2. Production branch: `main`.
3. Framework preset: **None**.
4. Build command: `exit 0` (or leave blank if allowed).
5. Build output directory: `.` (the repository root). Keep the root directory at its default.
6. Deploy and test the temporary `*.pages.dev` site **before** changing mtdavishvac.com DNS.

## Before launch
- Confirm the business phone numbers, service area, emergency hours, and destination email for the quote form (currently a `mailto:` demonstration, **not** a server-submitted form).
- Check each quotation in the review carousel with the owner against the original public review and obtain approval for publication; review count and average rating are currently hardcoded and should be refreshed.
- Remove `<meta name="robots" content="noindex,nofollow">` and the footer's demo wording **only after owner approval and when the new domain is ready**.
- Verify the contact workflow on a mobile device.
- Check spelling, image alt text, gallery categories, and links.
- Save all existing DNS records (especially MX, SPF, DKIM, DMARC) before pointing the existing domain's nameservers away from GoDaddy.

## Adding work photos
1. Send approved, properly named photographs in categories such as Heating, Cooling, Mini-Splits, Heat Pumps, and Service.
2. Optimize large images (prefer WebP or appropriately compressed JPEG).
3. Add images in `hvac-assets/`; add matching cards in the gallery section of `index.html` with `data-category` tags.
4. Commit to `main`; Cloudflare Pages will redeploy automatically.

The gallery is currently a **static, categorized gallery** rather than a web-based upload system. The owner can send photos to the site maintainer, or later use a separate private upload form and editorial workflow.
