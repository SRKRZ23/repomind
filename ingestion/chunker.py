"""Smart, structure-aware chunking with priority scoring.

Per file:
  1. Detect language (filesystem extension).
  2. Extract top-level symbols via tree-sitter (or regex fallback).
  3. Slice file into chunks aligned to symbol boundaries when possible;
     otherwise split on paragraph / blank lines / hard cut.
  4. Tag each chunk with a priority used by the token budgeter:
        0 = README / top-level docs
        1 = top-level symbols (functions, classes)
        2 = nested / private symbols
        3 = test / vendored / generated code
        4 = unknown / binary-ish

The agent only sees chunks that fit its context budget — priorities decide
who gets in first when a 50K-LOC kernel doesn't fit at all.
"""
from __future__ import annotations
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from .parser import Symbol, detect_language, extract_symbols
from .token_budget import count_tokens


SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__",
    "dist", "build", "target", ".next", ".nuxt", ".cache",
    "vendor", "third_party", "external", ".gradle", ".idea", ".vscode",
}
SKIP_BIN_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".tiff",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".7z", ".xz", ".whl", ".egg",
    ".so", ".dylib", ".dll", ".exe", ".o", ".a", ".class", ".jar",
    ".bin", ".pkl", ".parquet", ".safetensors", ".pt", ".onnx",
    ".woff", ".woff2", ".ttf", ".otf", ".mp3", ".mp4", ".mov", ".wav",
}
README_NAMES = {"README.md", "README.rst", "README.txt", "README"}
TEST_PATTERNS = (re.compile(r"(?:^|/)tests?/"), re.compile(r"(?:^|/)test_"), re.compile(r"_test\."))


@dataclass
class Chunk:
    chunk_id: str
    repo: str
    path: str
    section: str            # symbol name or "header"
    start_line: int
    end_line: int
    text: str
    n_tokens: int
    priority: int


def _is_test_path(rel: str) -> bool:
    return any(p.search(rel) for p in TEST_PATTERNS)


def _file_priority(rel: str, name: str) -> int:
    if name in README_NAMES or rel.endswith(("README.md", "README.rst")):
        return 0
    if _is_test_path(rel):
        return 3
    if any(seg in rel.split("/") for seg in ("docs", "doc")):
        return 0
    return 1


def _chunk_text_by_symbols(
    text: str, symbols: List[Symbol], max_tokens: int, overlap_lines: int = 4,
) -> List[tuple[str, str, int, int]]:
    """Return [(section, text, start_line, end_line)]. Symbols are sorted by start_line."""
    lines = text.split("\n")
    n = len(lines)
    if not symbols:
        return _chunk_lines("body", lines, 1, n, max_tokens)

    symbols = sorted(symbols, key=lambda s: s.start_line)
    out: List[tuple[str, str, int, int]] = []

    # Header / preamble before first symbol
    if symbols[0].start_line > 1:
        out.extend(_chunk_lines("header", lines, 1, symbols[0].start_line - 1, max_tokens))

    for i, sym in enumerate(symbols):
        end = symbols[i + 1].start_line - 1 if i + 1 < len(symbols) else n
        if end < sym.start_line:
            continue
        out.extend(_chunk_lines(sym.name or sym.kind, lines, sym.start_line, end, max_tokens))
    return out


def _chunk_lines(section: str, lines: list[str], lo: int, hi: int, max_tokens: int):
    """Split a slice of [lo..hi] (1-indexed inclusive) into <= max_tokens pieces."""
    pieces: List[tuple[str, str, int, int]] = []
    cur: List[str] = []
    cur_tokens = 0
    cur_start = lo
    for idx in range(lo, hi + 1):
        line = lines[idx - 1] if 0 < idx <= len(lines) else ""
        line_tokens = count_tokens(line) + 1
        if cur and cur_tokens + line_tokens > max_tokens:
            pieces.append((section, "\n".join(cur), cur_start, idx - 1))
            cur = [line]
            cur_tokens = line_tokens
            cur_start = idx
        else:
            cur.append(line)
            cur_tokens += line_tokens
    if cur:
        pieces.append((section, "\n".join(cur), cur_start, hi))
    return pieces


def chunk_file(
    repo: str,
    path: Path,
    rel_path: str,
    max_tokens_per_chunk: int = 1024,
) -> List[Chunk]:
    name = path.name
    if path.suffix.lower() in SKIP_BIN_EXT:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    if not text.strip():
        return []

    lang = detect_language(path)
    symbols = extract_symbols(text, lang)
    base_priority = _file_priority(rel_path, name)
    pieces = _chunk_text_by_symbols(text, symbols, max_tokens_per_chunk)

    chunks: List[Chunk] = []
    for i, (section, ctext, start, end) in enumerate(pieces):
        # Nested / very small private fragments get bumped down a tier.
        prio = base_priority
        if base_priority == 1 and section.startswith("_"):
            prio = 2
        chunks.append(Chunk(
            chunk_id=f"{rel_path}#{i}",
            repo=repo,
            path=rel_path,
            section=section,
            start_line=start,
            end_line=end,
            text=ctext,
            n_tokens=count_tokens(ctext),
            priority=prio,
        ))
    return chunks


def walk_repo(
    root: str | Path,
    repo_label: str,
    max_tokens_per_chunk: int = 1024,
    follow_symlinks: bool = False,
) -> Iterable[Chunk]:
    root = Path(root).resolve()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = Path(dirpath) / fn
            try:
                rel = str(full.relative_to(root))
            except ValueError:
                continue
            yield from chunk_file(repo_label, full, rel, max_tokens_per_chunk)


def ingest_to_json(
    root: str | Path,
    out_path: str | Path,
    repo_label: Optional[str] = None,
    max_tokens_per_chunk: int = 1024,
) -> dict:
    root = Path(root).resolve()
    label = repo_label or root.name
    chunks = list(walk_repo(root, label, max_tokens_per_chunk))
    summary = {
        "repo": label,
        "root": str(root),
        "n_files": len({c.path for c in chunks}),
        "n_chunks": len(chunks),
        "total_tokens": sum(c.n_tokens for c in chunks),
        "by_priority": {
            str(p): sum(1 for c in chunks if c.priority == p)
            for p in sorted({c.priority for c in chunks})
        },
        "chunks": [asdict(c) for c in chunks],
    }
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False))
    return {k: v for k, v in summary.items() if k != "chunks"}
