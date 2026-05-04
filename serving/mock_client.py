"""Deterministic offline LLM stub. Drives unit tests without a GPU.

Each call inspects the latest user / tool message and decides what to do
based on simple heuristics:
  - Question contains 'grep' or 'search' → emit grep_codebase tool call
  - Question contains 'read' or 'show' → emit read_file tool call
  - After two tool turns → emit a final answer
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List

from .base import LLMClient, LLMResponse, ToolCall


@dataclass
class MockClient(LLMClient):
    max_tool_turns: int = 2

    def complete(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]], **kwargs: Any) -> LLMResponse:
        tool_turns = sum(1 for m in messages if m.get("role") == "tool")
        last_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        question = (last_user.get("content") if last_user else "") or ""

        if tool_turns >= self.max_tool_turns:
            tool_outputs = [m.get("content", "") for m in messages if m.get("role") == "tool"]
            joined = "\n".join(tool_outputs)[:1500]
            answer = (
                "Based on the inspected files, here is what I found:\n\n"
                f"{joined or '(no tool output)'}\n\n"
                f"Original question: {question.strip()}"
            )
            return LLMResponse(content=answer, tool_calls=[], usage={"prompt": 0, "completion": 0})

        # Decide which tool to call next
        q = question.lower()
        if any(k in q for k in ("grep", "search", "find", "where", "occurr")):
            call = ToolCall(
                id=f"call_{tool_turns}", name="grep_codebase",
                arguments={"pattern": _extract_term(question), "max_results": 10},
            )
        elif any(k in q for k in ("git", "history", "commits", "log")):
            call = ToolCall(id=f"call_{tool_turns}", name="git_log", arguments={"limit": 10})
        elif any(k in q for k in ("test", "run", "pytest")):
            call = ToolCall(id=f"call_{tool_turns}", name="run_tests", arguments={})
        elif any(k in q for k in ("read", "show", "open", "file")):
            call = ToolCall(
                id=f"call_{tool_turns}", name="read_file",
                arguments={"path": _extract_path(question) or "README.md"},
            )
        else:
            # default to a grep so we always exercise tool path
            call = ToolCall(
                id=f"call_{tool_turns}", name="grep_codebase",
                arguments={"pattern": _extract_term(question), "max_results": 5},
            )
        return LLMResponse(content="", tool_calls=[call], usage={"prompt": 0, "completion": 0})


def _extract_term(text: str) -> str:
    # crude term extraction for tests: take first identifier-like token longer than 3 chars
    import re
    for m in re.finditer(r"[A-Za-z_][\w]{3,}", text):
        if m.group(0).lower() not in {"what", "where", "find", "grep", "search", "show", "file", "read"}:
            return m.group(0)
    return text.strip()[:32] or "."


def _extract_path(text: str) -> str:
    import re
    m = re.search(r"[\w./-]+\.[A-Za-z]{1,5}", text)
    return m.group(0) if m else ""
