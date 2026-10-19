# Phase: seo

## Objective
One SEO plugin, The SEO Framework (owner preference), carrying all the SEO data the site already had, plus the SEO the site was missing.

## Determine
- SEO plugins present (active or not) and overlaps: more than one plugin printing titles, meta tags, structured data or sitemaps.
- SEO data stored by each one: per-content titles, descriptions, canonical URLs, robots directives, social titles, descriptions and images, primary terms, per-term and per-author data, global title templates, organization or person data, logo, social profiles, sitemap settings, breadcrumbs, redirects managed by the SEO plugin.
- Rendered SEO of every inventory URL (from the baseline): title, meta description, canonical, robots, social tags, structured data, sitemap URL and contents, robots.txt.
- Gaps: missing or duplicate titles and descriptions, thin or service pages that are indexable, author archives and useless taxonomy archives that are indexable, archives that redirect but are listed in the sitemap, missing organization data, headings (one H1 per page).
- Whether the site is multilingual.

## Decide
- Target: The SEO Framework as the only SEO plugin, unless the user says otherwise for this site.
- Migration path: a migration tool from the target plugin's ecosystem when it covers the source plugin and every field in use; otherwise map the source fields to the target fields directly in the database. Redirects managed by the source plugin move to the site's redirect mechanism.
- Remove the source plugin and its data only after the migration is verified.
- Create what is missing: titles and descriptions written from each page's content, in the site's language, keeping brand words unchanged; noindex for service and thin pages, author archives and useless taxonomies; sitemap with indexable URLs only; organization data, logo and social profiles taken from the site itself.
- Content claims that only the owner can confirm are flagged in the report, not invented.

## Risks to check
- Title templates differ between plugins: rendered titles can change even when per-page data was migrated.
- Per-content robots and canonical settings are easy to miss in a migration.
- Redirects stored by the source plugin disappear with it.
- Two SEO plugins active at once print duplicate tags.
- The sitemap URL can change: robots.txt and search engine submissions must follow.

## Exit criteria
For every inventory URL the rendered SEO tags match the baseline or differ only by intended improvements; one sitemap, valid, with indexable URLs only; no duplicate SEO output; no SEO plugin other than the target.

## Report
SEO plugins found and removed, fields migrated (counts), redirects moved, SEO created (counts by type), indexing policy, sitemap URL; production actions when the sitemap URL changed.
