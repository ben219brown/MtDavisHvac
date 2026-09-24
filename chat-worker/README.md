# Mt Davis HVAC website assistant

This dedicated Cloudflare Worker is intentionally separate from the existing Cloudflare static website Worker. Do not replace the existing Worker or change any mail-related DNS.

## Visitor flow

The website assistant collects inquiry type, home/business, equipment, urgency, issue description, optional AI follow-up, town/ZIP, name, phone, optional email, and contact preference. Visitors review their answers and must consent before their information is sent to FormSubmit's AJAX service for delivery to the existing business inbox. No lead is stored by the Worker. If the AI Worker fails or is not yet deployed, the chat asks a standard follow-up question and can still submit the lead.

Only the equipment category and redacted issue text are sent to the AI Worker, never the separately collected contact fields or chat history. Visitors must avoid including personal information in the issue text. For gas, CO, smoke or fire warnings, the widget bypasses AI and tells visitors to contact emergency services or a gas utility from a safe location. It does not perform live dispatch or equipment diagnosis.

## Deploy and activate

1. Review the website assistant, privacy notice and any data-handling expectations with the business owner. Publish static-site changes through the normal GitHub-to-Cloudflare workflow, preserving the existing form.
2. Have the owner submit a test to the existing homepage FormSubmit form. Click FormSubmit's mailbox activation link if needed; confirm a real test reaches the inbox. An AJAX success response alone cannot prove mail delivery.
3. Create an OpenAI API project, enable API billing, set conservative project spend limits and alerts, and obtain an API key. A ChatGPT subscription is not an API billing account.
4. Using the correct Cloudflare account, from this chat-worker directory run: npx wrangler deploy. Wrangler 4.36 or later is required for rate-limit bindings. The configuration provisions the separate mtdavishvac-chat Worker with a custom domain, chat.mtdavishvac.com. Check for conflicting DNS records first. Cloudflare normally creates this subdomain record; do not touch the main website's DNS or Microsoft 365 mail records.
5. From the same directory, run: npx wrangler secret put OPENAI_API_KEY. Supply the project API key only when prompted; never commit it. For local development, use a git-ignored .dev.vars file, never GitHub.
6. Add appropriate Cloudflare WAF protection and watch Worker logs and OpenAI spending. The built-in limits allow up to 3 requests per visitor IP and a coarse 30 requests globally per minute per Cloudflare edge location. They are soft abuse safeguards, NOT a financial hard limit. Consider server-side Turnstile validation if abuse occurs.
7. Test on a published site: guided chat, case-specific AI question, fallback when API unavailable, emergency call-out, phone/email validation, mobile layout, consent, FormSubmit success and failure, and the actual email delivered to the owner.

## Integration notes

AI endpoint: https://chat.mtdavishvac.com/chat. It accepts POST JSON with service and issue fields from the website Origin only. A command-line request must include an allowed Origin header for testing; spoofing that header alone is still possible for non-browser clients, so continue to monitor abuse.

Static assets: /chatbot.js and /chatbot.css, injected on homepage, contact, privacy and service pages. The ordinary quote form remains in place. The FormSubmit recipient address is present in the browser code because the current provider's AJAX integration requires it; after verifying the mailbox the owner can set up FormSubmit's invisible-email alias to remove it from the code.

References:
- https://formsubmit.co/ajax-documentation
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
- https://platform.openai.com/docs/api-reference/responses

Release blocker: Do not claim that AI answers are active or that real lead emails are arriving until the dedicated Worker has been deployed with its secret and FormSubmit mail delivery has been verified.
