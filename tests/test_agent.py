"""End-to-end agent loop tests with the mock LLM. No GPU, no network."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from agent.loop import Agent
from ingestion.chunker import ingest_to_json
from serving.mock_client import MockClient
from tools.registry import default_registry


SAMPLE_PY = """\
def authenticate(user, password):
    \"\"\"Check credentials.\"\"\"
    return user == 'admin' and password == 'hunter2'


def logout():
    pass
"""

SAMPLE_README = """\
# Sample Project

A tiny project used by REPOMIND tests.

## Authentication

See `auth.py` for the authenticate function.
"""


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "auth.py").write_text(SAMPLE_PY)
        (root / "README.md").write_text(SAMPLE_README)
        self.root = root
        self.summary_path = root / "summary.json"
        ingest_to_json(root, self.summary_path, repo_label="sample")
        self.summary = json.loads(self.summary_path.read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def test_agent_runs_grep(self):
        agent = Agent(
            llm=MockClient(max_tool_turns=1),
            tools=default_registry(self.root),
            max_steps=4,
        )
        result = agent.run("Where is the authenticate function?", self.summary)
        self.assertTrue(result.finished)
        self.assertGreater(len(result.tool_calls), 0)
        # Mock should choose grep_codebase for "where" queries
        self.assertEqual(result.tool_calls[0]["name"], "grep_codebase")

    def test_agent_runs_read_file(self):
        agent = Agent(
            llm=MockClient(max_tool_turns=1),
            tools=default_registry(self.root),
            max_steps=4,
        )
        result = agent.run("Read the README.md file", self.summary)
        self.assertTrue(result.finished)
        self.assertEqual(result.tool_calls[0]["name"], "read_file")

    def test_agent_produces_answer(self):
        agent = Agent(
            llm=MockClient(max_tool_turns=2),
            tools=default_registry(self.root),
            max_steps=4,
        )
        result = agent.run("Find all functions in this project", self.summary)
        self.assertGreater(len(result.answer), 0)
        self.assertGreaterEqual(len(result.tool_calls), 1)


if __name__ == "__main__":
    unittest.main()
