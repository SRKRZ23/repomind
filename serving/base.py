"""LLM client protocol used by the agent loop."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class LLMResponse:
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    usage: Dict[str, int] = field(default_factory=dict)
    raw: Any = None


class LLMClient(Protocol):
    def complete(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> LLMResponse: ...
