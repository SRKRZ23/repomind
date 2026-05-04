# GitHub: создать `SRKRZ23/repomind` и запушить v0.1

## Шаг 1 — Создать пустой repo через github.com

1. Открой https://github.com/new (залогинен под `SRKRZ23`).
2. Заполни:
   - **Owner**: `SRKRZ23`
   - **Repository name**: `repomind`
   - **Description**: `Open-source repo-scale coding agent on AMD MI300X (256K context, FP8). Built for AMD Developer Hackathon 2026.`
   - **Visibility**: **Public**
   - **Initialize this repository**: **NE STAW NIČEGO** (ни README, ни .gitignore, ни LICENSE — у нас уже свои локально, иначе будет конфликт при первом push)
3. Нажми **Create repository**.

GitHub покажет страницу с командами «…or push an existing repository from the command line». Нам нужны они — но я тебе уже всё подготовил ниже, копируй мои.

## Шаг 2 — Запушить локальное содержимое

Открой terminal и выполни одной серией:

```bash
cd /Users/sardorrazikov1/Alish/competitions/repomind

# инициализация (если git ещё не инициализирован в этой папке)
git init -b main

# проверь что .gitignore работает (не должно быть .repomind_cache/, __pycache__/, .pytest_cache/)
git status --short

# добавь всё кроме игнорируемого
git add .

# первый коммит
git commit -m "REPOMIND v0.1 — repo-scale coding agent skeleton

- Ingestion pipeline (tree-sitter + smart chunker + priority token budget)
- 5-tool registry: read_file, grep_codebase, execute_code, run_tests, git_log
- SC-TIR agent loop adapted from AIMO3 math pipeline
- vLLM ROCm 7 client + offline mock client
- Gradio UI scaffold
- Benchmarks plan + AMD Cloud setup playbook
- Build-in-Public materials (X / LinkedIn templates)
- 27/27 unit tests passing without GPU"

# подключи remote
git remote add origin https://github.com/SRKRZ23/repomind.git

# push
git push -u origin main
```

Если push просит логин — используй **personal access token** вместо пароля
(Settings → Developer settings → Personal access tokens → классический PAT
со scope `repo`). Однажды залогинишься — потом git кэширует.

Если используешь SSH ключ:

```bash
# вместо https remote — поставь ssh
git remote set-url origin git@github.com:SRKRZ23/repomind.git
git push -u origin main
```

## Шаг 3 — После пуша

1. Открой https://github.com/SRKRZ23/repomind
2. **Settings → General → Topics**: добавь
   `amd-mi300x`, `rocm`, `vllm`, `qwen3-coder`, `coding-agent`, `long-context`,
   `open-source`, `mit-license`, `hackathon`
3. **About** (gear-icon рядом с About справа): впиши описание
   `Open-source repo-scale coding agent on AMD MI300X (256K context, FP8)`
   и website `https://lablab.ai/event/amd-developer-hackathon`
4. **Settings → Pages**: оставь disabled пока (включим если будет static demo)
5. Включи **Discussions** (Settings → Features → Discussions ✓) — чтобы
   судьи могли задать вопрос публично, это очко в Originality / Presentation

## Шаг 4 — Verify

```bash
# должно показать https URL твоего публичного repo
git remote -v

# должно показать main → origin/main
git status

# проверь что бейджи работают (открой README.md на github.com — все badges зелёные)
```

## Шаг 5 — Tweet-ready link

После успешного пуша — копируй этот URL для X-поста:

```
https://github.com/SRKRZ23/repomind
```

И вставь в текст из `docs/x_post_day1.md`.

---

## На случай мелких граблей

| Симптом | Фикс |
| --- | --- |
| `error: src refspec main does not match any` | `git branch -m master main` (если init создал master), потом push |
| `Updates were rejected because the remote contains work` | GitHub repo создан с README — удали repo и создай заново БЕЗ инициализации |
| Огромный размер коммита | Проверь `git ls-files .repomind_cache` — должен быть пустой; иначе `git rm -r --cached .repomind_cache && git commit --amend --no-edit` |
| Публичные секреты в коммите | НЕ ПРИШЁЛ ВОТ ЭТОТ СЛУЧАЙ — мы ничего такого не клали; но проверь `git diff HEAD~ -- .env*` |

## Что НЕ делать

- ❌ Не делай force-push (`-f`) на main после первого пуша — это сбивает clone'ов.
- ❌ Не добавляй `.env` или ключи API в repo. У нас в `.gitignore` всё перечислено.
- ❌ Не клади модели (`*.safetensors`, `*.bin`) в git. HF Hub для этого.
