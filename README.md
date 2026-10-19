# wpress-maintenance

A Claude Code plugin that takes an [All-in-One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/) backup (`.wpress`) of any WordPress site, restores it locally in Docker, finds and removes compromises, removes everything the site does not use, optimizes media, SEO, accessibility and performance, verifies that nothing changed unintentionally compared with the live site, and delivers a technical report and — on confirmation — an optimized `.wpress`.

It is an adaptive playbook, not a fixed script: every phase defines an objective, the criteria to decide, the risks to check and the exit criteria, and Claude adapts the work to the theme, builder, plugins, server stack and state of the site in front of it.

## Requirements
- Claude Code
- Docker
- Python 3
- Free disk space of roughly the archive size plus the database
- The All-in-One WP Migration Unlimited Extension zip (placed in the working folder, or downloaded by the flow)

## Install

### With one prompt (Claude Code or Claude Desktop "Code", local session)
Paste this prompt and let Claude do it:

```
Install the Claude Code plugin wpress-maintenance for me.
If the claude command is available (command -v claude):
  1. Run: claude plugin marketplace add aledrosera/wpress-maintenance
  2. Run: claude plugin install wpress-maintenance@wpress-maintenance --scope user
  3. Run: claude plugin details wpress-maintenance and show me the result.
If it is not available (for example in Claude Desktop), edit ~/.claude/settings.json yourself:
  merge, without removing or changing anything else in the file,
  "extraKnownMarketplaces": { "wpress-maintenance": { "source": { "source": "github", "repo": "aledrosera/wpress-maintenance" } } }
  and
  "enabledPlugins": { "wpress-maintenance@wpress-maintenance": true }
  then check that the file is still valid JSON.
Finally tell me to run /reload-plugins or to open a new session (in Claude Desktop: restart the app); the plugin is downloaded and installed automatically.
```

### Manually
From a terminal:
```
claude plugin marketplace add aledrosera/wpress-maintenance
claude plugin install wpress-maintenance@wpress-maintenance --scope user
```
or, on Claude Code 2.1.292 or later, in one step:
```
claude plugin install wpress-maintenance --marketplace aledrosera/wpress-maintenance
```
or inside a Claude Code terminal session:
```
/plugin marketplace add aledrosera/wpress-maintenance
/plugin install wpress-maintenance@wpress-maintenance
```
Then run `/reload-plugins` or open a new session.

### Claude Desktop ("Code" tab)
- The terminal, the desktop app's local sessions and the VS Code extension read the same settings: once installed at user scope (with the prompt or the commands above), the plugin is available in Desktop too. You can manage it from **+ → Plugins → Manage plugins**; once the marketplace is added, it is also listed under **+ → Plugins → Add plugin**.
- Use a **local** session: plugins are not available in cloud sessions or in WSL sessions, and the flow needs the local Docker.
- Docker and Python 3 must be reachable from your shell profile; restart the app after changing the PATH.
- If the Bash sandbox is enabled, Docker commands must run outside it (`excludedCommands` in the sandbox settings, e.g. for `docker compose` and `docker exec`).

## Usage
1. Create a working folder and put the site's `.wpress` in it (optionally also the Unlimited Extension zip). If there is no `.wpress`, the flow asks for a URL and downloads it.
2. Open Claude Code (or a local session of Claude Desktop "Code") in that folder and run `/wpress` (listed as `/wpress-maintenance:wpress` in the slash menu).
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
| seo | The SEO Framework as the only SEO plugin, previous SEO data migrated, missing SEO created |
| accessibility | Audit and fixes: alt texts, contrast, names, headings, forms, language consistency |
| performance | Measured improvement of response and load |
| verification | Full real visit, comparison with the live site, integrity checks, quality targets |
| delivery | Report, production checklist, optimized backup, cleanup |

## License
MIT
