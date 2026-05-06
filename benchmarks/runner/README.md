# REPOMIND benchmark suite — runner

What's in this folder:

| File | What it does | Where it runs |
| --- | --- | --- |
| `_common.py` | Token counting, prompt construction, HTTP call helpers | both |
| `_stub_server.py` | Tiny OpenAI-compatible stub for local validation only | laptop |
| `bench_throughput.py` | tok/s + TTFT vs context length (single user) | droplet |
| `bench_concurrency.py` | latency + aggregate tok/s for N parallel users | droplet |
| `bench_long_context.py` | needle-in-haystack at 200K context (early/middle/late) | droplet |
| `bench_e2e.py` | clone + chunk + ask 3 questions on 3 real repos | droplet |
| `bench_cost.py` | cost-per-query + Cursor break-even from above results | anywhere |
| `bench_plot.py` | matplotlib PNGs for slides | anywhere |
| `run_all.sh` | runs the four GPU benches + cost in order | droplet |

## Running on the MI300X droplet

```bash
# 1. SSH into the droplet, attach to the rocm container with vllm running.
docker exec -it rocm /bin/bash

# 2. Inside the container, the repomind checkout should be at /workspace.
cd /workspace
git pull origin main          # ensure benchmark scripts are present

# 3. (One-time) install matplotlib — already pulled in by requirements.txt.
pip install matplotlib

# 4. With `vllm serve` already running on http://localhost:8000, fire the runner.
bash benchmarks/runner/run_all.sh
```

The runner:
1. Sanity-checks `/v1/models`
2. Runs throughput sweep — ~5 min
3. Runs concurrency stress (3 contexts × 4 concurrency levels) — ~30 min
4. Runs long-context needle test (3 positions at 200K) — ~10 min
5. Runs E2E repo ingestion (3 repos, 9 questions) — ~25 min
6. Runs cost analysis (no GPU, ~1 sec)
7. Snapshots `rocm-smi` to `benchmarks/results/rocm_smi_final.txt`

Total wall clock: ~70 minutes on a single MI300X.
Total cost at $1.99/hr: **~$2.50**.

## Pulling results back to laptop

From the droplet:
```bash
tar czf /tmp/repomind_bench_results.tar.gz benchmarks/results/
```
From the laptop:
```bash
scp root@<droplet-ip>:/tmp/repomind_bench_results.tar.gz ~/Desktop/
```

## Generating slide-ready plots

```bash
python3 -m benchmarks.runner.bench_plot
# Writes plot_throughput.png, plot_concurrency.png, plot_cost.png
# into benchmarks/results/
```

## Outputs to expect

```
benchmarks/results/
├── bench_throughput.json      # tok/s curve
├── bench_concurrency.json     # parallel-user latency matrix
├── bench_long_context.json    # needle pass/fail at 200K
├── bench_cost.json            # $/1M tokens, dev/MI300X, savings
├── e2e/
│   ├── small_repomind.json    # ingest summary
│   ├── small_repomind_prompt.txt   # exact prompt sent to vLLM
│   ├── small_repomind_<N>_q1.txt  # answer dump per question
│   └── ...
├── rocm_smi_final.txt
├── plot_throughput.png         # 1280x720, dark theme
├── plot_concurrency.png
└── plot_cost.png
```

These four JSONs + three PNGs are the entire evidence pack for the verified
business case. They feed straight into the README "Verified benchmarks"
table, the demo video, and the slide deck.

## Local smoke test (no GPU)

```bash
python3 benchmarks/runner/_stub_server.py 8000 &
REPOMIND_BENCH_BASE_URL=http://127.0.0.1:8000/v1 \
REPOMIND_BENCH_OUT=/tmp/repomind_bench_smoke \
  python3 -m benchmarks.runner.bench_throughput --lengths 1024,4096 --max-tokens 16
kill %1
```

This validates the HTTP path without burning GPU credits.
