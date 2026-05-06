#!/usr/bin/env bash
# REPOMIND extended benchmarks — comprehensive answer to Hakob's
# AMD Developer Community thread questions:
#
#   Q1. "30 tok/s at 8K feels slow for 80B MoE — did you try tweaking
#       any vLLM settings to get that higher?"
#       → measure HOT throughput at 8K and 32K (no cold-start outlier)
#       → second pass with --attention-backend AITER for direct comparison
#
#   Q2. "What does concurrency look like at 8K-32K, where most users
#       actually live?"
#       → 4 context points in range: 8K, 16K, 32K (already), 64K
#         each at N=1, 8, 16, 31 — fills the realistic-use sweep
#
# Usage on the droplet (after `bash run_all.sh` from session 1):
#
#   PHASE 1 — default backend (vLLM serve with no --attention-backend flag):
#     bash benchmarks/runner/run_extended.sh
#
#   PHASE 2 — AITER backend (must restart vLLM with --attention-backend AITER):
#     AITER=1 bash benchmarks/runner/run_extended.sh
#
# Outputs: bench_*_extended.json and bench_*_aiter.json — separate files
# so we can compare. Total expected wall clock for full PHASE 1: ~12-15 min.
# Total cost: ~$0.50 per phase.
set -euo pipefail

cd "$(dirname "$0")/../.."

BASE_URL="${REPOMIND_BENCH_BASE_URL:-http://localhost:8000/v1}"
MODEL="${REPOMIND_BENCH_MODEL:-Qwen/Qwen3-Coder-Next-FP8}"
OUT_DIR="${REPOMIND_BENCH_OUT:-benchmarks/results}"

if [ -n "${AITER:-}" ]; then
    SUFFIX="aiter"
    echo "[runner] PHASE 2 — AITER mode. Assumes vllm serve was restarted with --attention-backend AITER."
else
    SUFFIX="extended"
    echo "[runner] PHASE 1 — default attention backend."
fi

mkdir -p "$OUT_DIR"

echo "[runner] base_url=$BASE_URL model=$MODEL suffix=$SUFFIX"
echo "[runner] sanity-checking endpoint…"
curl -fsS "$BASE_URL/models" -H "Authorization: Bearer EMPTY" \
    | python3 -c "import json, sys; d=json.load(sys.stdin); ids=[m.get('id') for m in d.get('data', [])]; print('[runner] models served:', ids)"

# ============================================================================
# Throughput sweeps — answers Q1 (vLLM speed)
# Hot measurements (no cold start) at sizes that matter for "real use"
# ============================================================================
echo "[runner] === bench 1/3: hot throughput sweep at 8K + 32K + 64K ==="
REPOMIND_BENCH_OUT="$OUT_DIR/_tmp" python3 -m benchmarks.runner.bench_throughput \
    --base-url "$BASE_URL" --model "$MODEL" \
    --max-tokens 64 \
    --lengths "8192,32768,65536"
mv "$OUT_DIR/_tmp/bench_throughput.json" "$OUT_DIR/bench_throughput_hot_${SUFFIX}.json"
rm -rf "$OUT_DIR/_tmp"

# ============================================================================
# Concurrency sweep — answers Q2 (concurrency at 8K-32K range)
# Adds 8K, 16K, 64K to existing 32K/128K/256K data from session 1
# ============================================================================
echo "[runner] === bench 2/3: concurrency stress at 8K + 16K + 64K ==="
REPOMIND_BENCH_OUT="$OUT_DIR/_tmp" python3 -m benchmarks.runner.bench_concurrency \
    --base-url "$BASE_URL" --model "$MODEL" \
    --max-tokens 64 \
    --contexts "8192,16384,65536" \
    --concurrency "1,8,16,31" \
    --timeout 600
mv "$OUT_DIR/_tmp/bench_concurrency.json" "$OUT_DIR/bench_concurrency_realistic_${SUFFIX}.json"
rm -rf "$OUT_DIR/_tmp"

# ============================================================================
# 32K AITER comparison — only when AITER=1 (PHASE 2)
# Re-runs 32K cells at N=1, 8 to compare against PHASE 1 baseline
# ============================================================================
if [ -n "${AITER:-}" ]; then
    echo "[runner] === bench 3/3: AITER vs default at 32K (N=1, 8, 16) ==="
    REPOMIND_BENCH_OUT="$OUT_DIR/_tmp" python3 -m benchmarks.runner.bench_concurrency \
        --base-url "$BASE_URL" --model "$MODEL" \
        --max-tokens 64 \
        --contexts "32768" \
        --concurrency "1,8,16" \
        --timeout 600
    mv "$OUT_DIR/_tmp/bench_concurrency.json" "$OUT_DIR/bench_concurrency_32k_aiter_compare.json"
    rm -rf "$OUT_DIR/_tmp"
fi

# ============================================================================
# Final GPU snapshot
# ============================================================================
echo "[runner] === final rocm-smi snapshot ==="
if command -v rocm-smi >/dev/null 2>&1; then
    rocm-smi > "$OUT_DIR/rocm_smi_${SUFFIX}.txt" || true
    rocm-smi --showmeminfo vram >> "$OUT_DIR/rocm_smi_${SUFFIX}.txt" || true
fi

echo
echo "[runner] DONE. Files added:"
ls -la "$OUT_DIR/" | grep -E "(${SUFFIX}|aiter_compare)" || ls -la "$OUT_DIR/"

cat <<HINT

Next step:

  PHASE 1 done? Now do PHASE 2 — AITER comparison:
    1. In Terminal 1, Ctrl+C to stop current vLLM
    2. Restart with: vllm serve Qwen/Qwen3-Coder-Next-FP8 \\
         --max-model-len 262144 --kv-cache-dtype fp8 \\
         --port 8000 --host 0.0.0.0 \\
         --gpu-memory-utilization 0.92 \\
         --attention-backend AITER
    3. Wait ~1.5 min for warm restart
    4. In Terminal 2: AITER=1 bash benchmarks/runner/run_extended.sh

  Or skip PHASE 2 if you'd rather move to demo recording — PHASE 1 alone
  fully answers Hakob's Q2 (concurrency at 8K-64K). PHASE 2 is the bonus
  data point for Q1 (vLLM tuning).
HINT
