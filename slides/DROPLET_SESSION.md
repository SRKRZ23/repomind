# Droplet Session — Extended Bench + Demo Recording

Combined session: answers Hakob's open questions (8K concurrency + AITER
test) + records the demo video. ~60-70 min wall clock, ~$2.

## 0. Pre-flight check (laptop)

- [ ] Cap installed (`/Applications/Cap.app` exists) ✅
- [ ] `~/Desktop/repomind_bench_runner.tar.gz` exists (16887 bytes, includes run_extended.sh)
- [ ] Slide PDF rendered at `slides/SLIDE_DECK.pdf`
- [ ] Browser tabs pre-arranged in order

## 1. Spin up MI300X (3 min, $0.10)

cloud.amd.com → New Droplet:
- Plan: **MI300X x1** (NOT x8)
- Image: **vLLM 0.17.1, ROCm 7.2.0** Quick Start
- Region: ATL1
- SSH key: ✅ already added
- Click Create

Wait ~3 min, note public IP.

## 2. Open port 8000 (per Steve's tutorial) (1 min)

```bash
# On laptop:
ssh root@<DROPLET-IP> 'ufw allow 8000 && curl -fsS http://localhost/health 2>&1 | head -5; echo done'
```

Verify port open from outside (later, once vLLM is up):
```bash
curl -s http://<DROPLET-IP>:8000/v1/models | head
```

## 3. Deploy scripts (1 min)

```bash
# laptop:
scp ~/Desktop/repomind_bench_runner.tar.gz root@<DROPLET-IP>:/tmp/

# droplet:
ssh root@<DROPLET-IP>
docker cp /tmp/repomind_bench_runner.tar.gz rocm:/tmp/
docker exec -it rocm /bin/bash

# inside docker:
mkdir -p /workspace/repomind && cd /workspace/repomind
git clone https://github.com/SRKRZ23/repomind.git .
tar xzf /tmp/repomind_bench_runner.tar.gz
pip install matplotlib tiktoken gitpython tree-sitter tree-sitter-languages
```

## 4. Start vLLM with default settings (3.5 min cold start)

```bash
# Terminal 1 inside docker:
vllm serve Qwen/Qwen3-Coder-Next-FP8 \
  --max-model-len 262144 \
  --kv-cache-dtype fp8 \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.92
```

Wait for `Application startup complete`. Verify:
```bash
curl -fsS http://localhost:8000/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print('max_model_len:', d['data'][0].get('max_model_len'))"
# Expect: max_model_len: 262144
```

## 5. Run extended benchmarks (8K + AITER) (~10-15 min)

### 5.a — 8K + extended concurrency (no AITER, default backend)

```bash
# Terminal 2 inside docker:
docker exec -it rocm /bin/bash
cd /workspace/repomind
nohup bash benchmarks/runner/run_extended.sh > benchmarks/results/run_extended.log 2>&1 &
echo $! > /tmp/bench_ext.pid
echo "PID: $(cat /tmp/bench_ext.pid)"
```

Monitor:
```bash
watch -n 5 'ps -p $(cat /tmp/bench_ext.pid) -o pid,etime,stat 2>/dev/null || echo DONE; echo; tail -10 benchmarks/results/run_extended.log; echo; ls -la benchmarks/results/'
```

Expected outputs in `benchmarks/results/`:
- `bench_throughput_8k_hot_extended.json` (clean 8K throughput, no cold start)
- `bench_concurrency_8k_extended.json` (4 cells: N=1, 8, 16, 31)
- `rocm_smi_extended.txt`

### 5.b (Optional) — AITER backend test

If you want to answer Hakob's "did you tune anything" with measurement:

```bash
# Stop current vLLM (Terminal 1: Ctrl+C, wait shutdown)
# Restart with AITER backend:
vllm serve Qwen/Qwen3-Coder-Next-FP8 \
  --max-model-len 262144 \
  --kv-cache-dtype fp8 \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.92 \
  --attention-backend AITER
```

Wait warm restart (~1.5 min). Then in Terminal 2:
```bash
AITER=1 bash benchmarks/runner/run_extended.sh
```

This produces `bench_concurrency_32k_aiter_compare.json` for comparison.

## 6. Record demo video with Cap (~30 min wall clock for 3-5 takes)

### 6.a — Wire local Gradio to live MI300X

On **laptop** (NOT droplet):
```bash
cd /Users/sardorrazikov1/Alish/competitions/repomind/hf_space
VLLM_BASE_URL=http://<DROPLET-IP>:8000/v1 \
MODEL_NAME=Qwen/Qwen3-Coder-Next-FP8 \
PYTHONPATH=/opt/homebrew/Cellar/certifi/2026.2.25/lib/python3.12/site-packages \
/opt/homebrew/bin/python3.12 app.py
```

Open `http://localhost:7860` — banner should show "🟢 Live AMD MI300X".

Test ingest with `pallets/flask` and ask "Where is the WSGI entry point?" — verify it works against real MI300X (TTFT ~3s at 32K).

### 6.b — Cap recording

1. Open Cap from /Applications
2. Choose "Window mode" → select Chrome window with Gradio
3. (Optional) Webcam in corner
4. Pre-arrange browser tabs:
   - Tab 1: SLIDE_DECK.pdf (full screen)
   - Tab 2: localhost:7860 (Gradio with live MI300X)
   - Tab 3: github.com/SRKRZ23/repomind (backup)
5. Press Record → follow `slides/DEMO_FLOW.md` script
6. Take 1: practice (don't keep)
7. Take 2-3: real recording
8. After recording: Cap auto-edits + zooms
9. Manual trim if needed
10. Export 1080p MP4

## 7. Pull results + DESTROY droplet (5 min)

```bash
# Inside docker container:
cd /workspace/repomind
tar czf /tmp/repomind_results_extended.tar.gz benchmarks/results/
exit  # leave container

# On droplet host:
docker cp rocm:/tmp/repomind_results_extended.tar.gz /tmp/
exit  # leave SSH

# On laptop:
scp root@<DROPLET-IP>:/tmp/repomind_results_extended.tar.gz ~/Desktop/

# CRITICAL: DESTROY droplet via cloud.amd.com UI
# 1. GPU Droplets → click your droplet
# 2. "..." / Settings → "Destroy"
# 3. Type droplet name → confirm
```

## 8. Update local docs (~30 min, free, after destroy)

After destroy, update locally:
- [ ] Extract `repomind_results_extended.tar.gz` into `benchmarks/2026-05-05-mi300x-stress-test/` (overwrite if needed) or new folder `benchmarks/2026-05-06-mi300x-extended/`
- [ ] Re-run `python3 -m benchmarks.runner.bench_plot` to refresh plots
- [ ] Update README.md with extended findings (8K cells + AITER comparison)
- [ ] Update SUMMARY.md
- [ ] Update HF Space README local
- [ ] Update slides if any number changed (re-render Marp)
- [ ] Update Hakob follow-up reply with measured 8K numbers
- [ ] Update DEMO_FLOW.md / SPEAKER_NOTES.md if needed

## 9. Post-edit demo video + final submit

- Edit Cap recording → export 1080p MP4 → upload to YouTube unlisted (or Vimeo)
- Get URL → fill in `LABLAB_STEP2_TEXT.md` → final submit
- After submit confirmation: trigger build-in-public posts wave per `POSTS_DRAFTS.md`
- Big push to GitHub + HF Spaces (one coherent commit)

## Cost discipline

- Phone alarm: 60 min from droplet creation
- Total budget for this session: $2.50
- If Cap crashes during recording: don't spin droplet again unless absolutely needed; we have benchmark data already, can use mock backend for re-take with voiceover
- After destroy: $0 billing, plenty of credits left for any follow-up

## Backup plan if MI300X capacity issue

If AMD Cloud says "out of GPUs":
- Try ATL1 first, then other regions if available
- Worst case: record demo with mock backend, voice over verified numbers from existing evidence pack
- We already have everything needed for submission — droplet is for demo video only
