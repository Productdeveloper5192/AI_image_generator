# AI Image Generator

A minimal Streamlit app that turns a text prompt into an image, with zero API keys or account setup — it calls [Pollinations.ai](https://pollinations.ai)'s free public image-generation endpoint directly.

## What It Does

- Takes a text prompt and generates an image from it, with adjustable width/height (256–1024px) and an optional seed for reproducible results (same seed + same prompt = same image).
- Displays the generated image inline and offers a one-click download.
- Requires no sign-up, no API key, and no backend of its own — the entire "model" call is a single HTTP GET to Pollinations' hosted service.

## End-to-End Flow

```
 User enters a prompt + picks width/height/seed, clicks "Generate Image"
        │
        ▼
 Prompt is URL-encoded and built into:
   https://image.pollinations.ai/prompt/{prompt}?width=..&height=..&seed=..&nologo=true
        │
        ▼
 requests.get(url, timeout=30)
   - Pollinations generates the image server-side and returns raw image bytes
        │
        ▼
 response.status_code == 200
   - image bytes wrapped in BytesIO
   - rendered with st.image()
   - offered via st.download_button() as a .jpg
        │
        └── non-200 / exception -> error shown in the UI instead of a blank page
```

There's no local model, no GPU, and no persisted state — every generation is a fresh request to Pollinations' API, and the app itself is just a thin UI over that one endpoint.

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Image generation | [Pollinations.ai](https://pollinations.ai) public API (no key required) |
| HTTP | `requests` |

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run Model_api.py
```
Open the URL Streamlit prints (typically `http://localhost:8501`), type a prompt (e.g. *"A futuristic city with flying cars, cyberpunk style"*), and click **Generate Image**.

## Note

Since generation happens entirely on Pollinations' free public service, availability and rate limits are outside this app's control — an error banner (rather than a crash) is shown if their endpoint is slow or returns a non-200 response.
