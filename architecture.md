# LlamaBox — Architecture

This document explains **what LlamaBox is** and **why it is built the way it is**. It is written for developers, contributors, and curious users who want to understand the system beneath the app — not just the feature list.

> The source code lands in this repository when LlamaBox exits closed beta. Until then, this document describes the architecture at a level that lets you evaluate, extend, and build on the project.

---

## 1. What LlamaBox is

LlamaBox is a **React Native Android application that runs large language models (LLMs) entirely on-device**, with no network calls for inference and no cloud dependency. You download a quantized GGUF model, the app loads it into RAM, and llama.cpp generates tokens directly on your phone's CPU (and, in future, GPU).

The product goal is simple: **private, offline AI chat.** Your conversations, prompts, and images never leave the device.

### Key facts

| | |
|---|---|
| **Platform** | Android 7.0+ (arm64-v8a). iOS is a future target. |
| **Framework** | React Native 0.81 with the New Architecture (Fabric + JSI/TurboModules) |
| **Inference** | `llama.rn` 0.12.0-rc.8 wrapping `llama.cpp` |
| **Model format** | GGUF (Q4_K_M recommended) |
| **Compute today** | CPU-only (4 threads, ARM NEON) |
| **Multimodal** | Vision models via `initMultimodal` — image encoder on CPU |
| **State** | Zustand (UI), SQLite (chat history), AsyncStorage (settings) |
| **Context window** | 2048 tokens default (512–8192 configurable); auto 4096 for vision |

---

## 2. High-level architecture

```
┌─────────────────────────────────────────────┐
│              JavaScript Layer                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ ChatStore│  │ModelStore│  │ Settings │   │
│  │ (Zustand)│  │ (Zustand)│  │(Zustand) │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │          │
│  ┌────▼─────────────▼─────────────▼──────┐  │
│  │           UI Components               │  │
│  │  ChatScreen · ChatBubble · ChatInput  │  │
│  │  ModelSidebar · SystemMonitor · …      │  │
│  └────┬─────────────────────────────────┘  │
│       │                                      │
│  ┌────▼─────┐  ┌──────────┐  ┌───────────┐  │
│  │ LlmService│  │ Database │  │ Settings  │  │
│  │ (llama.rn)│  │ (SQLite) │  │Persistence│  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
└───────┼─────────────┼─────────────┼────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────┐
│        React Native Bridge (JSI)            │
└───────┬────────────────────────────────────┘
        │
┌───────▼────────────────────────────────────┐
│              Native Layer (C++)             │
│   llama.rn module → llama.cpp → ggml (CPU)  │
└─────────────────────────────────────────────┘
```

**Three layers:**
1. **JavaScript layer** — React Native UI + Zustand stores + service classes.
2. **Bridge** — JSI/TurboModules give near-zero-overhead JS↔native calls (New Architecture).
3. **Native layer** — `llama.rn` ships `llama.cpp` + `ggml` compiled for arm64. Inference runs here.

---

## 3. The "why" — design decisions explained

This is the section most people want. Each decision has a short rationale.

### Why on-device / offline?
Privacy is the product. The moment inference touches a server, the privacy claim is unverifiable. Running the model locally means the claim is auditable — and the app genuinely has no code path that sends your prompts anywhere. Offline is a *consequence* of privacy, not just a feature: if nothing leaves the device, the app works without a network.

### Why `llama.cpp` + `llama.rn`?
`llama.cpp` is the most mature, mobile-optimized CPU inference engine for GGUF models — pure C/C++ with hand-tuned ARM NEON kernels. `llama.rn` is its React Native bridge, exposing `initLlama`, `completion`, `tokenize`, `initMultimodal`, and friends as JS-callable functions. This gives us native-class inference without writing our own JNI.

### Why React Native + the New Architecture?
A single TypeScript codebase runs on Android today and can target iOS later. The New Architecture (Fabric + JSI/TurboModules) matters specifically here: inference calls pass large token buffers between JS and native, and JSI avoids the legacy async bridge's serialization overhead. For a hot path like token streaming, that is the difference between smooth and janky.

### Why CPU-only today? (and the GPU plan)
On every device tested so far, GPU detection returns none. The current build uses `llama.rn`'s **prebuilt binaries**, which ship an OpenCL-capable library, but the Java loader only attempts that library when a Qualcomm Hexagon DSP is also detected — an overly strict condition that couples two independent backends. The roadmap is to:
1. Add a **GPU diagnostics** panel so we can see exactly which library loads and why OpenCL probes fail per device.
2. Decouple OpenCL from Hexagon in the loader (via a `patch-package` patch or a fork of `llama.rn`).
3. Ship a user-facing **Inference Engine** selector (Auto / CPU / GPU) with a GPU smoke test in Settings, defaulting to safe CPU fallback.

Until that is validated across real devices, CPU-only is the honest, stable default. We will not ship a "GPU" toggle that does not work.

### Why is the vision encoder forced onto CPU?
Vision encoding is a one-shot burst that consumes significant GPU memory. On Android devices with limited GPU bandwidth, running the CLIP-style encoder on the GPU can **freeze the system UI for several seconds**. Forcing `use_gpu: false` for the vision encoder — while the text model can still use GPU layers when available — keeps the interface responsive during image processing. The text decoder is the long-running part; the encoder runs once per image.

### Why no Reanimated?
Reanimated crashes with the New Architecture in this specific setup. The app uses React Native's built-in `Animated` API with `useNativeDriver: true` for every animation (sidebar slide, download progress, pill toggle, chevron rotation). This is a deliberate constraint, not an oversight — any new animation must follow it or the app will crash.

### Why Zustand + SQLite + AsyncStorage (three stores)?
Each does what it is best at:
- **Zustand** — reactive UI state that does not need persistence (in-memory message list, generation flags, theme). Lightweight, no boilerplate.
- **SQLite (WAL mode)** — the durable chat history. Indexed by `(conversation_id, position)` for fast message loads and `updated_at` for sidebar sorting.
- **AsyncStorage** — key/value settings and per-model overrides, hydrated into Zustand on startup.

Mixing these would mean fighting a single store's limits. Keeping them separate is simpler and faster.

### Why memory-mapped weights (`use_mmap: true`) with no `mlock`?
A 1–4 GB GGUF file is mapped into virtual address space and paged in on demand, so startup is fast and apparent RAM use stays low. We do **not** `mlock` (pin pages in RAM) because on low-memory phones that risks OOM. The tradeoff is occasional micro-stutters from page faults during generation — acceptable for the stability it buys.

### Why is the KV cache not persisted across sessions?
When you resume an old conversation, the entire history is fed back as a fresh prompt and llama.cpp rebuilds the KV cache from scratch. This means **long conversations are slower to resume** (a 50-message chat must process all 50 messages before the first new token). The alternative — persisting and rehydrating a multi-hundred-MB FP16 KV cache — is fragile and unsafe across model/context changes. We chose simple and correct over fast-and-fragile. This is a known limitation, not a bug.

### Why a singleton model context?
Only one model is loaded at a time; loading a new one unloads the previous. On a phone, RAM is the hard constraint — a 2B model plus its KV cache already sits at ~500 MB–2 GB at peak. Multi-model residency is not realistic on most Android hardware today.

### Why context 2048 (4096 for vision)?
RAM again. KV cache grows linearly with context (`≈ 2 × layers × n_ctx × d_head × sizeof(fp16)`). 2048 is the sweet spot for fluid chat on mid-range devices. Vision auto-bumps to 4096 because image tokens are expensive (1000+ per image), and `ctx_shift` is disabled for multimodal sessions because shifting a KV cache that contains image embeddings can corrupt generation.

### Why Q4_K_M?
Of the GGUF quantization levels, Q4_K_M is the best speed/quality tradeoff on CPU. Smaller (Q2/Q3) degrades quality noticeably; larger (Q5/Q6/Q8) is slower with marginal gains on a phone. Models like Qwen2.5 0.5B and SmolLM2 360M run smoothly even on mid-range devices.

### Why AGPL-3.0 + a reserved trademark?
A privacy-first app that is closed source asks you to *trust* its privacy claim. Open source lets you *verify* it. We use **AGPL-3.0** (strong copyleft) so any fork that ships must also be open — preventing silent closed commercial clones. "LlamaBox" is a reserved trademark so the name itself cannot be used to endorse derived works without permission. A separate commercial license is available for closed-source commercial use; contact `aalhad.dev@gmail.com`.

---

## 4. The inference engine

### Native API surface used

| JS function | Native equivalent | Purpose |
|---|---|---|
| `initLlama()` | `llama_load_model_from_file` | Load GGUF, create context |
| `context.completion()` | `llama_decode` loop | Generate tokens |
| `context.tokenize()` | `llama_tokenize` | String → token IDs |
| `context.clearCache()` | `llama_kv_cache_clear` | Wipe KV cache |
| `context.stopCompletion()` | abort callback | Stop generation |
| `context.initMultimodal()` | clip/llava encoder init | Load vision projector (mmproj) |
| `getBackendDevicesInfo()` | `ggml_backend_dev_get_info` | Query compute devices |
| `releaseAllLlama()` | `llama_free` / backend free | Cleanup |

### Model loading parameters

| Parameter | Default | Effect |
|---|---|---|
| `n_ctx` | 2048 (4096 vision) | Max tokens the model can attend to |
| `n_threads` | 4 | CPU threads for matrix ops (1–8) |
| `n_gpu_layers` | 0 | GPU offload layers (always 0 today) |
| `use_mmap` | true | Memory-map weights instead of loading to RAM |
| `use_mlock` | false | Do not pin pages in RAM |
| `ctx_shift` | true (false for vision) | Slide context window when full |

The app surfaces the full `llama.cpp` sampling parameter set — temperature, top_p, top_k, min_p, repeat_penalty, Mirostat, DRY, XTC, typical_p, top_n_sigma, seed, and more — with user-friendly labels ("Creativity", "Memory Length", "Anti-Repetition") in Settings.

### Token generation pipeline (per output token)

```
1. Embedding lookup            (single-threaded)
2. Transformer block × N layers (4 worker threads)
     - LayerNorm, Q/K/V GEMM, RoPE, attention, FFN, residuals
3. Final LayerNorm + output projection (multi-threaded)
4. Sampling                     (temperature, top-p/k, repeat penalty)
5. KV cache append              (RAM write)
```

**Performance characteristics** (mid-range device, ~1B Q4_K_M model):

| Phase | Typical | Bottleneck |
|---|---|---|
| Prompt processing | 1–5 tok/s | Full forward pass per input token |
| Token generation | 2–8 tok/s | Attention over growing KV cache |
| Model load | 5–30 s | File I/O (mmap) + graph compile |

Longer context = slower generation. At 512 tokens, per-token generation is roughly 4× faster than at 2048.

---

## 5. Multimodal vision

```
User picks/captures image
   → expo-image-picker returns a temp URI
   → copied to persistent storage (FileSystem.Paths.document/attachments/{uuid}.jpg)
   → message sent with OpenAI-style content array:
       { role:'user', content:[ {type:'text',...}, {type:'image_url', image_url:{url:'file://...'}} ] }
   → native: image → CLIP encoder (CPU) → image embeddings → llama.cpp decode
```

**Image persistence is critical.** `expo-image-picker` returns temp/cache URIs that get cleaned up unpredictably; the native encoder needs a stable `file://` path at generation time. Images are copied to persistent storage before being sent.

A model is detected as vision-capable when its filename matches vision keywords (`llava`, `vision`, `mmproj`, `minicpm`, `moondream`, `internvl`, `idefics`, …) **and** a matching `mmproj` file is found alongside it (`{base}.mmproj.gguf`, `mmproj-{base}.gguf`, `{base}_mmproj.gguf`, plus heuristic fallbacks).

---

## 6. State, persistence, and the chat lifecycle

### Zustand stores
- **`chatStore`** — active conversation, in-memory messages, generation flags, streaming buffer, generation config, theme, presets.
- **`modelStore`** — loaded model, available models, download progress.

### SQLite schema (`llamabox.db`, WAL mode)
- `conversations` — id, title, model_name, model_path, system_prompt, context_size, timestamps, message_count.
- `messages` — id, conversation_id (FK, cascade delete), content, is_user, is_streaming, position, created_at, `attachments` (JSON image metadata).
- Indexes on `(conversation_id, position)` and `updated_at DESC`.

The `attachments` column is added via an idempotent `ALTER TABLE … ADD COLUMN` wrapped in try/catch, so existing installs migrate safely without crashing.

### Sending a message (the critical path)
1. Build prompt as `[system, ...history, user]`.
2. Estimate tokens per message; prune oldest user/assistant pairs (system prompt always kept) until the prompt fits `contextSize − maxTokens − 256`.
3. Insert the user message + an empty streaming placeholder into SQLite.
4. Call `LlmService.generateChat`; tokens stream back via a throttled callback (~150 ms UI updates).
5. On completion, finalize the assistant message in SQLite; on error, append the error text. Always release the generation flag.

**The KV cache is never restored** — resuming an old chat reprocesses the whole history (see *Why* above).

---

## 7. UI architecture

- **Screens** (expo-router): `/` → ChatScreen, `/settings` → SettingsScreen.
- **Key components:** `ChatScreen`, `ChatBubble`, `ChatInput`, `ModePill` (animated Chat↔Vision toggle), `ModelSidebar`, `SystemMonitor`, `ModelDownloader`.
- **Theming:** custom `useTheme()` hook over Zustand `colorScheme` — light, dark, amoled, system. Color tokens in `src/constants/theme.ts`.
- **Animations:** `Animated` + `useNativeDriver: true` only. No Reanimated (see *Why*).

---

## 8. Model management

- **Format:** GGUF; Q4_K_M recommended; typical size 500 MB – 4 GB.
- **Import:** pick a file → copy to `FileSystem.Paths.document/models/` → tracked in `modelStore`.
- **Download:** stream from Hugging Face URLs by `hfRepo` + `hfFile`, with live progress.
- **Vision detection:** scanner pairs `.gguf` models with sibling `mmproj` files (see §5).
- **One model at a time:** loading a new model unloads the current one (RAM constraint).

---

## 9. Memory footprint

| Component | Approx. size | Where |
|---|---|---|
| GGUF model (memory-mapped) | 1–4 GB | Virtual address space (paged) |
| KV cache (FP16) | 200–800 MB | RAM |
| llama.cpp runtime | 50–100 MB | RAM |
| React Native JS heap | 50–150 MB | RAM |
| UI / images / SQLite | 20–50 MB | RAM |
| **Typical active peak** | **500 MB – 2 GB** | RAM |

OOM during `initLlama` is caught and surfaced as a friendly "try a smaller model or reduce context size" message.

---

## 10. Current limitations & roadmap

**Limitations today**
- CPU-only inference (GPU enablement in progress — see §3).
- KV cache is not persisted; resuming long chats is slower to first token.
- One model loaded at a time.
- Android-first; iOS not yet built.

**Roadmap (tentative)**
- GPU (OpenCL) enablement with a device diagnostics panel and an Auto/CPU/GPU engine selector.
- Expanded model presets and one-click custom GGUF import.
- Plugin / tool-use system (calculator, code execution, retrieval).
- More vision model preset packs (DeepSeek, Qwen, Gemma families).
- Automatic context-window sizing based on available RAM.
- iOS port and Apple Silicon GPU acceleration research.

---

## 11. Licensing & trademark

LlamaBox is **dual-licensed**:
- **AGPL-3.0** — free, copyleft open-source use.
- **Commercial license** — for closed-source commercial derivatives; contact `aalhad.dev@gmail.com`.

"LlamaBox" is a **reserved trademark** of the project. The name may not be used to endorse or promote derived works without written permission. See `LICENSE` and `CONTRIBUTING.md` (CLA) for details.

---

*Last updated: 2026-07-26. This document describes the architecture as of the closed beta; specifics may evolve before and after public source release.*