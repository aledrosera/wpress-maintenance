# Phase: performance

## Objective
Faster response and loading, measured, with no functional or visual regression.

## Determine
- Reference measurements at the start of this phase with the baseline method; decisions compare with them; the report shows baseline, start of phase and final.
- Caching already present: server or proxy page cache (headers, lifetime, key, bypass for logged-in users), WordPress page cache (drop-ins, constants, active components), object cache, compression, protocol.
- Front-end cost: render-blocking resources, requests, unused CSS and JavaScript, third-party resources, assets loaded site-wide by components used only on some pages.
- The largest contentful element per page and device: whether it is discoverable early and prioritized, and what competes with it for bandwidth.
- Rules needed for the first paint that arrive late (styles placed at the end of the page), layout shifts (media without reserved space, elements hidden after load), fonts that block or reflow text, off-screen media loaded eagerly, videos that download before they are visible or in a version unsuited to the device.

Points to weigh case by case, not rules: deferred scripts can start together and take bandwidth from the main image; simulated measurements can mislead when the server is slow; reduced-motion settings can break animations; some test browsers do not play every video codec; a cache key that depends on request headers is not warmed by command-line requests.

## Decide
- Prefer, in order: settings of components already present, small code in `wp-content` (principle 9), a new component only when neither works and the gain is measured.
- Page cache coherent with the stack: a WordPress-level page cache when production has no page cache at any level, or when the user asks for one as a second layer (it serves pages while the server cache misses and survives a migration). Constants a cache needs go in the local configuration to test it and in the production checklist, because they do not travel.
- Reduce render-blocking CSS and JavaScript, keeping in their original position the inline scripts that act while the page is parsed or that decide which resources to download.
- Load a component's assets only on the pages that use it, decided on database references for the whole site, not on the sample.
- Settings that live in the hosting panel (cache lifetime and key, static file serving, PHP version) go to the production checklist.

## Risks to check
- Deferring inline scripts can make them run too late and change what the page downloads.
- A server cache serves the previous version of a page until it expires; layered caches show an old version unless cleared in order: regenerate builder files first, then page caches from the innermost layer (WordPress) to the outermost (server or proxy); check with a cache-busting parameter.
- Local measurements lack production compression and protocol: compare before and after locally, never present local absolute values as production values.

## Exit criteria
Final measurements with the same method: no metric worse than the start of the phase; zero JavaScript errors; downloaded resources match the original behavior on the covered pages; no visual change on the sampled pages.

## Report
Caching layers found and added, asset changes and exclusions with their reason, measurements table (baseline, start of phase, final).
