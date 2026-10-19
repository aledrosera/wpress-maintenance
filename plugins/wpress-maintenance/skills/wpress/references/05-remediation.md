# Phase: remediation

## Objective
No malicious element left in the local copy, exploited or exploitable vectors closed in a way that fits the stack, known vulnerabilities fixed where a fix is available.

## Determine
- For every CRITICAL and HIGH finding: the exact records, files, accounts and credentials involved, and what depends on them (content authored by an account, integrations using a credential, settings referencing a file).
- Persistence mechanisms: code or scheduled tasks that recreate removed accounts, files or options.

## Decide
- Remove the mechanism before its products, then the malicious records and files.
- Delete illegitimate accounts: content made as part of the attack is deleted, other content is reassigned to an existing legitimate account, never to the local administrator.
- Revoke credentials an attacker may know (application passwords, sessions) and list those that legitimate integrations will need again after deployment.
- Discard pending administrative changes nobody confirmed.
- Spam URLs already indexed: answer them with a "gone" status through the site's existing redirect mechanism or rules that travel with the site, matched to the observed spam patterns and checked against the inventory so that no legitimate URL changes status.
- Vulnerable core or component with a fix: update to the fixed version when it supports the production PHP and WordPress versions, carrying over customizations made inside it; a premium package needs the vendor's file from the user (stop 4); without it the finding stays open as a pending item with its risk stated.
- Hardening chosen from the findings and the stack: close remote entry points that were abused and are not used, block account enumeration, prevent code execution in upload folders. Prefer implementations in `wp-content`; hardening that depends on the web server is checked against the production server family, and where it would not apply there it goes to the production checklist.
- Anything that exists only on the server goes to the production checklist.

## Risks to check
- Deleting an account without reassignment deletes or orphans its content.
- Revoked credentials can break integrations staff rely on.
- Hardening can break legitimate remote clients: check what uses an entry point before closing it.
- `wp-config.php` and the root rewrite file are not carried by the export.
- Reinfection: after removal, load several pages and run the scheduled tasks once; nothing must return.

## Exit criteria
The checks that produced the findings, run again, show no CRITICAL or HIGH finding in the local copy, except those pending on the owner with their risk stated.

## Report
Action taken for each finding; vulnerabilities fixed and pending; server-only items moved to the production checklist; credentials to recreate after deployment.
