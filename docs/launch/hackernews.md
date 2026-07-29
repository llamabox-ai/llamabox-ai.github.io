# Hacker News — Show HN

**When:** After waitlist is live and you can handle traffic (APK path even better).

**Title:**

```text
Show HN: LlamaBox – offline LLM chat on Android (llama.cpp, no cloud)
```

**Text:**

```text
LlamaBox is a React Native Android app that runs GGUF models fully on-device via llama.cpp.

- No cloud inference, no accounts, no telemetry
- Optional vision (on-device); CPU-only generation today (GPU roadmap)
- Closed beta: https://llamabox-ai.github.io/waitlist.html
- Architecture write-up: https://llamabox-ai.github.io/architecture.html
- Site: https://llamabox-ai.github.io/

Happy to discuss mobile llama.cpp tradeoffs, RAM budgets, and why we keep the vision encoder on CPU.
```

**First comment (post immediately):**

```text
Author here. Stack is RN 0.81 + llama.rn / llama.cpp, SQLite history, Zustand.

Deliberately not claiming GPU yet — mid-range phones need honest tok/s.

Looking for beta testers on arm64 Android 7+. Feedback on OOM and model presets especially welcome.
```
