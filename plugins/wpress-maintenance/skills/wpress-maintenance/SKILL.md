---
name: wpress-maintenance
description: Use when a WordPress site has to be restored from an All-in-One WP Migration (.wpress) backup and then secured, cleaned up, de-bloated, optimized or verified, when a .wpress file sits in the working folder and the user asks for maintenance, malware cleanup or performance work on that site, or when /wpress is invoked.
---

# wpress-maintenance

## Overview
An adaptive playbook that turns a `.wpress` backup of any WordPress site into a local copy that is remediated, free of unused components and data, optimized, and verified against the live site; it ends with a technical report and, on confirmation, an optimized `.wpress`.

Every decision comes from evidence collected on the site in front of you: its theme, builder, plugins, server stack, content and state. The phase cards give objectives, decision criteria, risks to check and exit criteria — never a fixed recipe.

## Scope
- In scope: local restore, security audit and remediation, cleanup, media, SEO, accessibility and performance optimization, verification, report, optimized backup.
- Out of scope: deploying to production; any write to the live site, its server or external services; redesign or content changes not required by remediation, cleanup or optimization.

## Operating principles
1. The original `.wpress` stays byte-identical: read it in streaming or extract only the parts you need; mount it read-only for the import.
2. Backup copies are created only for a serious, stated reason; the original `.wpress` is the reference backup.
3. Every temporary file and temporary tool created by the flow is removed by the end; the working folder ends with the deliverables only.
4. Verify with real checks at the end of each phase and before destructive actions; between them, work at speed.
5. The live site is the visual reference for spotting unrequested changes: read-only requests, low concurrency, third-party resources blocked while rendering it.
6. Choices follow the evidence on this site and the user's stated preferences.
7. Existing accounts stay untouched; work through a dedicated local administrator, removed before the final export.
8. The report is written in the user's language, technical, in bullet points, essentials only.
9. What you announce, you do now — or you say clearly who has to do it.
10. Owner preference: the site ends with The SEO Framework as its only SEO plugin, with the data of any previous SEO plugin migrated (see the seo card).

## Phases
Load a phase card only when that phase starts. Each card lists Objective, Determine, Decide, Risks to check, Exit criteria, Report.

| id | card | objective | exit |
|---|---|---|---|
| preflight | references/00-preflight.md | complete inputs, suitable machine | archive valid, add-on available, requirements met |
| environment | references/01-environment.md | local WordPress matching production versions | site reachable locally |
| import | references/02-import.md | site restored, local admin | site and admin work |
| baseline | references/03-baseline.md | URL inventory and reference state | inventory and baseline recorded |
| audit | references/04-audit.md | compromises, risks, unused components | findings with severity and evidence |
| remediation | references/05-remediation.md | malicious items removed, vectors closed | no critical/high finding open locally |
| cleanup | references/06-cleanup.md | unused components, content, data, files removed | no residues, public pages unchanged |
| media | references/07-media.md | only used media, optimized | zero missing media in a real visit |
| seo | references/08-seo.md | one SEO plugin with migrated and completed SEO | rendered SEO tags as baseline or improved, valid sitemap |
| accessibility | references/09-accessibility.md | pages usable by everyone | audit target reached, meaningful alt texts |
| performance | references/10-performance.md | measured speed improvement | improvement measured, no regressions |
| verification | references/11-verification.md | full real visit, live comparison, integrity, targets | all checks pass or exceptions explained |
| delivery | references/12-delivery.md | report, checklist, backup, cleanup | deliverables in place, temp removed |

## When to stop and ask
The flow runs autonomously. It pauses only in these four cases:
1. An input is missing or ambiguous (see the preflight card).
2. The audit found a compromise: show the critical findings with evidence, then continue unless the user intervenes.
3. Before exporting the final backup: ask for confirmation.
4. An action needs a license, a purchase, credentials, or a write outside the local environment.

Questions to the user always come from the main session (with the interactive question tool when the client offers it, otherwise in plain text); agents never ask, they return findings.

## Audit delegation
In the `audit` phase launch the agents `audit-files`, `audit-database` and `audit-components` in parallel. Give each one: the working folder, the local URL, how to reach files, database and wp-cli in the environment, the live site URL, and what the baseline already established. They are read-only and return findings with severity, location, evidence and proposed action.

## State and resume
The report being written in the working folder is the state: each completed phase appends its section with findings and numbers. `/wpress resume` reads the report and the running environment and continues from the first phase without a section. `/wpress <id>` runs one phase.

## Archive reader
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/wpress.py"` — read-only, Python standard library only.

| subcommand | arguments | output |
|---|---|---|
| info | ARCHIVE | site URL, versions, table prefix, theme, active plugins, encryption, entry count |
| list | ARCHIVE [GLOB] | size, mtime, path per entry |
| cat | ARCHIVE PATH | one entry streamed to stdout |
| extract | ARCHIVE DEST GLOB... | matching entries written under DEST |

Exit codes: 0 ok, 2 usage, 3 not a valid/readable archive or encrypted, 4 entry not found. An encrypted archive needs the All-in-One WP Migration password from the user.

## Temporary work
Keep scratch files in the session scratch area or inside the containers, keep a running list of what you create there and of tools installed temporarily, and remove all of it in the `delivery` phase.

## Process pitfalls
| Situation | What to do |
|---|---|
| Unsure whether to proceed | Proceed unless it is one of the four stops |
| A screenshot differs from the live site | Check the DOM (elements, loaded images, layout boxes) before concluding |
| About to delete content or a component | Map what depends on it first (hierarchies, menus, widgets, derived files, URLs) |
| About to remove a plugin that renders something | Rebuild what it renders with a legitimate equivalent and compare with the live site |
| Tempted to copy data "to be safe" | The original `.wpress` is the backup; read from it instead |
