# Search engine verification files

Place ownership-verification files in this directory before a production build:

- Google Search Console: `google<token>.html`
- Bing Webmaster: `BingSiteAuth.xml`

`scripts/build_research_site.py` copies only files matching those names to the deployed site root. Do not commit account credentials, API keys, or unrelated files here.

See `docs/seo-geo-release-runbook.md` for the complete post-deployment checklist.
