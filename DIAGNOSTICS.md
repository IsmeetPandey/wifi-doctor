# Diagnostic Interpretation

Wi-Fi Doctor is a layered connectivity check. The useful question is where connectivity begins to fail.

## Suggested reading order

1. **Gateway** — tests whether the local network path can reach the default gateway.
2. **DNS** — measures whether names can be resolved and how long the lookup takes.
3. **Internet reachability** — checks whether a public endpoint can be reached.
4. **Latency and reply rate** — adds basic stability signals to the diagnosis.

## Interpreting results

A failed gateway probe points toward the local network path. A healthy gateway with DNS problems suggests a resolver issue. A healthy gateway and DNS path with failed public reachability suggests the problem may be farther upstream.

These are heuristics, not proof of root cause. VPNs, firewalls, captive portals, routing changes, and temporary server failures can affect observations.

## Measurement boundary

Run the application locally when diagnosing your own device/network. A deployed copy observes the server's network rather than the visitor's Wi-Fi connection.
