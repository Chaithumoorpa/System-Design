# Scalability

Scalability is the ability to handle growth in load (users, data, requests) by adding resources, without redesigning the system.

## Vertical vs horizontal

| | Vertical (scale up) | Horizontal (scale out) |
|---|---|---|
| How | Bigger machine | More machines |
| Pros | Simple, no distribution problems | No hard ceiling, fault tolerant |
| Cons | Ceiling, single point of failure, cost curve | Needs LB, partitioning, coordination |

Interview stance: start simple, scale vertically while cheap, and go horizontal when a requirement or estimate says so.

## Stateless services

A stateless service keeps no per-user state in memory between requests. Any instance can serve any request, so you can add or kill instances freely.

- Move sessions to a shared store (Redis) or into signed tokens (JWT).
- Move uploads and files to object storage.
- Keep local caches as optimisations only, never as the source of truth.

## Scaling each tier

| Tier | Techniques |
|---|---|
| Clients / edge | CDN, caching headers, compression, connection reuse |
| Web/app | Stateless replicas behind LB, autoscaling |
| Cache | Distributed cache, consistent hashing |
| Database | Read replicas, indexing, partitioning/sharding, denormalisation |
| Async work | Queues and workers, batch jobs |
| Search / analytics | Dedicated stores (search index, OLAP), fed asynchronously |

## Bottleneck hunt

Ask in order: CPU, memory, disk I/O, network, locks/contention, downstream dependency. Then apply the fix: cache it, batch it, shard it, make it async, or remove it.

## Read-heavy vs write-heavy

- **Read-heavy**: caching, replicas, CDN, precomputed views, denormalisation.
- **Write-heavy**: partitioning, append-only logs, batching, queues to smooth bursts, LSM-tree stores, async indexing.

## Scaling laws to remember

- **Amdahl's law**: speedup is limited by the serial portion. Shared locks and single leaders cap scale.
- **Hot spots**: uniform hashing does not help if one key is hot (celebrity user, viral post). Use key splitting, local caching, replication of hot keys.
- **Tail latency**: with fan-out to N services, p99 of the whole approaches the worst of them. Use hedged requests, timeouts, and fewer hops.

## Interview questions

1. Your service handles 1k QPS on one node and needs 100k. Walk through the steps.
2. What stops a stateless tier from scaling infinitely?
3. Why can adding shards make some queries slower?

---

## 🔗 Used in these case studies

- [News Feed](../05-case-studies/Social-and-Content/NewsFeed/README.md)
- [Chat System](../05-case-studies/Real-Time-Communication/ChatSystem/README.md)
- [URL Shortener](../05-case-studies/Basics/URLShortener/README.md)
