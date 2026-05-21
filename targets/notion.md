# Notion

Date observed: 2026-05-19 
URL: https://notion.so
Category: Productivity 

## Tech stack (from Wappalyzer)
- JavaScript framework: Next.js 14.2.35, React
- PaaS / hosting: Vercel, Amazon Web Services
- CDN: Cloudflare, Amazon S3
- Issue tracker / error monitoring: Sentry
- Feature management: Statsig 3.32.6
- Analytics / advertising: LinkedIn Insight Tag, LinkedIn Ads
- Security: hCaptcha
- Cookie compliance / privacy: Transcend
- Protocol / metadata: HTTP/3, Open Graph

## Third-party scripts loaded
Filtered Network tab to JS: 82 requests across 3 distinct domains:

- **www.notion.com** — ~79 requests. All third-party SDKs (Sentry, Statsig, Transcend backend) appear to be first-party proxied: hosted on Notion's own servers and served from notion.com rather than from each service's CDN. Visible filenames include `airgap.js`, `sentry.next.*.js`, `transport-support.*.js`. Performance-, privacy-, and supply-chain-motivated.
- **transcend-cdn.com** — 2 requests (`ui.js`, `airgap.js`). Consent UI loaded directly from Transcend rather than proxied. Likely so Transcend can push regulatory updates without requiring Notion to redeploy.
- **accounts.google.com** — 1 request (`client`). Google identity client for "Sign in with Google." Cannot be proxied for OAuth security reasons.

Architectural observation: Notion proxies third-party JavaScript through their own domain rather than loading directly from third-party CDNs. This is a mature security/privacy choice — it bypasses ad-blockers (improving analytics reliability), reduces supply-chain risk (Notion controls when third-party updates take effect), and minimizes DNS/TLS overhead.

## API endpoints visible in JS
- No application API URLs visible in inline HTML.
- All 12 "api" matches are references to __tcfapi (IAB Transparency & Consent Framework JavaScript API), used for GDPR cookie-consent handling. This is a privacy-compliance stub, not a Notion application endpoint.

## Feature flag system (if identified)
- Wappalyzer detected Statsig 3.32.6 on page.
- Zero matches for "flag" or "statsig" in inline HTML view-source. Statsig SDK loads from external bundle or is initialized after consent gate, not inline. No flag names, client keys, or environment IDs visible in initial HTML response.
- Compare across targets: which sites embed flag config in inline HTML vs. lazy-load it.

## Tokens / keys observed
- sentry-public_key: d9ffc21a... — Sentry DSN. Public by design. Required for client-side error reporting. Sentry's security model does not depend on this being secret; the worst-case misuse is polluting Notion's error stream. NOT a vulnerability.
- No items matching "token" found in inline HTML. (Expected for a public landing page — auth tokens are user-specific and post-login.)

## Security headers
- **Grade (securityheaders.com): A** (capped at A, not A+, due to CSP warnings — see below)

### Present:
- **Content-Security-Policy** — full allowlist for scripts, styles, frames, workers, child resources. Notable allowed script-src domains include `*.sentry.io`, `*.hcaptcha.com`, `js.stripe.com`, `cdn.amplitude.com`, `http-inputs-notion.splunkcloud.com` (Splunk Cloud HEC endpoint — Notion's SIEM), and AI support vendors `solve-widget.forethought.ai`, `decagon.ai`, `sierra.chat`.
- **Strict-Transport-Security**: `max-age=31536000; includeSubDomains; preload` — gold-standard HSTS. One-year enforcement, applies to all subdomains, on the browser-vendor preload list.
- **Referrer-Policy**: `strict-origin-when-cross-origin` — leaks only the origin (not the full URL) to other sites.
- **X-Frame-Options** — present, supplemented by `frame-ancestors` in CSP.

### Warnings:
- CSP `script-src` contains `'unsafe-inline'` and `'unsafe-eval'`. These are escape hatches that weaken the CSP's anti-XSS effectiveness. Almost certainly required by Notion's Next.js/React/third-party-SDK stack — removing them would be a significant engineering project. Tradeoff is defensible but represents the gap between A and A+.

### Missing:
- **X-Content-Type-Options** (`nosniff`) — would prevent MIME-sniffing. Minor gap.
- **Permissions-Policy** — would explicitly disable camera/mic/geolocation/etc. for the page. Free hardening that's missing.

### Notable Raw Headers:
- `server: cloudflare` — confirms CDN
- `x-powered-by: Next.js` — leaks framework (minor hardening miss; strip recommended)
- `x-vercel-cache: MISS` — confirms Vercel hosting
- `cf-ray: 9fe979bd3d833c2a-DUB` — request was served from Cloudflare's Dublin POP 

## Source maps exposed?
- No `sourceMappingURL` references found in inline HTML. Source maps either not generated, or uploaded privately to Sentry and stripped from public assets. Either way, no public access to original (un-minified) source code from this entry point.
- Note: external JS bundles may still reference source maps; can only confirm definitively by inspecting each bundle in DevTools Sources tab.

## Public files
- robots.txt: Present, disciplined. Disallow rules are index-hygiene only
  (search pages, experiments, embeds) — no sensitive paths leaked. Corroborates
  Vercel (Disallow: /_vercel/insights/view). One named path of interest:
  /product/agents-homepage. Aggressively blocks SEO/AI scrapers (Ahrefs,
  Semrush, Amazonbot, BLEXBot, dotbot). Reveals subdomain: sitemaps.notion.com.
- security.txt: ABSENT (404). No published disclosure contact via this convention.
- sitemap.xml: Sitemap INDEX (not flat). Internationalized (es-es, zh-cn, …),
  segmented by section. Indicates large multi-locale public footprint. 

## Certificate transparency
- Subdomains visible (crt.sh, query *.notion.com): a few hundred certs. Distinct
  subdomains group into three tiers:
  - Production: www, app, api, mail, events, community, academy, trustcenter,
    developers, help, info, identity, file, faces, cloud, services.cloud.
  - Non-production (notable): stg.notion.com, dev.notion.com, prod.notion.com
    and wildcards; deeper: api-stg, integrations-api-stg, admin-stg, app.dev,
    mail.dev, identity.dev, file.dev, faces.dev.
  - Infra internals: imgproxy.infra-prod / infra-dev, regional prefixes
    (ap-northeast-1, us-west-2, eu-central-1), mail-resource-proxy.
- CT exposes full environment-tier topology (prod/staging/dev) passively. NOT
  PROBED — names recorded, none visited. (Discipline note for writeup.)
- Issuer history: earliest certs (2013–16) from paid CAs (GlobalSign, USERTrust,
  Comodo); migrated to automated issuance (Cloudflare, Let's Encrypt, Google
  Trust Services, Amazon) as they scaled. Maturity signal, not a hosting fact.

## Anything unusual
- No HTML comments found in production source. Build pipeline strips them — including framework boilerplate. Consistent with overall pattern of minimal-surface-area inline HTML.
- robots.txt independently corroborates Vercel hosting (second signal after the
  x-vercel-cache header in Security headers) — and reveals a previously unseen
  subdomain, sitemaps.notion.com, to verify in Certificate transparency.

## Network performance (from DevTools)
- 169 total requests
- 5.49 MB total transferred (uncompressed) / 164.74 kB (compressed/cached)
- DOMContentLoaded: 396 ms
- Load event: 1.98 s
- Finish: 43.45 s (background activity continues long after visible load)
- Architecturally: optimized for fast first paint, heavy lazy-loading of analytics/consent/error tooling

## Notes for write-up
- Stack is entirely modern, mainstream, and conservative. No homegrown infrastructure visible. Engineering posture appears mature: Sentry for error tracking, Transcend for privacy ops, hCaptcha for bot defense, Statsig for feature management. This is what a well-engineered SaaS looks like at the infrastructure layer.
- Page source contains only 12 matches for "api" and no API-shaped URLs are visible in the inline HTML. Page appears to be client-rendered (Next.js), so application code and API calls live in external JS bundles loaded after page-load. Methodology note: view-source alone is insufficient for modern SaaS recon; the Network tab and Sources tab are where the real signal lives for these sites.
- Page ships the IAB TCF consent stub as the first inline script in <head>, before any other JavaScript runs. This is the gold-standard pattern for GDPR cookie consent: queue consent questions until the real consent platform (Transcend, per Wappalyzer) loads. Strong engineering signal — Notion is treating privacy compliance as infrastructure, not as an afterthought tacked onto the marketing site.
- Worth comparing across targets: which sites ship a TCF stub in the head, which ship a banner-only solution, and which ship nothing.
- Sentry DSN visible in inline HTML. This is by design (Sentry's security model assumes the DSN is public), but the visibility of "sentry-public_key=..." in 30 seconds of recon is a useful illustration of how much can be learned about a site's infrastructure from passive observation. Worth noting in the writeup: many of the "credentials" found in landing-page recon are intentionally public — the discipline is knowing which are intentional and which aren't.
- Pattern emerging: Notion's inline HTML is *unusually lean*. The first 55 lines are TCF consent infrastructure; the only credential visible is the Sentry DSN (intentionally public); Statsig is absent entirely from inline source despite being on the page. This is what disciplined client-side architecture looks like. Use as the "well-engineered baseline" target in the writeup — the standard other sites get measured against.
- Methodology insight from target #1: For modern client-rendered SaaS (Next.js, React, etc.), inline HTML view-source yields very little signal — the interesting code lives in external JS bundles loaded post-render. Page-source recon is necessary but not sufficient. The DevTools Network tab and Sources tab are where the real observations happen. The TCF consent stub and intentional public credentials (like the Sentry DSN) are the exceptions that prove the rule.
- Discovery: Notion uses first-party proxying for nearly all third-party JavaScript. The Wappalyzer-detected services (Sentry, Statsig, LinkedIn) are running, but their code is served from www.notion.com rather than each service's own CDN. This is uncommon at smaller SaaS and likely a deliberate engineering decision. Worth contrasting in the writeup against targets that load third parties directly.
- Methodology insight: Network tab on first-party-proxying sites looks "boring" but is itself a finding. The "boring" Network tab is the artifact.
- The CSP allowlist is itself an intelligence document. Beyond confirming services Wappalyzer detected (Sentry, hCaptcha), it reveals:
  - Splunk Cloud HEC as the SIEM (`http-inputs-notion.splunkcloud.com`) — client-side JS sends events directly to Splunk
  - Amplitude as a second product analytics platform alongside Statsig
  - Stripe for payment processing
  - Three different AI customer-support vendors (Forethought, Decagon, Sierra) — suggests active vendor evaluation
  - Sunshine Conversations (smooch.io) for messaging — Zendesk family
- CSP `unsafe-inline` and `unsafe-eval` are not negligence — they're a tradeoff most large React-based SaaS make. Worth comparing across targets: which ones manage strict CSP (likely smaller/newer sites with simpler stacks) vs. which accept unsafe-inline (likely larger SaaS with many vendors).
- HSTS configuration is gold-standard; missing X-Content-Type-Options and Permissions-Policy are free hardening Notion hasn't added yet.
- Public-files discipline as a maturity signal: clean robots (no leaks), no
  accidental path disclosure. Worth tracking the security.txt present/absent
  ratio across all 10 — that ratio is a finding in itself, not any single 404.
  - sitemaps.notion.com (seen in robots.txt) did not appear as a named identity
  in crt.sh — likely covered by a *.notion.com wildcard cert rather than its own,
  so it can't be independently confirmed via CT. Not a discrepancy; just noted.

  ## Posture summary

Notion presents one of the leanest, most disciplined public surfaces you could
pick as a baseline target — restraint at every layer. Production HTML is stripped
of comments and exposes no API endpoints or unintended secrets (the lone Sentry
DSN is public by design); meaningful client config loads from external bundles;
security headers earn an A with gold-standard HSTS and a rich CSP; robots.txt
leaks nothing. The richest intelligence came not from mistakes but from things
Notion publishes on purpose: the CSP allowlist mapped their full third-party
vendor stack (Splunk as SIEM, Stripe, Amplitude, three AI support vendors), and
certificate transparency exposed their entire prod/staging/dev environment
topology. Hardening gaps are minor and cosmetic — two missing low-impact headers,
a framework-version leak via x-powered-by, no published security.txt. Net read:
a mature engineering org whose attack surface is small by design, where the
useful recon signal lives in public-by-design metadata, not leaks.