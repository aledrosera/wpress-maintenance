# Phase: baseline

## Objective
Know what exists and how it behaves before anything changes.

## Determine
- URL inventory:
  - every URL in the sitemaps;
  - internal links discovered recursively from those pages;
  - public URLs reachable but not linked (archives of public taxonomies and post types);
  - redirects and their targets.
- Local state per URL, with a real browser at desktop, tablet and mobile widths, scrolling to the bottom: status, assets requested, JavaScript errors, missing assets, upload files referenced in the DOM and in CSS.
- Live state for the same URLs, read-only and with third-party resources blocked: status and assets.
- Production stack from response headers: web server, cache layers, cache status and lifetime, behavior for logged-in users, compression, protocol, cache policy of static files.
- Editor map: which editor or builder (and which version of it) built each page, template, header and footer; overlaps of editors or plugins doing the same job.
- Raw shortcodes visible as text on pages.
- Rendered SEO per URL: title, meta description, canonical, robots, social tags, structured data; sitemap and robots.txt.
- Measurements on 5–7 representative pages, two runs each (cold and warm cache), with real network and CPU throttling rather than simulated estimates; the same method is reused after every change.
- Accessibility audit on the same pages.
- Local server and PHP error log at rest.

## Decide
- Keep only the reference data later phases need (per-page asset and reference lists, visual references of pages with complex layouts) in the scratch area.
- On the live site use one flow of requests at a time with pauses; heavy test bursts can take a small server down.

## Risks to check
- Lazy-loaded media appear only after scrolling.
- Rendering the live site can execute injected code: block third parties when rendering it.
- Rule-based redirects legitimately answer 3xx: record them as such.
- Local generated files can still point to the production domain.

## Exit criteria
The inventory covers sitemaps, discovered links and unlinked public URLs; local and live baselines are recorded.

## Report
Inventory size by type, errors present before any change, production stack summary.
