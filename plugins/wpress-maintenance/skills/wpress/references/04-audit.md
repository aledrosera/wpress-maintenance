# Phase: audit

## Objective
Find compromises, risks and unused elements, each with evidence, severity and a proposed action.

## Determine
- Launch the three audit agents in parallel with this brief: working folder and working data folder; local URL; how to reach files, database and command line in the environment; table prefix; installed components with versions; archive path and reader; live URL (reference only, agents do not request it); baseline facts (site profile, stack, inventory, errors).
- Merge and deduplicate their findings.
- Correlate timelines across sources: account creation times, clusters of file modifications, bursts of database records, log entries. Coinciding timestamps are the strongest evidence.
- Separate what the archive cannot show (core and root files, server configuration, host scheduler): these become production checks.

## Decide
- Severity: CRITICAL active compromise, backdoor, malicious payload; HIGH exploitable vulnerability, illegitimate administrator, dormant malicious code; MEDIUM nulled or unlicensed code, weak configuration, excess privileges; LOW hygiene; INFO context.
- Keep facts and hypotheses apart in every finding.
- Compromise confirmed: stop 2 (notice with the critical findings, evidence and planned remediation), then continue.
- An account created by an exploit may later have been used by legitimate staff: it goes to the owner questions for stop 3, never assumed either way.

## Risks to check
Recurring compromise signatures:
- administrator accounts with anomalous names or addresses, or created at the same time as other artifacts;
- records of internal types created in bursts with identical or backdated timestamps;
- options or content storing script URLs or encoded payloads;
- configuration files generated in bulk across many folders within seconds;
- empty or unknown plugin folders, logs of self-deleting tools;
- redirect rules or pages serving spam, and large volumes of spam URL patterns in 404 logs or search engine crawls;
- nulled components that redirect license, update or template requests to third parties;
- application credentials or sessions for unexpected accounts.

## Exit criteria
All three agent reports received; one consolidated list with severity, location, evidence and action; production-only items separated.

## Report
Findings table (severity, area, evidence summary, action) and, when compromised, the timeline.
