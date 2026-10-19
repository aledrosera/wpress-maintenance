# Phase: delivery

## Objective
Deliverables in place, local environment usable, nothing temporary left behind.

## Determine
- Report completeness, in this order: environment; security findings; remediation; plugins and themes; database; content; media; performance; verification; production actions; pending items.
- Production checklist, limited to what the clean copy does not carry:
  - a clean deployment (empty document root, fresh core, new configuration secrets, then import), because the import does not delete files already on the server;
  - host-level credentials and host scheduler;
  - hosting panel settings (cache lifetime, PHP version);
  - settings stored in files the export does not carry, to re-activate;
  - credentials revoked locally that integrations need again;
  - personal accounts for staff who used removed accounts;
  - removal of spam URLs from search engines.

## Decide
- Ask for confirmation before exporting the backup.
- On confirmation:
  1. remove the local administrator;
  2. export with All-in-One WP Migration;
  3. move the exported file out of the container into the working folder, next to the original, under a name that does not exist yet;
  4. validate it with the reader `info`.
- Remove every temporary file, every tool installed temporarily in containers, and the inputs the flow downloaded unless the user wants them.
- Leave the local environment running unless the user asks otherwise.

## Risks to check
- The export must not carry local-only accounts or settings.
- Moving means no copy of the export stays inside the container volume.
- The original archive must be byte-identical to the start (size and modification time).

## Exit criteria
Report complete; backup, when confirmed, next to the original and readable; original unchanged; no temporary files in the working folder, the scratch area or the containers.

## Report
Deliverables list, production checklist, pending items.
