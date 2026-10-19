# Phase: cleanup

## Objective
Remove the plugins, themes, content, data and files the site does not need, without touching owner records (principle 7) or anything in use (principle 8).

## Determine
- For each plugin and theme: evidence of use (shortcodes, blocks, widgets in content of any status and builder data, options, rendered pages, data it created, settings changed after install, recent log entries), whether it is nulled or vulnerable without a fix, which package (free or premium) provides each element in use.
- Content: empty, duplicate, spam or attacker-made drafts; trash and auto-drafts; revisions; content of post types no longer registered by the running site; forms, menus and widgets rendered nowhere; parent/child hierarchies and menu items pointing to each item.
- Database: tables and options of absent components, transients, orphan rows (meta, relationships, terms, comments), logs, scheduled hooks and roles of absent components with nobody assigned.
- Files: non-media folders in uploads belonging to absent components, archives in content folders, configuration and drop-ins of absent components, translations of removed components.

## Decide
- Keep what is in use and what the site needs to operate (security, redirects, forms, the user's backup tool). SEO plugins are left to the seo phase.
- Remove what is unused, nulled, or vulnerable without a fix. An admin-side component counts as unused only without evidence of use by staff.
- A component in use that must go: rebuild what it renders with legitimate elements already available, matching measurements taken on the live page (sizes, typography per breakpoint, spacing, behavior), then compare with the live page.
- Editors or plugins overlapping on the same job: consolidate on one when the parts of the other can be rebuilt identically with it (verified against the live page) and the gain is real; otherwise keep both and put the consolidation proposal in the report.
- Rebuilding in a duplicate draft is fine when the result finally keeps the original slug, URL and SEO data.
- A public URL that disappears or moves gets a redirect, or a "gone" status when nothing replaces it.
- Before deleting content, map its dependencies; keep unpublished containers that define URL hierarchies.
- Keep a few revisions per item and set a limit that travels with the site.
- An untrusted component (nulled, malicious) is removed without running its uninstall routine; its data is cleaned manually.
- Themes that generate CSS and JavaScript from their options: save the options again so the static files are written.

## Risks to check
- Deleting a parent page changes its children's URLs; deleting content can delete the menu items linked to it.
- Widgets, blocks and shortcodes of a removed component render nothing, a notice or raw shortcode text, without errors.
- Free and premium packages of the same family provide different elements.
- Option and table names of removed components can share prefixes with active ones: review the list before deleting.
- Builder caches keep references to removed elements, and data written outside a builder's editor is not shown until its files are regenerated and caches cleared.

## Exit criteria
Covered pages unchanged against the baseline (URLs, statuses, text, media references, no raw shortcodes); no residues of removed components in database and files.

## Report
Components removed and kept with the reason; consolidation done or proposed; content removed (identifiers, recoverable from the original archive); database before/after (size, tables, options, autoload size, revisions).
