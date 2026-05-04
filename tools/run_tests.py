"""run_tests tool — pytest invocation inside the ingested repo (read-only)."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

from .base import ToolResult, ToolSpec


def make_tool(repo_root: str | Path, timeout: int = 120) -> ToolSpec:
    root = Path(repo_root).resolve()

    def run(test_path: str = "", k_expression: str = "", max_lines: int = 200) -> ToolResult:
        target = (root / test_path).resolve() if test_path else root
        try:
            target.relative_to(root)
        except ValueError:
            return ToolResult(ok=False, output="", error=f"path outside repo: {test_path}")

        cmd = [sys.executable, "-m", "pytest", "-x", "--tb=short", "-q", str(target)]
        if k_expression:
            cmd += ["-k", k_expression]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(root), timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, output="", error=f"pytest timeout after {timeout}s")
        except FileNotFoundError:
            return ToolResult(ok=False, output="", error="pytest not installed")

        lines = (proc.stdout or "").splitlines()[-max_lines:]
        out = "\n".join(lines)
        err = (proc.stderr or "").strip()
        if proc.returncode == 0:
            return ToolResult(ok=True, output=out or "(all passed)", extra={"returncode": 0})
        return ToolResult(
            ok=False, output=out, error=err or f"pytest exit {proc.returncode}",
            extra={"returncode": proc.returncode},
        )

    return ToolSpec(
        name="run_tests",
        description="Run pytest on the ingested repo (or a sub-path). Read-only.",
        parameters={
            "type": "object",
            "properties": {
                "test_path": {"type": "string", "default": ""},
                "k_expression": {"type": "string", "default": "", "description": "pytest -k expression"},
                "max_lines": {"type": "integer", "default": 200},
            },
        },
        runner=run,
    )
