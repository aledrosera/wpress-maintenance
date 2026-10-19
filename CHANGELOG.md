# Changelog

## 0.3.0 - 2026-10-19
- Structure: the skill is `wpress` (invoked as `/wpress-maintenance:wpress [phase|resume]`); the legacy command is removed; card paths via `${CLAUDE_SKILL_DIR}`.
- Principles: the local copy never acts on the outside world (mail, scheduled tasks, outbound requests, licenses, production domain); owner records are never cleanup material; "in use" defined once (any status, meta, options, builder data, code, by name or id); editor-format rule and code placement defined once.
- Coverage and scale rule for large inventories; proportionate phase-end checks; full visit and visual comparison once, in verification.
- Working data folder inside the working folder; progress table in the report; resume across sessions; nothing temporary under the site's files.
- Stops: the compromise stop is a notice; owner questions are collected and asked before the export.
- Preflight and environment: network (multisite) exports, PHP extensions and loaders, drop-in services, production server family, cut-off verification.
- Import: base plugin version matching the add-on, import-failure exit, encrypted archive password handling, components deactivated by the import tool, settings forcing the production host.
- Baseline: site profile, live-vs-archive divergence check, logged-in templates, SEO snapshot, measurements reused at fixed points.
- Remediation: persistence check, vulnerability updates (license-bound ones pending), hardening checked against the production server family, attacker content never reassigned to the local administrator.
- Cleanup: admin-side tools kept on evidence of staff use; consolidation only with identical rebuilds; SEO plugins left to the seo phase.
- Media: references by identifier across the whole site, offloaded media, quality floor and colour profile, modern formats only where served.
- SEO: multilingual sites, elements rendered besides head tags, objective noindex criteria, search-engine visibility setting.
- Accessibility: alt texts written where the page keeps its own copy.
- Performance: measurements at baseline, start of phase and final; preference order for interventions; targets never block locally, a regression does.
- Verification: logged-in flows, second browser engine, license-bound differences recorded.
- Delivery: content of the local administrator reassigned before removal; export settings; production deployment installs All-in-One WP Migration and the add-on before the import.
- Agents: no live requests, site code not executed until reviewed, customizations vs tampering, secrets masked.
- Reader: compressed archives refused, boolean flags parsed consistently, network field in `info`.
- README rewritten: requirements, install, update/uninstall, usage, limitations, development.

## 0.2.0 - 2026-10-19
- New phases: seo (The SEO Framework as the only SEO plugin, migration of previous SEO data, missing SEO created) and accessibility.
- Baseline: editor map, raw shortcodes, rendered SEO tags, measurements with real throttling on representative pages, accessibility audit.
- Cleanup: consolidation of overlapping editors/plugins with identical rebuilds, redirects for removed URLs, builder regeneration, theme static files.
- Performance: first-paint, layout-shift, font and media-loading checks; points to weigh case by case.
- Verification: WebKit rendering, sampled functional checks, quality targets.
- Delivery: hosting cache checks when detected, sitemap URL changes.

## 0.1.0 - 2026-10-19
- First release.
