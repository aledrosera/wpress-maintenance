# Phase: verification

## Objective
Prove that the cleaned site behaves and looks like the live site, except for intended changes, and that the copy is clean.

## Determine
- Full real visit of the inventory at every width: statuses, assets, JavaScript errors.
- Visual comparison with the live site for every URL at desktop and mobile width, with animations paused and third parties blocked on both sides.
- Text and media references of every page against the baseline.
- Functional checks: forms (validation without sending), admin screens of the remaining components (loading and their API calls), redirects.
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
