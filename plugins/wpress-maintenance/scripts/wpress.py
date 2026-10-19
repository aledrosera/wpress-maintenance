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
import fnmatch
import io
import json
import os
import sys
from collections import namedtuple

HEADER = 4377
CHUNK = 1 << 20
HEX = b'0123456789abcdefABCDEF'
Entry = namedtuple('Entry', 'path size mtime offset')


class FormatError(Exception):
    pass


class EncryptedError(Exception):
    pass


def _number(raw, what, offset):
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
            # end marker: all zeros (older writers) or empty name/mtime/prefix with size and crc (newer writers)
            if not h[:255].strip(b'\0') and not h[269:4369].strip(b'\0'):
                return
            name = h[:255].rstrip(b'\0').decode('utf-8', 'surrogateescape')
            size = _number(h[255:269], 'size', offset)
            mtime = _number(h[269:281], 'mtime', offset)
            tail = h[4369:4377]
            # newer writers: 8 hex chars of crc32 after a 4088-byte prefix
            has_crc = h[4368:4369] == b'\0' and not tail.strip(HEX)
            prefix = (h[281:4369] if has_crc else h[281:4377]).rstrip(b'\0').decode('utf-8', 'surrogateescape')
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
    buf = io.BytesIO()
    _copy(archive, _find(archive, 'package.json'), buf)
    try:
        return json.loads(buf.getvalue().decode('utf-8'))
    except ValueError as exc:
        raise FormatError(f'package.json is not valid JSON: {exc}')


def _flag(value):
    return value is True or value == 1 or str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def _refuse_if_unreadable(archive):
    try:
        pkg = read_package(archive)
    except KeyError:
        return
    if _flag(pkg.get('Encrypted')):
        raise EncryptedError('archive is encrypted: file contents cannot be read without the All-in-One WP Migration password')
    if _flag(pkg.get('Compressed')) or _flag(pkg.get('Compression')):
        raise FormatError('archive is compressed: entries are not stored as plain files, this reader cannot decode them')


def stream_entry(archive, path, out):
    if path != 'package.json':
        _refuse_if_unreadable(archive)
    return _copy(archive, _find(archive, path), out)


def _safe_target(dest, path):
    parts = path.replace('\\', '/').split('/')
    if os.path.isabs(path) or path.startswith(('/', '\\')) or '..' in parts:
        raise FormatError(f'unsafe entry path refused: {path!r}')
    target = os.path.realpath(os.path.join(dest, path))
    if not target.startswith(os.path.realpath(dest) + os.sep):
        raise FormatError(f'unsafe entry path refused: {path!r}')
    return target


def extract(archive, dest, patterns):
    _refuse_if_unreadable(archive)
    matched = [e for e in iter_entries(archive) if any(fnmatch.fnmatch(e.path, p) for p in patterns)]
    targets = [(e, _safe_target(dest, e.path)) for e in matched]  # validate every path before writing anything
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
        ('encrypted', _flag(pkg.get('Encrypted'))),
        ('compressed', _flag(pkg.get('Compressed')) or _flag(pkg.get('Compression'))),
        ('network', _flag(pkg.get('Multisite')) or _flag(pkg.get('Network')) or 'unknown (not in metadata)'),
        ('active_plugins', ', '.join(pkg.get('Plugins') or [])),
    ]
    entries = list(iter_entries(archive))
    rows += [('entries', len(entries)), ('content_bytes', sum(e.size for e in entries))]
    return '\n'.join(f'{k}: {v}' for k, v in rows)


def _usage_ok(argv):
    if len(argv) < 2 or argv[0] not in ('info', 'list', 'cat', 'extract'):
        return False
    return {'info': len(argv) == 2, 'list': len(argv) in (2, 3), 'cat': len(argv) == 3, 'extract': len(argv) >= 4}[argv[0]]


def main(argv):
    if not _usage_ok(argv):
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
