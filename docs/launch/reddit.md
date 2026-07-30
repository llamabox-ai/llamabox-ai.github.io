# Reddit posts

Post once per subreddit. Answer comments same day. Don’t cross-post identical walls of text within minutes.

---

## r/LocalLLaMA

**Title:** Offline LLM chat on Android (llama.cpp / GGUF) — LlamaBox closed beta

**Body:**

Built **LlamaBox** — an Android app for fully on-device chat with GGUF models via llama.cpp (llama.rn on React Native).

**What it is**
- Inference on-device only (no cloud API for chat)
- No accounts / no telemetry by design
- Model hub + local GGUF import
- Vision multimodal supported (encoder on CPU for UI stability)
- Package: `com.llamabox` · Android 7.0+ arm64

**Honest limits**
- CPU-only by design (no GPU dependencies)
- Phone speeds ≠ desktop — start with small Q4_K_M models

**Links**
- Site: https://llamabox-ai.github.io/
- Waitlist: https://llamabox-ai.github.io/waitlist.html
- Architecture: https://llamabox-ai.github.io/architecture.html
- How-to: https://llamabox-ai.github.io/how-to-run-llm-on-android.html

Happy to answer stack questions. Feedback from this community is the point of the beta.

---

## r/androidapps or r/privacy

**Title:** LlamaBox — private offline AI chat for Android (on-device LLM, no cloud)

**Body:**

Most AI apps need the network. **LlamaBox** runs the model on your phone so chats work offline (including airplane mode after the model is downloaded).

- No cloud inference, no account, no telemetry
- GGUF models + llama.cpp
- Free / dual-licensed (AGPL + commercial); source lands after closed beta
- Android 7+ arm64

Waitlist: https://llamabox-ai.github.io/waitlist.html  
Details: https://llamabox-ai.github.io/

Not a ChatGPT wrapper — local weights only. Tradeoff is speed vs privacy; we document real numbers on the site.
