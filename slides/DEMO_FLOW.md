# REPOMIND — Demo Recording Flow (Cap)

Exact sequence of actions during screen recording. Practice once with mock,
then record once with live MI300X. Total target: 3 minutes 50 seconds
(now 11 slides including AITER tuning slide).

## Pre-recording checklist

- [ ] Cap installed: `brew install --cask cap` or download from cap.so
- [ ] MI300X x1 droplet up, vLLM serving (`Application startup complete`)
- [ ] **CRITICAL**: vLLM serving with **default Triton attention backend**
      (NOT `--attention-backend ROCM_AITER_FA`). If your droplet was used
      for PHASE 2 AITER benchmarks, you MUST restart vLLM without the
      `--attention-backend` flag, otherwise the live demo will produce
      `!!!!!!!!` instead of real answers. See "AITER → default rollback"
      section below.
- [ ] `ufw allow 8000` on droplet (open public port for HF Space → MI300X)
- [ ] `curl http://<droplet-ip>:8000/v1/models` returns `max_model_len: 262144`
- [ ] Smoke test the live backend produces real text, not `!!!!!`:
  ```bash
  curl -s http://<droplet-ip>:8000/v1/chat/completions \
    -H "Authorization: Bearer EMPTY" -H "Content-Type: application/json" \
    -d '{"model":"Qwen/Qwen3-Coder-Next-FP8","messages":[{"role":"user","content":"Say hello in 5 words"}],"max_tokens":32}' \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
  ```
  Expect: a real English greeting. If you see `!!!!`-style output, vLLM
  is still on AITER — restart it.
- [ ] Local Gradio launched with env vars set:
  ```bash
  cd hf_space/
  VLLM_BASE_URL=http://<droplet-ip>:8000/v1 \
  MODEL_NAME=Qwen/Qwen3-Coder-Next-FP8 \
  python3 app.py
  ```
- [ ] Browser opens to `http://localhost:7860`
- [ ] PDF slides open in another tab (for B-roll if needed)
- [ ] Quiet room, USB mic ideally, MacBook mic OK if quiet
- [ ] Webcam: optional PiP for intro/outro
- [ ] Cap auto-zoom + smooth animations enabled

## AITER → default Triton rollback (only if needed)

If vLLM in your docker container was started with `--attention-backend ROCM_AITER_FA`,
restart it cleanly:

```bash
# inside the rocm docker container:
ps aux | grep vllm | grep -v grep | awk '{print $2}' | xargs -r kill -INT
sleep 5  # wait for clean shutdown
nohup vllm serve Qwen/Qwen3-Coder-Next-FP8 \
  --max-model-len 262144 \
  --kv-cache-dtype fp8 \
  --port 8000 --host 0.0.0.0 \
  --gpu-memory-utilization 0.92 \
  > /tmp/vllm_default.log 2>&1 &
disown
# wait ~1.5 min for warm restart, then test:
sleep 90 && curl -fsS http://localhost:8000/v1/models | python3 -c \
  "import sys,json; print('max_model_len:', json.load(sys.stdin)['data'][0].get('max_model_len'))"
```

Expect `max_model_len: 262144` and real prose in the smoke-test curl
above. Only then proceed to recording.

## Recording sequence (3:50 target — 11 slides + live demo)

### 0:00 - 0:20 — Intro slate (slide 1)
- **Visual**: Title slide of SLIDE_DECK.pdf (full screen)
- **Voice**: "I'm Sardor Razikov, solo from Tashkent. I built REPOMIND — an open-source repo-scale coding agent that runs on a single AMD MI300X."
- **Cap action**: zoom on title

### 0:20 - 0:50 — The problem + architectural moat (slides 2-3)
- **Visual**: Slide 2 (closed agents table) → Slide 3 (VRAM math)
- **Voice**: "Banks can't use Cursor. Defense can't. Pharma can't. Why MI300X specifically? Qwen3-Coder-Next-FP8 weights 80 GB plus 256K KV cache 38 GB plus activations equals 143 GB total. H100 caps at 80. MI300X 192 has the headroom."
- **Cap action**: highlight "143 GB" and "192 GB" with auto-zoom

### 0:50 - 1:10 — Verified evidence (slide 4)
- **Visual**: Slide 4 verification table
- **Voice**: "We ran 124 minutes of stress testing across two sessions on real MI300X hardware. Weights 77.29 gibibytes, KV cache 94.58 gibibytes, peak 92 percent of the 192 gigs. The vLLM API confirms 256K context. Cold start three and a half minutes. Total cost across both sessions: $4.12."
- **Cap action**: zoom on each verified value sequentially

### 1:10 - 1:30 — Throughput + concurrency (slides 5-6)
- **Visual**: Slide 5 (throughput plot) → Slide 6 (24-cell concurrency table)
- **Voice**: "Throughput across six contexts, all hot measurements. 31 of 31 concurrent users succeed at every context from 8K through 64K under default Triton."
- **Cap action**: highlight 31/31 row across 4 contexts

### 1:30 - 1:55 — Tuning attempt (slide 7, NEW)
- **Visual**: Slide 7 (AITER A/B table)
- **Voice**: "Hakob from the AMD forum asked if we tried any vLLM tuning. We did — measured the AITER attention backend. Throughput 2 to 4 times higher, but output degenerates to repeating punctuation tokens in the FP8 KV cache configuration. 137 of 144 cells produce gibberish. Default Triton stays our production-safe choice. Filed for AMD upstream."
- **Cap action**: zoom on `137/144 broken` row

### 1:55 - 2:15 — Long-context coherence (slide 8)
- **Visual**: Slide 8 (needle test results)
- **Voice**: "200K-token needle test. Three of three pass — the model recovers planted facts from the deep middle of the prompt. The 256K window is usable, not just allocated."

### 2:15 - 2:35 — Live demo opening (Gradio Tab 1)
- **Visual**: Switch from PDF to browser → REPOMIND on `localhost:7860`
- **Voice**: "Let me show this live. The Space is wired to a real MI300X."
- **Action**: Click Tab "1. Ingest"
- **Visual**: Show form

### 2:35 - 3:00 — Repo ingestion live
- **Visual**: Type or paste `pallets/flask` in URL field
- **Voice**: "I'll ingest Flask — about 408,000 tokens across 227 files. The chunker prioritizes README, then top-level symbols, then nested code."
- **Action**: Click Ingest button
- **Visual**: Wait ~3-5 seconds for clone+chunk
- **Voice**: "Done — 1,995 chunks, fitted to a 256K-token window."

### 3:00 - 3:30 — Live agent question
- **Visual**: Click Tab "2. Ask"
- **Visual**: Type "Where is the WSGI request entry point in this codebase?"
- **Voice**: "Now I ask: Where is the WSGI request entry point?"
- **Action**: Click Ask button
- **Visual**: Wait for streaming response from MI300X (TTFT ~1.5-3 sec at 16K-32K context)
- **Voice**: "Streaming live from MI300X. It identifies the wsgi_app method in src/flask/app.py and explains the __call__ delegation. Correct file path. Correct method."
- **Cap action**: auto-zoom on the response as it streams

### 3:30 - 3:40 — Cost + closing (slides 10-11)
- **Visual**: Slide 10 (cost) → Slide 11 (closing)
- **Voice**: "Forty-six dollars per million completion tokens. Seventy to one-forty bursty dev seats per MI300X. Open-source MIT, verified, evidence pack public. Five to ten billion dollar TAM that doesn't have a product today. Thank you."

## After recording

1. Cap auto-edits cuts and zooms
2. Manual trim if needed
3. Export 1080p MP4 (target: 30-60 MB)
4. Upload to YouTube (unlisted) or Vimeo
5. Use the URL in lablab Step 2

## Emergency fallback

If MI300X is down or slow during recording:
- Switch to mock backend (`VLLM_BASE_URL=""`)
- Voice over with verified-evidence numbers from Tab 3
- Mention "the mock backend mirrors the same UI you'd see live"
- Rest of demo proceeds with cached responses

## Tips

- **Voice**: practice the script once before recording. Don't read robotically.
- **Pace**: about 130-140 words per minute. Don't rush.
- **Pauses**: Cap will edit out long pauses; OK to think briefly.
- **Mistakes**: Cap can cut. If you stumble badly, restart that 30-sec block.
- **Tabs**: pre-arrange browser tabs in order before Cap recording starts.
- **Zoom**: Cap auto-zooms on cursor activity. Click + hover deliberately
  on key elements you want highlighted (numbers, plot peaks, file paths).

## Browser tab order (left to right)

1. SLIDE_DECK.pdf (full-screen capable)
2. localhost:7860 (REPOMIND Gradio)
3. github.com/SRKRZ23/repomind (in case asked)
4. huggingface.co/spaces/lablab-ai-amd-developer-hackathon/repomind (in case asked)
