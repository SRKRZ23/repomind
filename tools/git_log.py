"""git_log tool — read-only commit history queries."""
from __future__ import annotations
import subprocess
from pathlib import Path

from .base import ToolResult, ToolSpec


def make_tool(repo_root: str | Path, max_commits: int = 50) -> ToolSpec:
    root = Path(repo_root).resolve()

    def run(path: str = "", limit: int = 20, since: str = "") -> ToolResult:
        if not (root / ".git").exists():
            return ToolResult(ok=False, output="", error="not a git repository")
        n = max(1, min(limit, max_commits))
        cmd = ["git", "log", f"-n{n}", "--pretty=format:%h|%an|%ai|%s"]
        if since:
            cmd += [f"--since={since}"]
        if path:
            cmd += ["--", path]
        try:
            proc = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, output="", error="git log timeout")
        if proc.returncode != 0:
            return ToolResult(ok=False, output="", error=proc.stderr.strip())
        rows = [_format_row(line) for line in proc.stdout.splitlines() if line]
        return ToolResult(ok=True, output="\n".join(rows), extra={"commits": len(rows)})

    return ToolSpec(
        name="git_log",
        description="Read commit history. Optionally filter by path or --since.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": ""},
                "limit": {"type": "integer", "default": 20},
                "since": {"type": "string", "default": "", "description": "git --since (e.g. '2 weeks ago')"},
            },
        },
        runner=run,
    )


def _format_row(line: str) -> str:
    parts = line.split("|", 3)
    if len(parts) != 4:
        return line
    sha, author, date, subject = parts
    return f"{sha[:9]}  {date[:10]}  {author[:24]:<24}  {subject}"
