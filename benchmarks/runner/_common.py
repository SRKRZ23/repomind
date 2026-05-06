"""Shared helpers for benchmark scripts.

All scripts:
- target an OpenAI-compatible endpoint (vLLM with `--max-model-len 262144`)
- write a single JSON result blob into RESULTS_DIR
- log progress to stderr so stdout stays parseable

Synthetic prompts are built from a code corpus by repeating until the target
token count is hit. Tokenization uses tiktoken cl100k_base as a proxy
(Qwen3-Coder-Next-FP8 uses its own tokenizer, but for budgeting purposes
cl100k is within ~5% of qwen-coder for code-heavy text).
"""
from __future__ import annotations
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_BASE_URL = os.environ.get("REPOMIND_BENCH_BASE_URL", "http://localhost:8000/v1")
DEFAULT_MODEL = os.environ.get("REPOMIND_BENCH_MODEL", "Qwen/Qwen3-Coder-Next-FP8")
RESULTS_DIR = Path(os.environ.get("REPOMIND_BENCH_OUT", "benchmarks/results")).resolve()


def log(msg: str) -> None:
    print(f"[bench] {msg}", file=sys.stderr, flush=True)


def ensure_results_dir() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR


def write_result(filename: str, payload: Dict[str, Any]) -> Path:
    out = ensure_results_dir() / filename
    out.write_text(json.dumps(payload, indent=2, default=str))
    log(f"wrote {out}")
    return out


def get_tokenizer():
    """Return a tiktoken encoder. Used only for *budgeting* prompt size."""
    try:
        import tiktoken  # type: ignore
    except ImportError:
        log("tiktoken not installed — falling back to char/4 estimate")
        return None
    return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str, enc=None) -> int:
    if enc is None:
        return max(1, len(text) // 4)
    return len(enc.encode(text))


CORPUS_SNIPPET = '''\
# Synthetic code corpus chunk used for prompt padding.
# This is repeated to hit a target token count for context-length benchmarks.
def merge_sort(arr):
    """Standard divide-and-conquer merge sort. O(n log n) time, O(n) space."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


class LRUCache:
    """Doubly-linked-list LRU cache with O(1) get/put."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = self._Node(None, None)
        self.tail = self._Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    class _Node:
        __slots__ = ("key", "val", "prev", "next")
        def __init__(self, key, val):
            self.key, self.val = key, val
            self.prev = self.next = None

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node); self._add_front(node)
        return node.val

    def put(self, key, val):
        if key in self.map:
            self._remove(self.map[key])
        node = self._Node(key, val)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.capacity:
            old = self.tail.prev
            self._remove(old)
            del self.map[old.key]


def longest_common_subsequence(a, b):
    """Classic LCS via DP. Returns the LCS string, not just its length."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    out = []
    i, j = n, m
    while i and j:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))
'''


def build_prompt(target_tokens: int, enc=None) -> str:
    """Repeat CORPUS_SNIPPET until the prompt has approximately target_tokens."""
    base_tokens = count_tokens(CORPUS_SNIPPET, enc)
    repeats = max(1, target_tokens // base_tokens)
    body = CORPUS_SNIPPET * repeats
    while count_tokens(body, enc) < target_tokens:
        body += CORPUS_SNIPPET
    # Truncate from the front by trimming whole snippets, keeping tail intact.
    while count_tokens(body, enc) > target_tokens + 200 and body.count(CORPUS_SNIPPET) > 1:
        body = body[len(CORPUS_SNIPPET):]
    return body


def make_question_prompt(target_context_tokens: int, enc=None) -> List[Dict[str, str]]:
    """Build a [system, user] message pair with user prompt sized to target tokens.

    The user message contains a code corpus + a final question that forces
    the model to actually attend to the context (not just last few tokens).
    """
    sentinel = "// SENTINEL_LINE_42: function name is `longest_common_subsequence`"
    padding_target = max(0, target_context_tokens - 200)
    body = build_prompt(padding_target, enc)
    user = (
        "Below is a Python codebase fragment. After reading it, answer the question at the end.\n\n"
        f"```python\n{body}\n{sentinel}\n```\n\n"
        "Question: name the LCS function defined in this codebase, and state the time complexity in big-O. "
        "Reply in one short sentence only."
    )
    return [
        {"role": "system", "content": "You are a precise code-reading assistant."},
        {"role": "user", "content": user},
    ]


def http_post_completion(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 64,
    temperature: float = 0.0,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    """Direct HTTP call (no OpenAI SDK) so we can run with stdlib only on droplet."""
    import urllib.request
    import urllib.error
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer EMPTY"},
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
        elapsed = time.perf_counter() - t0
        parsed = json.loads(body)
        return {"ok": True, "elapsed": elapsed, "response": parsed}
    except urllib.error.HTTPError as e:
        elapsed = time.perf_counter() - t0
        return {"ok": False, "elapsed": elapsed, "error": f"HTTP {e.code}", "body": e.read().decode("utf-8", errors="replace")}
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return {"ok": False, "elapsed": elapsed, "error": str(e)}


@dataclass
class CallResult:
    ok: bool
    elapsed: float
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    content: str = ""
    error: Optional[str] = None
    raw: Optional[Dict[str, Any]] = field(default=None, repr=False)

    @classmethod
    def from_http(cls, r: Dict[str, Any]) -> "CallResult":
        if not r.get("ok"):
            return cls(ok=False, elapsed=r.get("elapsed", 0.0), error=r.get("error", "unknown"), raw=r)
        resp = r["response"]
        usage = resp.get("usage") or {}
        msg = (resp.get("choices") or [{}])[0].get("message") or {}
        return cls(
            ok=True,
            elapsed=r["elapsed"],
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
            total_tokens=int(usage.get("total_tokens") or 0),
            content=msg.get("content") or "",
            raw=resp,
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("raw", None)
        return d
