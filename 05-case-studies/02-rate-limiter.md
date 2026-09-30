# Design a Distributed Rate Limiter

**Prompt:** Limit each client to N requests per time window across a fleet of API servers.

## Requirements

- Functional: configurable rules (per user, API key, IP, endpoint, tier); reject with 429; allow bursts within policy.
- Non-functional: adds under ~2 ms overhead, highly available, accurate enough (small overshoot acceptable), handles millions of keys.
- Decision: a shared library/sidecar at the gateway, backed by a central counter store.

## Estimates

- 500k requests/s at the gateway, 10M active limiter keys. Each key state is a few dozen bytes: ~1 GB. A Redis cluster comfortably handles it; the rate of checks is the constraint (500k ops/s means several shards).

## Design

```
Client -> API Gateway [rate-limit middleware] -> Redis cluster (counters)
                              ^
                        Rules service / config store (cached locally, pushed on change)
```

1. Middleware builds key `(rule_id, client_id)`.
2. Runs an atomic Redis Lua script implementing the algorithm; returns allow/deny plus remaining and reset time.
3. Allowed: forward. Denied: 429 with `Retry-After` and `X-RateLimit-*` headers.

## Algorithm choice

Token bucket (bursty, cheap: store `tokens`, `last_refill`), or sliding window counter for smooth accuracy. Discuss the boundary-burst flaw of fixed windows.

```
-- Lua (atomic): refill by elapsed time, cap at capacity, take 1 token
```

## Deep dives

- **Atomicity**: read-modify-write races across gateways; Lua script or single `INCR` solves.
- **Sharding**: Redis Cluster, key hashed by client; hot clients (one abusive key) get a dedicated local first-level limiter.
- **Latency**: keep-alive pooled connections; optionally **local pre-limit** with periodic sync, so most requests avoid a network round trip. Trade accuracy for speed.
- **Failure policy**: Redis down -> fail open (protect availability) with a conservative local fallback limit; critical protective limits may fail closed.
- **Multi-region**: per-region budgets (each region gets a share) or asynchronous global counters; accept some overshoot.
- **Rules**: stored in a config service, versioned, hot-reloaded; tiered plans.
- **Race between check and work**: rate limit on entry; separate concurrency limits for expensive endpoints.

## Observability

Rejection rate per rule, top limited keys, limiter latency, Redis saturation.

## Follow-ups

- Limit by user across multiple devices and IPs?
- Different limits per endpoint cost (weighted tokens)?
- How do you stop retry storms after 429 (backoff and jitter guidance to clients)?
- Compare token bucket, sliding window log, sliding window counter on memory and accuracy.
