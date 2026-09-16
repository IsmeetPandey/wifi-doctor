# Wi-Fi Doctor 🩺

A local network diagnostic tool that answers a more useful question than a speed test: **which layer is failing?**

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

> Run this locally. A deployed copy diagnoses the server's network, not your phone/PC Wi-Fi.

## Current MVP

- Default-gateway discovery on common desktop OSes
- Gateway reachability probe
- DNS lookup timing
- Public internet reachability probe
- Basic latency and reply-rate signals
- Human-readable diagnosis page

Future versions can add jitter charts, HTTP/TLS checks, interface details, and a historical diagnostics timeline.
