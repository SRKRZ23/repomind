"""Tool layer tests — no GPU, no network."""
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.read_file import make_tool as make_read_file
from tools.grep import make_tool as make_grep
from tools.execute_code import make_tool as make_execute
from tools.git_log import make_tool as make_git_log
from tools.registry import default_registry


class TestReadFile(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "hello.txt").write_text("a\nb\nc\nd\ne\n")
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_read_full(self):
        tool = make_read_file(self.root)
        result = tool.runner(path="hello.txt")
        self.assertTrue(result.ok)
        self.assertIn("    1  a", result.output)
        self.assertIn("    5  e", result.output)

    def test_read_range(self):
        tool = make_read_file(self.root)
        result = tool.runner(path="hello.txt", start_line=2, end_line=4)
        self.assertTrue(result.ok)
        self.assertNotIn("    1  a", result.output)
        self.assertIn("    2  b", result.output)
        self.assertNotIn("    5  e", result.output)

    def test_path_traversal_blocked(self):
        tool = make_read_file(self.root)
        result = tool.runner(path="../etc/passwd")
        self.assertFalse(result.ok)
        self.assertIn("outside repo", result.error)

    def test_missing_file(self):
        tool = make_read_file(self.root)
        result = tool.runner(path="nope.txt")
        self.assertFalse(result.ok)


class TestGrep(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "a.py").write_text("def foo():\n    return 'hello'\n")
        (root / "b.py").write_text("def bar():\n    return 'world'\n")
        sub = root / "sub"; sub.mkdir()
        (sub / "c.py").write_text("def foo_two():\n    pass\n")
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_basic_match(self):
        tool = make_grep(self.root)
        result = tool.runner(pattern=r"def foo")
        self.assertTrue(result.ok)
        self.assertIn("a.py", result.output)
        self.assertIn("sub/c.py", result.output)

    def test_no_match(self):
        tool = make_grep(self.root)
        result = tool.runner(pattern="absolutely_does_not_exist")
        self.assertTrue(result.ok)
        self.assertEqual(result.extra.get("matches"), 0)

    def test_invalid_regex(self):
        tool = make_grep(self.root)
        result = tool.runner(pattern="[unclosed")
        self.assertFalse(result.ok)
        self.assertIn("invalid regex", result.error)

    def test_path_traversal_blocked(self):
        tool = make_grep(self.root)
        result = tool.runner(pattern="x", path="../..")
        self.assertFalse(result.ok)


class TestExecuteCode(unittest.TestCase):
    def test_simple_print(self):
        with TemporaryDirectory() as scratch:
            tool = make_execute(scratch, timeout=10)
            result = tool.runner(code="print('hello from sandbox')")
            self.assertTrue(result.ok, msg=f"output={result.output!r} err={result.error!r}")
            self.assertIn("hello from sandbox", result.output)

    def test_runtime_error(self):
        with TemporaryDirectory() as scratch:
            tool = make_execute(scratch, timeout=10)
            result = tool.runner(code="raise ValueError('boom')")
            self.assertFalse(result.ok)
            self.assertIn("ValueError", result.error)

    def test_timeout(self):
        with TemporaryDirectory() as scratch:
            tool = make_execute(scratch, timeout=2)
            result = tool.runner(code="while True:\n    pass\n", timeout_seconds=2)
            self.assertFalse(result.ok)
            # Either CPU rlimit kicks in (signal) or wall-clock timeout — both acceptable
            self.assertTrue("timeout" in result.error.lower() or "killed" in result.error.lower() or "non-zero" in result.error.lower())


class TestGitLog(unittest.TestCase):
    def test_not_a_repo(self):
        with TemporaryDirectory() as tmp:
            tool = make_git_log(tmp)
            result = tool.runner(limit=5)
            self.assertFalse(result.ok)
            self.assertIn("not a git", result.error)


class TestRegistry(unittest.TestCase):
    def test_default_registry_has_all_tools(self):
        with TemporaryDirectory() as tmp:
            with TemporaryDirectory() as scratch:
                reg = default_registry(tmp, scratch)
                names = set(reg.names())
                self.assertEqual(names, {"read_file", "grep_codebase", "execute_code", "run_tests", "git_log"})

    def test_registry_unknown_tool(self):
        with TemporaryDirectory() as tmp:
            reg = default_registry(tmp)
            result = reg.call("nope", {})
            self.assertFalse(result.ok)


if __name__ == "__main__":
    unittest.main()
