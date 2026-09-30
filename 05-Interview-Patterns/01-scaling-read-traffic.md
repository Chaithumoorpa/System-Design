# Pattern: Scaling Read Traffic

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [ZooKeeper](../04-Technology-Deep-Dives/12-zookeeper.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Scaling Write Traffic](02-scaling-write-traffic.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Reads outnumber writes 10–1000× (feeds, catalogues, profiles, short links) and the
database or origin cannot keep up, or latency is too high.

## Recognise it when

- The estimate shows read QPS ≫ write QPS.
- The prompt says "millions of users viewing…", "read-heavy", "low latency".
- Data is tolerant of a little staleness.

## The ladder (apply in order; stop when the numbers are satisfied)

| Step | Technique | Gain | Cost |
|---|---|---|---|
| 1 | **Fix queries and indexes**, connection pooling | Often 10× for free | Index write overhead |
| 2 | **Cache** hot data (browser, CDN, app, Redis) | 10–100× fewer DB reads | Staleness, invalidation |
| 3 | **Read replicas** | Linear read capacity | Replication lag, read-your-writes issues |
| 4 | **Denormalise / precompute** (materialised views, counters, timelines) | Cheap reads | Write complexity, sync |
| 5 | **CDN for cacheable responses** | Global latency, origin offload | Purge complexity |
| 6 | **Partition (shard)** data | Scale storage and throughput | Cross-shard queries |
| 7 | **Specialised read stores** (search index, key-value view) | Fit-for-purpose speed | Extra pipeline, eventual consistency |

## Caching layers

```
Client cache → CDN → API gateway cache → local (in-process) cache → Redis → DB buffer pool → disk
```
Each layer multiplies the effective hit ratio; higher layers are cheaper and less consistent.

**Hit-ratio math:** DB load = (1 − hit) × QPS. Going 90% → 99% cuts DB reads 10×. See [Caching](../03-Concept-Deep-Dives/02-caching.md).

## Read replicas: handling lag

| Symptom | Fix |
|---|---|
| User writes then reads stale data | Read-your-writes: route recent writers to the primary, or track a version/LSN token |
| Time going backwards between reads | Sticky reads to one replica per session |
| Replica far behind | Remove from rotation when lag > threshold |

## Precompute vs compute on read

Precompute when the read pattern is stable and staleness is fine (timeline lists, like counts, search
facets). Compute on read when the query space is large or must be fresh. Often hybrid: precompute
candidates, refine per request.

## Worked example: product page

1. Static/CDN: images, JS, CSS (versioned URLs, cache forever).
2. API response for product details cached at CDN/Redis for 60 s; price/stock fetched separately at lower TTL.
3. Reviews count and rating average maintained as denormalised fields updated asynchronously.
4. Replicas serve non-critical reads; checkout reads from primary.

## Pitfalls

- Caching before measuring; cache stampede on hot key expiry; unbounded key cardinality.
- Read replicas for data needing read-your-writes.
- Forgetting negative caching for "not found".
- Sharding when replicas and caching would do.

## Interview questions (with answers)

**Q1. Reads are 100k QPS on one Postgres. First steps?** Check indexes/queries, add pooling, put a Redis cache-aside layer (target ≥95% hit), then add read replicas; only then consider sharding.

**Q2. How do you keep cached data fresh after a write?** Invalidate on write (delete key) with TTL as a safety net; CDC-driven invalidation for other writers; accept bounded staleness.

**Q3. When are read replicas the wrong tool?** When reads need immediate consistency with writes, or when the bottleneck is a hot key/row (replicas don't spread a single hot key's cache-miss storm as well as caching does).

## Last-minute revision

Index → cache → replicas → precompute → CDN → shard. Quantify hit ratio; handle replication lag and stampedes.

Related: [Handling Hot Keys](03-handling-hot-keys.md) · [Caching](../03-Concept-Deep-Dives/02-caching.md) · [Replication](../03-Concept-Deep-Dives/05-Distributed-Systems/01-replication.md)
