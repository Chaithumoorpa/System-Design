# Pattern: Handling Hot Keys

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Scaling Write Traffic](02-scaling-write-traffic.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Absorbing Traffic Spikes](04-absorbing-traffic-spikes.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Traffic is not uniform. One key (a celebrity profile, viral post, flash-sale product,
popular short link) receives a huge share of requests, overloading the single cache shard, DB
partition or counter that owns it, even when the cluster as a whole has spare capacity.

## Recognise it when

- Access follows a power law (Zipf): top 1% of keys get most traffic.
- Metrics show one shard/partition saturated while others idle; throttling on one key (DynamoDB), a single Redis node at 100% CPU.
- Prompts mention celebrities, viral content, flash sales, live events.

## Detect first

- Per-key request counters with sampling; top-K heavy hitters (Count-Min Sketch).
- Proxy/client-side stats; shard-level skew dashboards.
- Load tests with Zipfian distributions, not uniform.

## Read hot keys

| Technique | How | Trade-off |
|---|---|---|
| **Local (in-process) cache** with tiny TTL | Each app server holds the value for 1–5 s | Bounded staleness; memory |
| **Replicate the key** across shards (`key#1..N`) | Clients read a random replica | Write fan-out to N copies; invalidation |
| **CDN / edge cache** | Serve popular content at the edge | Purge complexity |
| **Request coalescing (single-flight)** | One miss fetch serves all waiters | Latency for waiters |
| **Stale-while-revalidate** | Serve stale while one request refreshes | Slight staleness |
| **Jittered TTLs** | Avoid simultaneous expiry | None |

## Write hot keys

| Technique | How | Trade-off |
|---|---|---|
| **Key splitting / sharded counters** | Write to `k#rand(0..N-1)`, sum on read | Reads cost N lookups; approximate in flight |
| **Buffer and batch** | Accumulate in memory/Redis, flush periodically | Loss window on crash; use durable log if needed |
| **Stream aggregation** | Events → Kafka → aggregator → store | Delay; more infrastructure |
| **Approximate structures** | HyperLogLog, Count-Min | Error bounds |
| **Optimistic conditional writes with backoff** | Reduce lock contention | Retries under load |
| **Serialise via a queue per key** | Single consumer per hot key | Throughput bound by one consumer |

## Worked example: viral like counter (100k likes/s on one post)

1. API records `like(user, post)` in an idempotent store (unique `(user, post)`) to prevent duplicates.
2. Increments go to **sharded Redis counters** (`likes:{post}:{0..15}`).
3. A periodic job (or stream aggregator) sums shards and writes the total to the post record.
4. Display reads a cached total (few seconds stale).

## Worked example: celebrity profile read (5M req/s)

CDN caches the profile JSON (short TTL) + app-local cache (2 s) + Redis; hot-key detection promotes the
profile to a "pinned" replicated set across all cache shards.

## Pitfalls

- Fixing with more shards (does nothing for one key).
- Replicating without a plan for invalidation.
- Local caches with long TTL on data that must be fresh.
- Salting keys and forgetting how to read them back.

## Interview questions (with answers)

**Q1. One Redis shard is at 100% CPU because of one key. Fix?** Add a short-TTL local cache in app servers; replicate the key to multiple shards with random reads; coalesce misses; long term detect and auto-promote hot keys.

**Q2. How do you implement a counter for a viral post without a hot row?** Shard the counter into N sub-counters, increment a random one, sum on read (or aggregate asynchronously).

**Q3. Why doesn't consistent hashing solve hot keys?** It balances *keys* across nodes, not *traffic per key*; one key still maps to one node.

## Last-minute revision

Detect → cache locally → replicate/split → coalesce → aggregate writes. "Uniform hashing balances keys, not load."

Related: [Counting at Scale](20-counting-at-scale.md) · [Caching](../03-Concept-Deep-Dives/02-caching.md) · [Fan-out & hot keys notes](../_Reference/fanout-and-hot-keys.md)
