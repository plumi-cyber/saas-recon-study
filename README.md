# SaaS Landing Page Recon Study

A passive OSINT study of what 10 well-known B2B SaaS companies expose in their public landing pages — no logins, no probing, no testing of discovered endpoints.

Motivated by the @weezerOSINT ClickUp thread (April 2026), which showed how much enterprise risk lives in plain JavaScript bundles.

**Status:** Targets selected. Recon phase beginning.

## Scope
- 10 public B2B SaaS landing pages
- Observation only: page source, network tab, DevTools, public DNS, certificate transparency
- No interaction with any discovered endpoints, keys, or tokens

## Targets
A balanced mix across categories, company sizes, and recognizability:

| # | Company   | Category                  |
|---|-----------|---------------------------|
| 1 | Notion    | Productivity              |
| 2 | Linear    | Project management        |
| 3 | Loom      | Async video               |
| 4 | Intercom  | Customer support          |
| 5 | HubSpot   | Marketing / CRM           |
| 6 | Mailchimp | Marketing / email         |
| 7 | Sentry    | Error tracking            |
| 8 | Vanta     | Compliance / security     |
| 9 | Gusto     | HR / payroll              |
| 10| PostHog   | Product analytics         |

One file per target lives in `targets/`. The template they were generated from is `targets/_template.md`.

## Methodology
See `writeup/methodology.md` (coming soon).

## Findings
See `writeup/findings.md` (coming soon).

## Author
Oluwapelumi Kolawole.  
[GitHub](https://github.com/plumi-cyber)
