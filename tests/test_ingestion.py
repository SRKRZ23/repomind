"""Ingestion pipeline tests — no GPU, no network."""
import json
import os
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ingestion.parser import detect_language, extract_symbols
from ingestion.token_budget import count_tokens, fit_priority, truncate_to
from ingestion.chunker import chunk_file, ingest_to_json, walk_repo


PY_SAMPLE = textwrap.dedent('''\
    """Module docstring."""

    import os


    def alpha(x):
        return x + 1


    class Beta:
        def gamma(self, n):
            return n * 2


    def _private():
        pass
''')

MD_SAMPLE = textwrap.dedent('''\
    # Title

    Intro text.

    ## Section A

    body.

    ### Subsection

    more body.
''')


class TestParser(unittest.TestCase):
    def test_language_detection(self):
        self.assertEqual(detect_language("foo.py"), "python")
        self.assertEqual(detect_language("foo.rs"), "rust")
        self.assertEqual(detect_language("foo.unknown"), None)

    def test_python_symbols(self):
        syms = extract_symbols(PY_SAMPLE, "python")
        names = {s.name for s in syms}
        self.assertIn("alpha", names)
        self.assertIn("Beta", names)
        # _private is still extracted; its priority is downgraded later
        self.assertIn("_private", names)

    def test_markdown_headings(self):
        syms = extract_symbols(MD_SAMPLE, "markdown")
        names = {s.name for s in syms}
        self.assertTrue(any("Title" in n for n in names))


class TestTokenBudget(unittest.TestCase):
    def test_count_tokens(self):
        self.assertGreater(count_tokens("hello world this is a test"), 3)
        self.assertEqual(count_tokens(""), 0)

    def test_truncate(self):
        long = "word " * 1000
        out = truncate_to(long, 100)
        self.assertLessEqual(count_tokens(out), 105)  # ±5 tolerance for encoder rounding

    def test_fit_priority(self):
        items = [
            ("zzzz " * 200, 5),  # low priority, would blow budget
            ("aaaa " * 50, 0),   # highest priority
            ("bbbb " * 50, 1),
        ]
        out = fit_priority(items, max_tokens=100)
        # priority 0 must be present, priority 5 must not (or only as tail)
        self.assertIn("aaaa", out)


class TestChunker(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "README.md").write_text(MD_SAMPLE)
        (root / "src").mkdir()
        (root / "src" / "main.py").write_text(PY_SAMPLE)
        (root / "tests").mkdir()
        (root / "tests" / "test_main.py").write_text("def test_x():\n    assert True\n")
        # bin file we should skip
        (root / "image.png").write_bytes(b"\x89PNG\r\n")
        # node_modules we should skip
        (root / "node_modules").mkdir()
        (root / "node_modules" / "x.js").write_text("function x() {}")
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_chunk_file_python(self):
        chunks = chunk_file("test", self.root / "src" / "main.py", "src/main.py")
        self.assertGreater(len(chunks), 0)
        sections = {c.section for c in chunks}
        # Symbol sections should appear, not just "body"
        self.assertTrue(any(s in {"alpha", "Beta", "gamma", "_private", "header"} for s in sections))

    def test_walk_skips_node_modules_and_binary(self):
        chunks = list(walk_repo(self.root, "test"))
        paths = {c.path for c in chunks}
        self.assertNotIn("image.png", paths)
        self.assertFalse(any(p.startswith("node_modules") for p in paths))
        self.assertIn("README.md", paths)
        self.assertIn("src/main.py", paths)

    def test_priority_assignment(self):
        chunks = list(walk_repo(self.root, "test"))
        # Group priorities per path (a file produces multiple chunks).
        per_path: dict = {}
        for c in chunks:
            per_path.setdefault(c.path, set()).add(c.priority)

        # README is always 0.
        self.assertEqual(per_path["README.md"], {0})
        # tests/ live in priority tier 3.
        self.assertEqual(per_path["tests/test_main.py"], {3})
        # src/main.py mixes top-level (1) and private (_private → 2). Both must exist.
        self.assertIn(1, per_path["src/main.py"])
        self.assertIn(2, per_path["src/main.py"])

    def test_ingest_to_json(self):
        with TemporaryDirectory() as out_dir:
            out_path = Path(out_dir) / "summary.json"
            summary = ingest_to_json(self.root, out_path, repo_label="test")
            self.assertGreater(summary["n_chunks"], 0)
            data = json.loads(out_path.read_text())
            self.assertEqual(data["repo"], "test")
            self.assertIn("chunks", data)


if __name__ == "__main__":
    unittest.main()
