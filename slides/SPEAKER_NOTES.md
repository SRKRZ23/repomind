# REPOMIND — Speaker Notes / Demo Video Script

Full talk track for narrating the slide deck or recording the 3-5 minute
demo video. Each section is timed and matches a slide.

**Total runtime target**: ~4 min 50 sec narration (under 5-min lablab cap).
Updated 2026-05-06 to reflect 11-slide deck with new "Tuning attempt" slide.

---

## Slide 1 — Title (~20 sec)

> "Hi, I'm Sardor Razikov, solo from Tashkent. I built REPOMIND — an
> open-source repo-scale coding agent that runs on a single AMD MI300X.
> The pitch is simple: load an entire git repository at 256K context on
> one GPU, reason across the whole codebase with multi-step tool use,
> and ship it MIT so banks, defense, healthcare — the people who can't
> legally use Cursor — finally have an option."

**Visual**: Title slide. No demo yet.

---

## Slide 2 — The problem (~25 sec)

> "Closed coding agents are great if you're a startup. But banks can't
> send code to OpenAI. Defense contractors can't. Pharma can't. JP
> Morgan has 50,000 developers with no AI tooling at all because of
> compliance. That's not 'savings vs Cursor' — that's an unlock of a
> whole market that doesn't have a product today."
>
> "REPOMIND is open-source, MIT, runs on your own AMD hardware, code
> never leaves your VPC."

**Visual**: Comparison table on slide.

---

## Slide 3 — Architectural moat (~30 sec)

> "Why MI300X specifically. Qwen3-Coder-Next FP8 weights are about 80
> gigabytes. The 256K KV cache at FP8 is about 38 gigabytes. Plus
> activations and framework, that's 143 gigabytes total."
>
> "NVIDIA H100 single-card caps at 80. By VRAM accounting, you'd have
> to shard across 2 to 4 H100s with all the AllReduce overhead."
>
> "MI300X 192 gigabytes just runs it on one card. AMD's own February
> 2026 blog positioned this exact workload — REPOMIND is the first
> open-source proof shipped."

**Visual**: VRAM math + comparison table.

---

## Slide 4 — Verified on real hardware (~25 sec)

> "This isn't theory. We ran 124 minutes of stress testing across two
> sessions on real MI300X hardware on May fifth and sixth, twenty
> twenty six."
>
> "Model weights took 77.29 gibibytes in VRAM. KV cache 94.58 gibibytes
> available — over 2 million tokens of cache. Peak utilization 92
> percent of the 192 gigs."
>
> "The vLLM API confirms 256K context window via the models endpoint.
> Cold start three and a half minutes. Total cost across both
> sessions: $4.12."

**Visual**: Verification table.
**Optional B-roll**: rocm-smi snapshot showing 92% VRAM.

---

## Slide 5 — Throughput plot (~20 sec)

> "Throughput sweep across six context lengths from 8K to 256K, all
> hot measurements with no cold-start outliers. Time-to-first-token at
> 8K is under half a second; at 256K, 117 seconds."
>
> "Linear in prompt size — that's the prefill cost. Long-context
> inference is prefill-bound; decode itself is fast."

**Visual**: Throughput plot (left half: tps; right half: TTFT).

---

## Slide 6 — Concurrency stress (~30 sec)

> "Twenty-four cells of concurrency data across six context lengths.
> The clean story: 31 out of 31 concurrent users succeed at every
> context from 8K up through 64K under the default Triton backend."
>
> "At 128K, 25 of 31 within our 15-minute window. At 256K, the
> realistic ceiling is six to eight for unique-prompt workloads."
>
> "The 8K and 16K rows directly answer the question 'where do most
> users live' — for typical developer queries, this is over 78
> aggregate tokens per second on a single GPU."

**Visual**: Concurrency plot (p95 latency + aggregate tps).

---

## Slide 7 — Tuning attempt: AITER backend (~30 sec)

> "Hakob from the AMD Developer Forum asked if we tried any vLLM
> tuning. We did — measured the AITER attention backend, AMD's
> hand-tuned MI300X kernels."
>
> "Two findings. First: throughput is genuinely 2 to 4 times higher
> under AITER. Time-to-first-token at 64K is nearly 3 times faster."
>
> "Second: the output degenerates to repeating punctuation tokens.
> 137 of 144 cells produce gibberish in the FP8 KV cache
> configuration. So default Triton stays our production-safe choice."
>
> "This is the kind of regression you only catch by actually running
> the workload — and exactly the kind of bug AMD's ROCm team will
> want flagged. Filed upstream as a tracked issue."

**Visual**: A/B table showing throughput gain vs output quality loss.
**Optional B-roll**: side-by-side terminal output of correct response
vs `!!!!!!!!`.

---

## Slide 8 — Long-context coherence (~25 sec)

> "Most '256K context' claims in the industry are memory allocation,
> not usable accuracy. Models hold the prompt but their attention
> degrades past 64K."
>
> "We tested this: planted a unique sentinel function name and a magic
> constant deep inside a 200,000-token code corpus, at three positions
> — early, middle, late. Three out of three pass. The model returns
> valid JSON with both facts recovered, even from the middle of the
> 199,413-token prompt."
>
> "This is required for repo-scale reasoning to actually work."

**Visual**: Needle test results table.
**Optional B-roll**: Show model's exact JSON response.

---

## Slide 9 — End-to-end repo Q&A (~30 sec)

> "This is the killer demo. We ran end-to-end ingestion on three real
> repos: REPOMIND itself at 68K tokens, Flask at 408K, and pytorch/vision
> at ONE POINT THREE MILLION tokens."
>
> "The largest is five times bigger than any context window — including
> ours. Our priority-aware chunker prioritizes READMEs, then top-level
> symbols, then nested code, with a token budget. It trims pytorch/vision
> down to 180K of the highest-priority content."
>
> "The agent answers all nine questions correctly with right file path
> citations. Cursor sends fragments because they're remote-API-bound.
> REPOMIND constructs the right 180K window per question because it
> owns the inference path."

**Visual**: 3-tier table + sample model answer.
**Optional B-roll**: Live demo if MI300X is up — paste GitHub URL,
ingest, ask question.

---

## Slide 10 — Cost economics (~25 sec)

> "Cost economics. AMD Cloud at $1.99 per GPU per hour. Forty-six
> dollars per million completion tokens at our best aggregate
> throughput."
>
> "One MI300X handles 14 continuous queriers, or 70 to 140 developer
> seats for typical bursty engineering workloads where 10 to 20
> percent are active at any moment."
>
> "Owned MI300X breaks even versus Cursor Teams in three to six months
> for a 100-developer team. But the deeper story: for banks and
> defense and pharma who legally can't use SaaS coding agents, this
> isn't competing with Cursor. We're the first option that exists."

**Visual**: Cost plot + economics table.

---

## Slide 11 — Closing with Lisa Su tie-in (~30 sec)

> "AMD CEO Lisa Su said at CES 2026 — and I quote — 'AI is for everyone.' We took that literally."
>
> "REPOMIND is open-source MIT, runs on a single AMD MI300X — banks, defense, pharma, Apple iOS team, indie developers — all get the same agent. The same canonical lablab and AMD pattern from Steve Kimoi's tutorial, taken to its logical extreme: full 256K context, agentic tool use, repo-scale ingestion."
>
> "Verified yesterday on real hardware. Five to ten billion dollar TAM that doesn't have a product today. AMD made the hardware. We made the open-source unlock."
>
> "Thank you. Questions?"

**Visual:** Slide 11 (closing with Lisa Su quote at top + REPOMIND links).

---

## Slide 11 — Original closing fallback (~25 sec, if Lisa Su quote feels too much)

> "To wrap up. AMD made the hardware that makes 256K-context, repo-
> scale coding possible on a single GPU. We made the open-source
> unlock that lets banks, defense, pharma, healthcare, and consumer-
> tech teams use it."
>
> "Same canonical lablab and AMD pattern from Steve Kimoi's tutorial —
> vLLM endpoint plus Hugging Face Space — taken to its logical
> extreme: full 256K context, agentic tool use, repo-scale ingestion.
> MIT licensed. Verified yesterday."
>
> "Five to ten billion dollar TAM that doesn't have a product today.
> Thank you. Questions?"

**Visual**: Closing slide with links.

---

## Live demo segment (insert between slide 9 and 10 if MI300X is up)

If recording with live MI300X backend, insert a 30-45 sec segment:

> "Let me show this live. I'm pasting the URL of pytorch/vision into
> REPOMIND on Hugging Face Space. The Space is wired to a live MI300X
> on AMD Developer Cloud."

[Click "Ingest" — wait 2-3 sec]

> "Repo ingested — 581 files, 6,799 chunks, fitted to a 180K-token
> window via priority-aware truncation."

[Switch to "Ask" tab, paste question]

> "Now I ask: 'Where does video decoding live in this repo?'"

[Click submit, wait for response — 2-3 sec TTFT]

> "Here's the answer streaming in. It identifies torchvision.io.video,
> the pyav backend, and the C++ implementation directory — all
> correctly cited from a repository 5x bigger than the context window."

---

## Recording tips

- **Voice**: clear, steady pace. Don't rush. Practice once before
  recording.
- **Slide pacing**: ~20-30 sec per slide.
- **Cursor**: use Cap's auto-zoom on key elements (numbers, plots).
- **Audio**: use a quiet room. Built-in MacBook mic is OK if quiet.
  USB mic better.
- **Take 1**: practice run, ignore mistakes
- **Take 2-3**: real recording
- **Edit**: Cap will auto-edit cuts. Manual trim if needed.

## Demo flow during recording

1. Open browser tab to slide deck (PDF rendered from Marp)
2. Open second tab to HF Space (live MI300X backend wired)
3. Open third tab to GitHub repo (in case asked)
4. Cap recording starts → slides → live demo segment → slides → end

---

## What NOT to say

- ❌ "Just runs at 256K" → use "verified at 256K"
- ❌ "Cursor for self-hosters" → trademark issue, use "self-hosted alternative"
- ❌ "Physically OOMs on H100" → use "by VRAM accounting cannot accommodate"
- ❌ "200 devs per GPU" → use "14 continuous, 70-140 bursty"
- ❌ Trash-talk competitors → just compare factually
