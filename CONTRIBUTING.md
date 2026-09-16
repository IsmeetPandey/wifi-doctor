# Contributing to Wi-Fi Doctor

Wi-Fi Doctor is a local network diagnostic tool that helps identify which layer of a connection may be failing.

## Development flow

1. Create a focused branch for one change.
2. Keep diagnostics transparent: report measurements and observations rather than overstating certainty.
3. Add tests when changing parsing, probes, diagnosis logic, or API behavior.
4. Run the test suite locally before opening a pull request.
5. Explain what changed and how you verified it.

## Privacy and safety

Run network diagnostics on systems and networks you are authorized to inspect. Do not commit network credentials, tokens, personal configuration, or private diagnostic data.

## Pull requests

Small reliability fixes, tests, documentation, portability improvements, and clearer diagnostic output are welcome. Keep changes focused so the result is easy to review.
