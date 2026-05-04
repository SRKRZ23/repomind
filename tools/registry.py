"""Build the default tool registry for a given repo root."""
from __future__ import annotations
from pathlib import Path

from .base import ToolRegistry
from .execute_code import make_tool as make_execute
from .git_log import make_tool as make_git_log
from .grep import make_tool as make_grep
from .read_file import make_tool as make_read_file
from .run_tests import make_tool as make_run_tests


def default_registry(repo_root: str | Path, scratch_dir: str | Path = ".repomind_cache/scratch") -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(make_read_file(repo_root))
    reg.register(make_grep(repo_root))
    reg.register(make_execute(scratch_dir))
    reg.register(make_run_tests(repo_root))
    reg.register(make_git_log(repo_root))
    return reg
