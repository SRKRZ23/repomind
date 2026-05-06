"""Tiny OpenAI-compatible stub for local benchmark validation.

NOT used on the MI300X. Only for smoke-testing the runner scripts on a laptop
without a GPU. Returns a deterministic completion and a fake token usage block.

Run:
    python3 benchmarks/runner/_stub_server.py 8000 &
    REPOMIND_BENCH_BASE_URL=http://localhost:8000/v1 python3 -m benchmarks.runner.bench_throughput
"""
from __future__ import annotations
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


CANNED_TEXT = "calc_repomind_token_budget_v7 — magic constant 4242"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}

    def do_GET(self):
        if self.path.endswith("/models"):
            body = json.dumps({
                "data": [{"id": "Qwen/Qwen3-Coder-Next-FP8",
                          "max_model_len": 262144}]
            }).encode("utf-8")
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body))); self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        req = self._read_json()
        msgs = req.get("messages") or []
        prompt_chars = sum(len(m.get("content") or "") for m in msgs)
        prompt_tokens = max(1, prompt_chars // 4)
        completion_tokens = min(req.get("max_tokens") or 64, 64)
        is_stream = bool(req.get("stream"))

        # Simulate latency proportional to prompt size
        time.sleep(0.001 + prompt_tokens / 200_000.0)

        if not is_stream:
            body = json.dumps({
                "id": "stub-1",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": CANNED_TEXT},
                    "finish_reason": "stop",
                }],
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                },
            }).encode("utf-8")
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body))); self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        for tok in CANNED_TEXT.split():
            chunk = json.dumps({"choices": [{"delta": {"content": tok + " "}, "index": 0}]})
            self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
            self.wfile.flush()
            time.sleep(0.005)
        self.wfile.write(b"data: [DONE]\n\n")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"[stub] listening on http://127.0.0.1:{port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
