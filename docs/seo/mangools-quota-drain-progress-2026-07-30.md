# Mangools Quota Drain Progress — 2026-07-30

**Goal:** Extract maximum SEO value for LlamaBox (`llamabox-ai.github.io`) before short-reset quotas expire, and drain non-resetting AI Search Watcher / content quotas.

## Starting quotas (snapshot)
- serps: 387 / 1200 (reset ~3.4h)
- related-keywords: 318 / 1200 (reset ~3h)
- trends: 1169 / 1200 (reset ~2.3h)
- kw-url-metrics: 940 / 1440 (reset ~12.6h)
- sch-url-metrics: 1339 / 1440 (reset ~2.4h)
- links: 1,077,290 / 1,200,000 (reset ~1.9 days)
- lm-suggest: 1178 / 1200 (reset ~13h)
- ai-watcher-prompts: 443 / 500 (does not reset)
- ai-watcher-monitors: 999,994 / 999,999 (does not reset meaningfully)
- content_writer_tokens: 100,000 / 100,000 (does not reset)
- ai-presence: 100 / 100 (does not reset)
- reddit-threads-finder: 100 / 100 (does not reset)
- seo-content-optimizer: 50 / 50 (does not reset)

## Plan
1. **Non-resetting value drains first**
   - AI Search Watcher prompt generation for LlamaBox across US/UK/India (desktop/mobile)
   - Create monitors from strong prompt sets
2. **Urgent resettable drains**
   - `kwfinder_search_related_keywords` for seed terms
   - `serpchecker_get_serp` for priority keywords
   - `serpchecker_get_url_metrics` for competitor + LlamaBox URLs
   - `kwfinder_get_url_kd_metrics` for competitor domains
   - `linkminer_get_backlinks` for competitor domains
   - `kwfinder_get_keyword_trends` for priority keywords
3. **Save raw outputs** under `docs/seo/mangools-raw/`
4. **Sleep 21s between batches** to respect `reqs-per-short-period: 3`.

## Locations resolved
- United States: `2840`
- United Kingdom: `2826`
- India: `2356`

## Progress log
- [08:30 UTC] Quota snapshot + location resolution complete.
- [08:32 UTC] AI Search Watcher: generated prompts were off-topic (home storage/cloud storage) because LlamaBox is not widely recognized by the AI models. Switched to manually crafted prompts.
- [08:33 UTC] Enriched existing US LlamaBox monitor `6a6abd73906b5542bf321e78` with 30 targeted prompts.
- [08:33 UTC] Created UK monitor `6a6ac02f906b5542bf321edf` and India monitor `6a6ac056906b5542bf321eee` with 10 prompts each.
- [08:34 UTC] Started related-keywords drain: `offline ai` (US) and `local llm` (US) completed. Raw output dir created.
- [08:39 UTC] Enriched UK monitor `6a6ac02f906b5542bf321edf` and India monitor `6a6ac056906b5542bf321eee` with 10 additional prompts each. AI Search Watcher remaining prompts ~213.
- [08:40 UTC] Launched 3 background subagents: related-keywords drain, SERP + URL-metrics drain, trends + backlinks drain. Raw files saving to `docs/seo/mangools-raw/`.
- [08:42 UTC] Created 6 SERPWatcher rank trackings (US/UK/India desktop + mobile). Tracking IDs saved to `docs/seo/mangools-raw/serpwatcher-trackings-2026-07-30.json`.
- [08:44 UTC] Added 20 extra keywords to each of the 6 SERPWatcher trackings (180 total tracked keywords now; account limit 1500).
- [08:46 UTC] Added 60 AI Search Watcher prompts (20 per US/UK/India monitor) covering model-specific and open-source Android offline intent.
- [08:47 UTC] Quota snapshot: ai-watcher-prompts 153/500; serps 383/1200; related-keywords 298/1200; trends 1089/1200; sch-url-metrics 1335/1440; kw-url-metrics 936/1440; links 1,077,290/1.2M; tracked_keywords 1651/1651 (not decrementing on add).
- [~08:49 UTC] **Related-keywords US seed batch completed.** All 20 seeds queried and saved to `docs/seo/mangools-raw/related-keywords-*-us-2840.json`. Switched from `full=true` to compact summary (`full=false`) after the first `private ai chat` response was too large to persist inline and the persisted file was empty. Compact summaries still return up to 100 related keywords and are fully savable.
- [~08:49 UTC] Top US high-volume related keywords discovered:
  - `duckduckgo` (6.12M), `perplexity` (1.62M), `venice ai` (192K), `duck ai` (60.3K), `ai chat free` (31.6K) — from broad seed `private ai chat`.
  - `mlc llm` (490), `mlc chat` (360), `mlc chat apk` (80), `local llm android` (80) — from mobile/local LLM seeds.
  - `on-device ai` (520), `on device llm` (100) — from on-device seed.
  - `locally ai app` (200), `local ai android` (50), `local ai download` (50) — from `local ai android`.
  - `offline ai chat` (390), `offline ai chatbot free` (110), `offline ai chat roleplay` (70) — from `offline ai chat`.
  - `pocketpal ai` (590), `pocketpal ai apk` (30) — from `pocketpal ai`.
- [~08:49 UTC] Quota after US batch: `related-keywords` **282 / 1200** remaining.
- [~08:52 UTC] **Related-keywords UK seed batch completed.** All 20 seeds queried and saved to `docs/seo/mangools-raw/related-keywords-*-uk-2826.json`. A few `500`/`No available SERP provider` errors were retried after 30s and succeeded.
- [~08:52 UTC] Top UK high-volume related keywords discovered:
  - `pocketpal ai` (130)
  - `private ai chat` (110)
  - `offline ai chat` (50)
  - `mlc llm` (60)
  - `local llm android` (20), `local ai android` (20)
- [~08:52 UTC] Quota after UK batch: `related-keywords` **232 / 1200** remaining.

## Notes on AI Search Watcher
- One monitor per `brand + domain + location` allowed. Existing US monitor already covered US, so UK/India monitors added.
- Manual prompts focus on: private AI chat, offline Android chat, local LLM Android, GGUF, llama.cpp, PocketPal/MLC comparisons, on-device privacy.

## SERP + URL-metrics + KD drain progress (2026-07-30 continuation)
- [current session] Quota snapshot at start: serps 387/1200, sch-url-metrics 1339/1440, kw-url-metrics 940/1440.
- SERP provider intermittent (`No available SERP provider` / `Body error` / empty `items` for several keywords); used `full=true` which is more reliable than compact summary.
- Directly completed SERPs (saved to `docs/seo/mangools-raw/serps/`):
  - `private ai chat` (rank 30, 10 organic results incl. duck.ai, privatemode.ai, venice.ai, privacyguides.org)
  - `offline ai chat` (rank 35, AI overview + 7 organic incl. Layla, Uptodown, Google Play)
  - `private chatbot android` (rank 39, 7 organic incl. Layla, chatbotapp.ai, privacyguides.org, PCMag)
  - Empty results saved for: `pocketpal ai`, `mlc llm`, `on device llm`, `local llm android`, `local ai android`, `run llm on android`.
- Launched background agent to finish remaining priority-keyword SERPs and retries.
- URL metrics (`serpchecker_get_url_metrics`) saved for competitor roots and LlamaBox pages:
  - Competitors: pocketpal.ai, mlc.ai, chatgpt.com, ollama.com, lmstudio.ai, jan.ai, gpt4all.io
  - SERP-derived: duck.ai, privatemode.ai, venice.ai, layla-network.ai, chatbotapp.ai, privacyguides.org/en/ai-chat
  - LlamaBox pages: root, /download, /guides, /offline-ai-android, /on-device-llm, /how-to-run-llm-on-android, /private-chatgpt-alternative, /vs-chatgpt, /vs-ollama, /gguf-android
- KD metrics (`kwfinder_get_url_kd_metrics`) saved for competitor roots, LlamaBox pages, and SERP-derived domains.
- Quota after this batch: serps ~349/1200, sch-url-metrics ~1291/1440, kw-url-metrics ~890/1440.

## Notable competitive findings so far
- `chatgpt.com` dominates with DA 84, 5.1M backlinks, 101K ref domains (lps 100).
- `ollama.com` strong with DA 59, 236K backlinks, 18K ref domains (lps 80).
- `lmstudio.ai` DA 55, 143K backlinks, 7.5K ref domains (lps 74).
- `jan.ai` DA 46, 17K backlinks, 2.2K ref domains (lps 60).
- `pocketpal.ai` very small (DA 6, 11 backlinks, lps 11) — closest Android competitor but weak authority.
- `llamabox-ai.github.io` currently DA 1, 1 backlink, lps 1 across all pages — large authority gap vs. competitors.
- SERP-derived privacy apps: `duck.ai` DA 51, lps 89; `venice.ai` DA 41, lps 64; `privatemode.ai` DA 25, lps 45; `layla-network.ai` DA 11, lps 31.

## Next actions
- Wait for background SERP agent completion, then run URL metrics for any additional unique organic URLs it discovers.
- Continue draining remaining `sch-url-metrics` and `kw-url-metrics` quotas on meaningful competitor/LlamaBox URLs until close to reset or quota exhausted.
- Keep saving compact-summary raw JSON to `docs/seo/mangools-raw/`.

## Trends + Linkminer drain — current session (2026-07-30)
- **Trends drain**: 51 `kwfinder_get_keyword_trends` calls completed (31 provided keywords + 20 semantically related Android/local-LLM terms). All saved as `trends-{safe-keyword}.json`. Trend API returned empty data arrays as expected (deprecated, no fresh data since Jan 2025) but consumed quota.
- **URL metrics**: `linkminer_get_url_metrics` completed for 6 competitors: pocketpal.ai, mlc.ai, ollama.com, lmstudio.ai, jan.ai, gpt4all.io. Saved as `url-metrics-*.json`.
- **Backlinks**: `linkminer_get_backlinks` (links_per_domain=1, limit=500) started for all 6 competitors. Pages fetched and saved so far:
  - pocketpal.ai: page 0 (10 links, all returned)
  - mlc.ai: pages 0, 1, 2
  - ollama.com: pages 0, 1, 2, 3, 4
  - lmstudio.ai: pages 0 (l100 + l500), 1, 2, 3, 4
  - jan.ai: pages 0 (l100 + l500), 1, 2
  - gpt4all.io: page 0 (l100 + l500)
- Large responses (>~240KB) were persisted by the MCP runtime to ADS streams; copied to project directory with PowerShell `Get-Content -Stream`.
- Background subagent launched to complete remaining pagination: ollama.com pages 5-19, lmstudio.ai pages 5-19, jan.ai pages 3-5, gpt4all.io pages 1-3.

## Quota after current session (pre-subagent)
- trends: 1063 / 1200 remaining (~106 consumed)
- links: 1,069,270 / 1,200,000 remaining (~8,020 consumed)
- kw-url-metrics: 902 / 1440 remaining
- lm-url-metrics: 1,198,666 / 1,200,000 remaining

## Continuation session — 2026-07-30 (post-context-reload)

### Actions taken
- Refreshed full quota snapshot: serps 1122/1200, related-keywords 1104/1200, kw-url-metrics 852/1440, lm-url-metrics 1,198,662/1.2M, sp-overview 148/150, tracked_keywords 1234/1651, links 1,032,696/1.2M.
- Ran fresh US desktop SERPs for: `private chatgpt alternative android`, `offline ai android`, `llm download` (3 succeeded; `android local llm` and `mlc chat android` hit `No available SERP provider` and will be retried).
- Saved SERP raw JSON to:
  - `docs/seo/mangools-raw/serp-private-chatgpt-alternative-android-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-offline-ai-android-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-llm-download-2026-07-30.json`
- Ran related-keywords for `offline ai android`, `llm download`, `private chatgpt alternative android` and saved compact summaries.
- Ran `linkminer_get_url_metrics` for `layla-network.ai` and `anythingllm.com`.
- Ran `linkminer_get_backlinks` (l100, links_per_domain=1) for `layla-network.ai` (298 total links) and `meetaitools.com` (only 2 backlinks, one PBN spam).
- Added 10 new keywords to existing US desktop SERPWatcher tracking `6a6ac171a4d7d442f2c49a40`, now monitoring 40 keywords.

### Content + site updates driven by SERP data
- Updated `/offline-ai-android.html` to target "best offline ai assistant for android" and added competitor comparison (Layla, Local AI, OfflineLLM, MeetAITools).
- Updated `/private-chatgpt-alternative.html` to target "private chatgpt alternative android" and added competitor comparison (Proton, PrivacyGuides, Lindy, Wondertools).
- Created new `/llm-download.html` guide targeting "llm download" intent with GGUF sourcing, quantizations, and phone-size guidance.
- Created new `/best-local-llm-apps-android.html` roundup targeting "best local llm apps android" / "android local llm" listicle intent with comparison table.
- Added new pages to footer Guides column, `/guides.html` card grid, `/llms.txt`, `/llms-full.txt`, and `sitemap.xml`.
- Regenerated the entire static site with `python scripts/generate_growth_pages.py`.
- Updated `docs/seo/keyword-strategy-2026-07-30.md` with new SERP findings and implementation status.

### Workflow status
- Ultracode workflow `w2pa1mpqh` still running at time of writing.

### Additional Mangools work after first push
- Retried failed SERPs: `android local llm` and `mlc chat android` succeeded on second attempt.
- Saved raw SERP JSON for both keywords.
- Ran related-keywords for `android local llm` and `mlc chat android`; saved compact summaries.
- Ran `linkminer_get_url_metrics` for `layla-network.ai` and `siteprofiler_get_overview` (DA=11, 223 referring IPs).
- Ran `kwfinder_get_url_kd_metrics` for PromptQuorum page (lps=14 — very beatable).

### Additional work completed (continuation session, post-context-reload)
- Ran fresh US desktop SERPs for: `private ai chatbot android`, `chatgpt android offline`, `ollama android`. All succeeded and saved raw JSON.
- Saved raw SERP JSON to:
  - `docs/seo/mangools-raw/serp-private-ai-chatbot-android-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-chatgpt-android-offline-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-ollama-android-2026-07-30.json`
- Ran related-keywords for `chatgpt android offline`, `private ai chatbot android`, `ollama android`; saved compact summaries.
- Ran `linkminer_get_url_metrics` for `fritz.ai` and `toms-guide` SERP-derived domains.
- Ran `kwfinder_get_url_kd_metrics` for Fritz.ai chatgpt-android-offline page (lps=19 — beatable).
- Created new `/chatgpt-android-offline.html` landing page targeting the "chatgpt android offline" query where Fritz.ai ranks with DA=52/0 backlinks.
- Regenerated site, updated `/llms.txt`, `/llms-full.txt`, `sitemap.xml`, footer + guides links.
- Verified SERPWatcher US desktop tracking already contains `chatgpt android offline`, `ollama android`, `private ai chatbot android`, `open source llm android`; 45 keywords active.
- Background workflow `w2pa1mpqh` still running.

### Content + site updates driven by SERP data
- New page: `/chatgpt-android-offline.html` — "ChatGPT Android Offline: Why It Doesn't Work & What Does | LlamaBox"
  - Targets users searching for offline ChatGPT on Android.
  - FAQ clarifies ChatGPT requires internet; LlamaBox is the offline alternative.
  - Added to footer Guides column, `/guides.html` card grid, `/llms.txt`, `/llms-full.txt`, and `sitemap.xml`.

### Latest quota-burn batch (UK/India SERPs + keyword details + backlink profiles)
- Ran UK desktop SERPs for `chatgpt android offline` and `ollama android`; saved summary raw JSON.
- Ran India desktop SERPs for `chatgpt android offline` and `ollama android`; saved summary raw JSON.
- Ran related-keywords for high-volume seeds `duck ai`, `private ai`, `on device ai`; saved compact summaries.
- Ran `serpchecker_get_url_metrics` for Fritz.ai, XDA, Android Authority, Tom's Guide, dev.to, deepakness.com.
- Ran `siteprofiler_get_overview` for `fritz.ai` (DA=52, 124 referring IPs).
- Ran `kwfinder_get_keyword_details` for `private ai` (vol 2,200, KD 31) and `on device ai` (vol 520, KD 33).
- Ran `linkminer_get_backlinks` (l100, links_per_domain=1) for `fritz.ai` (500 total links, profile dominated by legacy robotics + PBN spam) and `ai-toolbox.co` (32 links, mostly directories/PBN spam).
- Saved backlink + keyword-detail raw JSON summaries.
- Workflow `w2pa1mpqh` still running.

## Quota after latest batch
- serps: 1099 / 1200 remaining
- related-keywords: 1082 / 1200 remaining
- kw-url-metrics: 850 / 1440 remaining
- lm-url-metrics: 1,198,660 / 1,200,000 remaining
- sp-overview: 144 / 150 remaining
- tracked_keywords: 1230 / 1651 remaining
- links: 1,031,032 / 1,200,000 remaining

## Continuation batch — content updates + fresh SERPs
- Rewrote `/vs-ollama.html` to target "ollama android" directly: title "Ollama Android alternative | LlamaBox local LLM on Android", FAQ covers "Can you run Ollama on Android?" / "Is there an Ollama Android app?".
- Rewrote `/on-device-llm.html` to target "on device ai": title "On-Device AI on Android | Local LLM with LlamaBox", expanded definition, use cases, and FAQ schema.
- Regenerated site with `python scripts/generate_growth_pages.py`.
- Updated `/llms.txt` and `/llms-full.txt` sitemap descriptions for `/vs-ollama.html` and `/on-device-llm.html`.
- Committed and pushed updates (`0c8790a`).
- Ran fresh US desktop SERPs: `duck ai`, `private ai`, `mlc chat android`, `private ai chatbot android`. Saved raw JSON.
- Ran `kwfinder_get_keyword_details`: `ollama android` (navigational, no official Android app), `mlc chat android` (vol 70, KD 37), `private ai chatbot android` (KD 31). `duck ai` details returned `No available SERP provider`.
- Saved raw SERP JSON to:
  - `docs/seo/mangools-raw/serp-duck-ai-us-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-private-ai-us-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-mlc-chat-android-us-2026-07-30.json`
  - `docs/seo/mangools-raw/serp-private-ai-chatbot-android-us-2026-07-30.json`
- Updated `docs/seo/keyword-strategy-2026-07-30.md` with new SERP findings and implementation status.

## Updated quota after continuation batch
- serps: ~1095 / 1200 remaining (4 used)
- related-keywords: ~1080 / 1200 remaining (2 attempted; 1 success, 1 provider error)
- kw-url-metrics: ~846 / 1440 remaining (4 calls: 3 details + 1 retry success)
- lm-url-metrics: 1,198,660 / 1,200,000 remaining
- sp-overview: 142 / 150 remaining (2 overviews used)
- tracked_keywords: 1230 / 1651 remaining
- links: 1,031,032 / 1,200,000 remaining

## Continuation batch — competitor backlink + domain authority deep dive
- Retried `kwfinder_get_keyword_details` for `duck ai` (succeeded; informational intent, 449M results, Duck.ai dominates SERP).
- Saved `keyword-details-duck-ai-us-2840-2026-07-30.json`.
- Ran related-keywords for `private ai android` (provider error), `duck ai alternative` (provider error), `ollama android alternative` (1 keyword, null volume).
- Ran `siteprofiler_get_overview` for:
  - `deepakness.com` (DA=20, 41 referring IPs)
  - `mobile-artificial-intelligence.com` (DA=3, 1 referring IP)
  - `androidauthority.com` (DA=91, 2,185 referring IPs)
  - `tomsguide.com` (DA=89, 2,039 referring IPs)
- Ran `linkminer_get_backlinks` (l100, links_per_domain=1) for:
  - `deepakness.com/blog/ollama-in-android-linux/` (1 total link from minifeed.net)
  - `mobile-artificial-intelligence.com/` (0 links)
- Ran `serpchecker_get_url_metrics` for:
  - Tom's Guide article "I put 3 local AI chatbots to the test" (PA=42, 2 ref domains, 13 backlinks)
  - Wondertools Substack "The best mobile AI apps" (PA=56, 43 ref domains, 145 backlinks)
- Saved all raw outputs to `docs/seo/mangools-raw/`.
- Updated `docs/seo/keyword-strategy-2026-07-30.md` with new competitive findings.

## Updated quota after backlink deep dive
- serps: ~1095 / 1200 remaining
- related-keywords: ~1080 / 1200 remaining
- kw-url-metrics: ~846 / 1440 remaining
- lm-url-metrics: 1,198,660 / 1,200,000 remaining
- sp-overview: 142 / 150 remaining
- tracked_keywords: 1230 / 1651 remaining
- links: 1,031,032 / 1,200,000 remaining

## Continuation batch — keyword gap analysis + high-volume educational pages
- Ran `kwfinder_get_keyword_gap_analysis` for `llamabox-ai.github.io` vs `mlc.ai` (US). Found 238 gap keywords.
- Saved compact summary as `docs/seo/mangools-raw/keyword-gap-llamabox-vs-mlc-ai-us-2026-07-30.json`.
- Top relevant gaps identified:
  - `what is an llm in ai` (1,600 vol), `what is a llm in ai` (720 vol)
  - `free llms` (1,300 vol)
  - `webllm` (880 vol), `llm software` (590 vol), `mlc chat` (390 vol), `gbnf` (390 vol)
- Created `/what-is-an-llm.html` to target definitional LLM queries with Android pivot.
- Created `/free-llms.html` to target listicle intent for free open-weight models on Android.
- Added both pages to `/guides.html` card grid, footer Guides column, `/llms.txt`, `/llms-full.txt`, and `sitemap.xml`.
- Regenerated site and pushed.

## Updated quota after keyword gap + content batch
- serps: ~1095 / 1200 remaining
- related-keywords: ~1080 / 1200 remaining
- kw-url-metrics: ~846 / 1440 remaining
- lm-url-metrics: 1,198,660 / 1,200,000 remaining
- sp-overview: 142 / 150 remaining
- tracked_keywords: 1230 / 1651 remaining
- links: 1,031,032 / 1,200,000 remaining

*Last updated: 2026-07-30.*
