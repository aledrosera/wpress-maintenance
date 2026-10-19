# Phase: remediation

## Objective
No malicious element left in the local copy, and the exploited or exploitable vectors closed in a way that fits the stack.

## Determine
- For every CRITICAL and HIGH finding: the exact records, files, accounts and credentials involved, and what depends on them (content authored by an account, integrations using a credential, settings referencing a file).

## Decide
- Remove malicious records and files.
- Delete illegitimate accounts, reassigning their content to a legitimate account.
- Revoke credentials an attacker may know (application passwords, sessions) and list those that legitimate integrations will need again after deployment.
- Discard pending administrative changes nobody confirmed.
- Spam URLs already indexed: answer them with a "gone" status through the site's existing redirect mechanism or rules that travel with the site.
- Hardening chosen from the findings and the stack: close remote entry points that were abused and are not used, block account enumeration, prevent code execution in upload folders. Prefer implementations that live in `wp-content` when the equivalent setting would sit in files the export does not carry.
- Anything that exists only on the server goes to the production checklist.

## Risks to check
- Deleting an account without reassignment deletes or orphans its content.
- Revoked credentials can break integrations staff rely on.
- Hardening can break legitimate remote clients: check what uses an entry point before closing it.
- `wp-config.php` and the root rewrite file are not carried by the export.

## Exit criteria
The checks that produced the findings, run again, show no CRITICAL or HIGH finding in the local copy.

## Report
Action taken for each finding; server-only items moved to the production checklist; credentials to recreate after deployment.
