# Phase: import

## Objective
The production site restored locally, self-contained, reachable, with a dedicated local administrator.

## Determine
- Version of the add-on in the zip, the base plugin version it supports, the version that wrote the archive (`info`), and whether the add-on reports an update after installation.
- After the import: site and home URLs, table prefix, active components and drop-ins compared with the archive's list, existing accounts (read only).
- Services the site talks to (mail transport, payment, webhooks, newsletter or CRM sync, license servers, remote APIs) and where their keys live, never printed: they feed the cut-off check, the production checklist and the list of credentials to recreate.
- Settings that force the production scheme or host (forced HTTPS, host redirects, cookie domain, asset or CDN rewriting, other domains).

## Decide
- Install a minimal WordPress core (its temporary administrator is replaced by the import), then the base plugin in the version the add-on supports and not older than the one that wrote the archive, then the add-on from the zip. An add-on update that needs a license is stop 4; without it keep the zip's version. The import tool keeps itself and its extensions through the restore: they are what runs it.
- Import with the add-on's command-line restore, reading the read-only mounted archive; an encrypted archive gets its password at the restore only.
- Import failure: read output and logs, fix environment causes (limits, space, permissions) and retry; when the cause is in the archive (truncated data, unsupported format, database errors not explained by versions) or two retries with different fixes fail, stop with the exact error as a missing input.
- Components the import tool deactivated: reactivate them, or record why they stay off and add them to the production checklist.
- Make the copy self-contained preferably without touching what travels; any travelling setting changed for local use is noted in the working data and restored before the export.
- Create a dedicated local administrator with a random password; give the credentials to the user once, outside the report; leave every existing account as it is.

## Risks to check
- The import replaces users and settings: access must be re-created after it.
- Internal pages, not only the home, must answer: rewrite rules may need refreshing.
- Generated files (builder CSS, local font caches, minified bundles) can still contain absolute production URLs: list them for regeneration; local browser requests to the production domain reveal them.
- Production plugins now run locally with their live keys: the cut-off of principle 3 must already be in place.

## Exit criteria
The home and a sample of internal pages answer 200 without requests to the production domain; login with the local administrator works.

## Report
Import: base plugin and add-on versions, outcome, components reactivated or left off, local-only changes noted, local URL, presence of a local administrator (never its credentials).
