# Phase: baseline

## Objective
Know what exists and how it behaves before anything changes; keep what later phases will compare against.

## Determine
- Site profile: single site or network; languages; commerce, membership, bookings, forums or other logged-in areas and the records they hold (principle 7); where media are served from (local, production domain, media or CDN host); editors and builders per page, template, header and footer, and overlaps of editors or plugins doing the same job.
- URL inventory: sitemaps, internal links discovered recursively, public URLs reachable but not linked (archives of public taxonomies and post types), redirects and their targets; grouped by what renders them (coverage rule).
- Local state per covered URL, with a real browser at desktop, tablet and mobile widths, scrolling to the bottom: status, assets requested, JavaScript errors, missing assets, raw shortcodes visible as text, upload files referenced in the DOM and in CSS, requests to the production domain or third parties (blocked and recorded). Logged-in areas: their main templates with a temporary local account of the needed role, created and removed by the flow.
- Live state for the same URLs, read-only, third parties blocked: status, assets, screenshots at desktop and mobile width.
- Production stack from the live response headers: web server family, cache layers, cache status and lifetime, behavior for logged-in users, compression, protocol, cache policy of static files.
- Rendered SEO per URL: title, meta description, canonical, robots, social tags, structured data; sitemap and robots.txt; search-engine visibility setting.
- Measurements on 5–7 representative pages, two runs each (cold and warm cache), with real network and CPU throttling rather than simulated estimates; accessibility audit on the same pages. The same method is reused at the start and end of the performance phase and in verification.
- Local server and PHP error log at rest.

## Decide
- Before using the live site as reference, compare a sample of pages with the local copy (text, menus, media). Where live diverges (newer content, redesign, already cleaned, compromised output, challenge or maintenance page), the local baseline is the visual reference for those pages and live-only media are listed, not required; keep local screenshots of those page groups.
- Keep the reference data in the working data folder: per-URL asset and reference lists, SEO snapshot, measurements, screenshots.

## Risks to check
- Lazy-loaded media appear only after scrolling.
- Rendering the live site can execute injected code: third parties blocked.
- Rule-based redirects legitimately answer 3xx: record them as such.

## Exit criteria
Site profile recorded; the inventory covers sitemaps, discovered links and unlinked public URLs; local and live baselines recorded with their coverage.

## Report
Site profile, inventory size by type and coverage, errors present before any change, production stack summary, whether live is usable as reference.
