"""read_file tool — read a slice of a file inside the ingested repo root."""
from __future__ import annotations
from pathlib import Path

from .base import ToolResult, ToolSpec


def make_tool(repo_root: str | Path, max_bytes: int = 200_000) -> ToolSpec:
    root = Path(repo_root).resolve()

    def run(path: str, start_line: int = 1, end_line: int = -1) -> ToolResult:
        # security: only allow paths inside the ingested root
        target = (root / path).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            return ToolResult(ok=False, output="", error=f"path outside repo: {path}")
        if not target.exists():
            return ToolResult(ok=False, output="", error=f"not found: {path}")
        try:
            text = target.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return ToolResult(ok=False, output="", error=str(e))
        if len(text) > max_bytes:
            text = text[:max_bytes] + f"\n[... truncated at {max_bytes} bytes]"
        lines = text.split("\n")
        start = max(1, start_line)
        end = len(lines) if end_line in (-1, 0) else min(len(lines), end_line)
        slice_text = "\n".join(lines[start - 1:end])
        numbered = "\n".join(f"{i:>5}  {l}" for i, l in enumerate(lines[start - 1:end], start=start))
        return ToolResult(
            ok=True,
            output=numbered,
            extra={"path": path, "lines": (start, end), "total_lines": len(lines)},
        )

    return ToolSpec(
        name="read_file",
        description="Read a file from the ingested repo. Optionally restrict to a line range.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path relative to repo root."},
                "start_line": {"type": "integer", "description": "1-indexed inclusive start.", "default": 1},
                "end_line": {"type": "integer", "description": "1-indexed inclusive end. -1 = end of file.", "default": -1},
            },
            "required": ["path"],
        },
        runner=run,
    )
