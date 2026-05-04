"""Gradio UI scaffold.

The UI is intentionally tiny — paste a path or URL, ingest, ask a question,
see streaming answer + sources. Gets fancier once the LLM backend exists.

Run:
    python -m ui.app
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingestion.chunker import ingest_to_json
from ingestion.cloner import clone


REPO_CACHE: dict = {"summary": None, "summary_path": None}
DEFAULT_INGEST_OUT = Path(".repomind_cache/ui/active.json")


def ingest(url_or_path: str, max_tokens: int) -> str:
    if not url_or_path.strip():
        return "Provide a URL or local path."
    out = DEFAULT_INGEST_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    if Path(url_or_path).is_dir():
        repo_root = Path(url_or_path)
        label = repo_root.name
    else:
        res = clone(url_or_path)
        repo_root = res.local_path
        label = res.url.split("/")[-1].removesuffix(".git")
    summary = ingest_to_json(repo_root, out, repo_label=label, max_tokens_per_chunk=max_tokens)
    REPO_CACHE["summary_path"] = str(out)
    return json.dumps(summary, indent=2)


def ask(question: str, backend: str, base_url: str) -> Tuple[str, str]:
    if not REPO_CACHE.get("summary_path"):
        return "Ingest a repo first.", ""
    if not question.strip():
        return "Type a question.", ""

    from agent.loop import Agent
    from tools.registry import default_registry

    summary_path = Path(REPO_CACHE["summary_path"])
    summary = json.loads(summary_path.read_text())
    root = Path(summary.get("root", "."))

    if backend == "vllm":
        from serving.vllm_client import VLLMClient
        llm = VLLMClient(base_url=base_url)
    else:
        from serving.mock_client import MockClient
        llm = MockClient()

    agent = Agent(llm=llm, tools=default_registry(root), max_steps=6)
    result = agent.run(question, summary)
    tool_log = "\n".join(f"- {tc['name']} {tc['arguments']}" for tc in result.tool_calls)
    return result.answer, tool_log


def build_ui():
    try:
        import gradio as gr
    except ImportError:
        raise SystemExit("pip install gradio")

    with gr.Blocks(title="REPOMIND — repo-scale coding agent on AMD MI300X") as demo:
        gr.Markdown(
            "# REPOMIND\n"
            "Open-source repo-scale coding agent. Ingest any git repository, "
            "ask any question, watch the agent reason and use tools."
        )
        with gr.Row():
            url = gr.Textbox(label="Git URL or local path", placeholder="https://github.com/torvalds/linux", scale=4)
            chunk_tokens = gr.Slider(256, 4096, 1024, step=128, label="Tokens / chunk", scale=1)
            ingest_btn = gr.Button("Ingest", variant="primary", scale=1)
        ingest_out = gr.Code(label="Ingestion summary", language="json")

        with gr.Row():
            backend = gr.Radio(["mock", "vllm"], value="mock", label="Backend", scale=1)
            base_url = gr.Textbox(value="http://localhost:8000/v1", label="vLLM base URL", scale=2)
        question = gr.Textbox(label="Question", placeholder="Where does authentication happen in this repo?", lines=3)
        ask_btn = gr.Button("Ask", variant="primary")
        answer = gr.Markdown(label="Answer")
        tool_trace = gr.Code(label="Tool trace")

        ingest_btn.click(ingest, [url, chunk_tokens], ingest_out)
        ask_btn.click(ask, [question, backend, base_url], [answer, tool_trace])

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
