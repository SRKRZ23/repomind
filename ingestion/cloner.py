"""Clone a git repository into a local cache directory.

Uses GitPython if installed, falls back to shelling out to `git`. Always
shallow-clones (depth=1) by default — for retrieval we don't need history,
and shallow makes the Linux kernel ingest in seconds instead of minutes.
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


URL_RE = re.compile(r"^(https?://|git@)([\w./:-]+?)(\.git)?/?$")


@dataclass
class CloneResult:
    url: str
    local_path: Path
    sha: str
    cached: bool


def normalize_url(url_or_path: str) -> str:
    """Accept https://, git@, owner/repo, or a local path."""
    s = url_or_path.strip()
    if os.path.isdir(s):
        return os.path.abspath(s)
    if s.startswith("git@") or s.startswith("http"):
        return s
    if "/" in s and not s.startswith("/"):
        # owner/repo shorthand -> github
        return f"https://github.com/{s}.git"
    return s


def slugify(url: str) -> str:
    """Stable filesystem-friendly slug from a URL."""
    if os.path.isdir(url):
        return Path(url).name
    m = URL_RE.match(url)
    if not m:
        return re.sub(r"[^a-zA-Z0-9._-]+", "_", url)
    body = m.group(2)
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", body)


def _git(*args: str, cwd: Optional[Path] = None) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def clone(
    url_or_path: str,
    cache_dir: str | Path = ".repomind_cache/repos",
    depth: int = 1,
    force: bool = False,
) -> CloneResult:
    """Clone url to cache_dir/<slug>. If local path is given, just return it."""
    url = normalize_url(url_or_path)
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Local-path mode — no clone, just record the SHA if it's a git repo.
    if os.path.isdir(url):
        local = Path(url)
        try:
            sha = _git("rev-parse", "HEAD", cwd=local)
        except Exception:
            sha = "no-git"
        return CloneResult(url=str(local), local_path=local, sha=sha, cached=True)

    target = cache_dir / slugify(url)
    if target.exists() and not force:
        try:
            sha = _git("rev-parse", "HEAD", cwd=target)
            return CloneResult(url=url, local_path=target, sha=sha, cached=True)
        except Exception:
            shutil.rmtree(target, ignore_errors=True)

    if target.exists() and force:
        shutil.rmtree(target, ignore_errors=True)

    args = ["clone", "--filter=blob:none"]
    if depth > 0:
        args += ["--depth", str(depth)]
    args += [url, str(target)]
    _git(*args)
    sha = _git("rev-parse", "HEAD", cwd=target)
    return CloneResult(url=url, local_path=target, sha=sha, cached=False)
