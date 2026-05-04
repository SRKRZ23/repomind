"""SC-TIR-style agent loop adapted from AIMO3 (math) to coding.

Loop:
    user → LLM → (tool calls?) → tools → LLM → ... → final answer

Stops when:
  - LLM emits content with no tool calls, OR
  - max_steps hit (forces a final response without tools)

The pattern mirrors Sardor's AIMO3 SC-TIR pipeline: the model alternates
between thinking and tool-augmented action, with deterministic verification
on the tool side.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List

from serving.base import LLMClient, LLMResponse, ToolCall
from tools.base import ToolRegistry, ToolResult
from agent.prompts import SYSTEM, build_repo_overview, initial_user_prompt


@dataclass
class AgentTurn:
    role: str
    content: str
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_call_id: str | None = None


@dataclass
class AgentRun:
    answer: str
    transcript: List[Dict[str, Any]]
    tool_calls: List[Dict[str, Any]]
    steps: int
    finished: bool


class Agent:
    def __init__(
        self,
        llm: LLMClient,
        tools: ToolRegistry,
        max_steps: int = 6,
        max_tool_output_chars: int = 6000,
    ):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.max_tool_output_chars = max_tool_output_chars

    def run(self, question: str, repo_summary: Dict[str, Any]) -> AgentRun:
        overview = build_repo_overview(
            repo=repo_summary.get("repo", ""),
            n_files=repo_summary.get("n_files", 0),
            n_chunks=repo_summary.get("n_chunks", 0),
            total_tokens=repo_summary.get("total_tokens", 0),
            top_paths=_pick_top_paths(repo_summary),
        )
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": initial_user_prompt(question, overview)},
        ]
        tool_schema = self.tools.schema()
        tool_calls_log: List[Dict[str, Any]] = []
        step = 0
        finished = False

        while step < self.max_steps:
            resp = self.llm.complete(messages, tools=tool_schema)
            assistant_msg: Dict[str, Any] = {"role": "assistant"}
            if resp.content:
                assistant_msg["content"] = resp.content
            if resp.tool_calls:
                assistant_msg["tool_calls"] = [self._tool_call_to_msg(tc) for tc in resp.tool_calls]
            else:
                assistant_msg.setdefault("content", "")
            messages.append(assistant_msg)

            if not resp.tool_calls:
                finished = True
                break

            for tc in resp.tool_calls:
                tool_calls_log.append({"name": tc.name, "arguments": tc.arguments})
                result = self.tools.call(tc.name, tc.arguments)
                tool_msg = {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.name,
                    "content": self._format_tool_output(result),
                }
                messages.append(tool_msg)
            step += 1

        # If we hit max_steps without a final answer, force one more text-only call.
        if not finished:
            messages.append({
                "role": "user",
                "content": "You've used the tool budget. Provide your best final answer now, without tool calls.",
            })
            resp = self.llm.complete(messages, tools=[])
            messages.append({"role": "assistant", "content": resp.content or ""})

        # Final answer = last assistant message with content
        answer = ""
        for m in reversed(messages):
            if m.get("role") == "assistant" and m.get("content"):
                answer = m["content"]
                break

        return AgentRun(
            answer=answer,
            transcript=messages,
            tool_calls=tool_calls_log,
            steps=step,
            finished=finished,
        )

    def _tool_call_to_msg(self, tc: ToolCall) -> Dict[str, Any]:
        return {
            "id": tc.id,
            "type": "function",
            "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)},
        }

    def _format_tool_output(self, result: ToolResult) -> str:
        body = result.output if result.ok else f"[error] {result.error}"
        if len(body) > self.max_tool_output_chars:
            body = body[: self.max_tool_output_chars] + "\n[... truncated]"
        return body


def _pick_top_paths(summary: Dict[str, Any]) -> List[str]:
    chunks = summary.get("chunks") or []
    seen: List[str] = []
    seen_set = set()
    # priority 0 first, then 1; keep insertion order
    for prio in (0, 1, 2):
        for c in chunks:
            if c.get("priority") == prio and c.get("path") not in seen_set:
                seen.append(c["path"])
                seen_set.add(c["path"])
                if len(seen) >= 60:
                    return seen
    return seen
