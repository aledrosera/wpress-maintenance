# Phase: verification

## Objective
Prove that the cleaned site behaves and looks like the live site, except for intended changes, and that the copy is clean.

## Determine
- Full real visit of the inventory at every width: statuses, assets, JavaScript errors.
- Visual comparison with the live site for every URL at desktop and mobile width, with animations paused and third parties blocked on both sides.
- Text and media references of every page against the baseline; no raw shortcodes; rendered SEO tags against the baseline.
- Rendering with a second browser engine besides Chromium (WebKit) on a sample of pages.
- Functional checks on a sample: sliders, galleries and lightboxes, mobile menu, filters, animations with and without reduced motion, forms (validation only, no sending: there is no mail server locally), admin screens of the remaining components (loading and their API calls), redirects.
- Measurements with the baseline method on the same pages, compared with the targets below (they apply to the live site after deployment; locally they show the trend):

  | indicator | target |
  |---|---|
  | mobile performance, inner pages | ≥ 85 |
  | mobile performance, home with video | ≥ 75 |
  | desktop performance | ≥ 95 |
  | largest contentful paint, mobile | ≤ 3.0 s |
  | cumulative layout shift | ≤ 0.05 |
  | accessibility | ≥ 95 |
  | best practices / SEO | 100 / ≥ 95 |
  | server response with cache | ≤ 0.2 s |
  | active plugins | the minimum |
- Integrity:
  - core checksums including root files;
  - checksums of components from the official directory;
  - pattern scan for malicious code in all PHP, including premium components without public checksums;
  - no executable files in upload folders;
  - drop-ins and must-use plugins reviewed;
  - scheduled hooks all belonging to present components;
  - accounts, roles and application credentials;
  - options and content free of payloads;
  - registration settings.

## Decide
- Each difference is either intended and documented, or fixed.
- When a screenshot differs, check the DOM (elements, loaded images, layout boxes, heights) to tell timing from real change before concluding.

## Risks to check
- Full-page screenshots of sliders, lazy content and animations depend on timing.
- Rule-based redirects answer 3xx by design.

## Exit criteria
Every check passes, or each exception is explained in the report.

## Report
Verification section: coverage, real visit results, visual comparison results, functional checks, integrity checks.
