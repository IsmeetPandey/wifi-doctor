# Wi-Fi Doctor 🩺

> Find which layer of a local network is failing.

Wi-Fi Doctor is a **local network diagnostic tool** that checks gateway reachability, DNS timing, public internet reachability, and basic latency signals. It is designed to give a more useful starting point than a single speed-test number.

## What it checks

- Default-gateway discovery on common desktop operating systems
- Gateway reachability
- DNS lookup timing
- Public internet reachability
- Basic latency and reply-rate signals
- Human-readable diagnosis output

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

> **Important:** run this locally. A deployed copy diagnoses the server's network, not the Wi-Fi connection of the device viewing it.

## How to interpret results

Think in layers: **device → gateway → DNS → public internet**. A failure at one layer can make later checks fail too, so the output is diagnostic evidence rather than a definitive root-cause claim.

## Quality & maintenance

- Dependency updates are managed with Dependabot.
- CI performs a Python compilation/smoke check on pushes and pull requests.
- Contributions are documented in `CONTRIBUTING.md`.
- Security reports should follow `SECURITY.md`.

## Roadmap

- [ ] Jitter charts
- [ ] HTTP/TLS checks
- [ ] Network-interface details
- [ ] Historical diagnostic timeline

## Scope & privacy

The tool is intended for local diagnostics. Avoid collecting or exposing network information you do not need for the diagnostic task.
