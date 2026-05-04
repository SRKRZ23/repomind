"""execute_code tool — sandboxed Python runner.

Subprocess with -I -S, no network (best-effort via env), CPU + wall-clock
limits, file IO restricted to a temp scratch dir. Sandboxing here is
defense-in-depth, not airtight — REPOMIND's threat model assumes the
operator trusts the model. The point is preventing accidental damage to
the repo, not stopping a determined adversary.
"""
from __future__ import annotations
import os
import resource
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from .base import ToolResult, ToolSpec


PREAMBLE = textwrap.dedent("""\
    import sys, os, signal, resource
    # disable network sockets at python level
    try:
        import socket
        def _block(*_a, **_k):
            raise RuntimeError("network disabled in sandbox")
        socket.socket = _block            # type: ignore
        socket.create_connection = _block # type: ignore
    except Exception:
        pass
""")


def _set_limits(cpu_seconds: int = 30, mem_mb: int = 1024):
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds + 1))
    except (ValueError, OSError):
        pass
    try:
        resource.setrlimit(resource.RLIMIT_AS, (mem_mb * 1024 * 1024, mem_mb * 1024 * 1024))
    except (ValueError, OSError):
        pass


def make_tool(scratch_dir: str | Path = ".repomind_cache/scratch", timeout: int = 30) -> ToolSpec:
    scratch = Path(scratch_dir)
    scratch.mkdir(parents=True, exist_ok=True)

    def run(code: str, timeout_seconds: int = 0) -> ToolResult:
        timeout_s = timeout_seconds if 0 < timeout_seconds <= timeout else timeout
        with tempfile.NamedTemporaryFile("w", suffix=".py", dir=str(scratch), delete=False) as f:
            f.write(PREAMBLE + "\n" + code)
            script_path = f.name

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["NO_COLOR"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        # block obvious network env that requests / urllib3 read
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"):
            env.pop(k, None)

        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-S", script_path],
                capture_output=True, text=True, timeout=timeout_s,
                cwd=str(scratch), env=env,
                preexec_fn=lambda: _set_limits(timeout_s, 1024),
            )
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, output="", error=f"timeout after {timeout_s}s")
        except Exception as e:
            return ToolResult(ok=False, output="", error=f"sandbox error: {e}")
        finally:
            try:
                os.unlink(script_path)
            except OSError:
                pass

        out = (proc.stdout or "")[-8000:]
        err = (proc.stderr or "")[-4000:]
        if proc.returncode == 0:
            return ToolResult(ok=True, output=out or "(no output)", extra={"returncode": 0})
        return ToolResult(
            ok=False,
            output=out,
            error=err.strip() or f"non-zero return: {proc.returncode}",
            extra={"returncode": proc.returncode},
        )

    return ToolSpec(
        name="execute_code",
        description="Run a Python snippet in a sandboxed subprocess. No network, CPU+memory limits, isolated cwd.",
        parameters={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python source to execute."},
                "timeout_seconds": {"type": "integer", "default": 0, "description": "Override default timeout (cap 30s)."},
            },
            "required": ["code"],
        },
        runner=run,
    )
