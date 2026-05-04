"""vLLM-backed client (OpenAI-compatible API).

Targets a local vLLM server running:
    vllm serve Qwen/Qwen3-Coder-Next-FP8 \\
        --tool-call-parser qwen3_coder \\
        --max-model-len 262144 \\
        --kv-cache-dtype fp8

The server returns tool-calls in the OpenAI function-calling format, which
we translate to our internal ToolCall dataclass.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List

from .base import LLMClient, LLMResponse, ToolCall


@dataclass
class VLLMClient(LLMClient):
    base_url: str = "http://localhost:8000/v1"
    model: str = "Qwen/Qwen3-Coder-Next-FP8"
    api_key: str = "EMPTY"          # vLLM ignores the key but the SDK requires one
    timeout: float = 300.0
    temperature: float = 0.2
    max_tokens: int = 2048

    def __post_init__(self):
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as e:
            raise ImportError("pip install openai") from e
        self._client = OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=self.timeout)

    def complete(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> LLMResponse:
        kw = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        if tools:
            kw["tools"] = tools
            kw["tool_choice"] = kwargs.get("tool_choice", "auto")

        resp = self._client.chat.completions.create(**kw)
        choice = resp.choices[0].message
        content = choice.content or ""
        tool_calls: List[ToolCall] = []
        for tc in (choice.tool_calls or []):
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            tool_calls.append(ToolCall(id=tc.id, name=tc.function.name, arguments=args))

        usage = {}
        if getattr(resp, "usage", None):
            usage = {
                "prompt": resp.usage.prompt_tokens,
                "completion": resp.usage.completion_tokens,
            }
        return LLMResponse(content=content, tool_calls=tool_calls, usage=usage, raw=resp)
