"""Token-aware operations: counting + priority-based truncation.

Uses tiktoken when available (cl100k_base encoder approximates Qwen tokens
within ~3 % on natural code/prose). Falls back to a 3.6 chars-per-token
estimator otherwise.
"""
from __future__ import annotations
from typing import Iterable, List, Sequence


_ENC = None


def _get_encoder():
    global _ENC
    if _ENC is not None:
        return _ENC
    try:
        import tiktoken
        _ENC = tiktoken.get_encoding("cl100k_base")
    except Exception:
        _ENC = False
    return _ENC


def count_tokens(text: str) -> int:
    """Best-effort token count for the configured encoder."""
    if not text:
        return 0
    enc = _get_encoder()
    if enc:
        return len(enc.encode(text, disallowed_special=()))
    # Heuristic: ~3.6 chars/token on mixed code+prose
    return max(1, int(len(text) / 3.6))


def truncate_to(text: str, max_tokens: int) -> str:
    """Drop trailing tokens to fit a budget."""
    if max_tokens <= 0:
        return ""
    enc = _get_encoder()
    if enc:
        toks = enc.encode(text, disallowed_special=())
        if len(toks) <= max_tokens:
            return text
        return enc.decode(toks[:max_tokens])
    # heuristic
    chars = int(max_tokens * 3.6)
    return text[:chars]


def fit_priority(
    items: Sequence[tuple[str, int]],   # (text, priority — lower = include first)
    max_tokens: int,
) -> str:
    """Pack texts in priority order until budget exhausted; truncate the last fitting one."""
    out: List[str] = []
    used = 0
    sorted_items = sorted(items, key=lambda t: t[1])
    for text, _prio in sorted_items:
        n = count_tokens(text)
        if used + n <= max_tokens:
            out.append(text)
            used += n
        else:
            remaining = max_tokens - used
            if remaining > 32:
                out.append(truncate_to(text, remaining))
                used = max_tokens
            break
    return "\n\n".join(out)
