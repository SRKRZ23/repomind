"""grep_codebase tool — ripgrep-style search inside the ingested repo.

Uses Python's `re` so we don't depend on rg being installed; that lets the
tool run identically in tests, in the local sandbox, and on AMD Cloud.
"""
from __future__ import annotations
import os
import re
from pathlib import Path
from typing import List

from .base import ToolResult, ToolSpec


SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "target", "build", "dist"}


def make_tool(
    repo_root: str | Path,
    max_matches: int = 200,
    max_file_size: int = 2_000_000,
) -> ToolSpec:
    root = Path(repo_root).resolve()

    def run(pattern: str, path: str = "", case_sensitive: bool = False, max_results: int = 50) -> ToolResult:
        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            rx = re.compile(pattern, flags)
        except re.error as e:
            return ToolResult(ok=False, output="", error=f"invalid regex: {e}")

        scope = (root / path).resolve() if path else root
        try:
            scope.relative_to(root)
        except ValueError:
            return ToolResult(ok=False, output="", error=f"path outside repo: {path}")
        if not scope.exists():
            return ToolResult(ok=False, output="", error=f"not found: {path}")

        hits: List[str] = []
        n = 0
        cap = min(max_results, max_matches)

        def consider(filepath: Path):
            nonlocal n
            if n >= cap:
                return
            try:
                if filepath.stat().st_size > max_file_size:
                    return
            except OSError:
                return
            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                return
            for ln, line in enumerate(text.split("\n"), start=1):
                if rx.search(line):
                    rel = str(filepath.relative_to(root))
                    hits.append(f"{rel}:{ln}: {line.rstrip()}")
                    n += 1
                    if n >= cap:
                        return

        if scope.is_file():
            consider(scope)
        else:
            for dirpath, dirnames, filenames in os.walk(scope):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for fn in filenames:
                    consider(Path(dirpath) / fn)
                    if n >= cap:
                        break
                if n >= cap:
                    break

        if not hits:
            return ToolResult(ok=True, output="(no matches)", extra={"matches": 0})
        return ToolResult(ok=True, output="\n".join(hits), extra={"matches": n, "capped": n >= cap})

    return ToolSpec(
        name="grep_codebase",
        description="Search regular expression across files in the ingested repo. Returns path:line:match.",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "path": {"type": "string", "description": "Limit search to this subpath. Empty = whole repo.", "default": ""},
                "case_sensitive": {"type": "boolean", "default": False},
                "max_results": {"type": "integer", "default": 50},
            },
            "required": ["pattern"],
        },
        runner=run,
    )
