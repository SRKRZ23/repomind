# AMD Developer Cloud — setup playbook

The 30-minute path from "credits arrived" to "vLLM serving Qwen3-Coder-Next-FP8 on MI300X".

## 0. Prerequisites

- AMD AI Developer Program account: ✅ active (`razikovsardor1@gmail.com`)
- $100 credit code from `devcloudrequests@amd.com`
- DigitalOcean account on `amd.digitalocean.com` (link from credit email)

## 1. Apply credits

1. Open the unique credit link from the email.
2. Sign in / create the AMD Developer Cloud (DigitalOcean) account.
3. Verify the credit appears in **Billing → Credits**.

## 2. Spin up MI300X droplet

```
Project    → AMD Developer Cloud
Image      → ROCm 7 / vLLM Quick Start  (NOT Fireworks)
GPU        → MI300X x1 (one card is enough for Qwen3-Coder-Next-FP8 @ 256K)
Region     → AMS3 or NYC3 (whichever is closest)
Storage    → ≥ 200 GB volume (model weights + KV cache scratch)
SSH key    → upload your local public key
```

Don't pick the 8x configuration unless we have time to use it — it burns
credits 8× faster.

## 3. SSH and verify

```bash
ssh root@<droplet-ip>
rocm-smi
# Should list one MI300X.

vllm --version
# Should be ≥ 0.6 with ROCm support.

python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# True · "AMD Instinct MI300X"
```

## 4. Pull the prebuilt vLLM ROCm container (if not in image)

```bash
docker pull rocm/vllm:rocm7.0_vllm_qwen3coder_next
```

Or build from source if the registry tag has shifted:

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
docker build -f Dockerfile.rocm -t vllm-rocm:dev .
```

## 5. Serve Qwen3-Coder-Next-FP8

```bash
docker run --device=/dev/kfd --device=/dev/dri --group-add video \
  --shm-size 16g --rm -p 8000:8000 \
  -v $PWD:/workspace -w /workspace \
  rocm/vllm:rocm7.0_vllm_qwen3coder_next \
  bash -c "vllm serve Qwen/Qwen3-Coder-Next-FP8 \
    --tool-call-parser qwen3_coder \
    --max-model-len 262144 \
    --kv-cache-dtype fp8 \
    --gpu-memory-utilization 0.92 \
    --enforce-eager"
```

Tweak knobs:

- `--max-model-len 262144` — full 256K context window
- `--kv-cache-dtype fp8` — halves KV cache footprint
- `--gpu-memory-utilization 0.92` — leaves headroom for activations
- `--enforce-eager` — disables CUDA graphs (cleaner first-run; remove later for ~10 % throughput)

## 6. Smoke test from local machine

```bash
curl http://<droplet-ip>:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-Next-FP8",
    "messages": [{"role":"user","content":"Reply with one word: pong."}],
    "max_tokens": 8
  }'
```

If you see `pong` in the response, you are live.

## 7. Wire REPOMIND

```bash
python -m scripts.ask_agent \
  --question "What does ingestion/chunker.py prioritize?" \
  --repo .repomind_cache/self.json \
  --backend vllm \
  --base-url http://<droplet-ip>:8000/v1
```

## 8. Cost discipline

- $100 credit budget = ~30 GPU-hours at MI300X x1 published rates.
- **Stop the droplet** between sessions: `doctl compute droplet-action shutdown <id>`.
- Volume storage continues to bill at ~$0.10/GB/month (negligible).
- Single-GPU + FP8 + bounded `max-model-len` = stays inside the budget.

## 9. When things go wrong

| Symptom | Fix |
| --- | --- |
| `HIP error: out of memory` at startup | Lower `--gpu-memory-utilization` to 0.88 |
| First-token latency >5 s after warm-up | Drop `--enforce-eager`, let CUDA graphs build |
| Tool-call parsing fails | Ensure `--tool-call-parser qwen3_coder`; vLLM ≥ 0.6 |
| `Killed` mid-generation | Shared memory too small; bump `--shm-size` to 32g |
| Response stalls under load | Add `--max-num-batched-tokens 16384` |

## 10. Tear-down at hackathon end

```bash
doctl compute droplet delete <id>
doctl compute volume delete <volume-id>
```

(Don't delete on day 6 — you'll need the droplet for the demo recording.)
