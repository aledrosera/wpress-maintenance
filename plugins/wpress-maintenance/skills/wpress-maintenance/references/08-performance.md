# Phase: performance

## Objective
Faster response and loading, measured, with no functional or visual regression.

## Determine
- Caching already present: server or proxy page cache (headers, lifetime, bypass for logged-in users), WordPress page cache (drop-ins, constants, active components), object cache, compression, protocol.
- Front-end cost: render-blocking resources, requests, unused CSS and JavaScript, the largest contentful element and what delays it, third-party resources.
- Assets loaded site-wide by components used only on some pages.
- A baseline measurement taken with the same tool and conditions that will be used afterwards.

## Decide
- Page cache coherent with the stack, without duplicate layers that add nothing; the user's stated preference wins. A WordPress-level cache is useful when it serves pages while the server cache misses and when it must survive a migration.
- Reduce render-blocking CSS and JavaScript, keeping in their original position the inline scripts that act while the page is parsed or that decide which resources to download.
- Load a component's assets only on the pages that use it.
- Settings that live in the hosting panel (cache lifetime, PHP version) go to the production checklist.

## Risks to check
- Deferring inline scripts can make them run too late and change what the page downloads.
- Cache constants live in `wp-config.php`, which the export does not carry: plan their re-activation after deployment.
- A server cache serves the previous version of a page until it expires.
- Local measurements lack production compression and protocol: compare before and after locally, never present local absolute values as production values.

## Exit criteria
Improvement measured before and after in identical conditions; zero JavaScript errors; downloaded resources match the original behavior; visual comparison unchanged.

## Report
Caching layers found and added, asset changes and exclusions with their reason, before/after metrics table.
