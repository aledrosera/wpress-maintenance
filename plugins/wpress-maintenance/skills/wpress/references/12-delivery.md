# Phase: delivery

## Objective
Deliverables in place, local environment usable, nothing temporary left behind.

## Determine
- Report completeness, reordered for the reader: environment; security findings; remediation; plugins and themes; database; content; media; SEO; accessibility; performance; verification; production actions; pending items and owner questions. The progress table stays at the top.
- Production checklist, limited to what the clean copy does not carry:
  - a clean deployment: empty document root, fresh WordPress core with new configuration secrets, All-in-One WP Migration and the Unlimited Extension installed on it, then the import of the optimized archive — because an import does not delete files already on the server;
  - host-level credentials and host scheduler;
  - hosting panel and server cache behavior observed in the baseline that the copy cannot carry (cache lifetime and key, static file serving, PHP version) and the order to clear cache layers;
  - settings stored in files the export does not carry, to re-activate;
  - a new sitemap URL to submit to search engines, when it changed;
  - credentials revoked locally that integrations need again;
  - personal accounts for staff who used removed accounts;
  - removal of spam URLs from search engines.
- Local-only changes noted in the working data (import card), to restore before the export.

## Decide
- Stop 3: ask for confirmation of the export together with the collected owner questions.
- On confirmation:
  1. restore the noted local-only changes; reassign everything the local administrator authored (content of every type and status, media, templates) to the existing account that owns the site's content, then remove the local administrator;
  2. export the whole site with All-in-One WP Migration, nothing excluded, encrypted when the original was (same password unless the user gives another);
  3. move the exported file out of the container into the working folder, next to the original, under a name that does not exist yet;
  4. validate it with the reader `info`.
- Remove every temporary file, every tool installed temporarily in containers, the working data folder, and the downloaded inputs the user did not ask to keep.
- Leave the local environment running unless the user asks otherwise.

## Risks to check
- The export must not carry local-only accounts, settings or the cut-off of principle 3.
- Moving means no copy of the export stays inside the container volume.
- The original archive must be byte-identical to the start (size and modification time).

## Exit criteria
Report complete; backup, when confirmed, next to the original and readable; original unchanged; no temporary files in the working folder, the scratch area or the containers.

## Report
Deliverables list, production checklist, pending items and owner answers.
