# wpress-maintenance

A Claude Code plugin that takes an [All-in-One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/) backup (`.wpress`) of any WordPress site, restores it locally in Docker, finds and removes compromises, removes everything the site does not use, optimizes media and performance, verifies that nothing changed unintentionally compared with the live site, and delivers a technical report and — on confirmation — an optimized `.wpress`.

It is an adaptive playbook, not a fixed script: every phase defines an objective, the criteria to decide, the risks to check and the exit criteria, and Claude adapts the work to the theme, builder, plugins, server stack and state of the site in front of it.

## Requirements
- Claude Code
- Docker
- Python 3
- Free disk space of roughly the archive size plus the database
- The All-in-One WP Migration Unlimited Extension zip (placed in the working folder, or downloaded by the flow)

## Install
```
/plugin marketplace add aledrosera/wpress-maintenance
/plugin install wpress-maintenance@wpress-maintenance
```

## Usage
1. Create a working folder and put the site's `.wpress` in it (optionally also the Unlimited Extension zip). If there is no `.wpress`, the flow asks for a URL and downloads it.
2. Open Claude Code in that folder and run `/wpress`.
3. `/wpress resume` continues an interrupted run; `/wpress <phase>` reruns a single phase.

The flow runs autonomously. It stops only for missing inputs, for a short summary when a compromise is found, before exporting the final backup, and for anything that needs licenses, purchases, credentials or writes outside the local environment.

## What you get
- A Markdown report in the working folder: findings, actions, before/after numbers, verification results, production checklist, pending items.
- The local Docker environment of the cleaned site.
- On confirmation, an optimized `.wpress` placed next to the original (never overwriting it).

## Safety
- The original `.wpress` is never modified or deleted; it is read in streaming and mounted read-only.
- The live site is only read, with low concurrency and third-party resources blocked while rendering.
- Nothing is written to production, servers or external services.
- Temporary files and tools are removed at the end.

## Phases
| Phase | Objective |
|---|---|
| preflight | Complete inputs and a suitable environment |
| environment | Local WordPress matching the production versions |
| import | Site restored locally with a dedicated local admin |
| baseline | Inventory of public URLs and reference state |
| audit | Compromises, risks and unused components, with evidence |
| remediation | Malicious items removed, vectors closed |
| cleanup | Unused plugins, themes, content, data and files removed |
| media | Only used media, optimized |
| performance | Measured improvement of response and load |
| verification | Full real visit, comparison with the live site, integrity checks |
| delivery | Report, production checklist, optimized backup, cleanup |

## License
MIT
