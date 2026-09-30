# Rate Limiting

Rate limiting caps how much a client can do in a time window. It protects services from abuse, overload and cost blowups, and enforces fair use and quotas.

## Where to enforce

API gateway / edge (best for coarse limits), service middleware (per-endpoint), or client-side (courtesy only). Limit by user ID, API key, IP, tenant, or endpoint, often in layers.

## Algorithms

| Algorithm | How | Pros | Cons |
|---|---|---|---|
| **Token bucket** | Bucket refills at rate r up to capacity b; each request takes a token | Allows bursts, tiny state, widely used | Two parameters to tune |
| **Leaky bucket** | Requests enter a queue drained at fixed rate | Smooth output rate | Bursts delayed or dropped |
| **Fixed window counter** | Count per calendar window | Very simple | Boundary burst: up to 2x limit around a window edge |
| **Sliding window log** | Store timestamps, count within last window | Exact | Memory heavy |
| **Sliding window counter** | Weighted blend of current and previous window counts | Good approximation, low memory | Approximate |

### Token bucket pseudocode

```
refill = (now - last_ts) * rate
tokens = min(capacity, tokens + refill)
last_ts = now
if tokens >= 1: tokens -= 1; allow
else: reject with 429 and Retry-After
```

## Distributed rate limiting

State must be shared so limits hold across gateway instances.

- **Central store (Redis)**: atomic ops via Lua script or `INCR` + `EXPIRE`. Simple and accurate; adds a hop and a dependency. Shard by limiter key.
- **Local + sync**: each node enforces a share of the limit and syncs periodically. Fast, approximate.
- **Sticky routing**: route a key to one node. Simple but uneven.

Race conditions: read-modify-write across two commands is not atomic. Use a Lua script or `INCR` result to decide.

Failure policy: **fail open** (allow if limiter store is down; protects availability) or **fail closed** (block; protects backend). Choose per use case and say so.

## Response behaviour

- HTTP 429 with `Retry-After`, plus `X-RateLimit-Limit/Remaining/Reset` headers.
- Clients should use exponential backoff with jitter.
- Options beyond rejecting: queue, degrade, shed low-priority traffic first.

## Related protections

Load shedding, concurrency limits (bulkheads), circuit breakers, quotas per billing plan, CAPTCHA and bot detection for abuse.

## Design details to discuss

- Rules config store with hot reload (per-tier and per-endpoint limits).
- Multi-region: per-region limits or approximate global counters.
- Cost of the check on the hot path: aim for a single Redis round trip, or local pre-check.
- Observability: rejection rate, top offenders, rule hit counts.

## Interview questions

1. Why does fixed window allow twice the limit, and how does sliding window counter fix it?
2. Design distributed rate limiting for 10 gateways with a shared 100 req/s per user limit.
3. What should happen when Redis is down?
4. Token bucket vs leaky bucket for API protection vs traffic shaping?

---

## 🔗 Used in these case studies

- [Rate Limiter](../05-case-studies/Basics/RateLimiter/README.md)
- [Flash Sale / Inventory](../05-case-studies/Commerce-and-Payments/FlashSaleInventory/README.md)
- [Ticket Booking](../05-case-studies/Commerce-and-Payments/TicketBooking/README.md)
