"""Run a single question through the agent.

Examples:
    python -m scripts.ask_agent --question "what does chunker do?" \\
                                  --repo cache/self.json --backend mock

    python -m scripts.ask_agent --question "explain mm/slab.c" \\
                                  --repo cache/linux.json --backend vllm \\
                                  --base-url http://localhost:8000/v1
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.loop import Agent
from tools.registry import default_registry


def make_llm(backend: str, base_url: str, model: str):
    if backend == "mock":
        from serving.mock_client import MockClient
        return MockClient()
    if backend == "vllm":
        from serving.vllm_client import VLLMClient
        return VLLMClient(base_url=base_url, model=model)
    raise SystemExit(f"unknown backend: {backend}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--repo", required=True, help="Path to ingested JSON summary")
    ap.add_argument("--backend", choices=["mock", "vllm"], default="mock")
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--model", default="Qwen/Qwen3-Coder-Next-FP8")
    ap.add_argument("--max-steps", type=int, default=6)
    args = ap.parse_args()

    repo_summary = json.loads(Path(args.repo).read_text())
    repo_root = Path(repo_summary.get("root", ".")).resolve()

    tools = default_registry(repo_root)
    llm = make_llm(args.backend, args.base_url, args.model)
    agent = Agent(llm=llm, tools=tools, max_steps=args.max_steps)

    result = agent.run(args.question, repo_summary)
    print("=" * 60)
    print("ANSWER:")
    print(result.answer)
    print("=" * 60)
    print(f"steps={result.steps}  finished={result.finished}  tool_calls={len(result.tool_calls)}")


if __name__ == "__main__":
    main()
