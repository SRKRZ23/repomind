"""End-to-end ingest CLI.

Examples:
    python -m scripts.ingest --url https://github.com/torvalds/linux --out cache/linux.json
    python -m scripts.ingest --path . --out cache/self.json
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingestion.cloner import clone
from ingestion.chunker import ingest_to_json


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="Git URL or owner/repo shorthand")
    g.add_argument("--path", help="Local repo path (no clone)")
    ap.add_argument("--out", required=True, help="Output JSON path")
    ap.add_argument("--cache-dir", default=".repomind_cache/repos")
    ap.add_argument("--depth", type=int, default=1, help="git clone --depth (0 = full history)")
    ap.add_argument("--chunk-tokens", type=int, default=1024)
    ap.add_argument("--label", default=None)
    args = ap.parse_args()

    if args.url:
        res = clone(args.url, cache_dir=args.cache_dir, depth=args.depth)
        repo_root = res.local_path
        label = args.label or res.url.split("/")[-1].removesuffix(".git")
    else:
        repo_root = Path(args.path)
        label = args.label or repo_root.name

    summary = ingest_to_json(repo_root, args.out, repo_label=label, max_tokens_per_chunk=args.chunk_tokens)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
