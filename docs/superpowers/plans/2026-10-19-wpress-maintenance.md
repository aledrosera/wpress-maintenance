# wpress-maintenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A public Claude Code plugin (repo = marketplace + plugin) that turns a `.wpress` backup of any WordPress site into a cleaned, optimized, verified local copy, a technical report, and (on confirmation) an optimized `.wpress`.

**Architecture:** An adaptive playbook: one orchestrating skill (`SKILL.md`, short) + one reference card per phase (objective, decision criteria, risks to check, exit criteria) + three read-only audit agents + a `/wpress` command. The only script is a read-only `.wpress` reader (fixed binary format). Everything else Claude builds per site.

**Tech Stack:** Claude Code plugin format (marketplace.json, plugin.json, commands/agents/skills markdown), Python 3 stdlib (`unittest`), git, GitHub CLI.

**Spec:** `docs/superpowers/specs/2026-10-19-wpress-maintenance-design.md`

## Global Constraints
- Plugin instructions in English; reports/dialogue in the user's language.
- No product recommendations and no example commands in the playbook (skill, references, agents, command): decisions come from evidence on the site under maintenance.
- Unlimited Extension default URL, written verbatim once: `https://nextcloud.joinindots.com/index.php/s/PJxrSyW2gSwqDxZ/download/all-in-one-wp-migration-unlimited-extension.zip`
- Original `.wpress`: never modified or deleted; read in streaming or partial extraction; mounted read-only for import.
- No extra backup copies except in serious, justified cases.
- Temporary files and temporary tools removed at the end of the flow.
- Verification at phase ends and before destructive actions; speed and common sense.
- Live site: read-only, low concurrency, third-party resources blocked when rendering.
- Existing accounts never modified; dedicated local admin, removed before final export.
- Stops only: missing inputs; post-audit compromise summary (then continue); before final backup export; licenses/purchases/credentials/writes outside local env.
- Final backup: exported with All-in-One WP Migration, MOVED next to the original `.wpress`, never overwriting.
- Script: Python 3 stdlib only; read-only on the archive.
- Public repo: no client data (names, URLs, credentials, reports, archives). Commit identity: `Alessandro Drosera <130907945+aledrosera@users.noreply.github.com>`.

## Review Focus
- Archive written by an older AIOWM (header without CRC) → reader must list/read it like the newer variant.
- Encrypted archive → `info` reports it; `cat`/`extract` refuse with a clear message instead of emitting ciphertext.
- Malicious entry paths (`../`, absolute) in an archive → `extract` must refuse to write outside the destination.
- Truncated or non-`.wpress` file → clear error, non-zero exit, no partial output presented as success.
- Reader must never change the archive (size and mtime identical after any operation).

---

### Task 1: Repository scaffold (marketplace + plugin manifest + docs)

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/wpress-maintenance/.claude-plugin/plugin.json`
- Create: `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`

**Interfaces:**
- Produces: plugin name `wpress-maintenance`, marketplace name `wpress-maintenance`, plugin root `plugins/wpress-maintenance/`.

- [ ] **Step 1: Write `.claude-plugin/marketplace.json`**
```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "wpress-maintenance",
  "description": "Clean, secure, optimize and verify a WordPress site from an All-in-One WP Migration (.wpress) backup.",
  "owner": { "name": "Alessandro Drosera", "url": "https://github.com/aledrosera" },
  "plugins": [
    {
      "name": "wpress-maintenance",
      "description": "Adaptive playbook: local restore of a .wpress, security audit and remediation, cleanup, media and performance optimization, verification against the live site, report and optimized backup.",
      "source": "./plugins/wpress-maintenance",
      "category": "productivity"
    }
  ]
}
```
- [ ] **Step 2: Write `plugins/wpress-maintenance/.claude-plugin/plugin.json`**
```json
{
  "name": "wpress-maintenance",
  "version": "0.1.0",
  "description": "Adaptive playbook to restore a WordPress .wpress backup locally, remediate compromises, clean, optimize, verify against the live site and deliver a report and an optimized backup.",
  "author": { "name": "Alessandro Drosera", "url": "https://github.com/aledrosera" },
  "homepage": "https://github.com/aledrosera/wpress-maintenance",
  "repository": "https://github.com/aledrosera/wpress-maintenance",
  "license": "MIT",
  "keywords": ["wordpress", "wpress", "all-in-one-wp-migration", "security", "malware", "cleanup", "performance", "media"]
}
```
- [ ] **Step 3: Write `LICENSE`** (MIT, `Copyright (c) 2026 Alessandro Drosera`), `.gitignore` (`__pycache__/`, `*.pyc`, `.DS_Store`, `*.wpress`, `*.zip`), `CHANGELOG.md` (`## 0.1.0 - 2026-10-19` / `- First release.`)
- [ ] **Step 4: Write `README.md`** — sections: What it does (one paragraph, spec §1), Requirements (Claude Code, Docker, Python 3, disk space ≈ archive size + database), Install (`/plugin marketplace add aledrosera/wpress-maintenance`, `/plugin install wpress-maintenance@wpress-maintenance`), Usage (put the `.wpress` and optionally the Unlimited Extension zip in a working folder, run `/wpress`; `/wpress <phase>`; `/wpress resume`), What you get (report, local environment, optimized `.wpress` on confirmation), Safety (original never modified, live site read-only, no writes to production), Phases (list of the 11 phases with one line each), License.
- [ ] **Step 5: Validate and commit**
Run: `claude plugin validate --strict .` then `claude plugin validate --strict plugins/wpress-maintenance`
Expected: no errors (warnings about missing components are acceptable until Task 6; re-run with `--strict` in Task 7).
```bash
git add -A && git commit -m "feat: marketplace and plugin manifest, README, license"
```

### Task 2: `.wpress` reader (TDD)

**Files:**
- Create: `plugins/wpress-maintenance/scripts/wpress.py`
- Test: `plugins/wpress-maintenance/tests/test_wpress.py`

**Interfaces:**
- Produces (Python): `FormatError(Exception)`, `EncryptedError(Exception)`, `Entry(path: str, size: int, mtime: int, offset: int)`, `iter_entries(archive: str) -> Iterator[Entry]`, `read_package(archive: str) -> dict`, `stream_entry(archive: str, path: str, out: BinaryIO) -> int`, `extract(archive: str, dest: str, patterns: list[str]) -> list[str]`.
- Produces (CLI): `python3 wpress.py info|list|cat|extract ...`; exit 0 ok, 2 usage, 3 format/encryption error, 4 entry not found.

- [ ] **Step 1: Write the failing tests**
```python
import io, json, os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import wpress  # noqa: E402

def _header(name, size, mtime, prefix, crc):
    h = name.encode().ljust(255, b'\0') + str(size).encode().ljust(14, b'\0') + str(mtime).encode().ljust(12, b'\0')
    if crc:
        h += prefix.encode().ljust(4088, b'\0') + b'0badc0de'
    else:
        h += prefix.encode().ljust(4096, b'\0')
    assert len(h) == 4377
    return h

def make_archive(path, files, crc=True, package=None):
    pkg = package if package is not None else {'SiteURL': 'https://example.test', 'WordPress': {'Version': '6.0'}}
    entries = [('.', 'package.json', json.dumps(pkg).encode())] + files
    with open(path, 'wb') as f:
        for prefix, name, data in entries:
            f.write(_header(name, len(data), 1700000000, prefix, crc))
            f.write(data)
        f.write(b'\0' * 4377)

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.d = self.tmp.name
        self.files = [('.', 'database.sql', b'INSERT INTO t VALUES (1);\n'), ('uploads/2024/01', 'a.jpg', b'\xff\xd8jpeg'), ('plugins/x', 'x.php', b'<?php echo 1;')]
    def tearDown(self): self.tmp.cleanup()

    def test_lists_both_header_variants(self):
        for crc in (True, False):
            p = os.path.join(self.d, f'v{crc}.wpress'); make_archive(p, self.files, crc=crc)
            self.assertEqual([e.path for e in wpress.iter_entries(p)], ['package.json', 'database.sql', 'uploads/2024/01/a.jpg', 'plugins/x/x.php'])

    def test_stream_entry_exact_bytes(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        out = io.BytesIO(); n = wpress.stream_entry(p, 'uploads/2024/01/a.jpg', out)
        self.assertEqual(out.getvalue(), b'\xff\xd8jpeg'); self.assertEqual(n, 6)

    def test_missing_entry_raises(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        with self.assertRaises(KeyError): wpress.stream_entry(p, 'nope.txt', io.BytesIO())

    def test_read_package(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        self.assertEqual(wpress.read_package(p)['SiteURL'], 'https://example.test')

    def test_extract_only_matching(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        dest = os.path.join(self.d, 'out'); got = wpress.extract(p, dest, ['uploads/*'])
        self.assertEqual(got, ['uploads/2024/01/a.jpg'])
        self.assertTrue(os.path.isfile(os.path.join(dest, 'uploads/2024/01/a.jpg')))
        self.assertFalse(os.path.exists(os.path.join(dest, 'database.sql')))

    def test_extract_refuses_path_traversal(self):
        p = os.path.join(self.d, 'evil.wpress'); make_archive(p, [('../..', 'evil.php', b'x'), ('/etc', 'passwd', b'x')])
        dest = os.path.join(self.d, 'out')
        with self.assertRaises(wpress.FormatError): wpress.extract(p, dest, ['*'])
        self.assertFalse(os.path.exists(os.path.join(self.d, 'evil.php')))

    def test_truncated_and_garbage_raise_format_error(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        t = os.path.join(self.d, 't.wpress')
        with open(p, 'rb') as f, open(t, 'wb') as g: g.write(f.read(5000))
        with self.assertRaises(wpress.FormatError): list(wpress.iter_entries(t))
        gpath = os.path.join(self.d, 'g.wpress')
        with open(gpath, 'wb') as g: g.write(os.urandom(9000))
        with self.assertRaises(wpress.FormatError): list(wpress.iter_entries(gpath))

    def test_encrypted_archive_refuses_content(self):
        p = os.path.join(self.d, 'e.wpress'); make_archive(p, self.files, package={'SiteURL': 'x', 'Encrypted': True})
        with self.assertRaises(wpress.EncryptedError): wpress.stream_entry(p, 'database.sql', io.BytesIO())
        with self.assertRaises(wpress.EncryptedError): wpress.extract(p, os.path.join(self.d, 'o'), ['*'])

    def test_archive_unchanged(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        before = os.stat(p); list(wpress.iter_entries(p)); wpress.read_package(p)
        wpress.stream_entry(p, 'database.sql', io.BytesIO()); wpress.extract(p, os.path.join(self.d, 'o'), ['*.php'])
        after = os.stat(p)
        self.assertEqual((before.st_size, before.st_mtime_ns), (after.st_size, after.st_mtime_ns))

    def test_cli_info_and_exit_codes(self):
        p = os.path.join(self.d, 'a.wpress'); make_archive(p, self.files)
        script = os.path.join(HERE, '..', 'scripts', 'wpress.py')
        r = subprocess.run([sys.executable, '-I', script, 'info', p], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0); self.assertIn('https://example.test', r.stdout)
        r = subprocess.run([sys.executable, '-I', script, 'cat', p, 'nope'], capture_output=True)
        self.assertEqual(r.returncode, 4)
        bad = os.path.join(self.d, 'bad.wpress'); open(bad, 'wb').write(b'not an archive' * 400)
        r = subprocess.run([sys.executable, '-I', script, 'list', bad], capture_output=True)
        self.assertEqual(r.returncode, 3)

if __name__ == '__main__':
    unittest.main()
```
- [ ] **Step 2: Run tests, expect failure** — `python3 -I -m unittest discover -s plugins/wpress-maintenance/tests -v` → FAIL (`No module named 'wpress'`).
- [ ] **Step 3: Implement `scripts/wpress.py`**
```python
#!/usr/bin/env python3
"""Read-only reader for All-in-One WP Migration .wpress archives (stdlib only).

Format: sequence of [4377-byte header][file data], terminated by a 4377-byte all-zero header.
Header: name(255) size(14) mtime(12) prefix(4096). Newer writers use prefix(4088) + crc32 hex(8).

Usage:
  wpress.py info ARCHIVE                     metadata from package.json
  wpress.py list ARCHIVE [GLOB]              entries (size, mtime, path)
  wpress.py cat ARCHIVE PATH                 stream one entry to stdout
  wpress.py extract ARCHIVE DEST GLOB...     extract only matching entries under DEST
Exit codes: 0 ok, 2 usage, 3 format/encryption error, 4 entry not found.
"""
import fnmatch, json, os, sys
from collections import namedtuple

HEADER = 4377
CHUNK = 1 << 20
Entry = namedtuple('Entry', 'path size mtime offset')

class FormatError(Exception):
    pass

class EncryptedError(Exception):
    pass

def _field(raw, what, offset):
    raw = raw.rstrip(b'\0')
    if not raw.isdigit():
        raise FormatError(f'not a .wpress archive or corrupted header at offset {offset} ({what})')
    return int(raw)

def iter_entries(archive):
    total = os.path.getsize(archive)
    with open(archive, 'rb') as f:
        while True:
            offset = f.tell()
            h = f.read(HEADER)
            if len(h) < HEADER:
                raise FormatError(f'truncated archive: missing end-of-archive marker at offset {offset}')
            if not h.strip(b'\0'):
                return
            name = h[:255].rstrip(b'\0').decode('utf-8', 'surrogateescape')
            size = _field(h[255:269], 'size', offset)
            mtime = _field(h[269:281], 'mtime', offset)
            tail = h[4369:4377]
            crc_variant = h[4368:4369] == b'\0' and len(tail.strip(b'0123456789abcdefABCDEF')) == 0 and tail.strip(b'\0') == tail
            prefix = (h[281:4369] if crc_variant else h[281:4377]).rstrip(b'\0').decode('utf-8', 'surrogateescape')
            if not name:
                raise FormatError(f'empty entry name at offset {offset}')
            if offset + HEADER + size > total:
                raise FormatError(f'truncated archive: entry {name!r} exceeds file size')
            path = name if prefix in ('', '.') else f'{prefix}/{name}'
            yield Entry(path, size, mtime, offset + HEADER)
            f.seek(size, 1)

def _find(archive, path):
    for e in iter_entries(archive):
        if e.path == path:
            return e
    raise KeyError(path)

def _copy(archive, entry, out):
    with open(archive, 'rb') as f:
        f.seek(entry.offset)
        left = entry.size
        while left:
            chunk = f.read(min(CHUNK, left))
            if not chunk:
                raise FormatError(f'unexpected end of data in {entry.path!r}')
            out.write(chunk)
            left -= len(chunk)
    return entry.size

def read_package(archive):
    from io import BytesIO
    buf = BytesIO()
    _copy(archive, _find(archive, 'package.json'), buf)
    try:
        return json.loads(buf.getvalue().decode('utf-8'))
    except ValueError as exc:
        raise FormatError(f'package.json is not valid JSON: {exc}')

def _refuse_if_encrypted(archive):
    try:
        pkg = read_package(archive)
    except KeyError:
        return
    if pkg.get('Encrypted') in (True, 1, '1', 'true', 'yes'):
        raise EncryptedError('archive is encrypted: file contents cannot be read without the AIOWM password')

def stream_entry(archive, path, out):
    if path != 'package.json':
        _refuse_if_encrypted(archive)
    return _copy(archive, _find(archive, path), out)

def _safe_target(dest, path):
    if os.path.isabs(path) or path.startswith(('/', '\\')) or '..' in path.replace('\\', '/').split('/'):
        raise FormatError(f'unsafe entry path refused: {path!r}')
    target = os.path.realpath(os.path.join(dest, path))
    if not target.startswith(os.path.realpath(dest) + os.sep):
        raise FormatError(f'unsafe entry path refused: {path!r}')
    return target

def extract(archive, dest, patterns):
    _refuse_if_encrypted(archive)
    matched = [e for e in iter_entries(archive) if any(fnmatch.fnmatch(e.path, p) for p in patterns)]
    targets = [(e, _safe_target(dest, e.path)) for e in matched]  # validate all before writing anything
    for e, target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'wb') as out:
            _copy(archive, e, out)
    return [e.path for e, _ in targets]

def _info(archive):
    pkg = read_package(archive)
    wp, db, php = pkg.get('WordPress') or {}, pkg.get('Database') or {}, pkg.get('PHP') or {}
    rows = [
        ('site_url', pkg.get('SiteURL')), ('home_url', pkg.get('HomeURL')),
        ('wordpress', wp.get('Version')), ('php', php.get('Version')), ('database', db.get('Version')),
        ('table_prefix', db.get('Prefix')), ('charset', db.get('Charset')),
        ('template', pkg.get('Template')), ('stylesheet', pkg.get('Stylesheet')),
        ('aiowm_version', (pkg.get('Plugin') or {}).get('Version')),
        ('encrypted', bool(pkg.get('Encrypted'))), ('compression', pkg.get('Compression')),
        ('active_plugins', ', '.join(pkg.get('Plugins') or [])),
    ]
    entries = list(iter_entries(archive))
    rows += [('entries', len(entries)), ('content_bytes', sum(e.size for e in entries))]
    return '\n'.join(f'{k}: {v}' for k, v in rows)

def main(argv):
    if len(argv) < 2 or argv[0] not in ('info', 'list', 'cat', 'extract') or (argv[0] == 'cat' and len(argv) != 3) or (argv[0] == 'extract' and len(argv) < 4):
        print(__doc__, file=sys.stderr)
        return 2
    cmd, archive = argv[0], argv[1]
    try:
        if cmd == 'info':
            print(_info(archive))
        elif cmd == 'list':
            glob = argv[2] if len(argv) > 2 else '*'
            for e in iter_entries(archive):
                if fnmatch.fnmatch(e.path, glob):
                    print(f'{e.size}\t{e.mtime}\t{e.path}')
        elif cmd == 'cat':
            stream_entry(archive, argv[2], sys.stdout.buffer)
        else:
            for p in extract(archive, argv[2], argv[3:]):
                print(p)
    except KeyError as exc:
        print(f'entry not found: {exc.args[0]}', file=sys.stderr)
        return 4
    except (FormatError, EncryptedError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 3
    except BrokenPipeError:
        return 0
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```
- [ ] **Step 4: Run tests, expect pass** — same command → all OK.
- [ ] **Step 5: Real-archive read-only check** — on a real `.wpress` available locally: record `stat`, run `info`, `list ARCHIVE 'database.sql'`, `cat ARCHIVE package.json | head -c 200`, re-`stat` → size and mtime identical.
- [ ] **Step 6: Commit** — `git add plugins/wpress-maintenance/scripts plugins/wpress-maintenance/tests && git commit -m "feat: read-only .wpress reader with tests"`

### Task 3: Orchestrating skill `SKILL.md`

**Files:**
- Create: `plugins/wpress-maintenance/skills/wpress-maintenance/SKILL.md`

**Interfaces:**
- Consumes: reader CLI (Task 2) at `${CLAUDE_PLUGIN_ROOT}/scripts/wpress.py`; phase cards (Task 4) at `references/NN-*.md`; agents (Task 5) `audit-files`, `audit-database`, `audit-components`.
- Produces: phase ids used by `/wpress` (Task 6): `preflight, environment, import, baseline, audit, remediation, cleanup, media, performance, verification, delivery`.

- [ ] **Step 1: Write SKILL.md** with frontmatter `name: wpress-maintenance` and a `description` that triggers on: a `.wpress` backup in the working folder, requests to restore/clean/secure/optimize/verify a WordPress site from an All-in-One WP Migration backup. Body sections (English, concise, no example commands, no product names other than All-in-One WP Migration and its Unlimited Extension):
  1. *Outcome and scope* — spec §1 in 3 lines; deliverables in the working folder (spec §6.10); out of scope (spec §3): production deploy, any write to the live site/server/external services, redesign or content changes not needed for remediation/cleanup/optimization.
  2. *Operating principles* — the 8 principles of spec §5, one line each, verbatim in meaning.
  3. *Inputs* — spec §4: locate `.wpress` (ask for a reachable URL if missing, download with resume, validate with the reader; ask which one if several); locate the Unlimited Extension zip, else download from the Global Constraints URL, else ask the user for it or its location; read metadata with the reader (`info`); encrypted → ask for password; Docker, disk space, free port.
  4. *Phases* — table: id · reference file · objective (one line) · exit criterion (one line); instruction: load a phase card only when starting that phase.
  5. *Stops* — spec §7, the only four reasons to pause; at the compromise stop show critical findings with evidence, then continue without waiting unless the user intervenes.
  6. *Audit delegation* — launch the three audit agents in parallel in phase `audit`, passing: working folder, local URLs, how to reach wp-cli/db/files in the environment, live URL; they are read-only and return findings with severity, evidence, proposed action.
  7. *State and resume* — the report being written in the working folder is the state: each completed phase appends its section and numbers; `resume` reads it plus the environment and continues from the first incomplete phase; `<phase>` reruns one phase.
  8. *Archive reader* — what it does and its four subcommands with arguments (from the reader docstring), exit codes; never write into the archive.
  9. *Temporary work* — temp files only in the session scratch area or inside containers; list and remove them at the end; temporary tools installed in containers are removed at the end.
- [ ] **Step 2: Check** — `grep -niE 'docker run|wp plugin install|curl |wget |autoptimize|super cache|w3 total|litespeed|rocket|wordfence|imagify|smush' SKILL.md` → no matches (no example commands, no product recommendations).
- [ ] **Step 3: Commit** — `git commit -m "feat: orchestrating skill"`

### Task 4: Phase reference cards

**Files:** create in `plugins/wpress-maintenance/skills/wpress-maintenance/references/`:
`00-preflight.md, 01-environment.md, 02-import.md, 03-baseline.md, 04-audit.md, 05-remediation.md, 06-cleanup.md, 07-media.md, 08-performance.md, 09-verification.md, 10-delivery.md`

Every card has exactly these sections: **Objective**, **Determine** (what to find out on this site), **Decide** (criteria, alternatives depending on what was found), **Risks to check** (spec §8 items relevant to this phase, phrased as checks), **Exit criteria**, **Report** (what this phase adds to the report). No example commands, no product names (except AIOWM).

- [ ] **Step 1: 00-preflight** — spec §4 + §6.0; Unlimited URL from Global Constraints; download validation via reader; disk estimate; multiple archives → ask.
- [ ] **Step 2: 01-environment** — spec §6.1: versions from metadata, nearest compatible when exact unavailable (note it), import-capable PHP limits, a wp-cli service, archive mounted read-only, environment files in the working folder, free port; exit: local WordPress reachable.
- [ ] **Step 3: 02-import** — spec §6.2: base plugin from the official source, add-on from zip, check add-on update, CLI import reading the mounted archive; post-import: dedicated local admin (credentials shown to the user, never in the report), URL/permalink sanity; risks: archive table prefix vs environment, site URL replacement, existing accounts untouched.
- [ ] **Step 4: 03-baseline** — spec §6.3: URL inventory (sitemap, internal link discovery, reachable-but-unlinked URLs such as taxonomy archives), statuses/assets/errors on local, production stack from response headers (read-only), keep what later comparisons need, avoid storing more than needed.
- [ ] **Step 5: 04-audit** — spec §6.4 + compromise signatures from §8; how to brief the three agents; merge/deduplicate findings; severity scale CRITICAL/HIGH/MEDIUM/LOW/INFO; compromise stop (§7.2).
- [ ] **Step 6: 05-remediation** — spec §6.5: remove malicious items with evidence, close exploited/exploitable vectors in a way consistent with the stack, record server-only items for the production checklist; risks: removing payload storage while the injector still exists (only relevant on the server: goes to checklist), credentials exposure.
- [ ] **Step 7: 06-cleanup** — spec §6.6 + §8 content/component risks: evidence of use for each plugin/theme (content, builder data, options, rendered pages), free vs pro widget differences, rebuild with legitimate equivalents and compare with live, content dependencies (hierarchies, menus, references, URLs), DB residues of removed components, revisions policy, non-media upload folders of removed plugins.
- [ ] **Step 8: 07-media** — spec §6.7 + §8 media risks: usage from real-browser visits across viewports with full scroll plus DOM/CSS references, builder-derived files, dynamically built URLs in custom code, cross-check with live; consistent metadata when trimming generated sizes; recompression without changing names/paths, format/codec chosen by compatibility and measured gain; temporary tools in containers removed at end; exit: zero missing media in real visit, measured weight reduction.
- [ ] **Step 9: 08-performance** — spec §6.8 + §8 cache/optimization risks: detect existing server and WordPress caching (headers, drop-ins, active plugins), avoid duplicate layers without benefit, follow user preference, preserve early/ordered inline scripts, measure before/after in identical conditions; cache constants live in wp-config (not migrated).
- [ ] **Step 10: 09-verification** — spec §6.9: full real visit (pages, assets, JS errors), visual comparison with live (every difference explained or fixed; DOM-level check when screenshots differ because of animation), essential functional checks, integrity checks list; exit and report.
- [ ] **Step 11: 10-delivery** — spec §6.10: report structure (found, done, numbers before/after, verification, production actions, pending), production checklist limited to what the clean copy does not carry (§8 migration risk), backup on confirmation: remove local admin → export → MOVE next to the original with a non-colliding name; final temp cleanup; deliverables list.
- [ ] **Step 12: Check** — same grep as Task 3 Step 2 on `references/*.md` → no matches; each file contains the six section headings (`grep -c '^## ' file` = 6).
- [ ] **Step 13: Commit** — `git commit -m "feat: phase reference cards"`

### Task 5: Audit agents

**Files:** create in `plugins/wpress-maintenance/agents/`: `audit-files.md`, `audit-database.md`, `audit-components.md`

Frontmatter for each: `name`, `description` (when to use: delegated during the `audit` phase of wpress-maintenance), `tools: Read, Bash, Glob, Grep, WebSearch, WebFetch` (components agent needs Web*; files/database may omit them), `model: inherit`.
Body for each: Role and read-only constraint (no writes to files, database, or the live site; temp files only in the scratch area and removed before returning), Inputs expected from the orchestrator, Method (investigation approach, not a closed checklist — from spec §6.4 for that domain plus §8 compromise signatures), Output format (finding: severity, location, evidence ≤5 lines, interpretation, proposed action; then: exact list of proposed actions; what could not be verified; facts vs hypotheses).

- [ ] **Step 1: audit-files.md** — integrity vs official sources where available; anomalous code; misplaced executables; modification timeline clusters; mass-generated config files; empty/unknown plugin folders; nulled indicators (license bypass, hijacked update/template requests).
- [ ] **Step 2: audit-database.md** — users/capabilities/sessions/application credentials; injections in options, content, builder data, custom-code entities; cron hooks; redirect rules; exploit artifacts; timeline of suspicious records.
- [ ] **Step 3: audit-components.md** — known vulnerabilities for installed versions (active and inactive); real usage evidence per plugin/theme; database bloat and orphan tables/options of absent components; non-media upload folders.
- [ ] **Step 4: Check** — grep for product recommendations/example commands as in Task 3 → none; `claude plugin validate plugins/wpress-maintenance` → agents recognized.
- [ ] **Step 5: Commit** — `git commit -m "feat: read-only audit agents"`

### Task 6: `/wpress` command

**Files:** create `plugins/wpress-maintenance/commands/wpress.md`

- [ ] **Step 1: Write the command** — frontmatter: `description: Restore, secure, clean, optimize and verify a WordPress site from a .wpress backup in the current folder`, `argument-hint: [phase|resume]`. Body: use the `wpress-maintenance` skill; `$ARGUMENTS` empty → full flow from preflight; `resume` → continue from the first incomplete phase recorded in the report; a phase id → run only that phase (ids from Task 3).
- [ ] **Step 2: Validate** — `claude plugin validate --strict plugins/wpress-maintenance` and `claude plugin validate --strict .` → pass.
- [ ] **Step 3: Commit** — `git commit -m "feat: /wpress command"`

### Task 7: Install and smoke test

- [ ] **Step 1: Install from the local marketplace** — `claude plugin marketplace add ~/plugins/wpress-maintenance` then `claude plugin install wpress-maintenance@wpress-maintenance`; `claude plugin details wpress-maintenance` lists 1 skill, 3 agents, 1 command.
- [ ] **Step 2: Build a small test archive** — a throwaway local WordPress with AIOWM, a few pages and images, exported to a test folder (outside any client folder); remove the throwaway environment afterwards.
- [ ] **Step 3: Headless run** — in the test folder run `/wpress` non-interactively, answering the backup confirmation; expect: report written, optimized `.wpress` moved next to the original with a different name, original size/mtime unchanged, no temp files left in the folder or scratch area.
- [ ] **Step 4: Fix and commit** any instruction gaps found; bump CHANGELOG if behavior changes.

### Task 8: Publish

- [ ] **Step 1: Create the public repo and push** — `gh repo create aledrosera/wpress-maintenance --public --source ~/plugins/wpress-maintenance --push --description "Claude Code plugin: restore, secure, clean, optimize and verify WordPress sites from .wpress backups"`.
- [ ] **Step 2: Install from GitHub** — `claude plugin marketplace remove wpress-maintenance` (local), `claude plugin marketplace add aledrosera/wpress-maintenance`, `claude plugin install wpress-maintenance@wpress-maintenance`, `claude plugin details wpress-maintenance` → same inventory.
- [ ] **Step 3: Tag** — `claude plugin tag plugins/wpress-maintenance` and `git push --tags`.
