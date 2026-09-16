# Wi-Fi Doctor 📡

A network diagnostics tool that answers **where** a connection is struggling instead of reporting only one speed-test number.

## Diagnostic model

```text
Device → Gateway → DNS → Internet → Latency/Jitter → Throughput
```

The tool will test each layer independently and present evidence such as:

- gateway reachability
- DNS resolution time
- latency and jitter samples
- packet-loss observations
- HTTP reachability
- download/upload throughput
- a time-series stability view

The result should explain *which measurement is abnormal* rather than pretending to know the user's ISP problem from a single score.

## Build phases

- **Phase 1:** cross-platform connectivity checks
- **Phase 2:** repeated measurements + charts
- **Phase 3:** diagnostic rules with transparent evidence
- **Phase 4:** exportable diagnostic report

## Intended stack

Python + FastAPI + JavaScript + WebSockets + Chart.js.
