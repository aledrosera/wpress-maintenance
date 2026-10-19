import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, '..', 'scripts', 'wpress.py')
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


def make_archive(path, files, crc=True, package=None, sized_eof=False):
    pkg = package if package is not None else {'SiteURL': 'https://example.test', 'WordPress': {'Version': '6.0'}}
    entries = [('.', 'package.json', json.dumps(pkg).encode())] + files
    with open(path, 'wb') as f:
        for prefix, name, data in entries:
            f.write(_header(name, len(data), 1700000000, prefix, crc))
            f.write(data)
        if sized_eof:
            # newer writers: end marker with empty name/mtime, size = its own offset, crc32 in the last 8 bytes
            eof = b'\0' * 255 + str(f.tell()).encode().ljust(14, b'\0') + b'\0' * 12 + b'\0' * 4088 + b'999ee423'
            f.write(eof)
        else:
            f.write(b'\0' * 4377)


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.files = [
            ('.', 'database.sql', b'INSERT INTO t VALUES (1);\n'),
            ('uploads/2024/01', 'a.jpg', b'\xff\xd8jpeg'),
            ('plugins/x', 'x.php', b'<?php echo 1;'),
        ]

    def tearDown(self):
        self.tmp.cleanup()

    def _archive(self, name='a.wpress', **kw):
        p = os.path.join(self.d, name)
        make_archive(p, kw.pop('files', self.files), **kw)
        return p

    def test_lists_both_header_variants(self):
        for crc in (True, False):
            p = self._archive(f'v{crc}.wpress', crc=crc)
            self.assertEqual([e.path for e in wpress.iter_entries(p)],
                             ['package.json', 'database.sql', 'uploads/2024/01/a.jpg', 'plugins/x/x.php'])

    def test_sized_end_marker_of_newer_writers(self):
        p = self._archive('s.wpress', sized_eof=True)
        self.assertEqual([e.path for e in wpress.iter_entries(p)],
                         ['package.json', 'database.sql', 'uploads/2024/01/a.jpg', 'plugins/x/x.php'])

    def test_stream_entry_exact_bytes(self):
        p = self._archive()
        out = io.BytesIO()
        n = wpress.stream_entry(p, 'uploads/2024/01/a.jpg', out)
        self.assertEqual(out.getvalue(), b'\xff\xd8jpeg')
        self.assertEqual(n, 6)

    def test_missing_entry_raises(self):
        p = self._archive()
        with self.assertRaises(KeyError):
            wpress.stream_entry(p, 'nope.txt', io.BytesIO())

    def test_read_package(self):
        p = self._archive()
        self.assertEqual(wpress.read_package(p)['SiteURL'], 'https://example.test')

    def test_extract_only_matching(self):
        p = self._archive()
        dest = os.path.join(self.d, 'out')
        got = wpress.extract(p, dest, ['uploads/*'])
        self.assertEqual(got, ['uploads/2024/01/a.jpg'])
        self.assertTrue(os.path.isfile(os.path.join(dest, 'uploads/2024/01/a.jpg')))
        self.assertFalse(os.path.exists(os.path.join(dest, 'database.sql')))

    def test_extract_refuses_path_traversal(self):
        p = self._archive('evil.wpress', files=[('../..', 'evil.php', b'x'), ('/etc', 'passwd', b'x')])
        dest = os.path.join(self.d, 'out')
        with self.assertRaises(wpress.FormatError):
            wpress.extract(p, dest, ['*'])
        self.assertFalse(os.path.exists(os.path.join(self.d, 'evil.php')))

    def test_truncated_archive_raises_format_error(self):
        p = self._archive()
        t = os.path.join(self.d, 't.wpress')
        with open(p, 'rb') as f, open(t, 'wb') as g:
            g.write(f.read(5000))
        with self.assertRaises(wpress.FormatError):
            list(wpress.iter_entries(t))

    def test_garbage_raises_format_error(self):
        g = os.path.join(self.d, 'g.wpress')
        with open(g, 'wb') as f:
            f.write(b'not an archive' * 700)
        with self.assertRaises(wpress.FormatError):
            list(wpress.iter_entries(g))

    def test_encrypted_archive_refuses_content(self):
        p = self._archive('e.wpress', package={'SiteURL': 'x', 'Encrypted': True})
        with self.assertRaises(wpress.EncryptedError):
            wpress.stream_entry(p, 'database.sql', io.BytesIO())
        with self.assertRaises(wpress.EncryptedError):
            wpress.extract(p, os.path.join(self.d, 'o'), ['*'])

    def test_archive_unchanged(self):
        p = self._archive()
        before = os.stat(p)
        list(wpress.iter_entries(p))
        wpress.read_package(p)
        wpress.stream_entry(p, 'database.sql', io.BytesIO())
        wpress.extract(p, os.path.join(self.d, 'o'), ['*.php'])
        after = os.stat(p)
        self.assertEqual((before.st_size, before.st_mtime_ns), (after.st_size, after.st_mtime_ns))

    def test_cli_info_and_exit_codes(self):
        p = self._archive()
        r = subprocess.run([sys.executable, '-I', SCRIPT, 'info', p], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn('https://example.test', r.stdout)
        r = subprocess.run([sys.executable, '-I', SCRIPT, 'cat', p, 'nope'], capture_output=True)
        self.assertEqual(r.returncode, 4)
        bad = os.path.join(self.d, 'bad.wpress')
        with open(bad, 'wb') as f:
            f.write(b'not an archive' * 400)
        r = subprocess.run([sys.executable, '-I', SCRIPT, 'list', bad], capture_output=True)
        self.assertEqual(r.returncode, 3)
        r = subprocess.run([sys.executable, '-I', SCRIPT], capture_output=True)
        self.assertEqual(r.returncode, 2)


if __name__ == '__main__':
    unittest.main()
