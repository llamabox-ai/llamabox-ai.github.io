#!/usr/bin/env python3
"""Generate SEO, waitlist, download, and blog pages for LlamaBox site."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://llamabox-ai.github.io"

SHARED_HEAD = """  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="author" content="LlamaBox AI">
  <meta name="theme-color" content="#080808">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%230F0F0F' stroke='%23D4A54A' stroke-width='4'/%3E%3Ctext x='50' y='68' font-family='Georgia,serif' font-size='48' font-weight='700' fill='%23D4A54A' text-anchor='middle'%3ELB%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
  <link rel="alternate" type="text/plain" title="LLM brief" href="{base}/llms.txt">
"""

NAV = """  <div class="bg-mesh" aria-hidden="true"></div>
  <div class="bg-noise" aria-hidden="true"></div>
  <header class="nav" id="nav">
    <div class="nav-inner">
      <a href="/" class="wordmark" aria-label="LlamaBox home">Llama<span>Box</span></a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav-links" id="navLinks" aria-label="Primary">
        <a href="/#features">Features</a>
        <a href="/guides.html">Guides</a>
        <a href="/blog/">Blog</a>
        <a href="/architecture.html">Architecture</a>
        <a href="https://github.com/llamabox-ai" rel="noopener">GitHub</a>
        <a class="btn btn-primary btn-sm" href="/waitlist.html">Join waitlist</a>
      </nav>
    </div>
  </header>
"""

FOOTER = """  <footer class="footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="wordmark">Llama<span>Box</span></div>
          <p>Private offline AI chat for Android. On-device GGUF inference powered by llama.cpp.</p>
        </div>
        <div>
          <h4>Product</h4>
          <ul>
            <li><a href="/waitlist.html">Waitlist</a></li>
            <li><a href="/download.html">Download</a></li>
            <li><a href="/#features">Features</a></li>
            <li><a href="/#compare">Compare</a></li>
          </ul>
        </div>
        <div>
          <h4>Guides</h4>
          <ul>
            <li><a href="/offline-ai-android.html">Offline AI Android</a></li>
            <li><a href="/on-device-llm.html">On-device LLM</a></li>
            <li><a href="/private-chatgpt-alternative.html">Private ChatGPT alt</a></li>
            <li><a href="/gguf-android.html">GGUF on Android</a></li>
            <li><a href="/how-to-run-llm-on-android.html">How-to guide</a></li>
            <li><a href="/vs-chatgpt.html">vs ChatGPT</a></li>
            <li><a href="/vs-ollama.html">vs Ollama</a></li>
            <li><a href="/blog/">Blog</a></li>
          </ul>
        </div>
        <div>
          <h4>Developers</h4>
          <ul>
            <li><a href="/architecture.html">Architecture</a></li>
            <li><a href="/llms.txt">llms.txt</a></li>
            <li><a href="/privacy.html">Privacy</a></li>
            <li><a href="https://github.com/llamabox-ai" rel="noopener">GitHub</a></li>
            <li><a href="mailto:aalhad.dev@gmail.com">Contact</a></li>
          </ul>
        </div>
      </div>
      <p class="footer-legal">Source dual-licensed AGPL-3.0 (open-source) and a separate commercial license. “LlamaBox” is a reserved trademark. Full public source lands when closed beta ends. CPU-only inference by design.</p>
      <div class="footer-bottom">
        <span>© 2026 LlamaBox AI · Mythos Labs</span>
        <span>Package com.llamabox · Android 7.0+</span>
      </div>
    </div>
  </footer>
  <script src="/assets/site.js"></script>
"""

CTA_BLOCK = """
    <section class="section">
      <div class="wrap">
        <div class="final reveal">
          <div class="eyebrow" style="justify-content:center">Closed beta</div>
          <h2>Try private offline AI on Android.</h2>
          <p class="lead">Join the waitlist. No spam — beta access and release notes only.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="/waitlist.html">Join the waitlist</a>
            <a class="btn btn-ghost" href="/download.html">Download status</a>
            <a class="btn btn-ghost" href="https://github.com/llamabox-ai" rel="noopener">GitHub</a>
          </div>
        </div>
      </div>
    </section>
"""


def page(path: str, title: str, description: str, body: str, extra_head: str = "", og_title: str | None = None):
    url = f"{BASE}/{path.lstrip('/')}" if path not in ("", "/") else f"{BASE}/"
    norm = path.replace("\\", "/")
    if norm.endswith("blog/index.html"):
        url = f"{BASE}/blog/"
    og_t = og_title or title
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{SHARED_HEAD.format(base=BASE)}
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LlamaBox">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{og_t}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{BASE}/assets/screenshot-1-home.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_t}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{BASE}/assets/screenshot-1-home.png">
{extra_head}
</head>
<body>
{NAV}
  <main>
{body}
{CTA_BLOCK}
  </main>
{FOOTER}
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def article(eyebrow: str, h1: str, lead: str, content_html: str) -> str:
    return f"""
    <section class="section page-hero">
      <div class="wrap narrow">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
    <section class="section section-tight">
      <div class="wrap narrow prose reveal is-in">
{content_html}
      </div>
    </section>
"""


def faq_schema(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    import json

    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return f'  <script type="application/ld+json">\n  {json.dumps(data, ensure_ascii=False)}\n  </script>'


def faq_html(faqs: list[tuple[str, str]]) -> str:
    parts = ['<h2 id="faq">FAQ</h2>', '<div class="faq-list">']
    for i, (q, a) in enumerate(faqs):
        open_attr = " open" if i == 0 else ""
        parts.append(f'<details class="faq-item"{open_attr}><summary>{q}</summary><div class="ans">{a}</div></details>')
    parts.append("</div>")
    return "\n".join(parts)


def main():
    # --- waitlist ---
    page(
        "waitlist.html",
        "Join the LlamaBox waitlist | Offline AI Android beta",
        "Join the LlamaBox closed beta waitlist. Private offline AI chat for Android — on-device GGUF, no cloud, no accounts.",
        """
    <section class="section page-hero">
      <div class="wrap narrow">
        <div class="eyebrow">Waitlist</div>
        <h1>Join the closed beta.</h1>
        <p class="lead">Android 7.0+ arm64. Tell us your device — we prioritize testers who help us stress mid-range phones.</p>
      </div>
    </section>
    <section class="section section-tight">
      <div class="wrap narrow">
        <form class="waitlist-form glass reveal is-in" action="https://formsubmit.co/aalhad.dev@gmail.com" method="POST">
          <input type="hidden" name="_subject" value="LlamaBox waitlist signup">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_next" value="https://llamabox-ai.github.io/waitlist-thanks.html">
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
          <label>Email <span class="req">*</span>
            <input required type="email" name="email" placeholder="you@example.com" autocomplete="email">
          </label>
          <label>Android version
            <input type="text" name="android_version" placeholder="e.g. 14">
          </label>
          <label>Device + approximate RAM
            <input type="text" name="device" placeholder="e.g. Pixel 6a · 6 GB">
          </label>
          <label>Why offline AI? (optional)
            <textarea name="why" rows="3" placeholder="Privacy, travel, research…"></textarea>
          </label>
          <button type="submit" class="btn btn-primary" style="width:100%">Join waitlist</button>
          <p class="form-note">We only use your email for beta access and major releases. Fallback: <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20beta%20access">email us</a> or open a request on <a href="https://github.com/llamabox-ai" rel="noopener">GitHub</a>.</p>
        </form>
      </div>
    </section>
""",
    )

    page(
        "waitlist-thanks.html",
        "You're on the LlamaBox waitlist",
        "Thanks for joining the LlamaBox beta waitlist.",
        """
    <section class="section page-hero">
      <div class="wrap narrow">
        <div class="eyebrow">Confirmed</div>
        <h1>You're on the list.</h1>
        <p class="lead">We'll email when a beta slot or public APK is ready. Meanwhile, read the architecture and share LlamaBox with someone who needs offline AI.</p>
        <div class="cta-row" style="margin-top:1.5rem">
          <a class="btn btn-primary" href="/">Back home</a>
          <a class="btn btn-ghost" href="/architecture.html">Architecture</a>
          <a class="btn btn-ghost" href="/how-to-run-llm-on-android.html">How-to guide</a>
        </div>
      </div>
    </section>
""",
    )

    # --- download ---
    page(
        "download.html",
        "Download LlamaBox | Android offline AI app status",
        "LlamaBox download status: closed beta for Android. Join the waitlist for APK and Play Store access. Package com.llamabox.",
        article(
            "Download",
            "Get LlamaBox on Android.",
            "Closed beta today. Public APK and Play Store tracks land as testing opens.",
            """
        <h2>Current status</h2>
        <ul>
          <li><strong>Closed beta</strong> — install via invite / waitlist</li>
          <li><strong>Package</strong> — <code>com.llamabox</code></li>
          <li><strong>Requirements</strong> — Android 7.0+ (API 24), arm64-v8a</li>
          <li><strong>Public source</strong> — lands when closed beta ends (AGPL-3.0 + commercial)</li>
        </ul>
        <h2>What you need</h2>
        <ul>
          <li>Enough free storage for GGUF models (hundreds of MB to several GB)</li>
          <li>RAM headroom for Q4_K_M models (small 0.5B–1B models for mid-range phones)</li>
          <li>Optional network only to download models; chat works offline after that</li>
        </ul>
        <h2>Next step</h2>
        <p><a class="btn btn-primary" href="/waitlist.html">Join the waitlist</a></p>
        <p>Engineers: read <a href="/architecture.html">architecture</a> and <a href="/gguf-android.html">GGUF on Android</a>.</p>
""",
        ),
    )

    # --- guides hub ---
    page(
        "guides.html",
        "LlamaBox guides | Offline AI, GGUF, private chat on Android",
        "Guides for offline AI on Android, on-device LLMs, GGUF models, private ChatGPT alternatives, and LlamaBox setup.",
        article(
            "Guides",
            "Learn private, offline AI on Android.",
            "SEO-friendly deep dives. Every page is written for humans and safe for answer engines to cite.",
            """
        <div class="card-links">
          <a class="card-link glass" href="/offline-ai-android.html"><strong>Offline AI Android</strong><span>Airplane-mode chat that stays local</span></a>
          <a class="card-link glass" href="/on-device-llm.html"><strong>On-device LLM</strong><span>What “on-device” actually means</span></a>
          <a class="card-link glass" href="/private-chatgpt-alternative.html"><strong>Private ChatGPT alternative</strong><span>When cloud chat is the risk</span></a>
          <a class="card-link glass" href="/gguf-android.html"><strong>GGUF on Android</strong><span>Quantizations, RAM, imports</span></a>
          <a class="card-link glass" href="/how-to-run-llm-on-android.html"><strong>How to run an LLM on Android</strong><span>Step-by-step tutorial</span></a>
          <a class="card-link glass" href="/vs-chatgpt.html"><strong>LlamaBox vs ChatGPT</strong><span>Honest comparison table</span></a>
          <a class="card-link glass" href="/vs-ollama.html"><strong>LlamaBox vs Ollama</strong><span>Phone-native vs desktop local</span></a>
          <a class="card-link glass" href="/blog/"><strong>Blog</strong><span>Models, engineering notes, updates</span></a>
        </div>
""",
        ),
    )

    faqs_offline = [
        ("What is offline AI on Android?", "Offline AI means the model runs on the phone. After the model file is stored locally, chat works without a network — including airplane mode."),
        ("Is LlamaBox fully offline?", "Inference is fully offline. Optional internet is only for downloading models from public hubs like Hugging Face."),
        ("Does offline mean private?", "On-device inference means prompts and completions never hit a vendor server. LlamaBox adds no accounts or telemetry on top of that architecture."),
    ]
    page(
        "offline-ai-android.html",
        "Offline AI for Android | On-device chat with LlamaBox",
        "Run offline AI chat on Android. LlamaBox loads GGUF models with llama.cpp — no cloud, no accounts. Airplane mode friendly.",
        article(
            "Offline AI",
            "Offline AI chat for Android.",
            "Most “AI apps” die without signal. LlamaBox is built for the opposite: private conversation that never leaves the handset.",
            f"""
        <h2>Why offline AI matters</h2>
        <p>Travel, fieldwork, sensitive drafting, classrooms with locked networks, and regions with expensive data all break cloud chat. Offline AI keeps the loop local: model in RAM, tokens on CPU, history in SQLite on device.</p>
        <h2>How LlamaBox delivers offline AI</h2>
        <ul>
          <li>GGUF models via <strong>llama.cpp</strong> (through llama.rn on React Native)</li>
          <li><strong>CPU-only</strong> inference by design (no GPU dependencies)</li>
          <li>No account graph, no cloud inference endpoint</li>
          <li>Optional vision with on-device multimodal models</li>
        </ul>
        <h2>What works without internet</h2>
        <ul>
          <li>Chat completions once a model is installed</li>
          <li>History, settings, system monitor</li>
          <li>Vision on local images with a compatible model + mmproj</li>
          <li>TTS readback of local answers</li>
        </ul>
        <h2>What still needs a network (optional)</h2>
        <p>Downloading a GGUF the first time. After that, disconnect freely.</p>
        <h2>Who this is for</h2>
        <p>Privacy-first users, journalists, students, builders testing GGUF on real silicon, and anyone who wants ChatGPT-like chat without shipping transcripts to a data center.</p>
        <p>Related: <a href="/on-device-llm.html">on-device LLM</a> · <a href="/how-to-run-llm-on-android.html">how-to</a> · <a href="/vs-chatgpt.html">vs ChatGPT</a>.</p>
        {faq_html(faqs_offline)}
""",
        ),
        extra_head=faq_schema(faqs_offline),
    )

    faqs_od = [
        ("What is an on-device LLM?", "A language model that runs inference on the user’s hardware — here, an Android phone — rather than on a remote API server."),
        ("Is on-device slower?", "Usually yes versus frontier cloud APIs. Small Q4_K_M models on mid-range phones often land in a few tokens/sec. LlamaBox publishes honest ranges, not theater."),
        ("Does on-device require special hardware?", "No. LlamaBox runs on standard Android CPUs with ARM NEON. No GPU or datacenter hardware is needed."),
    ]
    page(
        "on-device-llm.html",
        "On-device LLM on Android | LlamaBox local inference",
        "On-device LLM inference on Android with LlamaBox: GGUF models, llama.cpp, private chat, no cloud API for generation.",
        article(
            "On-device LLM",
            "On-device LLM on your phone.",
            "“On-device” is not a marketing synonym for “mobile app.” It means the weights run where you are.",
            f"""
        <h2>Definition</h2>
        <p>An <strong>on-device LLM</strong> executes the forward pass on local hardware. For LlamaBox that is your Android SoC via llama.cpp, loading a quantized GGUF into app memory.</p>
        <h2>Stack (short)</h2>
        <ul>
          <li>React Native 0.81 (New Architecture)</li>
          <li>llama.rn wrapping llama.cpp</li>
          <li>GGUF (Q4_K_M recommended)</li>
          <li>Zustand + SQLite + AsyncStorage</li>
        </ul>
        <h2>Privacy property</h2>
        <p>If generation never leaves the process, you do not need to “trust a privacy policy” for that step — you can reason about the architecture. See <a href="/architecture.html">architecture</a>.</p>
        <h2>Performance expectations</h2>
        <p>Mid-range phones with ~1B Q4_K_M models: roughly 1–5 tok/s prompt processing and 2–8 tok/s generation (device dependent). Load times 5–30s. Peak memory often ~0.5–2 GB for small models.</p>
        <p>Next: <a href="/gguf-android.html">GGUF guide</a> · <a href="/offline-ai-android.html">offline AI</a>.</p>
        {faq_html(faqs_od)}
""",
        ),
        extra_head=faq_schema(faqs_od),
    )

    faqs_priv = [
        ("Is LlamaBox a ChatGPT clone?", "It offers chat UX for local models. It is not a hosted OpenAI service and does not call ChatGPT APIs for inference."),
        ("When should I still use ChatGPT?", "When you need frontier reasoning, tools, browsing, or speed that phone CPUs cannot match. Use LlamaBox when locality and privacy dominate."),
        ("Does private mean encrypted to a vendor?", "LlamaBox’s privacy story is stronger: no vendor inference path. Data stays on-device by design."),
    ]
    page(
        "private-chatgpt-alternative.html",
        "Private ChatGPT alternative for Android | LlamaBox",
        "Looking for a private ChatGPT-style chat? LlamaBox runs models on your Android phone — no cloud inference, no accounts, no telemetry.",
        article(
            "Private alternative",
            "A private ChatGPT-style chat that stays on your phone.",
            "Cloud assistants are brilliant and extractive. LlamaBox is the offline lane: same impulse to chat, opposite data gravity.",
            f"""
        <h2>The problem with “private mode” cloud chat</h2>
        <p>If tokens are produced in a data center, you are trusting retention policies, subprocessors, and account graphs. That can be fine for many tasks. It is the wrong tool for sensitive drafts, offline travel, or adversarial threat models.</p>
        <h2>What LlamaBox offers instead</h2>
        <ul>
          <li>Local GGUF models — you choose the weights</li>
          <li>No account required</li>
          <li>No telemetry by architecture</li>
          <li>Vision and TTS on device when models allow</li>
        </ul>
        <h2>Tradeoffs (read this)</h2>
        <p>You give up frontier-scale quality and speed. Phone CPUs are not H100s. Start small (0.5B–3B class quantizations) and upgrade models as RAM allows.</p>
        <h2>Fair comparison</h2>
        <p>See the full table on <a href="/vs-chatgpt.html">LlamaBox vs ChatGPT</a>.</p>
        {faq_html(faqs_priv)}
""",
        ),
        extra_head=faq_schema(faqs_priv),
    )

    faqs_gguf = [
        ("What is GGUF?", "GGUF is a file format for quantized LLM weights commonly used with llama.cpp. It packs tensors and metadata for efficient local loading."),
        ("Which quantization should I use?", "Q4_K_M is a strong default balance of quality and size for mobile. Smaller quants save RAM; larger improve quality if you have headroom."),
        ("Can I import my own GGUF?", "Yes — LlamaBox supports in-app downloads and local import workflows for models that fit device memory."),
    ]
    page(
        "gguf-android.html",
        "Run GGUF models on Android | LlamaBox + llama.cpp",
        "Run GGUF models on Android with LlamaBox. Q4_K_M tips, RAM guidance, llama.cpp stack, vision mmproj notes.",
        article(
            "GGUF",
            "Run GGUF models on Android.",
            "Builders already quantize for desktops. LlamaBox brings those GGUF files to arm64 phones without a cloud relay.",
            f"""
        <h2>Why GGUF on mobile</h2>
        <p>GGUF + llama.cpp is the de facto portable stack for local LLMs. Android arm64 can run the same ecosystem — carefully — with smaller models and honest thread counts.</p>
        <h2>Recommendations</h2>
        <ul>
          <li>Prefer <strong>Q4_K_M</strong> to start</li>
          <li>Match model size to free RAM (leave headroom for OS + UI)</li>
          <li>Context defaults to 2048 (configurable); vision may auto-raise</li>
          <li>Vision models need base GGUF + <strong>mmproj</strong></li>
        </ul>
        <h2>Workflow</h2>
        <ol>
          <li>Install LlamaBox beta</li>
          <li>Download from the in-app hub or import a local GGUF</li>
          <li>Load model · chat offline</li>
        </ol>
        <p>Deep stack notes: <a href="/architecture.html">architecture</a> · tutorial: <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a>.</p>
        {faq_html(faqs_gguf)}
""",
        ),
        extra_head=faq_schema(faqs_gguf),
    )

    faqs_how = [
        ("Do I need root?", "No. LlamaBox targets standard Android 7.0+ arm64 devices."),
        ("Why is generation slow?", "Phone CPUs are limited. Use smaller models, lower context, and close background apps. LlamaBox is CPU-only by design."),
        ("What if the app runs out of memory?", "Choose a smaller GGUF / heavier quantization, reduce context, and free RAM."),
    ]
    howto_schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "How to run an LLM on Android offline with LlamaBox",
    "description": "Install LlamaBox, load a GGUF model, and chat fully offline on Android.",
    "step": [
      {"@type": "HowToStep", "name": "Join the waitlist", "text": "Request closed beta access for Android 7.0+ arm64."},
      {"@type": "HowToStep", "name": "Install LlamaBox", "text": "Install the beta build for package com.llamabox."},
      {"@type": "HowToStep", "name": "Download or import a GGUF", "text": "Use the in-app hub or import a local Q4_K_M model that fits RAM."},
      {"@type": "HowToStep", "name": "Load the model", "text": "Open the model library, load weights, wait for initialization."},
      {"@type": "HowToStep", "name": "Chat offline", "text": "Enable airplane mode if you want — inference stays on-device."}
    ]
  }
  </script>
""" + faq_schema(faqs_how)

    page(
        "how-to-run-llm-on-android.html",
        "How to run an LLM on Android offline | LlamaBox guide",
        "Step-by-step: run an LLM on Android offline with LlamaBox. Install, load GGUF, chat without cloud. Troubleshooting tips included.",
        article(
            "Tutorial",
            "How to run an LLM on Android offline.",
            "Five practical steps. No root. No API keys for chat.",
            f"""
        <h2>Before you start</h2>
        <ul>
          <li>Android <strong>7.0+</strong>, <strong>arm64</strong></li>
          <li>Free storage for the model file</li>
          <li>Realistic expectations: CPU-only speeds</li>
        </ul>
        <h2>Steps</h2>
        <ol class="steps-ol">
          <li><strong>Join the beta</strong> — <a href="/waitlist.html">waitlist</a> for package <code>com.llamabox</code>.</li>
          <li><strong>Install</strong> the build you receive (status on <a href="/download.html">download</a>).</li>
          <li><strong>Get a GGUF</strong> — start small (0.5B–1B class Q4_K_M) via hub or import.</li>
          <li><strong>Load</strong> the model; wait through initialization (often 5–30s).</li>
          <li><strong>Chat offline</strong> — optional airplane mode to prove the loop is local.</li>
        </ol>
        <h2>Optional: vision</h2>
        <p>Pick a vision-capable model with mmproj. Attach a photo; encoding runs on-device (CPU path for UI stability).</p>
        <h2>Troubleshooting</h2>
        <ul>
          <li><strong>Slow tokens</strong> — smaller model, fewer threads contention, lower context</li>
          <li><strong>OOM / crash on load</strong> — smaller quant or model</li>
          <li><strong>Need network?</strong> — only for the download step</li>
        </ul>
        {faq_html(faqs_how)}
""",
        ),
        extra_head=howto_schema,
    )

    page(
        "vs-chatgpt.html",
        "LlamaBox vs ChatGPT | Offline private AI comparison",
        "LlamaBox vs ChatGPT: privacy, offline use, cost, speed, accounts. When to use on-device Android AI vs cloud chat.",
        article(
            "Compare",
            "LlamaBox vs ChatGPT.",
            "Different tools. Cloud intelligence versus local control.",
            """
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>ChatGPT (typical cloud)</th></tr></thead>
            <tbody>
              <tr><td>Inference location</td><td>On-device</td><td>Vendor cloud</td></tr>
              <tr><td>Works offline</td><td>Yes (after model download)</td><td>No</td></tr>
              <tr><td>Account required</td><td>No</td><td>Usually yes</td></tr>
              <tr><td>Telemetry / training use</td><td>None by design</td><td>Policy-dependent</td></tr>
              <tr><td>Model choice</td><td>Your GGUF files</td><td>Vendor models</td></tr>
              <tr><td>Peak quality / tools</td><td>Limited by phone</td><td>Frontier + tools</td></tr>
              <tr><td>Cost model</td><td>Free app + your hardware</td><td>Subscription / usage</td></tr>
              <tr><td>Best for</td><td>Privacy, offline, local experiments</td><td>Max capability online</td></tr>
            </tbody>
          </table>
        </div>
        <h2>Choose LlamaBox when</h2>
        <p>Transcripts must not leave the phone, airplane mode is required, or you want to run specific open weights.</p>
        <h2>Choose ChatGPT when</h2>
        <p>You need browsing tools, integrations, or frontier reasoning that phones cannot host.</p>
        <p>Also see <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a> and <a href="/vs-ollama.html">vs Ollama</a>.</p>
""",
        ),
    )

    page(
        "vs-ollama.html",
        "LlamaBox vs Ollama | Mobile local LLM vs desktop",
        "LlamaBox vs Ollama: Android on-device chat versus desktop/server local LLMs. Same GGUF world, different form factors.",
        article(
            "Compare",
            "LlamaBox vs Ollama.",
            "Both live in the local-GGUF universe. One is phone-native product UX; the other is the desktop/server operator’s toolkit.",
            """
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>Ollama (typical)</th></tr></thead>
            <tbody>
              <tr><td>Primary device</td><td>Android phone</td><td>Desktop / laptop / server</td></tr>
              <tr><td>UX</td><td>Mobile chat app</td><td>CLI + apps ecosystem</td></tr>
              <tr><td>Always with you</td><td>Yes</td><td>If the machine is with you</td></tr>
              <tr><td>Power envelope</td><td>Phone SoC / battery</td><td>Wall power / desktops often</td></tr>
              <tr><td>Model format</td><td>GGUF via llama.cpp stack</td><td>GGUF ecosystem</td></tr>
              <tr><td>Best for</td><td>Private pocket AI</td><td>Dev workflows, heavier local models</td></tr>
            </tbody>
          </table>
        </div>
        <p>Many builders will use <strong>both</strong>: Ollama on a workstation, LlamaBox on the phone. Related: <a href="/gguf-android.html">GGUF on Android</a>.</p>
""",
        ),
    )

    # --- blog ---
    posts = [
        (
            "2026-07-28-airplane-mode-ai.html",
            "2026-07-28",
            "ChatGPT in airplane mode: what actually works",
            "Cloud chat fails offline. Here is what on-device Android LLMs can and cannot do in airplane mode — and how LlamaBox approaches it.",
            """
        <p>Search “ChatGPT offline” and you will find workarounds, downloads of chat history, and disappointment. Frontier chat is a network product.</p>
        <p><strong>What works in airplane mode</strong> is a model that already lives on the device. LlamaBox loads GGUF weights and runs llama.cpp locally. After the file is on disk, radio silence is fine.</p>
        <h2>What still does not work offline</h2>
        <ul>
          <li>Downloading new models</li>
          <li>Web browsing tools inside a cloud assistant</li>
          <li>Frontier-scale reasoning that does not fit phone RAM</li>
        </ul>
        <h2>Practical setup</h2>
        <p>Follow <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a>, start with a small Q4_K_M model, then toggle airplane mode and keep chatting.</p>
""",
        ),
        (
            "2026-07-28-best-small-gguf-android.html",
            "2026-07-28",
            "Best small GGUF models for mid-range Android",
            "Model size guidance for mid-range phones: start tiny, measure RAM, then climb. Q4_K_M defaults and vision caveats.",
            """
        <p>Mid-range Android is not a 64 GB desktop. Treat model choice like packing a backpack.</p>
        <h2>Start here</h2>
        <ul>
          <li>Sub-1B to ~1B class instruct models in <strong>Q4_K_M</strong></li>
          <li>Examples people commonly try: Qwen2.5 0.5B-class, SmolLM2 360M-class (availability changes — verify licenses and cards)</li>
          <li>Leave headroom for the OS; do not fill RAM to the brim</li>
        </ul>
        <h2>Then scale</h2>
        <p>If load succeeds and tokens are usable, try larger instruct models carefully. Vision stacks need base + mmproj and more patience.</p>
        <p>Details: <a href="/gguf-android.html">GGUF on Android</a>.</p>
""",
        ),
        (
            "2026-07-28-vision-encoder-cpu.html",
            "2026-07-28",
            "Why we keep the vision encoder on CPU",
            "Engineering note: multimodal image encoding stays on CPU in LlamaBox so the UI remains responsive on every Android device.",
            """
        <p>Multimodal models tempt many mobile AI apps to reach for GPU acceleration. LlamaBox is CPU-only by design.</p>
        <p>Today LlamaBox runs text generation on CPU threads and keeps the <strong>vision encoder on CPU</strong> so the interface stays responsive under memory pressure. A frozen UI is a product bug, not a benchmark flex.</p>
        <h2>CPU-only scope</h2>
        <p>Keeping inference on CPU removes driver fragmentation and lets LlamaBox target the widest range of Android devices. Read <a href="/architecture.html">architecture</a> and <a href="/llms.txt">llms.txt</a>.</p>
""",
        ),
        (
            "2026-07-30-phone-faster-than-pc.html",
            "2026-07-30",
            "Phone vs PC for local LLMs: why fit beats raw power",
            "A desktop with a GPU should win on paper. In practice, the device that fits the workflow often wins. Why CPU-only Android can be the better tool.",
            """
        <p>A recent XDA piece made the observation that the author’s iPhone runs local LLMs faster than their gaming PC. It sounds wrong until you actually use both setups for real work.</p>
        <p>The desktop is faster on paper. The phone is faster in context. And context is where most LLM work actually happens.</p>
        <h2>The desktop is stretched, not slow</h2>
        <p>My desktop has a discrete GPU with finite VRAM, LM Studio open, a browser, Figma, Obsidian, and whatever else I need. If the 9B model I want to use does not fit entirely in VRAM, some layers get pushed to system RAM and CPU, and generation speed collapses. To keep the machine usable, I leave headroom, which means fewer GPU layers, which means slower tokens. The hardware is not the bottleneck — the multi-purpose workload is.</p>
        <h2>The phone is already focused</h2>
        <p>On a phone the model is the app. There is no browser battle for VRAM, no GPU layer slider to tune, no ten-second load because the app remembers the last model. You open it, type, and tokens appear. First-token latency often beats cloud chat because there is no network round-trip at all.</p>
        <p>Modern small models are also built for this. A 0.5B–1B Q4_K_M model is not a brute-forced desktop weights file; it is a smartphone deployment target. Quality has compressed faster than the parameter count suggests.</p>
        <h2>This applies to Android too — without GPU</h2>
        <p>The XDA example uses an iPhone with Metal and unified memory. That is one path. LlamaBox takes a different one: <strong>CPU-only on Android</strong>. No GPU dependency means it runs on mid-range devices, old flagships, and budget phones that have no usable compute driver path at all. The trade-off is smaller models and modest tok/s, but the <em>fit</em> is the same: the device you already have, the workflow you are already in, no setup tax.</p>
        <h2>Honest limits</h2>
        <ul>
          <li>Context length fills up fast on small models</li>
          <li>Sustained generation can thermal-throttle</li>
          <li>Heavy reasoning or document parsing still belongs on a desktop with RAM to spare</li>
        </ul>
        <h2>The real comparison</h2>
        <p>The phone does not beat the PC at everything. It beats the PC at the small, frequent, interruptible tasks that make up most LLM use: rephrase this, summarize that, draft a reply, check this claim. The tool you reach for is the one that removes friction, not the one with the best benchmark.</p>
        <p>LlamaBox is built for that reach. Download a small GGUF, load it once, and the model stays in your pocket — no gaming PC required.</p>
""",
        ),
    ]

    blog_cards = []
    for fname, date, title, desc, body in posts:
        page(
            f"blog/{fname}",
            f"{title} | LlamaBox Blog",
            desc,
            article("Blog · " + date, title, desc, body + '<p class="post-nav"><a href="/blog/">← All posts</a></p>'),
        )
        blog_cards.append(
            f'<a class="card-link glass" href="/blog/{fname}"><strong>{title}</strong><span>{date} · {desc[:90]}…</span></a>'
        )

    page(
        "blog/index.html",
        "LlamaBox Blog | Offline AI, GGUF, Android engineering",
        "LlamaBox blog: offline AI on Android, small GGUF models, on-device vision engineering, and product updates.",
        article(
            "Blog",
            "Notes from on-device AI.",
            "Short, citable posts for builders and privacy-first users.",
            f'<div class="card-links">{"".join(blog_cards)}</div>',
        ),
    )

    # sitemap
    urls = [
        ("/", "1.0", "weekly"),
        ("/architecture.html", "0.85", "monthly"),
        ("/architecture.md", "0.7", "monthly"),
        ("/privacy.html", "0.5", "yearly"),
        ("/waitlist.html", "0.9", "weekly"),
        ("/download.html", "0.9", "weekly"),
        ("/guides.html", "0.85", "weekly"),
        ("/offline-ai-android.html", "0.85", "weekly"),
        ("/on-device-llm.html", "0.85", "weekly"),
        ("/private-chatgpt-alternative.html", "0.85", "weekly"),
        ("/gguf-android.html", "0.85", "weekly"),
        ("/how-to-run-llm-on-android.html", "0.9", "weekly"),
        ("/vs-chatgpt.html", "0.8", "monthly"),
        ("/vs-ollama.html", "0.8", "monthly"),
        ("/blog/", "0.75", "weekly"),
        ("/blog/2026-07-28-airplane-mode-ai.html", "0.7", "monthly"),
        ("/blog/2026-07-28-best-small-gguf-android.html", "0.7", "monthly"),
        ("/blog/2026-07-28-vision-encoder-cpu.html", "0.7", "monthly"),
        ("/blog/2026-07-30-phone-faster-than-pc.html", "0.7", "monthly"),
        ("/llms.txt", "0.6", "monthly"),
        ("/llms-full.txt", "0.6", "monthly"),
    ]
    lastmod = "2026-07-30"
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri, freq in urls:
        sm.append("  <url>")
        sm.append(f"    <loc>{BASE}{loc if loc != '/' else '/'}</loc>")
        sm.append(f"    <lastmod>{lastmod}</lastmod>")
        sm.append(f"    <changefreq>{freq}</changefreq>")
        sm.append(f"    <priority>{pri}</priority>")
        sm.append("  </url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
