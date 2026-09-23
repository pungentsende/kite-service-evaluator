# Kite Service Evaluator

An offline preflight checker for x402 service manifests. It is intentionally read-only: no RPC calls, signatures, or settlement actions are performed.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
kite-eval examples/weather.json
python -m pytest
```

The evaluator focuses on errors that are easy to miss before integration: malformed recipient addresses, duplicate route paths, empty route sets, and non-positive prices. Findings have stable codes so a CI job can consume them without parsing prose.
