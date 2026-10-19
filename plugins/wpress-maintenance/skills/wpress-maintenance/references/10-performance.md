# Phase: performance

## Objective
Faster response and loading, measured, with no functional or visual regression.

## Determine
- Caching already present: server or proxy page cache (headers, lifetime, bypass for logged-in users), WordPress page cache (drop-ins, constants, active components), object cache, compression, protocol.
- Front-end cost: render-blocking resources, requests, unused CSS and JavaScript, the largest contentful element and what delays it, third-party resources.
- Assets loaded site-wide by components used only on some pages.
- The largest contentful element per page and device, whether it is discoverable early and prioritized, and what competes with it for bandwidth.
- Rules needed for the first paint that arrive late (styles placed at the end of the page), layout shifts (media without reserved space, elements hidden after load), fonts that block or reflow text, off-screen media loaded eagerly, videos that download before they are visible or in a version unsuited to the device.
- The baseline measurements (method of the baseline phase).

Points to weigh case by case, not rules: deferred scripts can start together and take bandwidth from the main image; simulated measurements can mislead when the server is slow; reduced-motion settings can break animations; some test browsers do not play every video codec; a cache key that depends on request headers is not warmed by command-line requests.

## Decide
- Page cache coherent with the stack, without duplicate layers that add nothing; the user's stated preference wins. A WordPress-level cache is useful when it serves pages while the server cache misses and when it must survive a migration.
- Reduce render-blocking CSS and JavaScript, keeping in their original position the inline scripts that act while the page is parsed or that decide which resources to download.
- Load a component's assets only on the pages that use it.
- Settings that live in the hosting panel (cache lifetime, PHP version) go to the production checklist.

## Risks to check
- Deferring inline scripts can make them run too late and change what the page downloads.
- Cache constants live in `wp-config.php`, which the export does not carry: plan their re-activation after deployment.
- A server cache serves the previous version of a page until it expires.
- Layered caches show an old version unless cleared in order: regenerate builder files first, then clear page caches from the innermost layer (WordPress) to the outermost (server or proxy); check with a cache-busting parameter.
- Local measurements lack production compression and protocol: compare before and after locally, never present local absolute values as production values.

## Exit criteria
Improvement measured before and after in identical conditions; zero JavaScript errors; downloaded resources match the original behavior; visual comparison unchanged.

## Report
Caching layers found and added, asset changes and exclusions with their reason, before/after metrics table.
