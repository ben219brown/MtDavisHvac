# Mt Davis HVAC: zero-additional-cost AI chatbot

The chatbot has an optional **real AI** follow-up powered by Cloudflare Workers AI. No OpenAI account, API key or monthly chatbot subscription is required.

**Critical billing condition:** Deploy this optional AI Worker ONLY in a Cloudflare account on the **Workers Free** plan, with **no upgrade to Workers Paid and no paid AI Gateway credits**. As of September 2026 Cloudflare includes 10,000 Workers AI Neurons/day on Workers Free. Exceeding that allocation causes AI requests to fail, not to incur an overage charge on a Free account. The chatbot then asks its standard follow-up and still gathers/emails the request. The separate Worker also shares the account's 100,000 free Worker requests/day allocation. Do not deploy this feature to a paid Workers account without separately implementing and verifying a HARD daily spending guard.

Cloudflare can change free-tier terms, supported free models and limits. Review official pricing before deployment and periodically afterward. Existing costs for the domain, business email and current website hosting are not eliminated by this feature.

## Customer workflow
The widget is included on the homepage, service pages, contact page and privacy page. It collects inquiry type, property type, equipment, urgency, issue, one optional follow-up, town/ZIP, name, phone, optional email and contact preference.

AI is **explicitly optional** and requires opt-in before sending equipment category and a redacted issue description to Cloudflare Workers AI. Personal contact fields and full chat history are NEVER added as separate AI inputs. Visitors are warned not to put personal details in their free-text issue description. It is not a technician or emergency dispatch service; gas/CO/smoke/fire warnings bypass AI.

After customers review their answers and agree to submission, the completed lead and chat transcript are sent to the existing **free FormSubmit** AJAX email service. The original quote form remains intact. The Worker itself never emails or stores leads.

## Deploy / verify
1. Confirm the Cloudflare Workers account hosting this *separate* chat Worker is on the **Free** plan. Do not enable Workers Paid, paid AI Gateway credits or another pay-as-you-go AI option. If the existing website is under a paid Workers account, use a separate Free account's workers.dev hostname instead; then update the constant AI_URL in chatbot.js to that exact workers.dev URL. A custom domain under mtdavishvac.com requires the Cloudflare account that controls the zone.
2. Verify current FormSubmit activation: have Mark submit a test to the existing form, click the one-time activation email if applicable, then confirm a real email reaches the business mailbox.
3. With Wrangler 4.36+ authenticated to the appropriate Cloudflare Free account, run from this chat-worker folder: npx wrangler deploy. The checked-in configuration deploys an isolated Worker to the chat.mtdavishvac.com custom domain. Confirm no existing DNS record uses that hostname. If using a standalone free account, modify the Wrangler route and enable a workers.dev endpoint, then update AI_URL accordingly.
4. The Worker declares the AI binding `AI` and invokes `@cf/zai-org/glm-4.7-flash`, which Cloudflare listed as supported on Workers Free in July 2026. **No API key, secret or billing details are required.**
5. Test: request an AI follow-up, skip AI, disable AI to observe the scripted fallback, choose an emergency option, verify mobile controls, review consent and submit a test. Check the FormSubmit response AND receipt of the actual email, including transcript. Verify production only after successful delivery.
6. Keep the Worker on the free plan. Review Cloudflare Workers AI free-tier usage and limits if model availability or pricing changes. Built-in rate limits reduce quota exhaustion but are not a billing cap on paid plans.

## Service boundaries
- Visitor web page: chatbot.js and chatbot.css; no external AI keys.
- Optional AI endpoint: chat.mtdavishvac.com/chat (Cloudflare Workers AI free plan only).
- Email delivery: existing FormSubmit AJAX endpoint to the established Mt Davis HVAC recipient, subject to its published free-service terms and mailbox activation.
- Fallback: when the Worker is absent, quota is exhausted, the service times out, or user declines AI, the chat still collects information and attempts to send it through FormSubmit.
- Do not touch current root/WWW routing, SEO, photos, Microsoft 365 mail DNS or the existing contact form while rolling out the assistant.

Official references:
- Cloudflare Workers AI pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
- Cloudflare Workers AI model: https://developers.cloudflare.com/workers-ai/models/glm-4.7-flash/
- Cloudflare Workers Free pricing: https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare Worker AI bindings: https://developers.cloudflare.com/workers-ai/configuration/bindings/
- FormSubmit: https://formsubmit.co/
