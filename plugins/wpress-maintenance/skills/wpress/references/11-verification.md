# Phase: verification

## Objective
Prove that the cleaned site behaves and looks like the live site, except for intended changes, and that the copy is clean.

## Determine
- Full real visit of the inventory (coverage rule) at every width: statuses, assets, JavaScript errors, raw shortcodes, requests to the production domain or third parties.
- Visual comparison with the live site, or with the baseline screenshots where live is not the reference, for every covered URL at desktop and mobile width, animations paused and third parties blocked on both sides.
- Text, media references and rendered SEO tags of every covered page against the baseline.
- Rendering with a second browser engine, different from the one used so far, on a sample of pages.
- Functional checks on a sample: sliders, galleries and lightboxes, mobile menu, filters, animations with and without reduced motion, forms (validation and local outcome only; outbound delivery is cut by the environment), admin screens of the remaining components (loading and their API calls), redirects. Sites with logged-in areas: their main flows (cart up to payment, login, account pages, protected content) with a temporary local account of the needed role, created and removed by the flow; existing accounts never used; payments never completed.
- Measurements with the baseline method on the same pages, compared with the targets below. The targets are goals for the live site after deployment; locally they never block the exit — a metric worse than the baseline does.

  | indicator | target |
  |---|---|
  | automated performance score, mobile, inner pages | ≥ 85 |
  | automated performance score, mobile, pages with a background video | ≥ 75 |
  | automated performance score, desktop | ≥ 95 |
  | largest contentful paint, mobile | ≤ 3.0 s |
  | cumulative layout shift | ≤ 0.05 |
  | automated accessibility score | ≥ 95 |
  | best practices / SEO checks | 100 / ≥ 95 |
  | server response with cache | ≤ 0.2 s |
  | active plugins | the minimum |
- Integrity: core checksums including root files; checksums of components from the official directory; pattern scan for malicious code in all PHP, including premium components without public checksums; no executable files in upload folders; drop-ins and must-use plugins reviewed; scheduled hooks all belonging to present components; accounts, roles and application credentials; options and content free of payloads; registration and search-engine visibility settings.

## Decide
- Each difference is either intended and documented, or fixed. A generated image size requested but missing is regenerated, not a failure.
- When a screenshot differs, check the DOM (elements, loaded images, layout boxes, heights) to tell timing from real change before concluding.
- Differences caused by a license not active on the local domain are recorded, never fixed by activating it.

## Risks to check
- Full-page screenshots of sliders, lazy content and animations depend on timing.
- Rule-based redirects answer 3xx by design.

## Exit criteria
Every check passes, or each exception is explained in the report.

## Report
Verification section: coverage, real visit results, visual comparison results, functional checks, measurements against the targets, integrity checks.
