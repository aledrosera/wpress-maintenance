# Phase: import

## Objective
The production site restored locally, reachable, with a dedicated local administrator.

## Determine
- Latest version of the base All-in-One WP Migration plugin on the official plugin directory; version of the add-on in the zip; whether the add-on reports an available update after installation.
- After the import: site and home URLs, table prefix in use, list of existing accounts (read only).

## Decide
- Install a minimal WordPress core; its temporary administrator is replaced by the import.
- Install the base plugin from the official directory, then the add-on from the zip; apply the add-on update when one is reported.
- Import with the add-on's command-line restore, reading the read-only mounted archive.
- When the import fails, read the tool's output and logs, fix the environment cause (limits, space, permissions) and retry; the archive never changes.
- After the import, create a dedicated local administrator with a random password; give the credentials to the user once, outside the report; leave every existing account as it is.

## Risks to check
- The import replaces users and settings: access must be re-created after it.
- Internal pages, not only the home, must answer: rewrite rules may need refreshing.
- Generated files (builder CSS, local font caches, minified bundles) can still contain absolute production URLs: list them for regeneration.
- Production plugins now run locally, including scheduled tasks that may contact external services.

## Exit criteria
The home and a sample of internal pages answer 200; login with the local administrator works.

## Report
Import: base plugin and add-on versions, outcome, local URL, presence of a local administrator (never its credentials).
