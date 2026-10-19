# Phase: cleanup

## Objective
Remove the plugins, themes, content, data and files the site does not need.

## Determine
- For each plugin and theme: evidence of use (shortcodes, blocks, widgets in published content and builder data, options, rendered pages), whether it is nulled, vulnerable or abandoned, whether it only offers admin conveniences, which package (free or premium) provides each element in use.
- Content: drafts, trash, auto-drafts, revisions, content of post types whose component is gone, forms, menus and widgets not rendered anywhere; parent/child hierarchies; menu items pointing to each item.
- Database: tables and options of absent components, transients, orphan rows (meta, relationships, terms, comments), logs, scheduled hooks and roles of absent components.
- Files: non-media folders in uploads belonging to absent components, archives in content folders, configuration and drop-ins of absent components, translations of removed components.

## Decide
- Keep what has evidence of use on public pages and what the site needs to operate (security, SEO, redirects, forms, the user's backup tool).
- Remove what is unused, nulled, vulnerable without a fix, or an admin-only convenience the user did not ask to keep.
- A component in use that must go: rebuild what it renders with legitimate elements already available, matching measurements taken on the live page (sizes, typography per breakpoint, spacing, behavior), then compare with the live page.
- Several editors or plugins overlapping on the same job: propose consolidating on one, then rebuild the affected parts identically with it, page by page.
- Each part is changed with the tools of the editor that built it; a page made with a builder is never saved from a different editor.
- Rebuilding in a duplicate draft is fine when the result finally keeps the original slug, URL and SEO data.
- A public URL that disappears or moves gets a redirect (or a "gone" status when nothing replaces it).
- Code outside the editor only where the editor cannot do it and a measurement shows the gain; it excludes the builder's editor and preview and never returns an empty page.
- Themes that generate CSS and JavaScript from their options: save the options again so the static files are written.
- Before deleting content, map its dependencies; keep unpublished containers that define URL hierarchies.
- Keep a few revisions per item and set a limit that travels with the site.
- An untrusted component (nulled, malicious) is removed without running its uninstall routine; its data is cleaned manually.

## Risks to check
- Deleting a parent page changes its children's URLs; deleting content can delete the menu items linked to it.
- Widgets and shortcodes of a removed plugin render nothing or a notice, without errors.
- Free and premium packages of the same family provide different elements.
- Option and table names of removed components can share prefixes with active ones: review the list before deleting.
- Builder caches keep references to removed elements: regenerate them.
- Data written to a builder outside its editor is not shown until its generated files are regenerated and caches are cleared.
- Raw shortcodes appearing as text after a removal.

## Exit criteria
Public pages unchanged against the baseline (URLs, statuses, text, media); no residues of removed components in database and files.

## Report
Components removed and kept with the reason; content removed (identifiers, recoverable from the original archive); database before/after (size, tables, options, autoload size, revisions).
