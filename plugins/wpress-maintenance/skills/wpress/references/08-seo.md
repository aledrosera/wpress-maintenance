# Phase: seo

## Objective
One SEO plugin, The SEO Framework (owner preference), carrying all the SEO data the site already had, plus the SEO the site was missing.

## Determine
- SEO plugins present (active or not) and overlaps: more than one plugin printing titles, meta tags, structured data or sitemaps.
- SEO data stored by each one: per-content titles, descriptions, canonical URLs, robots directives, social titles, descriptions and images, primary terms, per-term and per-author data, global title templates, organization or person data, logo, social profiles, sitemap settings, breadcrumbs, redirects managed by the SEO plugin.
- What the source plugin renders besides head tags: breadcrumbs called from templates, content blocks or shortcodes, structured data.
- Rendered SEO of every covered URL (baseline snapshot): title, meta description, canonical, robots, social tags, structured data, sitemap URL and contents, robots.txt, search-engine visibility setting.
- Gaps: missing or duplicate titles and descriptions; indexable URLs without search value by nature; archives that redirect but are listed in the sitemap; missing organization data; headings (one H1 per page).
- Languages (site profile) and what the translation component does for SEO today (per-language meta, alternate-language links, per-language sitemaps).

## Decide
- Target: The SEO Framework as the only SEO plugin, unless the user says otherwise for this site.
- Migration route: one that covers the source plugin and every field in use; a route that needs an account or license is stop 4; otherwise map the source fields to the target fields directly in the database. Redirects managed by the source plugin move to the site's redirect mechanism. What the source plugin renders besides head tags is rebuilt before its removal; structured data the target cannot reproduce is an explained exception.
- Remove the source plugin and its data only after the migration is verified on the rendered tags.
- Multilingual site: each language keeps its titles, descriptions, sitemap entries and alternate-language links; SEO written for a page is in that page's language; what the translation component does for SEO must keep working with the target, otherwise it is an explained exception.
- Create what is missing: titles and descriptions written from each page's content, in the page's language, keeping brand words unchanged; noindex only for URLs without search value by nature (author archives of single-author sites, empty or one-item taxonomy archives, internal search, account and checkout pages, attachment pages) — content pages that look thin are flagged for the owner; sitemap with indexable URLs only; organization data, logo and social profiles taken from the site itself.
- The search-engine visibility setting must match production, whatever the archive carried.
- Content claims that only the owner can confirm are flagged in the report, not invented.

## Risks to check
- Title templates differ between plugins: rendered titles can change even when per-page data was migrated.
- Per-content robots and canonical settings are easy to miss in a migration.
- Two SEO plugins active at once print duplicate tags.
- The sitemap URL can change: robots.txt and search engine submissions must follow.

## Exit criteria
For every covered URL the rendered SEO tags match the baseline or differ only by intended improvements; one sitemap, valid, with indexable URLs only; no duplicate SEO output; no SEO plugin other than the target.

## Report
SEO plugins found and removed, fields migrated (counts), redirects moved, elements rebuilt, SEO created (counts by type), indexing policy, sitemap URL, exceptions; production actions when the sitemap URL changed.
