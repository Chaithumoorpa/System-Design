# 🧩 Basics — High Level Design

Small, self-contained systems that teach the building blocks used everywhere else: **unique IDs,
caching, atomic counters, failure policy**. Start here.

Every problem follows the same flow:
**Clarify → Estimate → APIs → High-Level Design → Database → Deep Dive → Follow-ups (answered) → Practice → Revision**.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 1 | [URL Shortener](URLShortener/README.md) | Range-allocated codes, cache-aside, 301 vs 302, async click analytics, expiry | [Caching](../../02-core-concepts/03-caching.md), [Sharding](../../02-core-concepts/06-sharding-partitioning.md) |
| 2 | [Rate Limiter](RateLimiter/README.md) | Token bucket, Redis Lua atomicity, fail-open vs fail-closed, multi-region budgets | [Rate limiting](../../02-core-concepts/10-rate-limiting.md), [Redis](../../03-technologies/01-redis.md) |
| 3 | [Unique ID Generator](UniqueIdGenerator/README.md) | Snowflake bit layout, worker-ID leases, clock rollback handling | [Consistency & time](../../02-core-concepts/07-consistency-and-cap.md) |

⬅️ [All HLD problems](../README.md) · ➡️ Next category: [Real-Time Communication](../Real-Time-Communication/README.md)
