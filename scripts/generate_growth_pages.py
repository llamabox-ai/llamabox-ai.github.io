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
            <li><a href="/private-ai-android.html">Private AI Android</a></li>
            <li><a href="/chatgpt-android-offline.html">ChatGPT offline</a></li>
            <li><a href="/gguf-android.html">GGUF on Android</a></li>
            <li><a href="/llm-download.html">LLM download</a></li>
            <li><a href="/models.html">Model hub</a></li>
            <li><a href="/what-is-an-llm.html">What is an LLM?</a></li>
            <li><a href="/free-llms.html">Free LLMs</a></li>
            <li><a href="/how-to-run-llm-on-android.html">How-to guide</a></li>
            <li><a href="/vs-chatgpt.html">vs ChatGPT</a></li>
            <li><a href="/vs-ollama.html">vs Ollama</a></li>
            <li><a href="/vs-pocketpal.html">vs PocketPal AI</a></li>
            <li><a href="/vs-mlc-llm.html">vs MLC LLM</a></li>
            <li><a href="/best-local-llm-apps-android.html">Best local LLM apps</a></li>
            <li><a href="/blog/">Blog</a></li>
          </ul>
        </div>
        <div>
          <h4>Business</h4>
          <ul>
            <li><a href="/enterprise.html">Enterprise</a></li>
            <li><a href="/commercial-license.html">Commercial license</a></li>
            <li><a href="/partners.html">Partners</a></li>
            <li><a href="/investors.html">Investors &amp; acquisitions</a></li>
            <li><a href="/press-kit.html">Press kit</a></li>
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
          <label>Company / organization (optional)
            <input type="text" name="company" placeholder="e.g. Mythos Labs">
          </label>
          <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;margin:0.75rem 0">
            <input type="checkbox" name="commercial_interest" value="yes">
            <span>I’m interested in commercial / enterprise use</span>
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
          <a class="card-link glass" href="/private-ai-android.html"><strong>Private AI for Android</strong><span>Local AI chatbot with no cloud</span></a>
          <a class="card-link glass" href="/chatgpt-android-offline.html"><strong>ChatGPT Android offline</strong><span>Why cloud ChatGPT can’t, and what does</span></a>
          <a class="card-link glass" href="/gguf-android.html"><strong>GGUF on Android</strong><span>Quantizations, RAM, imports</span></a>
          <a class="card-link glass" href="/llm-download.html"><strong>LLM download</strong><span>Get GGUF models for Android</span></a>
          <a class="card-link glass" href="/models.html"><strong>Model hub</strong><span>GGUF models that run on Android</span></a>
          <a class="card-link glass" href="/what-is-an-llm.html"><strong>What is an LLM?</strong><span>Explained for Android local use</span></a>
          <a class="card-link glass" href="/free-llms.html"><strong>Free LLMs</strong><span>Open models you can run locally</span></a>
          <a class="card-link glass" href="/how-to-run-llm-on-android.html"><strong>How to run an LLM on Android</strong><span>Step-by-step tutorial</span></a>
          <a class="card-link glass" href="/vs-chatgpt.html"><strong>LlamaBox vs ChatGPT</strong><span>Honest comparison table</span></a>
          <a class="card-link glass" href="/vs-ollama.html"><strong>LlamaBox vs Ollama</strong><span>Phone-native vs desktop local</span></a>
          <a class="card-link glass" href="/vs-pocketpal.html"><strong>LlamaBox vs PocketPal AI</strong><span>Two offline Android LLM apps compared</span></a>
          <a class="card-link glass" href="/vs-mlc-llm.html"><strong>LlamaBox vs MLC LLM</strong><span>Chat app vs model compiler</span></a>
          <a class="card-link glass" href="/best-local-llm-apps-android.html"><strong>Best local LLM apps Android</strong><span>2026 comparison of on-device chat apps</span></a>
          <a class="card-link glass" href="/blog/"><strong>Blog</strong><span>Models, engineering notes, updates</span></a>
          <a class="card-link glass" href="/enterprise.html"><strong>Enterprise</strong><span>Offline AI for teams and organizations</span></a>
          <a class="card-link glass" href="/commercial-license.html"><strong>Commercial license</strong><span>Use LlamaBox in proprietary products</span></a>
          <a class="card-link glass" href="/partners.html"><strong>Partners</strong><span>OEMs, model authors, distributors</span></a>
          <a class="card-link glass" href="/investors.html"><strong>Investors &amp; acquisitions</strong><span>Strategic conversations welcome</span></a>
        </div>
""",
        ),
    )

    faqs_offline = [
        ("What is offline AI on Android?", "Offline AI means the model runs on the phone. After the model file is stored locally, chat works without a network — including airplane mode."),
        ("Is LlamaBox fully offline?", "Inference is fully offline. Optional internet is only for downloading models from public hubs like Hugging Face."),
        ("Does offline mean private?", "On-device inference means prompts and completions never hit a vendor server. LlamaBox adds no accounts or telemetry on top of that architecture."),
        ("What is the best offline AI assistant for Android?", "The best offline AI assistant keeps inference on-device, supports open GGUF models, and needs no cloud account. LlamaBox is built exactly for that: local chat, vision, and TTS on Android 7.0+ arm64."),
        ("Can ChatGPT work offline on Android?", "No. ChatGPT and other cloud assistants need an internet connection. LlamaBox is an offline ChatGPT alternative that runs the model directly on your phone."),
    ]
    page(
        "offline-ai-android.html",
        "Offline AI Android: Best Local LLM Chat Assistant | LlamaBox",
        "Looking for the best offline AI assistant for Android? LlamaBox runs local LLMs on-device — no internet, no cloud, no accounts. Private chat in airplane mode.",
        article(
            "Offline AI",
            "Offline AI for Android.",
            "The best offline AI assistant is the one that works when the network does not. LlamaBox runs local LLMs on your phone — private, account-free, and airplane-mode ready.",
            f"""
        <h2>What “offline AI Android” actually means</h2>
        <p>Offline AI on Android is a chat assistant that loads a language model onto the phone and runs inference locally. Once the model file is stored, you can chat without Wi-Fi, mobile data, or a cloud account. For journalists, travelers, students, field workers, and privacy-conscious users, that changes everything.</p>
        <h2>How LlamaBox delivers offline AI</h2>
        <ul>
          <li>GGUF models via <strong>llama.cpp</strong> (through llama.rn on React Native)</li>
          <li><strong>CPU-only</strong> inference by design — works on broad Android 7.0+ arm64 hardware</li>
          <li>No account graph, no cloud inference endpoint, no telemetry</li>
          <li>Optional vision with on-device multimodal models + mmproj</li>
          <li>Local history in SQLite, TTS readback, and system monitoring</li>
        </ul>
        <h2>LlamaBox vs other offline AI Android options</h2>
        <p>Several apps claim offline AI on Android. Here is how LlamaBox compares to the most-discussed alternatives:</p>
        <ul>
          <li><strong>Layla</strong> — private offline assistant for Android and iOS. LlamaBox differentiates with open-source GGUF weights, no vendor lock-in, and a CPU-only stack that targets older devices.</li>
          <li><strong>Local AI</strong> (Google Play) — closed, store-distributed app. LlamaBox gives you model choice, local import, and full source transparency under AGPL-3.0 plus commercial licensing.</li>
          <li><strong>OfflineLLM</strong> — open-source Android project. LlamaBox adds React Native portability, vision support, and a productized beta path for enterprises and OEMs.</li>
          <li><strong>MeetAITools roundups</strong> — directory-style lists. LlamaBox is a real product, not a review farm, with direct downloads and an open GitHub organization.</li>
        </ul>
        <h2>What works without internet</h2>
        <ul>
          <li>Chat completions once a model is installed</li>
          <li>History, settings, system monitor</li>
          <li>Vision on local images with a compatible model + mmproj</li>
          <li>TTS readback of local answers</li>
        </ul>
        <h2>What still needs a network (optional)</h2>
        <p>Downloading a GGUF the first time. After that, disconnect freely — including airplane mode.</p>
        <h2>Who this is for</h2>
        <p>Privacy-first users, journalists, students, builders testing GGUF on real silicon, and anyone who wants ChatGPT-like chat without shipping transcripts to a data center.</p>
        <p>Related: <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a> · <a href="/on-device-llm.html">on-device LLM</a> · <a href="/how-to-run-llm-on-android.html">how-to</a> · <a href="/vs-chatgpt.html">vs ChatGPT</a> · <a href="/vs-pocketpal.html">vs PocketPal AI</a>.</p>
        {faq_html(faqs_offline)}
""",
        ),
        extra_head=faq_schema(faqs_offline),
    )

    faqs_od = [
        ("What is on-device AI?", "On-device AI runs machine learning inference directly on the user’s hardware — in LlamaBox’s case, an Android phone — instead of sending data to a cloud API."),
        ("What is an on-device LLM?", "A language model that runs inference on the user’s hardware — here, an Android phone — rather than on a remote API server."),
        ("Is on-device AI the same as offline AI?", "Almost. On-device AI is local by architecture; if the model and app are fully self-contained, it also works offline. LlamaBox is both."),
        ("Is on-device slower?", "Usually yes versus frontier cloud APIs. Small Q4_K_M models on mid-range phones often land in a few tokens/sec. LlamaBox publishes honest ranges, not theater."),
        ("Does on-device AI require special hardware?", "No. LlamaBox runs on standard Android CPUs with ARM NEON. No GPU, NPU, or datacenter hardware is needed."),
        ("Why is on-device AI more private?", "Your prompts and generated answers never leave the device. There is no vendor inference endpoint, so there is no vendor retention policy or subprocessor list to trust."),
    ]
    page(
        "on-device-llm.html",
        "On-Device AI on Android | Local LLM with LlamaBox",
        "On-device AI for Android: run a local LLM directly on your phone. LlamaBox loads GGUF models with llama.cpp — private, offline, no cloud inference.",
        article(
            "On-device AI",
            "On-device AI: the LLM runs on your phone.",
            "“On-device” is not a marketing synonym for “mobile app.” It means the model weights and inference run where you are — on the Android SoC, not in a data center.",
            f"""
        <h2>What is on-device AI?</h2>
        <p><strong>On-device AI</strong> means machine-learning inference happens locally on the user’s hardware. For LlamaBox, that is your Android phone running a quantized LLM through llama.cpp. The forward pass, the chat history, and the generated text all stay inside the app process.</p>
        <h2>From on-device AI to on-device LLM</h2>
        <p>An <strong>on-device LLM</strong> is the text-generation subset of on-device AI. Instead of calling ChatGPT, Gemini, or Claude over the network, you load a GGUF file into app memory and run inference on the phone CPU. The device becomes the AI endpoint.</p>
        <h2>Stack (short)</h2>
        <ul>
          <li>React Native 0.81 (New Architecture)</li>
          <li>llama.rn wrapping llama.cpp</li>
          <li>GGUF (Q4_K_M recommended)</li>
          <li>Zustand + SQLite + AsyncStorage</li>
        </ul>
        <h2>Privacy property</h2>
        <p>If generation never leaves the process, you do not need to “trust a privacy policy” for that step — you can reason about the architecture. See <a href="/architecture.html">architecture</a> and <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a>.</p>
        <h2>Performance expectations</h2>
        <p>Mid-range phones with ~1B Q4_K_M models: roughly 1–5 tok/s prompt processing and 2–8 tok/s generation (device dependent). Load times 5–30s. Peak memory often ~0.5–2 GB for small models.</p>
        <h2>Use cases for on-device AI on Android</h2>
        <ul>
          <li>Private drafts and journaling without cloud retention</li>
          <li>Offline travel, field work, and low-connectivity environments</li>
          <li>Sensitive professional notes (healthcare, legal, journalism, research)</li>
          <li>Air-gapped or policy-controlled environments</li>
        </ul>
        <p>Next: <a href="/gguf-android.html">GGUF guide</a> · <a href="/offline-ai-android.html">offline AI</a> · <a href="/vs-ollama.html">Ollama Android alternative</a>.</p>
        {faq_html(faqs_od)}
""",
        ),
        extra_head=faq_schema(faqs_od),
    )

    faqs_priv = [
        ("Is LlamaBox a private ChatGPT alternative for Android?", "Yes. It offers chat UX for local models on Android and does not call OpenAI or any cloud inference API."),
        ("Can a private AI chatbot really run on Android?", "Yes. LlamaBox loads a quantized GGUF model into app memory and runs inference on the phone CPU. No server sees your prompts."),
        ("When should I still use ChatGPT?", "When you need frontier reasoning, tools, browsing, or speed that phone CPUs cannot match. Use LlamaBox when locality and privacy dominate."),
        ("Does private mean encrypted to a vendor?", "LlamaBox’s privacy story is stronger: no vendor inference path. Data stays on-device by design."),
    ]
    page(
        "private-chatgpt-alternative.html",
        "Private ChatGPT Alternative Android | LlamaBox Local AI Chatbot",
        "Looking for a private ChatGPT alternative for Android? LlamaBox is a local AI chatbot that runs offline — no cloud inference, no accounts, no telemetry.",
        article(
            "Private alternative",
            "Private ChatGPT alternative for Android.",
            "A private AI chatbot that runs on your phone, not in someone else's data center. LlamaBox keeps prompts, answers, and history local.",
            f"""
        <h2>Why users want a private ChatGPT alternative on Android</h2>
        <p>Cloud assistants are brilliant and extractive. Even “private mode” sends tokens to a vendor server, which means retention policies, subprocessors, and account graphs still apply. For sensitive drafts, offline travel, healthcare notes, journalism sources, or adversarial threat models, the right answer is a <strong>private AI chatbot</strong> that runs inference locally on the phone.</p>
        <h2>What LlamaBox offers</h2>
        <ul>
          <li>Local GGUF models — you choose the weights, not the vendor</li>
          <li>No account required, no cloud inference endpoint</li>
          <li>No telemetry by architecture; prompts never leave the device</li>
          <li>Vision and TTS on device when models allow</li>
          <li>Open source under AGPL-3.0 plus a separate commercial license for OEMs and enterprises</li>
        </ul>
        <h2>How LlamaBox compares to other private ChatGPT alternatives</h2>
        <p>Privacy-focused users often compare these options. LlamaBox is the only one built specifically for offline, open-weight chat on Android:</p>
        <ul>
          <li><strong>Proton AI / Lumo</strong> — privacy-first, but still cloud-hosted. LlamaBox removes the server entirely.</li>
          <li><strong>Privacy Guides recommendations</strong> — excellent editorial list. LlamaBox matches their criteria: open source, local inference, no account.</li>
          <li><strong>Lindy / Wondertools mobile AI roundups</strong> — comparison blogs. LlamaBox belongs in these lists because it is a real, shipping Android app, not a wrapper around a remote API.</li>
        </ul>
        <h2>Tradeoffs (read this)</h2>
        <p>You give up frontier-scale quality and speed. Phone CPUs are not H100s. Start small (0.5B–3B class quantizations) and upgrade models as RAM allows. The trade is control and privacy for raw capability.</p>
        <h2>Fair comparison</h2>
        <p>See the full table on <a href="/vs-chatgpt.html">LlamaBox vs ChatGPT</a>. Also see <a href="/offline-ai-android.html">offline AI Android</a> and <a href="/on-device-llm.html">on-device LLM</a>.</p>
        {faq_html(faqs_priv)}
""",
        ),
        extra_head=faq_schema(faqs_priv),
    )

    faqs_private_ai = [
        ("What is private AI on Android?", "Private AI on Android means the language model runs inference directly on your phone instead of sending prompts to a vendor server. Your data never leaves the device."),
        ("Is LlamaBox a private AI chatbot for Android?", "Yes. LlamaBox loads a quantized GGUF model into app memory and runs it on the phone CPU. There is no cloud inference endpoint, account, or telemetry."),
        ("How is local AI more private than cloud 'private mode'?", "Cloud 'private mode' still sends tokens to a server with retention policies and subprocessors. Local AI removes the server from the chat path entirely."),
        ("Can private AI work offline?", "Yes. Once a model is downloaded, LlamaBox works in airplane mode. Private AI and offline AI are the same architecture here."),
        ("What models can I use with LlamaBox?", "Any GGUF model that fits your phone's RAM. Start with small Q4_K_M quantizations (0.5B–3B class) and scale up on devices with more memory."),
        ("Is LlamaBox open source?", "The public codebase will be released under AGPL-3.0 when the closed beta ends. A separate commercial license is available for proprietary use."),
    ]
    page(
        "private-ai-android.html",
        "Private AI for Android | Offline AI Chatbot | LlamaBox",
        "Get private AI on Android with LlamaBox. Local LLM chatbot runs offline on your phone — no cloud, no account, no data sharing.",
        article(
            "Private AI",
            "Private AI for Android.",
            "A private AI chatbot that runs on your phone, not in someone else's cloud. LlamaBox keeps prompts, answers, and history on-device.",
            f"""
        <h2>What is private AI on Android?</h2>
        <p><strong>Private AI on Android</strong> means the large language model runs inference directly on your phone. Your prompts, generated answers, and chat history never leave the device. There is no cloud API call, no vendor retention policy, and no account graph to trust.</p>
        <h2>Why local beats cloud "private mode"</h2>
        <p>Many chatbots offer a "private mode," but that usually means the vendor promises not to train on your data. The prompts still travel to a server, are subject to subpoenas and breaches, and rely on a privacy policy you cannot verify. LlamaBox removes the server from the path entirely.</p>
        <ul>
          <li><strong>Cloud private mode:</strong> data is encrypted in transit and stored under a vendor policy.</li>
          <li><strong>LlamaBox local AI:</strong> data never leaves the device. The architecture is the privacy guarantee.</li>
        </ul>
        <h2>How LlamaBox keeps AI private</h2>
        <ul>
          <li>GGUF models load into app memory and run via llama.cpp on the phone CPU</li>
          <li>No account required and no telemetry by architecture</li>
          <li>Works offline after model download — airplane mode included</li>
          <li>Open source under AGPL-3.0 (public release after closed beta)</li>
          <li>Commercial license available for closed-source deployments</li>
        </ul>
        <h2>LlamaBox vs other private AI options</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>Cloud private mode</th><th>Other local apps</th></tr></thead>
            <tbody>
              <tr><td>Runs on Android phone</td><td>Yes — native app</td><td>Web/app wrapper</td><td>Varies</td></tr>
              <tr><td>Prompts leave device</td><td>No</td><td>Yes</td><td>Usually no</td></tr>
              <tr><td>Works offline</td><td>Yes</td><td>No</td><td>Sometimes</td></tr>
              <tr><td>Open weights / GGUF</td><td>Yes</td><td>Vendor model</td><td>Sometimes</td></tr>
              <tr><td>No account required</td><td>Yes</td><td>No</td><td>Varies</td></tr>
            </tbody>
          </table>
        </div>
        <h2>Use cases for private AI on Android</h2>
        <ul>
          <li><strong>Personal journaling and drafting</strong> — no cloud retention of intimate notes</li>
          <li><strong>Healthcare and therapy notes</strong> — local inference reduces compliance surface area</li>
          <li><strong>Journalism and sensitive sourcing</strong> — sources and drafts stay on-device</li>
          <li><strong>Legal and finance drafts</strong> — client-confidential material never touches a vendor</li>
          <li><strong>Travel and field work</strong> — private AI that works without internet</li>
        </ul>
        <h2>How to start</h2>
        <ol>
          <li>Join the LlamaBox beta waitlist for APK or Play Store access.</li>
          <li>Download a small GGUF model (0.5B–3B Q4_K_M) over Wi-Fi.</li>
          <li>Chat offline. No API key, no account, no cloud.</li>
        </ol>
        <p>Related: <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a> · <a href="/offline-ai-android.html">offline AI Android</a> · <a href="/on-device-llm.html">on-device AI</a> · <a href="/vs-chatgpt.html">vs ChatGPT</a> · <a href="/best-local-llm-apps-android.html">best local LLM apps</a>.</p>
        {faq_html(faqs_private_ai)}
""",
        ),
        extra_head=faq_schema(faqs_private_ai),
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

    faqs_models = [
        ("What GGUF models work on Android?", "Smaller quantized models generally work. Start with 0.5B–3B class Q4_K_M weights. Vision models need a base GGUF plus an mmproj file. LlamaBox detects presets from filename hints."),
        ("Can I run Llama 3 on Android?", "Yes, if you use a small enough GGUF quantization (for example a 1B–3B parameter variant). Larger 8B+ models usually need more RAM than mid-range phones offer."),
        ("What is the best model for offline chat on a phone?", "For most users, Qwen2.5 1.5B Q4_K_M or SmolLM2 360M/1.7B Q4_K_M are strong starting points: small, fast, and capable enough for drafting and问答."),
        ("How much RAM does a model need?", "A good rule of thumb: the GGUF file size plus 200 MB–1 GB runtime/KV overhead. A 1 GB model can run on a 4–6 GB RAM phone if background apps are closed."),
        ("Where do I download models?", "Use the LlamaBox in-app model hub, or import GGUF files you download from Hugging Face and other model hubs."),
    ]
    page(
        "models.html",
        "GGUF Models for Android | Local LLM Model Hub | LlamaBox",
        "Browse GGUF models that run locally on Android with LlamaBox. Small LLMs, vision models, RAM guidance, and quantization tips for on-device AI.",
        article(
            "Models",
            "GGUF models that run on Android.",
            "A practical index of local LLM models for Android phones. Quantized GGUF weights, RAM estimates, and what works offline with LlamaBox.",
            f"""
        <h2>What is the LlamaBox model hub?</h2>
        <p>The model hub inside LlamaBox is a curated list of GGUF models that fit Android phones. Each entry includes recommended quantization, estimated RAM use, and whether the model supports vision or TTS. You can download directly in the app or import a GGUF you already have.</p>
        <h2>Quick-start model picks</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th>Model family</th><th>Size class</th><th>Best for</th><th>Approx. RAM</th><th>Vision</th></tr></thead>
            <tbody>
              <tr><td>Qwen2.5-Instruct</td><td>0.5B–3B Q4_K_M</td><td>General chat, drafting, coding help</td><td>0.5–2 GB</td><td>No</td></tr>
              <tr><td>SmolLM2</td><td>360M–1.7B Q4_K_M</td><td>Fast answers on low-RAM phones</td><td>0.3–1 GB</td><td>No</td></tr>
              <tr><td>Gemma 3 4B IT</td><td>4B Q4_K_M</td><td>Balanced quality on 8GB+ phones</td><td>1.5–3 GB</td><td>Yes (with mmproj)</td></tr>
              <tr><td>MiniCPM-V / InternVL2</td><td>2B–4B Q4_K_M</td><td>On-device image understanding</td><td>1.5–3 GB</td><td>Yes (with mmproj)</td></tr>
            </tbody>
          </table>
        </div>
        <p>These are starting points, not guarantees. Real performance depends on free RAM, Android version, background apps, and the exact quantization. LlamaBox shows honest load-time and tok/s ranges per device.</p>
        <h2>How to choose a quantization</h2>
        <ul>
          <li><strong>Q4_K_M</strong> — best default for mobile. Good quality at roughly half the float16 size.</li>
          <li><strong>Q5_K_M / Q6_K</strong> — slightly better quality if you have RAM headroom.</li>
          <li><strong>Q3_K_M / Q2_K</strong> — smaller but quality drops noticeably; use only when RAM is tight.</li>
        </ul>
        <h2>Vision models need an mmproj</h2>
        <p>Vision-capable GGUF models also need a matching multimodal projector file (mmproj). LlamaBox pairs base and mmproj automatically when they share a filename prefix. See <a href="/gguf-android.html">GGUF on Android</a> for naming conventions.</p>
        <h2>Where to get GGUF models</h2>
        <ul>
          <li><a href="https://huggingface.co" rel="noopener">Hugging Face</a> — largest collection of quantized models</li>
          <li><a href="https://huggingface.co/models?library=gguf" rel="noopener">GGUF model catalog</a> — filter by GGUF format</li>
          <li>In-app LlamaBox model hub (curated for Android RAM limits)</li>
        </ul>
        <p>Next: <a href="/llm-download.html">LLM download guide</a> · <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/gguf-android.html">GGUF on Android</a>.</p>
        {faq_html(faqs_models)}
""",
        ),
        extra_head=faq_schema(faqs_models),
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

    faqs_what_llm = [
        ("What is an LLM in AI?", "A Large Language Model (LLM) is a neural network trained to predict and generate human-like text. It can answer questions, draft prose, summarize, translate, and help with code based on patterns learned from training data."),
        ("What is a local LLM?", "A local LLM runs on your own hardware instead of a remote API. With LlamaBox, the model file lives on your Android phone and inference happens on the device CPU."),
        ("Can you run an LLM on Android?", "Yes. Quantized GGUF models — especially small 0.5B–3B parameter versions — can run on Android phones with enough free RAM. LlamaBox is built specifically for this."),
        ("What does quantization mean?", "Quantization reduces the number of bits used to store model weights, shrinking file size and RAM use. Q4_K_M is a common mobile-friendly format that balances quality and speed."),
        ("Why run an LLM locally on a phone?", "Local inference keeps prompts and answers private, works offline, needs no account, and avoids API costs or rate limits. The tradeoff is smaller models and phone-class speed."),
    ]
    page(
        "what-is-an-llm.html",
        "What is an LLM? | Local LLM on Android Explained | LlamaBox",
        "What is an LLM? Learn what Large Language Models are and how LlamaBox runs them locally on Android — private, offline, no cloud inference.",
        article(
            "Explain",
            "What is an LLM?",
            "Large Language Models power ChatGPT, Claude, and Gemini. LlamaBox brings the same idea to your Android phone — locally.",
            f"""
        <h2>LLM definition (simple)</h2>
        <p>An <strong>LLM (Large Language Model)</strong> is a machine-learning model trained on a huge corpus of text. It learns to predict the next token — roughly, the next word or sub-word — and in doing so it learns to answer questions, write, summarize, translate, and help with code.</p>
        <p>Examples you may know: GPT-4, Claude, Gemini, Llama, Qwen, Mistral. Most people interact with them through cloud chat apps. LlamaBox lets you run compatible open-weight models directly on an Android phone.</p>
        <h2>From cloud LLM to local LLM</h2>
        <p>A <strong>local LLM</strong> is the same kind of model, but the file is stored on your device and inference happens on your hardware. LlamaBox loads a quantized GGUF file into app memory and runs it with llama.cpp on the phone CPU. Nothing is sent to a chat API.</p>
        <h2>Key terms</h2>
        <ul>
          <li><strong>Parameters</strong> — the "size" of a model, often 0.5B, 1B, 3B, 7B, etc. More parameters usually means more capability but more RAM and slower inference.</li>
          <li><strong>Quantization</strong> — compressing weights to fewer bits. Q4_K_M is a popular mobile format that keeps most quality while cutting size roughly in half versus float16.</li>
          <li><strong>GGUF</strong> — the file format used by llama.cpp to store quantized model weights and metadata.</li>
          <li><strong>Context window</strong> — how many tokens the model can "remember" at once. LlamaBox defaults to 2048.</li>
        </ul>
        <h2>What can a local LLM on Android do?</h2>
        <ul>
          <li>Draft notes, messages, and journal entries offline</li>
          <li>Answer questions without sending data to a vendor</li>
          <li>Summarize text you paste into the app</li>
          <li>Help with coding questions in offline environments</li>
          <li>Analyze images with a vision-capable model + mmproj</li>
        </ul>
        <h2>Tradeoffs vs cloud chatbots</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>Cloud LLM (ChatGPT, etc.)</th><th>Local LLM on Android (LlamaBox)</th></tr></thead>
            <tbody>
              <tr><td>Data leaves device</td><td>Yes</td><td>No</td></tr>
              <tr><td>Works offline</td><td>No</td><td>Yes</td></tr>
              <tr><td>Requires account</td><td>Usually yes</td><td>No</td></tr>
              <tr><td>Model size</td><td>Huge frontier models</td><td>Small quantized models (0.5B–4B)</td></tr>
              <tr><td>Speed</td><td>Fast (datacenter GPUs)</td><td>Slower (phone CPU)</td></tr>
              <tr><td>Cost after setup</td><td>Subscription / per-token</td><td>Free (open weights)</td></tr>
            </tbody>
          </table>
        </div>
        <p>Next: <a href="/models.html">GGUF models for Android</a> · <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/free-llms.html">free LLMs you can run locally</a> · <a href="/offline-ai-android.html">offline AI Android</a>.</p>
        {faq_html(faqs_what_llm)}
""",
        ),
        extra_head=faq_schema(faqs_what_llm),
    )

    faqs_free_llms = [
        ("Are there free LLMs I can run locally?", "Yes. Many open-weight LLMs are released under permissive licenses and can be downloaded as GGUF files for free. You pay only with your own device RAM and electricity."),
        ("What is the best free LLM for Android?", "For Android phones, small Q4_K_M models like Qwen2.5 1.5B, SmolLM2 1.7B, and Gemma 3 4B are popular free options that balance capability and RAM use."),
        ("Do free local LLMs need an API key?", "No. Once you download the GGUF model file, inference is local. There is no API key, subscription, or token metering."),
        ("Can free LLMs match ChatGPT?", "Not in raw capability. Free local models are smaller and run on phone CPUs. They excel at privacy, offline use, and cost — not at frontier reasoning or tool use."),
        ("Where can I download free LLMs?", "Hugging Face hosts the largest catalog of GGUF models. LlamaBox also includes an in-app hub with curated, Android-tested models."),
    ]
    page(
        "free-llms.html",
        "Free LLMs You Can Run Locally on Android | LlamaBox",
        "Discover free LLMs that run locally on Android with LlamaBox. Open-weight GGUF models, no API keys, no subscriptions, private offline chat.",
        article(
            "Free LLMs",
            "Free LLMs you can run locally.",
            "The best price for local AI is zero. These open-weight models run on Android phones with LlamaBox — no account, no cloud, no meter.",
            f"""
        <h2>Why free LLMs matter</h2>
        <p>Open-weight LLMs let anyone download the model weights and run them locally. There is no per-token bill, no subscription gate, and no vendor sees your prompts. For Android users, that means a free, private AI chatbot that works offline after the model file is on the device.</p>
        <h2>Best free LLMs for Android (2026)</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th>Model</th><th>Size class</th><th>Best for</th><th>Approx. RAM</th><th>License</th></tr></thead>
            <tbody>
              <tr><td>Qwen2.5-Instruct</td><td>0.5B–3B Q4_K_M</td><td>General chat, coding help</td><td>0.5–2 GB</td><td>Apache 2.0 / Qwen License</td></tr>
              <tr><td>SmolLM2</td><td>360M–1.7B Q4_K_M</td><td>Fast answers on low-RAM phones</td><td>0.3–1 GB</td><td>Apache 2.0</td></tr>
              <tr><td>Gemma 3 4B IT</td><td>4B Q4_K_M</td><td>Balanced quality, vision capable</td><td>1.5–3 GB</td><td>Gemma Terms of Use</td></tr>
              <tr><td>Llama 3.2 Instruct</td><td>1B–3B Q4_K_M</td><td>General instruction following</td><td>0.5–2 GB</td><td>Llama 3.2 License</td></tr>
              <tr><td>Phi-3 / Phi-4 Mini</td><td>3.8B Q4_K_M</td><td>Strong reasoning for the size</td><td>1.5–2.5 GB</td><td>MIT</td></tr>
            </tbody>
          </table>
        </div>
        <p>Always check the exact license for each GGUF upload before commercial use. License terms apply to the weights, not to LlamaBox itself.</p>
        <h2>How to run these free LLMs on Android</h2>
        <ol>
          <li>Install LlamaBox from the waitlist or Play Store beta.</li>
          <li>Open the in-app model hub or import a GGUF from Hugging Face.</li>
          <li>Load the model and chat. No API key needed.</li>
        </ol>
        <h2>Free LLMs vs free cloud chatbots</h2>
        <ul>
          <li><strong>Free cloud tiers</strong> (ChatGPT, Claude, Gemini) are free to the user but still send your data to a vendor server.</li>
          <li><strong>Free local LLMs</strong> are free and keep everything on your device. The cost is device RAM and some setup time.</li>
        </ul>
        <p>Related: <a href="/models.html">model hub</a> · <a href="/llm-download.html">LLM download</a> · <a href="/how-to-run-llm-on-android.html">how-to guide</a> · <a href="/what-is-an-llm.html">what is an LLM</a>.</p>
        {faq_html(faqs_free_llms)}
""",
        ),
        extra_head=faq_schema(faqs_free_llms),
    )

    page(
        "how-to-run-llm-on-android.html",
        "How to Run an LLM on Android Offline | LlamaBox Setup Guide",
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

    faqs_dl = [
        ("Where can I download an LLM for Android?", "The easiest path is the in-app hub inside LlamaBox, which lists compatible GGUF models. You can also import models from Hugging Face, GitHub releases, or your own storage."),
        ("What file format does LlamaBox use?", "GGUF — the standard quantized format used by llama.cpp. Start with Q4_K_M for a balance of size and quality."),
        ("Do I need an account to download models?", "No. Public model hubs do not require an account to download a GGUF, and LlamaBox adds no account layer of its own."),
    ]
    page(
        "llm-download.html",
        "LLM Download for Android | Get GGUF Models for LlamaBox",
        "Download LLM models for Android. Find GGUF files, quantizations, and sources that work offline in LlamaBox. No cloud inference needed.",
        article(
            "Models",
            "LLM download for Android.",
            "Get the right GGUF model onto your phone, then chat offline for good.",
            f"""
        <h2>What “LLM download” means for Android</h2>
        <p>Downloading an LLM for Android means getting a quantized model file (usually GGUF) onto your phone so a local app can load it. Unlike cloud chat apps, the download happens once; after that, inference works without internet.</p>
        <h2>Recommended sources for GGUF models</h2>
        <ul>
          <li><strong>Hugging Face</strong> — thousands of GGUF uploads from model authors and the community; filter by “GGUF” and “arm64-friendly” sizes.</li>
          <li><strong>GitHub releases</strong> — some converted models ship as release assets.</li>
          <li><strong>LlamaBox in-app hub</strong> — curated, tested-on-phone models with recommended quantizations.</li>
          <li><strong>Local import</strong> — transfer a GGUF via USB, cloud drive, or SD card and import it into LlamaBox.</li>
        </ul>
        <h2>Which quantization to download</h2>
        <p>For phones, start with <strong>Q4_K_M</strong>. It is the best-known balance of quality, file size, and RAM use for small models (0.5B–3B parameters). Smaller quants run faster and use less memory; larger quants improve quality if you have headroom.</p>
        <h2>Phone-size model guidance</h2>
        <ul>
          <li><strong>Entry phones (3–4 GB RAM)</strong> — 0.5B–1B Q4_K_M, context 512–1024</li>
          <li><strong>Mid-range phones (6–8 GB RAM)</strong> — 1B–2B Q4_K_M, context 1024–2048</li>
          <li><strong>Flagship phones (12 GB+ RAM)</strong> — 3B–7B Q4_K_M, context 2048+</li>
        </ul>
        <h2>How to load the downloaded model</h2>
        <ol>
          <li>Open LlamaBox and go to the model library.</li>
          <li>Tap download from the hub, or import your local GGUF.</li>
          <li>Wait for initialization (5–30s depending on model size).</li>
          <li>Chat — airplane mode optional.</li>
        </ol>
        <p>Next: <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/gguf-android.html">GGUF on Android guide</a> · <a href="/offline-ai-android.html">offline AI Android</a>.</p>
        {faq_html(faqs_dl)}
""",
        ),
        extra_head=faq_schema(faqs_dl),
    )

    faqs_best = [
        ("What is the best local LLM app for Android?", "It depends on your priorities. LlamaBox is the best choice if you want open-source GGUF support, CPU-only broad device coverage, and fully offline chat without accounts. Other apps may suit users who want GPU experimentation or a simpler store download."),
        ("Can these apps run without internet?", "Yes, once a model is downloaded. LlamaBox, PocketPal AI, and MLC LLM all support offline inference after setup."),
        ("Do I need a flagship phone?", "No for LlamaBox. Its CPU-only path runs on Android 7.0+ arm64. Some competitors target newer hardware or require GPU tuning."),
    ]
    faqs_chatgpt_offline = [
        ("Can you use ChatGPT offline on Android?", "No. ChatGPT and other cloud AI chatbots require an internet connection to send prompts to OpenAI's servers. There is no official offline ChatGPT mode."),
        ("What is the best ChatGPT offline alternative for Android?", "LlamaBox. It runs open-source GGUF models directly on your Android phone, so chat works without internet after the model is downloaded."),
        ("Does ChatGPT have an offline APK?", "No official offline APK exists. Any app claiming 'offline ChatGPT' is using a different model or misleading branding. Look for apps that explicitly run local LLMs, like LlamaBox."),
        ("Is LlamaBox free?", "Yes. The app is free during closed beta and will be open-sourced under AGPL-3.0 when beta ends. A commercial license is available for OEMs and enterprises."),
    ]
    page(
        "chatgpt-android-offline.html",
        "ChatGPT Android Offline: Why It Doesn’t Work & What Does | LlamaBox",
        "ChatGPT cannot run offline on Android. LlamaBox is the offline alternative — local GGUF models, no cloud, no account, private chat on your phone.",
        article(
            "Offline ChatGPT alternative",
            "ChatGPT offline on Android? Not yet.",
            "Cloud ChatGPT needs the network. LlamaBox is the offline alternative that keeps the model on your phone.",
            f"""
        <h2>Why ChatGPT cannot work offline on Android</h2>
        <p>ChatGPT is a cloud service. When you type a prompt, the app sends it to OpenAI's servers, the model runs there, and the answer travels back. That design needs an active internet connection. There is no official offline mode, no downloadable model, and no Android APK that lets you run the real ChatGPT weights locally.</p>

        <h2>What “ChatGPT Android offline” searchers actually want</h2>
        <p>Most people typing this do not need the exact ChatGPT model. They want a <strong>ChatGPT-like chat experience that works without internet</strong> — private, local, and available on their phone. That is exactly what on-device LLMs deliver.</p>

        <h2>The real solution: a local LLM app for Android</h2>
        <p>LlamaBox loads a quantized GGUF model onto your Android phone and runs inference with llama.cpp. After the one-time model download, you can chat in airplane mode. Your prompts never leave the device, no account is required, and no cloud privacy policy applies.</p>
        <ul>
          <li><strong>Model format</strong>: GGUF (Q4_K_M recommended)</li>
          <li><strong>Compute</strong>: CPU-only by design, Android 7.0+ arm64</li>
          <li><strong>Privacy</strong>: no cloud inference, no telemetry, no account</li>
          <li><strong>Extras</strong>: vision, TTS readback, offline history, system monitor</li>
        </ul>

        <h2>How it compares to "offline ChatGPT" apps in the Play Store</h2>
        <p>Some store apps brand themselves as "offline ChatGPT" or "OfflineGPT." Read carefully: many are closed products with unclear models, ads, or cloud fallbacks. LlamaBox differs because you choose the open-source GGUF weights, the source code will be public, and the architecture has no server path for chat.</p>

        <h2>How to set it up</h2>
        <ol>
          <li>Join the LlamaBox waitlist for the closed beta.</li>
          <li>Install the APK for package <code>com.llamabox</code>.</li>
          <li>Download a small Q4_K_M model from the in-app hub or import a GGUF.</li>
          <li>Load the model and chat — toggle airplane mode to prove it is local.</li>
        </ol>

        <p>Related: <a href="/offline-ai-android.html">offline AI Android</a> · <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a> · <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/vs-chatgpt.html">LlamaBox vs ChatGPT</a>.</p>
        {faq_html(faqs_chatgpt_offline)}
""",
        ),
        extra_head=faq_schema(faqs_chatgpt_offline),
    )

    page(
        "best-local-llm-apps-android.html",
        "Best Local LLM Apps for Android 2026 | LlamaBox",
        "The best local LLM apps for Android compared: LlamaBox, PocketPal AI, MLC LLM, Layla, Local AI, and OfflineLLM. Offline, private, on-device chat.",
        article(
            "Roundup",
            "Best local LLM apps for Android in 2026.",
            "A practical comparison of the apps that put language models on your phone — not in a data center.",
            f"""
        <h2>How we compare Android local LLM apps</h2>
        <p>We judge apps by four things that matter on a phone: <strong>privacy architecture</strong> (where inference runs), <strong>offline usability</strong>, <strong>device coverage</strong>, and <strong>model flexibility</strong>. Speed matters too, but only if the app runs reliably on your hardware.</p>
        <h2>1. LlamaBox — best for privacy and broad device coverage</h2>
        <ul>
          <li>Open-source, CPU-only by design, Android 7.0+ arm64</li>
          <li>GGUF models via llama.cpp; you choose or import weights</li>
          <li>No account, no telemetry, fully offline after model download</li>
          <li>Vision + TTS on device, system monitor, per-model settings</li>
          <li>Dual licensing: AGPL-3.0 + commercial license for enterprise/OEM</li>
        </ul>
        <p>Choose LlamaBox when you want the same chat experience on a mid-range phone and a flagship, without trusting a vendor server.</p>
        <h2>2. PocketPal AI — best for GPU experimentation</h2>
        <ul>
          <li>GGUF on Android with an optional GPU toggle</li>
          <li>Great speed on flagship devices with working GPU drivers</li>
          <li>May need per-device tuning; GPU path can fail silently on some chipsets</li>
        </ul>
        <p>See the full comparison: <a href="/vs-pocketpal.html">LlamaBox vs PocketPal AI</a>.</p>
        <h2>3. MLC LLM — best for model-compiler power users</h2>
        <ul>
          <li>Model compiler + runtime, not just a chat app</li>
          <li>Supports NPU/GPU acceleration where drivers allow</li>
          <li>Steeper setup; ideal for researchers and OEMs</li>
        </ul>
        <p>See the full comparison: <a href="/vs-mlc-llm.html">LlamaBox vs MLC LLM</a>.</p>
        <h2>4. Layla — best for assistant-style convenience</h2>
        <ul>
          <li>Private offline AI assistant for Android and iOS</li>
          <li>Closed product; less model choice than open GGUF apps</li>
        </ul>
        <h2>5. Local AI (Google Play) — best for one-tap store install</h2>
        <ul>
          <li>Closed, store-distributed offline chat app</li>
          <li>Convenient for casual users who do not need model flexibility</li>
        </ul>
        <h2>6. OfflineLLM — best for open-source tinkerers</h2>
        <ul>
          <li>Open-source Android project for private on-device chat</li>
          <li>Good starting point if you want to build your own fork</li>
        </ul>
        <h2>Quick comparison table</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th>App</th><th>Open source</th><th>CPU-only fallback</th><th>Model choice</th><th>Account needed</th><th>Best for</th></tr></thead>
            <tbody>
              <tr><td>LlamaBox</td><td>Yes (AGPL-3.0 + commercial)</td><td>Yes, by design</td><td>Any GGUF you choose</td><td>No</td><td>Privacy, broad device coverage</td></tr>
              <tr><td>PocketPal AI</td><td>Yes</td><td>Yes, with GPU option</td><td>GGUF</td><td>No</td><td>GPU speed on supported flagships</td></tr>
              <tr><td>MLC LLM</td><td>Yes</td><td>Model dependent</td><td>Compiled models</td><td>No</td><td>Researchers / compiler users</td></tr>
              <tr><td>Layla</td><td>No</td><td>Yes</td><td>Vendor-curated</td><td>No</td><td>Assistant convenience</td></tr>
              <tr><td>Local AI (Play)</td><td>No</td><td>Yes</td><td>Vendor-curated</td><td>No</td><td>One-tap install</td></tr>
              <tr><td>OfflineLLM</td><td>Yes</td><td>Yes</td><td>GGUF</td><td>No</td><td>Tinkering / forking</td></tr>
            </tbody>
          </table>
        </div>
        <h2>Our recommendation</h2>
        <p>If you want the <strong>best local LLM app for Android</strong> and your top priorities are privacy, offline reliability, and running on the widest range of phones, start with <a href="/waitlist.html">LlamaBox</a>. If you have a flagship with working GPU drivers and want to experiment with GPU offload, also try PocketPal AI. For compiler-level control, look at MLC LLM.</p>
        {faq_html(faqs_best)}
""",
        ),
        extra_head=faq_schema(faqs_best),
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
        <p>Also see <a href="/private-chatgpt-alternative.html">private ChatGPT alternative</a>, <a href="/vs-ollama.html">vs Ollama</a>, <a href="/blog/2026-07-30-llamabox-vs-pocketpal.html">vs PocketPal</a>, and <a href="/blog/2026-07-30-llamabox-vs-mlc-llm.html">vs MLC LLM</a>.</p>
""",
        ),
    )

    page(
        "vs-pocketpal.html",
        "LlamaBox vs PocketPal AI | Offline Android LLM comparison",
        "LlamaBox vs PocketPal AI: both run local LLMs offline on Android. Compare CPU-only coverage, GPU flexibility, privacy, and model support.",
        article(
            "Compare",
            "LlamaBox vs PocketPal AI.",
            "Two Android apps for private offline chat with local models. One is CPU-only by design; the other gives you a GPU toggle.",
            """
        <p><strong>PocketPal AI</strong> proved that local LLMs on a phone are usable. It loads GGUF models, runs them offline, and gives users a chat UI without a cloud round-trip. LlamaBox shares that goal but makes different trade-offs.</p>
        <h2>What both apps do</h2>
        <ul>
          <li>Load quantized GGUF models locally</li>
          <li>Run inference on-device after the model is downloaded</li>
          <li>Keep prompts off a vendor server</li>
          <li>Target Android as the primary mobile platform</li>
        </ul>
        <h2>Where they differ</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>PocketPal AI</th></tr></thead>
            <tbody>
              <tr><td>Compute path</td><td>CPU-only by design</td><td>CPU + optional GPU layers where supported</td></tr>
              <tr><td>Device coverage</td><td>Mid-range, old flagships, budget phones</td><td>Best on phones with usable GPU drivers</td></tr>
              <tr><td>Scope</td><td>Private offline chat + vision</td><td>General local LLM chat</td></tr>
              <tr><td>Distribution</td><td>Closed beta waitlist</td><td>Public via GitHub / side-load</td></tr>
            </tbody>
          </table>
        </div>
        <h2>Why CPU-only matters</h2>
        <p>Android GPU compute is fragmented across chipsets. A “GPU acceleration” toggle that works on a Snapdragon 8 Gen 3 may fail silently on a MediaTek or older Exynos. LlamaBox removes that variable: if the phone can run Android 7+ arm64 and has enough RAM, it can run the same model path as every other LlamaBox user.</p>
        <h2>Which to choose</h2>
        <p>Use <strong>PocketPal AI</strong> if you want the option to experiment with GPU offload on a flagship and do not mind tuning layers per device. Use <strong>LlamaBox</strong> if you want one consistent private chat experience across the widest range of Android hardware, including phones without a working GPU compute path.</p>
        <p>Read more: <a href="/architecture.html">CPU-only by design</a> · <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/blog/2026-07-30-llamabox-vs-pocketpal.html">blog version</a>.</p>
""",
        ),
    )

    page(
        "vs-mlc-llm.html",
        "LlamaBox vs MLC LLM | Android local AI comparison",
        "LlamaBox is a private chat app; MLC LLM is a model compiler. Compare CPU-only GGUF chat vs compiled-model performance for Android users.",
        article(
            "Compare",
            "LlamaBox vs MLC LLM.",
            "A privacy-first chat app versus a machine-learning compiler. Same local goal, different abstraction layers.",
            """
        <p><strong>MLC LLM</strong> is a machine-learning compiler project: take a model, compile it for a target device, and push it toward the hardware’s limits. <strong>LlamaBox</strong> is a privacy-first chat app: download a GGUF, load it, and chat offline on Android.</p>
        <h2>Different layers of the stack</h2>
        <p>MLC LLM is infrastructure. Developers use it to ship models in apps, browsers, and edge devices. LlamaBox is an end-user product built on llama.cpp + llama.rn. The comparison is really: “Do I want to build with MLC, or do I want a ready-to-use chat app that already handles models, history, and UI?”</p>
        <h2>For Android users specifically</h2>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>MLC LLM / MLC Chat</th></tr></thead>
            <tbody>
              <tr><td>What you get</td><td>Chat app + model hub + offline history</td><td>Model runtime / reference app + pre-converted weights</td></tr>
              <tr><td>Model format</td><td>GGUF via llama.cpp</td><td>Pre-compiled MLC weights (often from Hugging Face)</td></tr>
              <tr><td>Hardware path</td><td>CPU-only (ARM NEON)</td><td>CPU / GPU / NPU depending on compilation target</td></tr>
              <tr><td>Customization</td><td>Import any GGUF that fits RAM</td><td>Use supported prebuilt models or compile your own</td></tr>
              <tr><td>Privacy stance</td><td>No accounts, no telemetry, no cloud inference</td><td>Depends on wrapper app; runtime itself is local</td></tr>
            </tbody>
          </table>
        </div>
        <h2>When MLC LLM makes sense</h2>
        <p>If you are building your own Android app and need to squeeze every last token per second out of a specific SoC, MLC LLM is the deeper toolbox. If you just want private offline chat today, LlamaBox skips the compile step.</p>
        <h2>When LlamaBox makes sense</h2>
        <p>You want a chat history, vision support, and a model hub on a stock Android phone — including devices where GPU drivers are broken or missing. CPU-only by design is a compatibility choice.</p>
        <p>Read more: <a href="/gguf-android.html">GGUF on Android</a> · <a href="/architecture.html">LlamaBox architecture</a> · <a href="/blog/2026-07-30-llamabox-vs-mlc-llm.html">blog version</a>.</p>
""",
        ),
    )

    faqs_ollama = [
        ("Can you run Ollama on Android?", "Ollama is officially built for macOS, Linux, and Windows. It does not ship an Android app or APK. LlamaBox is the Android-native equivalent: it loads the same GGUF models with a mobile chat UI."),
        ("Is there an Ollama Android app?", "No official Ollama Android client exists. If you want local LLM chat on Android, LlamaBox is purpose-built for it — no terminal, no desktop dependency."),
        ("Why use LlamaBox instead of Ollama on Android?", "LlamaBox runs offline on stock Android phones using CPU-only inference. It is designed for mobile battery, touch UX, and APK distribution, not for a server you SSH into."),
        ("Do LlamaBox and Ollama use the same models?", "Yes — both use GGUF weights from the llama.cpp ecosystem. You can often load the same quantized models in both tools."),
    ]
    page(
        "vs-ollama.html",
        "Ollama Android alternative | LlamaBox local LLM on Android",
        "No official Ollama Android app exists. LlamaBox is the Android alternative: offline GGUF chat on your phone. Same models, mobile-native UX.",
        article(
            "Compare",
            "LlamaBox vs Ollama — the Android question.",
            "Ollama owns the desktop/server local-LLM workflow. LlamaBox brings the same GGUF model world to Android phones. If you searched for an Ollama Android app, this is the answer.",
            f"""
        <h2>The short answer</h2>
        <p>There is no official <strong>Ollama Android</strong> release. Ollama's supported platforms are macOS, Linux, and Windows. If you need local LLM chat on Android, <strong>LlamaBox</strong> is built for exactly that: load a GGUF model, chat offline, no cloud inference.</p>
        <h2>Why the comparison matters</h2>
        <p>Users who discover local LLMs through Ollama naturally want the same experience on their phone. They search for "ollama android" and find workarounds — Termux, remote tunnels, or unofficial clients. LlamaBox is a real Android app with a mobile-first interface, designed for the phone's battery, RAM, and storage constraints.</p>
        <div class="table-wrap">
          <table class="compare-table">
            <thead><tr><th></th><th>LlamaBox</th><th>Ollama (typical)</th></tr></thead>
            <tbody>
              <tr><td>Android app</td><td>Yes — built for Android 7+ arm64</td><td>No official Android app</td></tr>
              <tr><td>Primary device</td><td>Android phone / tablet</td><td>Desktop / laptop / server</td></tr>
              <tr><td>UX</td><td>Mobile chat app</td><td>CLI + apps ecosystem</td></tr>
              <tr><td>Always with you</td><td>Yes</td><td>If the machine is with you</td></tr>
              <tr><td>Power envelope</td><td>Phone SoC / battery</td><td>Wall power / desktops often</td></tr>
              <tr><td>Model format</td><td>GGUF via llama.cpp stack</td><td>GGUF ecosystem</td></tr>
              <tr><td>Offline use</td><td>Designed for offline chat</td><td>Local once set up, but not mobile</td></tr>
              <tr><td>Best for</td><td>Private pocket AI</td><td>Dev workflows, heavier local models</td></tr>
            </tbody>
          </table>
        </div>
        <h2>How to get local LLMs on Android today</h2>
        <ol>
          <li>Install LlamaBox from the Play Store or GitHub releases.</li>
          <li>Download a small GGUF model (0.5B–3B Q4_K_M) over Wi-Fi.</li>
          <li>Chat offline. No account, no API key, no desktop server.</li>
        </ol>
        <p>Many builders will use <strong>both</strong>: Ollama on a workstation, LlamaBox on the phone. Related: <a href="/gguf-android.html">GGUF on Android</a> · <a href="/on-device-llm.html">on-device LLM</a> · <a href="/offline-ai-android.html">offline AI Android</a>.</p>
        {faq_html(faqs_ollama)}
""",
        ),
        extra_head=faq_schema(faqs_ollama),
    )

    # --- business / monetization pages ---
    page(
        "enterprise.html",
        "Offline AI for enterprise teams | LlamaBox",
        "Deploy private, offline AI chat on Android devices for enterprise teams in journalism, healthcare, field work, education, and defense. No cloud inference.",
        article(
            "Enterprise",
            "Offline AI for teams that cannot use cloud chat.",
            "LlamaBox keeps language-model inference on the Android device. That property matters when regulation, connectivity, or operational security rule out hosted AI.",
            """
        <h2>Use cases</h2>
        <ul>
          <li><strong>Journalism &amp; sensitive sourcing</strong> — interviews and drafts never hit a vendor server</li>
          <li><strong>Healthcare &amp; clinical notes</strong> — local inference reduces HIPAA/GDPR surface area for note drafting</li>
          <li><strong>Field work &amp; disaster response</strong> — works offline in low-connectivity or denied-network environments</li>
          <li><strong>Education &amp; exam settings</strong> — AI assistance without internet or account requirements</li>
          <li><strong>Defense &amp; government edge</strong> — air-gapped deployment target on standard Android hardware</li>
        </ul>
        <h2>Deployment options</h2>
        <ul>
          <li><strong>Private APK distribution</strong> — sideload or internal enterprise app store</li>
          <li><strong>Managed Play Store track</strong> — closed testing for approved organization accounts</li>
          <li><strong>Curated GGUF model set</strong> — per-organization model whitelist and defaults</li>
          <li><strong>MDM-ready configuration</strong> — provisioning via managed app config</li>
          <li><strong>Commercial license &amp; support</strong> — clear IP terms and an engineering channel</li>
        </ul>
        <h2>Why CPU-only is an enterprise feature</h2>
        <p>Accelerated compute on Android is a driver lottery across chipsets. CPU-only inference means the same model path works on every supported Android 7+ arm64 device in the fleet. Predictability beats peak tok/s when you are supporting hundreds of heterogeneous handsets.</p>
        <h2 id="contact">Contact us</h2>
        <p>Tell us about your fleet, use case, and timeline. No pricing yet — we are prioritizing design partners and pilots.</p>
        <form class="waitlist-form glass" action="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20enterprise%20inquiry" method="POST" enctype="text/plain" style="margin-top:1rem">
          <label>Name <span class="req">*</span>
            <input required type="text" name="name" placeholder="Your name">
          </label>
          <label>Work email <span class="req">*</span>
            <input required type="email" name="email" placeholder="you@organization.com" autocomplete="email">
          </label>
          <label>Company / organization <span class="req">*</span>
            <input required type="text" name="company" placeholder="e.g. Mythos Labs">
          </label>
          <label>Role
            <input type="text" name="role" placeholder="e.g. CTO, Product lead, Security officer">
          </label>
          <label>Estimated devices
            <input type="text" name="devices" placeholder="e.g. 50–500">
          </label>
          <label>Use case (optional)
            <textarea name="use_case" rows="3" placeholder="Journalism, healthcare, field work, education, defense, other..."></textarea>
          </label>
          <button type="submit" class="btn btn-primary" style="width:100%">Request enterprise info</button>
          <p class="form-note">This opens your email client pre-filled with the inquiry. Prefer web mail? Send directly to <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20enterprise%20inquiry">aalhad.dev@gmail.com</a> or use the <a href="/waitlist.html">waitlist</a> and check “I’m interested in commercial / enterprise use.”</p>
        </form>
""",
        ),
    )

    page(
        "commercial-license.html",
        "Commercial license | LlamaBox",
        "Dual-licensed AGPL-3.0 + commercial. Get a commercial license to use LlamaBox in proprietary products, SaaS, or app stores without open-sourcing your code.",
        article(
            "Licensing",
            "Commercial license for LlamaBox.",
            "The public codebase will be AGPL-3.0 when released. A separate commercial license is available for organizations that cannot use copyleft.",
            """
        <h2>Who needs a commercial license</h2>
        <ul>
          <li>Companies shipping LlamaBox or derived code in a proprietary app</li>
          <li>SaaS products that include LlamaBox inference as a backend component</li>
          <li>OEMs pre-installing LlamaBox on devices without distributing source</li>
          <li>Teams that need legal indemnity and a clear IP chain</li>
        </ul>
        <h2>What the commercial license covers</h2>
        <ul>
          <li>Permission to use LlamaBox code without AGPL obligations</li>
          <li>Access to closed-beta builds and priority support</li>
          <li>Optional engineering consulting and custom feature development</li>
          <li>“LlamaBox” trademark usage under defined terms</li>
        </ul>
        <h2>Pricing</h2>
        <p>Pricing is negotiated per deployment: per-seat, per-device, or flat project license. We optimize for early partners and high-volume deployments.</p>
        <h2>Request a quote</h2>
        <p>Email <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20commercial%20license%20inquiry">aalhad.dev@gmail.com</a> with a short description of your use case, expected scale, and timeline.</p>
""",
        ),
    )

    page(
        "partners.html",
        "Partner with LlamaBox",
        "OEMs, device manufacturers, model authors, privacy organizations, and distributors: partner with LlamaBox to bring private offline AI to more users.",
        article(
            "Partners",
            "Partner with LlamaBox.",
            "We are building the default offline AI chat layer for Android. Partnerships accelerate distribution and deepen the ecosystem.",
            """
        <h2>Partnership models</h2>
        <ul>
          <li><strong>OEM / device pre-install</strong> — LlamaBox bundled on privacy-focused phones, rugged devices, or enterprise handsets</li>
          <li><strong>Model author placement</strong> — featured, tested GGUF models in the LlamaBox model hub</li>
          <li><strong>Distribution</strong> — app stores, side-load platforms, privacy-focused Android communities</li>
          <li><strong>Privacy &amp; rights organizations</strong> — co-marketing and validation for offline-by-design AI</li>
          <li><strong>Enterprise resellers</strong> — white-glove deployment and support for regulated customers</li>
        </ul>
        <h2>What we bring</h2>
        <ul>
          <li>React Native Android app with llama.cpp inference</li>
          <li>CPU-only path for broad device compatibility</li>
          <li>Vision, TTS, model hub, and offline history out of the box</li>
          <li>Dual licensing for commercial flexibility</li>
        </ul>
        <h2>Get in touch</h2>
        <p>Email <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20partnership">aalhad.dev@gmail.com</a> with your partnership idea and audience size.</p>
""",
        ),
    )

    page(
        "investors.html",
        "Investors &amp; acquisitions | LlamaBox",
        "LlamaBox: private offline AI chat for Android. Closed beta, CPU-only by design, open-core model. Strategic acquisition or investment conversations welcome.",
        article(
            "Investors",
            "LlamaBox is the offline AI layer for Android.",
            "A small, focused team is building the privacy-first alternative to cloud chat. We are open to strategic investment, partnership, and acquisition discussions.",
            """
        <h2>What we built</h2>
        <ul>
          <li>React Native Android app running GGUF models via llama.cpp / llama.rn</li>
          <li>CPU-only inference by design for maximum Android device coverage</li>
          <li>Private chat, vision, TTS, model hub, and offline history</li>
          <li>Closed beta with waitlist; dual-licensed AGPL-3.0 + commercial</li>
        </ul>
        <h2>Market opportunity</h2>
        <ul>
          <li>Privacy regulation and AI safety are pushing inference toward the edge</li>
          <li>Android dominates global mobile; most local-LLM tooling is desktop/server-first</li>
          <li>Competitors either require GPU drivers (PocketPal), compilation expertise (MLC), or cloud round-trips</li>
          <li>LlamaBox is positioned as the ChatGPT alternative that genuinely cannot leak prompts</li>
        </ul>
        <h2>Strategic fit</h2>
        <p>Ideal partners or acquirers: privacy-focused browsers/phones, secure messaging platforms, Android custom ROMs, on-device AI chipmakers, enterprise mobile security vendors, and AI-safety organizations that need a concrete, deployable local-AI product.</p>
        <h2>Contact</h2>
        <p>Email <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20investor%20%2F%20acquisition">aalhad.dev@gmail.com</a> for deck, demo, and discussion.</p>
""",
        ),
    )

    page(
        "press-kit.html",
        "LlamaBox Press Kit | Facts, logos, and contacts",
        "LlamaBox press kit: one-page facts for journalists, partners, and investors. Private offline AI chat for Android, CPU-only by design, open-core.",
        article(
            "Press kit",
            "LlamaBox press kit.",
            "Everything you need to write about, partner with, or evaluate LlamaBox — on one page.",
            """
        <h2>Boilerplate</h2>
        <p>LlamaBox is a free Android app that runs large language models entirely on-device. It gives users private, offline AI chat with no cloud inference, no accounts, and no telemetry. Built with React Native and llama.cpp, LlamaBox is CPU-only by design so it works across the widest range of Android 7.0+ arm64 phones.</p>

        <h2>Key facts</h2>
        <ul>
          <li><strong>Product</strong>: private offline AI chat for Android</li>
          <li><strong>Stack</strong>: React Native 0.81, llama.rn wrapping llama.cpp, GGUF models</li>
          <li><strong>Compute</strong>: CPU-only (ARM NEON, 4 threads); no GPU dependencies</li>
          <li><strong>Features</strong>: chat, vision, TTS readback, model hub, system monitor, offline history</li>
          <li><strong>Privacy</strong>: inference never leaves the device; no account required</li>
          <li><strong>License</strong>: dual-licensed AGPL-3.0 + commercial license</li>
          <li><strong>Status</strong>: closed beta (waitlist); package <code>com.llamabox</code></li>
          <li><strong>Creator</strong>: Aalhad (Mythos Labs)</li>
        </ul>

        <h2>What makes it different</h2>
        <p>Most "AI apps" send prompts to a vendor server. LlamaBox removes the server path entirely — the model runs on the phone. That makes it private by architecture, not by policy, and it works in airplane mode after the model file is downloaded.</p>

        <h2>Angles for coverage</h2>
        <ul>
          <li><strong>Privacy / AI safety</strong>: an Android chat app that cannot leak prompts because it never sends them</li>
          <li><strong>Hardware access</strong>: CPU-only inference reaches mid-range and older phones, not just flagships</li>
          <li><strong>Offline / field use</strong>: journalists, travelers, students, healthcare workers, and defense edge cases</li>
          <li><strong>Open core</strong>: AGPL-3.0 public source at beta end plus commercial licensing for OEMs and enterprises</li>
          <li><strong>Comparison</strong>: how LlamaBox differs from PocketPal AI, MLC LLM, Ollama, and cloud assistants</li>
        </ul>

        <h2>Important caveats (please include)</h2>
        <ul>
          <li>LlamaBox is <strong>CPU-only by design</strong>; do not claim GPU acceleration.</li>
          <li>Full public source lands when the closed beta ends.</li>
          <li>Phone CPUs are not datacenter GPUs — quality and speed are model-size dependent.</li>
        </ul>

        <h2>Links to cite</h2>
        <ul>
          <li>Homepage: <a href="/">https://llamabox-ai.github.io/</a></li>
          <li>Architecture: <a href="/architecture.html">https://llamabox-ai.github.io/architecture.html</a></li>
          <li>LLM brief: <a href="/llms.txt">https://llamabox-ai.github.io/llms.txt</a></li>
          <li>Waitlist: <a href="/waitlist.html">https://llamabox-ai.github.io/waitlist.html</a></li>
          <li>Compare: <a href="/best-local-llm-apps-android.html">https://llamabox-ai.github.io/best-local-llm-apps-android.html</a></li>
          <li>Enterprise: <a href="/enterprise.html">https://llamabox-ai.github.io/enterprise.html</a></li>
          <li>Investors: <a href="/investors.html">https://llamabox-ai.github.io/investors.html</a></li>
          <li>GitHub org: <a href="https://github.com/llamabox-ai" rel="noopener">https://github.com/llamabox-ai</a></li>
        </ul>

        <h2>Media assets</h2>
        <ul>
          <li>App screenshot: <a href="/assets/screenshot-1-home.png">/assets/screenshot-1-home.png</a></li>
          <li>Favicon / logo SVG: in site header (data URI) or contact us for vector files</li>
        </ul>

        <h2>Contacts</h2>
        <ul>
          <li><strong>General / press</strong>: <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20press">aalhad.dev@gmail.com</a></li>
          <li><strong>Enterprise / commercial</strong>: <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20enterprise">aalhad.dev@gmail.com</a></li>
          <li><strong>Investors / acquisitions</strong>: <a href="mailto:aalhad.dev@gmail.com?subject=LlamaBox%20investor%20%2F%20acquisition">aalhad.dev@gmail.com</a></li>
        </ul>
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
        (
            "2026-07-30-llamabox-vs-pocketpal.html",
            "2026-07-30",
            "LlamaBox vs PocketPal: private offline AI on Android",
            "Two Android apps run local LLMs offline. One is CPU-only by design for broad device support. See how LlamaBox compares to PocketPal AI.",
            """
        <p><strong>PocketPal AI</strong> proved that local LLMs on a phone are usable. It loads GGUF models, runs them offline, and gives users a chat UI without a cloud round-trip. LlamaBox shares that goal but makes different trade-offs.</p>
        <h2>What both apps do</h2>
        <ul>
          <li>Load quantized GGUF models locally</li>
          <li>Run inference on-device after the model is downloaded</li>
          <li>Keep prompts off a vendor server</li>
          <li>Target Android as the primary mobile platform</li>
        </ul>
        <h2>Where they differ</h2>
        <table class="compare-table">
          <thead><tr><th></th><th>LlamaBox</th><th>PocketPal AI</th></tr></thead>
          <tbody>
            <tr><td>Compute path</td><td>CPU-only by design</td><td>CPU + optional GPU layers where supported</td></tr>
            <tr><td>Device coverage</td><td>Mid-range, old flagships, budget phones</td><td>Best on phones with usable GPU drivers</td></tr>
            <tr><td>Scope</td><td>Private offline chat + vision</td><td>General local LLM chat</td></tr>
            <tr><td>Distribution</td><td>Closed beta waitlist</td><td>Public via GitHub / side-load</td></tr>
          </tbody>
        </table>
        <h2>Why CPU-only matters</h2>
        <p>Android GPU compute is fragmented across chipsets. A “GPU acceleration” toggle that works on a Snapdragon 8 Gen 3 may fail silently on a MediaTek or older Exynos. LlamaBox removes that variable: if the phone can run Android 7+ arm64 and has enough RAM, it can run the same model path as every other LlamaBox user. That predictability is the feature.</p>
        <h2>Which to choose</h2>
        <p>Use <strong>PocketPal AI</strong> if you want the option to experiment with GPU offload on a flagship and do not mind tuning layers per device. Use <strong>LlamaBox</strong> if you want one consistent private chat experience across the widest range of Android hardware, including phones without a working GPU compute path.</p>
        <p>Read more: <a href="/architecture.html">CPU-only by design</a> · <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a>.</p>
""",
        ),
        (
            "2026-07-30-llamabox-vs-mlc-llm.html",
            "2026-07-30",
            "LlamaBox vs MLC LLM: CPU-only vs model-compiler approach",
            "MLC LLM is a powerful model compiler for many devices. LlamaBox is a privacy-first Android chat app. Here is how the two compare for phone users.",
            """
        <p><strong>MLC LLM</strong> is a machine-learning compiler project: take a PyTorch/ONNX model, compile it for a target device, and push it toward the hardware’s limits. <strong>LlamaBox</strong> is a privacy-first chat app: download a GGUF, load it, and chat offline on Android.</p>
        <h2>Different layers of the stack</h2>
        <p>MLC LLM is infrastructure. Developers use it to ship models in apps, browsers, and edge devices. LlamaBox is an end-user product built on llama.cpp + llama.rn. The comparison is really: “Do I want to build with MLC, or do I want a ready-to-use chat app that already handles models, history, and UI?”</p>
        <h2>For Android users specifically</h2>
        <table class="compare-table">
          <thead><tr><th></th><th>LlamaBox</th><th>MLC LLM / MLC Chat</th></tr></thead>
          <tbody>
            <tr><td>What you get</td><td>Chat app + model hub + offline history</td><td>Model runtime / reference app + pre-converted weights</td></tr>
            <tr><td>Model format</td><td>GGUF via llama.cpp</td><td>Pre-compiled MLC weights (often from Hugging Face)</td></tr>
            <tr><td>Hardware path</td><td>CPU-only (ARM NEON)</td><td>CPU / GPU / NPU depending on compilation target</td></tr>
            <tr><td>Customization</td><td>Import any GGUF that fits RAM</td><td>Use supported prebuilt models or compile your own</td></tr>
            <tr><td>Privacy stance</td><td>No accounts, no telemetry, no cloud inference</td><td>Depends on wrapper app; runtime itself is local</td></tr>
          </tbody>
        </table>
        <h2>When MLC LLM makes sense</h2>
        <p>If you are building your own Android app and need to squeeze every last token per second out of a specific SoC, MLC LLM is the deeper toolbox. If you just want private offline chat today, LlamaBox skips the compile step.</p>
        <h2>When LlamaBox makes sense</h2>
        <p>You want a chat history, vision support, and a model hub on a stock Android phone — including devices where GPU drivers are broken or missing. CPU-only by design is a compatibility choice, not a performance compromise.</p>
        <p>Related: <a href="/gguf-android.html">GGUF on Android</a> · <a href="/architecture.html">LlamaBox architecture</a>.</p>
""",
        ),
        (
            "2026-07-30-best-private-ai-chat-android.html",
            "2026-07-30",
            "Best private AI chat apps for Android in 2026",
            "A no-nonsense list of Android apps that keep AI chat local and private — plus what makes LlamaBox different.",
            """
        <p>Privacy-first AI chat on Android breaks into two camps: apps that promise not to read your messages, and apps that genuinely cannot. This list focuses on the second camp — local inference, no cloud round-trip.</p>
        <h2>The shortlist</h2>
        <ol>
          <li><strong>LlamaBox</strong> — CPU-only offline chat for Android 7+ arm64. GGUF models, no GPU dependency, vision support.</li>
          <li><strong>PocketPal AI</strong> — Open-source GGUF chat with optional GPU layers. Great for users comfortable side-loading and tuning.</li>
          <li><strong>MLC Chat</strong> — Reference app for MLC LLM compiled models. Fast on supported hardware; narrower model selection.</li>
          <li><strong>Duck.ai / Venice AI</strong> — Privacy-oriented cloud assistants. Not local, but marketed as privacy-first.</li>
        </ol>
        <h2>What to check before trusting “private”</h2>
        <ul>
          <li>Does inference happen on-device or on a server?</li>
          <li>Is there an account requirement?</li>
          <li>Are telemetry / crash reports opt-out or opt-in?</li>
          <li>Can the app work in airplane mode after setup?</li>
        </ul>
        <h2>LlamaBox’s angle</h2>
        <p>We do not ask for trust; we remove the need for it. CPU-only inference means LlamaBox runs on the widest range of Android devices, including phones without working accelerated compute. No GPU toggle, no driver lottery, no cloud path for prompts.</p>
        <p>Get started: <a href="/how-to-run-llm-on-android.html">how to run an LLM on Android</a> · <a href="/waitlist.html">join the waitlist</a>.</p>
""",
        ),
        (
            "2026-07-30-what-is-offline-ai-chat.html",
            "2026-07-30",
            "What is offline AI chat?",
            "Offline AI chat means the language model runs on your device, not a server. Here is how it works, what it can do, and where it still needs the internet.",
            """
        <p><strong>Offline AI chat</strong> is a chat interface where the language model executes locally on your phone, tablet, or laptop instead of on a vendor’s server. After the model file is downloaded, the app does not need the internet to generate responses.</p>
        <h2>How it works</h2>
        <p>A quantized model file (for LlamaBox, a GGUF) is stored on the device. The app loads it into memory, runs the transformer forward pass on the local processor, and streams tokens back to the chat UI. Every step stays on the device.</p>
        <h2>What you can do offline</h2>
        <ul>
          <li>Draft, rephrase, summarize, and answer questions</li>
          <li>Run roleplay or creative writing locally</li>
          <li>Process local images with a vision-capable model</li>
          <li>Keep a chat history that never leaves the handset</li>
        </ul>
        <h2>What still needs internet</h2>
        <ul>
          <li>Downloading a new model the first time</li>
          <li>Web browsing, live search, or cloud-tool integrations</li>
          <li>Frontier-scale reasoning models that do not fit device RAM</li>
        </ul>
        <h2>Why it matters</h2>
        <p>Cloud chat requires you to trust the provider’s privacy policy, data retention, and security posture. Offline AI chat removes that dependency. The guarantee is architectural, not contractual.</p>
        <p>LlamaBox runs offline AI chat on Android with GGUF models and CPU-only inference. <a href="/how-to-run-llm-on-android.html">Set it up</a> or read the <a href="/architecture.html">architecture</a>.</p>
""",
        ),
        (
            "2026-07-30-why-cpu-only.html",
            "2026-07-30",
            "Why LlamaBox is CPU-only by design",
            "GPU acceleration sounds better on paper. For Android, CPU-only is the more honest default — and the one that reaches the most users.",
            """
        <p>Every local LLM project eventually faces the GPU question. On Android, the honest answer is that GPU compute is a gamble, not a guarantee.</p>
        <h2>The driver lottery</h2>
        <p>OpenCL support varies by chipset, vendor, Android version, and sometimes carrier build. A Snapdragon 8 Gen 3 may expose a compute path that a MediaTek Dimensity or an older Exynos does not. The same app, same model, same GGUF file can behave differently on two phones that look identical in a spec sheet.</p>
        <h2>The user-visible cost</h2>
        <p>A “GPU acceleration” toggle that fails silently is worse than no toggle at all. Users blame the app, leave a one-star review, and uninstall. The CPU path is predictable: slower tokens, but the same tokens on every supported device.</p>
        <h2>What CPU-only actually means</h2>
        <p>LlamaBox uses llama.cpp’s ARM NEON path with a fixed thread count. Mid-range phones, old flagships, and budget devices all run the same inference code. The trade-off is modest tok/s and smaller models, but the product works for the widest audience.</p>
        <h2>Honest exceptions</h2>
        <ul>
          <li>Flagship users with working GPU drivers could get faster generation</li>
          <li>Vision encoding stays on CPU anyway to keep the UI responsive</li>
          <li>Future hardware may make a GPU path worth revisiting — but only after real-device validation</li>
        </ul>
        <h2>The bottom line</h2>
        <p>CPU-only is not a temporary limitation. It is a scope decision that removes an entire class of device-specific bugs and lets LlamaBox target every Android 7+ arm64 phone with enough RAM. Read more in <a href="/architecture.html">architecture</a>.</p>
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
        ("/chatgpt-android-offline.html", "0.85", "weekly"),
        ("/gguf-android.html", "0.85", "weekly"),
        ("/llm-download.html", "0.85", "weekly"),
        ("/how-to-run-llm-on-android.html", "0.9", "weekly"),
        ("/vs-chatgpt.html", "0.8", "monthly"),
        ("/vs-ollama.html", "0.8", "monthly"),
        ("/vs-pocketpal.html", "0.8", "monthly"),
        ("/vs-mlc-llm.html", "0.8", "monthly"),
        ("/best-local-llm-apps-android.html", "0.85", "weekly"),
        ("/enterprise.html", "0.85", "weekly"),
        ("/commercial-license.html", "0.8", "monthly"),
        ("/partners.html", "0.8", "monthly"),
        ("/investors.html", "0.8", "monthly"),
        ("/press-kit.html", "0.8", "monthly"),
        ("/blog/", "0.75", "weekly"),
        ("/blog/2026-07-28-airplane-mode-ai.html", "0.7", "monthly"),
        ("/blog/2026-07-28-best-small-gguf-android.html", "0.7", "monthly"),
        ("/blog/2026-07-28-vision-encoder-cpu.html", "0.7", "monthly"),
        ("/blog/2026-07-30-phone-faster-than-pc.html", "0.7", "monthly"),
        ("/blog/2026-07-30-llamabox-vs-pocketpal.html", "0.7", "monthly"),
        ("/blog/2026-07-30-llamabox-vs-mlc-llm.html", "0.7", "monthly"),
        ("/blog/2026-07-30-best-private-ai-chat-android.html", "0.7", "monthly"),
        ("/blog/2026-07-30-what-is-offline-ai-chat.html", "0.7", "monthly"),
        ("/blog/2026-07-30-why-cpu-only.html", "0.7", "monthly"),
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
