"""Tool-call protocol shared by every tool. Mirrors the qwen3_coder schema
so vLLM's built-in tool parser can dispatch directly into our registry.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class ToolResult:
    ok: bool
    output: str
    error: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_message(self) -> Dict[str, Any]:
        body = self.output if self.ok else f"[error] {self.error}"
        return {"role": "tool", "content": body}


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Any]
    runner: Callable[..., ToolResult]


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec):
        self._tools[spec.name] = spec

    def names(self) -> List[str]:
        return list(self._tools)

    def schema(self) -> List[Dict[str, Any]]:
        """OpenAI / qwen3_coder tool schema (function-calling style)."""
        return [
            {
                "type": "function",
                "function": {
                    "name": s.name,
                    "description": s.description,
                    "parameters": s.parameters,
                },
            }
            for s in self._tools.values()
        ]

    def call(self, name: str, args: Dict[str, Any]) -> ToolResult:
        if name not in self._tools:
            return ToolResult(ok=False, output="", error=f"unknown tool: {name}")
        try:
            return self._tools[name].runner(**args)
        except TypeError as e:
            return ToolResult(ok=False, output="", error=f"bad args: {e}")
        except Exception as e:
            return ToolResult(ok=False, output="", error=f"{type(e).__name__}: {e}")
