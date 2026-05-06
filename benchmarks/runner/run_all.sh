#!/usr/bin/env bash
# REPOMIND benchmark suite — run on the MI300X droplet *after* `vllm serve`
# is up at http://localhost:8000.
#
# Usage (from the repomind/ checkout root, on the droplet):
#   bash benchmarks/runner/run_all.sh
#
# Optional environment overrides:
#   REPOMIND_BENCH_BASE_URL    OpenAI-compatible endpoint (default localhost:8000/v1)
#   REPOMIND_BENCH_MODEL       served model name
#   REPOMIND_BENCH_OUT         output dir (default benchmarks/results)
#   SKIP_E2E=1                 skip the end-to-end repo ingestion bench
#   SKIP_COST=1                skip cost analysis
#
# Total cost on AMD Cloud: ~3 hours of MI300X x1 ≈ $6 at $1.99/hr.
set -euo pipefail

cd "$(dirname "$0")/../.."

BASE_URL="${REPOMIND_BENCH_BASE_URL:-http://localhost:8000/v1}"
MODEL="${REPOMIND_BENCH_MODEL:-Qwen/Qwen3-Coder-Next-FP8}"
OUT_DIR="${REPOMIND_BENCH_OUT:-benchmarks/results}"

mkdir -p "$OUT_DIR"

echo "[runner] base_url=$BASE_URL model=$MODEL out=$OUT_DIR"
echo "[runner] sanity-checking endpoint…"
curl -fsS "$BASE_URL/models" -H "Authorization: Bearer EMPTY" \
    | python3 -c "import json, sys; d=json.load(sys.stdin); ids=[m.get('id') for m in d.get('data', [])]; print('[runner] models served:', ids)"

# 1. Throughput sweep (single user, multiple context lengths)
echo "[runner] === bench 1/5: throughput sweep ==="
python3 -m benchmarks.runner.bench_throughput \
    --base-url "$BASE_URL" --model "$MODEL" \
    --max-tokens 64

# 2. Concurrency stress
echo "[runner] === bench 2/5: concurrency stress ==="
python3 -m benchmarks.runner.bench_concurrency \
    --base-url "$BASE_URL" --model "$MODEL" \
    --max-tokens 64 \
    --contexts "32768,131072,258048" \
    --concurrency "1,8,16,31"

# 3. Long-context coherence (needle in haystack at ~200K)
echo "[runner] === bench 3/5: long-context needle ==="
python3 -m benchmarks.runner.bench_long_context \
    --base-url "$BASE_URL" --model "$MODEL" \
    --target-tokens 200000 \
    --positions "early,middle,late" \
    --max-tokens 128

# 4. End-to-end repo ingestion (real demo material)
if [ -z "${SKIP_E2E:-}" ]; then
    echo "[runner] === bench 4/5: end-to-end repo ingestion ==="
    python3 -m benchmarks.runner.bench_e2e \
        --base-url "$BASE_URL" --model "$MODEL" \
        --max-tokens 512 \
        --target-context 180000 \
        --tiers "small_repomind,medium_flask,large_pytorch_vision"
else
    echo "[runner] SKIP_E2E=1 — skipping end-to-end bench"
fi

# 5. Cost analysis (no GPU; consumes the JSON from above)
if [ -z "${SKIP_COST:-}" ]; then
    echo "[runner] === bench 5/5: cost analysis ==="
    python3 -m benchmarks.runner.bench_cost
else
    echo "[runner] SKIP_COST=1 — skipping cost analysis"
fi

# 6. Final snapshot of GPU state
echo "[runner] === final rocm-smi snapshot ==="
if command -v rocm-smi >/dev/null 2>&1; then
    rocm-smi > "$OUT_DIR/rocm_smi_final.txt" || true
    rocm-smi --showmeminfo vram >> "$OUT_DIR/rocm_smi_final.txt" || true
fi

echo "[runner] done. results in $OUT_DIR/"
ls -la "$OUT_DIR/"
