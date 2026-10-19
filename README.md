# wpress-maintenance

A Claude Code plugin that takes an [All-in-One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/) backup (`.wpress`) of any WordPress site, restores it locally in Docker, finds and removes compromises, removes everything the site does not use, optimizes media, SEO, accessibility and performance, verifies that nothing changed unintentionally compared with the live site, and delivers a technical report and — on confirmation — an optimized `.wpress` ready to be deployed.

It is an adaptive playbook, not a fixed script. Each of the 13 phases defines an objective, the facts to establish, the decision criteria, the risks to check and the exit criteria; Claude adapts the work to the theme, builder, plugins, hosting stack, content and state of the site in front of it. There are no product recommendations or canned commands inside: only All-in-One WP Migration (restore and export) and The SEO Framework (the SEO plugin the site ends with) are named.

## Contents
- [Requirements](#requirements)
- [Install](#install)
- [Update and uninstall](#update-and-uninstall)
- [Usage](#usage)
- [What you get](#what-you-get)
- [Safety](#safety)
- [Phases](#phases)
- [Limitations](#limitations)
- [Development](#development)
- [License](#license)

## Requirements
- **Claude Code**, in a local session: terminal, Claude Desktop ("Code" tab) or the VS Code extension. The one-step install below needs Claude Code 2.1.292 or later.
- **Docker** with Compose v2 (`docker compose`), running and reachable from the shell Claude uses. On macOS and Windows the site lives in Docker's virtual disk: it needs free space of about **twice the archive size** (restored files and database, media processing, final export).
- **Python 3** (3.8 or later, standard library only) on the shell path, for the archive reader.
- **Internet access**: container images, the WordPress plugin directory, vulnerability databases, the live site for comparisons.
- **All-in-One WP Migration Unlimited Extension**: put its zip in the working folder, or let the flow download it (it does so by itself when the zip is not there).
- Optional: the live site reachable. Without it the flow still runs, but compares only against the local baseline.

## Install

### With one prompt
Works in a Claude Code terminal session and in a local session of Claude Desktop "Code". Paste this and let Claude do it:

```
Install the Claude Code plugin wpress-maintenance for me.
If the claude command is available (command -v claude):
  1. Run: claude plugin marketplace add aledrosera/wpress-maintenance
     (if it says the marketplace already exists, continue)
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
or inside a Claude Code session:
```
/plugin marketplace add aledrosera/wpress-maintenance
/plugin install wpress-maintenance@wpress-maintenance
```
Then run `/reload-plugins` or open a new session.

### Check
`claude plugin details wpress-maintenance` must list one skill, `wpress`, and three agents: `audit-files`, `audit-database`, `audit-components`. In a session, typing `/wpress` shows `/wpress-maintenance:wpress` in the menu.

### Claude Desktop ("Code" tab)
- Desktop, the terminal and the VS Code extension read the same settings files: a plugin installed at user scope in one of them is available in the others. In Desktop you can also manage it from **+ → Plugins → Manage plugins**, and, once the marketplace is added, install it from **+ → Plugins → Add plugin**.
- Use a **local** session. Plugins are not available in cloud sessions or in WSL sessions, and the flow needs the local Docker.
- Docker and Python 3 must be on the PATH of your shell profile; restart the app after changing it.
- If the Bash sandbox is enabled, Docker is incompatible with it: add the Docker commands to `excludedCommands` in the sandbox settings (patterns such as `docker compose *`, `docker exec *`, `docker cp *`). See the [sandboxing docs](https://code.claude.com/docs/en/sandboxing).

## Update and uninstall
```
claude plugin marketplace update wpress-maintenance
claude plugin update wpress-maintenance@wpress-maintenance
```
Installed versions are pinned until you update. To remove the plugin:
```
claude plugin uninstall wpress-maintenance@wpress-maintenance
claude plugin marketplace remove wpress-maintenance
```

## Usage
1. Create a working folder and put the site's `.wpress` in it (and, if you have it, the Unlimited Extension zip). If there is no `.wpress`, the flow asks you for a reachable URL and downloads it.
2. Open a local Claude Code session in that folder and run `/wpress-maintenance:wpress`. Claude also picks the skill up by itself when you ask for maintenance, cleanup, security or performance work on a `.wpress` in the folder.
3. Let it run. The flow is autonomous and stops only in four cases: an input is missing or ambiguous; a compromise was found (you get a short summary with evidence, then it continues); before exporting the final backup; an action needs a license, a purchase, credentials, or a write outside the local environment.
4. `/wpress-maintenance:wpress resume` continues an interrupted run from the first phase not marked done in the report. `/wpress-maintenance:wpress <phase>` reruns one phase (ids in the table below).

What to expect on the first run: Docker pulls the WordPress and database images (hundreds of MB), the import of a large archive takes minutes to tens of minutes, and the audit and verification phases visit every public page of the site with a real browser. Claude talks to you and writes the report in your language.

## What you get
In the working folder:
- the Markdown report: what was found, what was done, numbers before and after, verification results, the production checklist (what the clean copy cannot carry: clean deployment, server credentials, hosting cache settings, search engine submissions), and pending items;
- the Docker environment files of the local copy of the site, which keeps running after the flow (stop it from the working folder with `docker compose down`; add `-v` to delete its volumes too);
- on confirmation, the optimized `.wpress`, placed next to the original with a different name.

The credentials of the local administrator are shown once in the chat and never written to the report. The report never contains credentials.

## Safety
- The original `.wpress` is never modified or deleted: it is read in streaming and mounted read-only in the container.
- No extra backup copies are made; the original archive is the reference backup.
- The live site is only read, one request flow at a time, with third-party resources blocked while rendering it (a compromised site may serve malicious scripts).
- Nothing is written to production, to the server or to external services; the local site cannot send e-mail.
- Existing accounts are never modified; the work goes through a dedicated local administrator, removed before the export.
- Transactional and personal data (orders, customers, members, form entries) are never treated as "unused content".
- Temporary files and tools are removed at the end; the working folder ends with the deliverables only.

## Phases
| id | objective |
|---|---|
| preflight | Complete inputs and a suitable machine |
| environment | Local WordPress matching the production versions |
| import | Site restored locally, dedicated local administrator |
| baseline | Public URL inventory, site profile, reference state and measurements |
| audit | Compromises, risks and unused components, with evidence (three agents in parallel) |
| remediation | Malicious items removed, exploited vectors closed |
| cleanup | Unused plugins, themes, content, data and files removed; overlapping editors consolidated |
| media | Only the media the site uses, optimized |
| seo | The SEO Framework as the only SEO plugin, previous SEO data migrated, missing SEO created |
| accessibility | Audit and fixes: alt texts, contrast, accessible names, headings, forms, language consistency |
| performance | Caching coherent with the stack, lighter loading, measured improvement |
| verification | Full real visit, comparison with the live site, integrity checks, quality targets |
| delivery | Report, production checklist, optimized backup, cleanup |

## Limitations
- It does not deploy. The report's production checklist tells what to do on the server; the deployment must be a clean one, because an All-in-One WP Migration import does not delete files already on the server.
- Encrypted archives need the All-in-One WP Migration password.
- Local measurements show the improvement, not the production numbers: the quality targets apply to the live site after deployment.
- Premium plugins and themes update only with a valid license; the flow lists them for you instead of installing anything from third-party sources.
- Not available in cloud or WSL sessions.

## Development
```
git clone https://github.com/aledrosera/wpress-maintenance
claude plugin marketplace add ./wpress-maintenance     # local marketplace
claude plugin install wpress-maintenance@wpress-maintenance
```
Repository layout:
```
.claude-plugin/marketplace.json          marketplace (this repo)
plugins/wpress-maintenance/
  .claude-plugin/plugin.json             manifest
  skills/wpress/SKILL.md                 the playbook: principles, phases, stops, resume
  skills/wpress/references/NN-*.md       one card per phase, loaded when the phase starts
  agents/audit-*.md                      read-only audit agents
  scripts/wpress.py                      read-only .wpress reader (list, info, cat, extract)
  tests/test_wpress.py                   reader tests
docs/superpowers/                        design spec and implementation plan
```
Checks:
```
python3 -I -m unittest discover -s plugins/wpress-maintenance/tests
claude plugin validate --strict .
claude plugin validate --strict plugins/wpress-maintenance
```
The reader works on its own: `python3 plugins/wpress-maintenance/scripts/wpress.py info site.wpress`.

## License
MIT
