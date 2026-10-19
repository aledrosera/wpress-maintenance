---
name: wpress
description: Restores a WordPress site locally from an All-in-One WP Migration (.wpress) backup, then audits and remediates compromises, removes unused components, content, data and media, optimizes media, SEO, accessibility and performance, verifies the result against the live site and delivers a report and an optimized backup. Use when a .wpress file is in the working folder, when the user asks for maintenance, malware cleanup, de-bloating, optimization or verification of a WordPress site from such a backup, or when /wpress-maintenance:wpress is invoked.
argument-hint: "[phase|resume]"
---

# wpress

Turn the `.wpress` in the working folder into a local copy that is remediated, free of what the site does not use, optimized and verified against the live site; deliver a report and, on confirmation, an optimized `.wpress`. Every decision comes from evidence on this site (theme, builder, plugins, hosting stack, content, state) and from the user's stated preferences; the phase cards give objectives, criteria, risks and exit criteria, never recipes.

Arguments `$ARGUMENTS`: empty = full flow from `preflight`; `resume` = continue from the first phase not marked done; a phase id = run that phase only.

## Operating principles
1. The original `.wpress` stays byte-identical: read it in streaming or extract only what you need; mount it read-only for the import. A `.wpress` the flow downloaded becomes the original: a deliverable, never removed.
2. The original archive is the only backup: no intermediate copies, no snapshots, no "just in case" saves. Work directly and fix forward.
3. The local copy never acts on the outside world: no outgoing mail by any transport, no scheduled task running on its own, no outbound request from the site's code, no license activation or deactivation, no request from the local browser to the production domain or to third parties (record and block them; a request to the production domain is a leftover to fix). Cut this at environment level before the first request to the restored site, with nothing that travels in the export.
4. Existing legitimate accounts stay untouched; work through a dedicated local administrator; its content is reassigned to the site's own account and the administrator removed before the export.
5. Verify with real checks at the end of each phase and before destructive actions, in proportion: cheap checks (statuses, HTML, database) first, a real browser where only rendering answers; the full real visit and the visual comparison happen once, in verification.
6. The live site is a read-only reference, one request flow at a time with pauses, third-party resources blocked while rendering it.
7. Owner records are never cleanup material: drafts, scheduled and private content, orders, customers, subscriptions, bookings, memberships, form entries, comments awaiting moderation, accounts and their roles. A component whose only remaining job is holding such records stays, inactive if it renders nothing, and is listed for the owner.
8. "In use" means referenced anywhere the site stores or renders it: public pages, content of any status, meta, options, widgets, builder data, commerce data, logged-in areas, code — by file name or by identifier. An ambiguous reference counts as use.
9. Each part of the site keeps the format of the editor that built it: change it through that editor or by writing that editor's own data, then regenerate its files; never convert a part to another editor's format or save it from a different editor. Code outside the editor only where the editor cannot do it and a measurement shows the gain; it lives in `wp-content` (a must-use plugin or the child theme, never the parent theme), excludes the builder's editor and preview, and never returns an empty page.
10. Temporary files and tools are removed by the end; nothing temporary is ever placed under the site's document root or `wp-content`, because it would be served and exported.
11. Owner preference: the site ends with The SEO Framework as its only SEO plugin, with the data of any previous SEO plugin migrated.
12. What you announce, you do now, or you say who has to do it. The report and the dialogue are in the user's language, technical, in bullet points, essentials only.

## Phases
Load a card only when its phase starts. Each card has Objective, Determine, Decide, Risks to check, Exit criteria, Report.

| id | card | objective |
|---|---|---|
| preflight | `${CLAUDE_SKILL_DIR}/references/00-preflight.md` | complete inputs, suitable machine |
| environment | `${CLAUDE_SKILL_DIR}/references/01-environment.md` | local WordPress matching production, cut off from the outside |
| import | `${CLAUDE_SKILL_DIR}/references/02-import.md` | site restored, local administrator |
| baseline | `${CLAUDE_SKILL_DIR}/references/03-baseline.md` | inventory, site profile, reference state, measurements |
| audit | `${CLAUDE_SKILL_DIR}/references/04-audit.md` | compromises, risks, unused components, with evidence |
| remediation | `${CLAUDE_SKILL_DIR}/references/05-remediation.md` | malicious items removed, vectors closed, vulnerabilities fixed |
| cleanup | `${CLAUDE_SKILL_DIR}/references/06-cleanup.md` | unused components, content, data and files removed |
| media | `${CLAUDE_SKILL_DIR}/references/07-media.md` | only used media, optimized |
| seo | `${CLAUDE_SKILL_DIR}/references/08-seo.md` | one SEO plugin, data migrated, missing SEO created |
| accessibility | `${CLAUDE_SKILL_DIR}/references/09-accessibility.md` | pages usable by everyone |
| performance | `${CLAUDE_SKILL_DIR}/references/10-performance.md` | measured speed improvement |
| verification | `${CLAUDE_SKILL_DIR}/references/11-verification.md` | full real visit, live comparison, integrity, targets |
| delivery | `${CLAUDE_SKILL_DIR}/references/12-delivery.md` | report, checklist, backup, cleanup |

Phase loop: read the card; do the work; run the card's exit check; append the phase's section to the report and mark the phase done in the progress table; move on. A phase with nothing to do still writes its section (one line).

## Coverage and scale
Full coverage is every URL when the inventory is small. When it is large, group URLs by what renders them (post type, taxonomy, template, editor) and cover every group: all URLs of small groups, a sample of large ones including the oldest, newest and heaviest items. Decisions that delete or restrict (media, per-page asset loading) also use database references for the whole site, never the sample alone. Data recorded at baseline is reused, not collected again; later visits cover what changed plus the sample. Long operations (download, import, export, media processing, visits) run in the background with progress checks. The report states the coverage.

## Stops
The flow runs autonomously and pauses only here:
1. An input is missing or ambiguous (preflight card).
2. The audit found a compromise: show the critical findings with evidence and the planned remediation, then continue in the same turn; it is a notice, not a wait.
3. Before exporting the final backup: ask for confirmation, together with everything only the owner can decide, collected during the flow (accounts of uncertain legitimacy, items flagged for the owner, downloaded inputs to keep). Until answered, things stay as found.
4. An action needs a license, a purchase, credentials, or a write outside the local environment.

Questions come from the main session only (with the interactive question tool when the client offers it, otherwise in plain text); agents never ask, they return findings. Rerunning `environment` or `import` on an existing environment discards all local work: ask first.

## Audit delegation
In the `audit` phase launch `wpress-maintenance:audit-files`, `wpress-maintenance:audit-database` and `wpress-maintenance:audit-components` in parallel, with the brief in the audit card. They are read-only and return findings with severity, location, evidence and proposed action.

## Working data, state and resume
Working data later phases need (inventory, baseline captures, measurements, the list of temporary tools and of local-only changes to undo before the export) lives in one folder inside the working folder, created in preflight and removed in delivery; a new session can resume from it. The report starts with a progress table (phase, status, note); `resume` starts the environment if stopped, reads the report and the working data, and continues from the first phase not marked done. Rerunning a phase marks later phases as "to redo".

## Archive reader
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/wpress.py"` — read-only, Python standard library only.

| subcommand | arguments | output |
|---|---|---|
| info | ARCHIVE | site URL, versions, table prefix, theme, active plugins, network, encryption, entry count |
| list | ARCHIVE [GLOB] | size, mtime, path per entry |
| cat | ARCHIVE PATH | one entry streamed to stdout |
| extract | ARCHIVE DEST GLOB... | matching entries written under DEST |

Exit codes: 0 ok, 2 usage, 3 not a readable archive (invalid, encrypted or compressed), 4 entry not found. An encrypted archive needs the All-in-One WP Migration password from the user; the password goes to the restore only, never to files or the report.

## Pitfalls
| Situation | What to do |
|---|---|
| Unsure whether to proceed | Proceed unless it is one of the four stops |
| A screenshot differs from the live site | Check the DOM (elements, loaded images, layout boxes, heights) before concluding |
| Tempted to copy data "to be safe" | The original `.wpress` is the backup; read from it instead |
