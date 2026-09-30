# Design a Distributed Cache

**Prompt:** Build an in-memory cache cluster (Redis/Memcached-like) used by many services.

## Requirements

- Functional: `get`, `set` (with TTL), `delete`; optional atomic ops; eviction when full.
- Non-functional: sub-ms latency, 1M+ ops/s cluster-wide, horizontal scaling, high availability, tolerable loss (it is a cache), hot-key resilience.

## Estimates

- 2 TB working set, 1M ops/s. Nodes of 64 GB usable -> ~32+ shards. Each shard ~30k ops/s: comfortable.

## Architecture

```
Clients (smart client lib or proxy) --consistent hashing--> Cache nodes (primary + replica)
Config/membership service (gossip or etcd) -> cluster topology
```

## Components and decisions

- **Partitioning**: consistent hashing with virtual nodes, or fixed hash slots (Redis Cluster: 16384). Client library caches the slot map; or a proxy (Twemproxy/Envoy) hides topology.
- **Node internals**: hash table for O(1) lookup, memory allocator (slab allocator to limit fragmentation), doubly linked list or approximate LRU/LFU for eviction, TTL via lazy expiry on access plus periodic sampling sweeps.
- **Replication**: async primary-replica per shard; failover via sentinel/consensus. Accept small data loss.
- **Concurrency**: single-threaded event loop (simple, no locks, atomic commands) or sharded multi-thread per core.
- **Eviction**: LRU (list + hash map), LFU (frequency counters with decay), TTL priority. Approximate algorithms (sample N keys, evict the least recent) save memory and CPU.
- **Consistency with DB**: cache-aside pattern by clients; invalidate on write; short TTLs; CDC-driven invalidation for critical data.

## Deep dives

- **Hot keys**: detect via sampling; client-side local caching with tiny TTL, replicate hot key to multiple shards, key suffix sharding.
- **Stampede protection**: single-flight per key, probabilistic early refresh, stale-while-revalidate.
- **Rebalancing on node add/remove**: consistent hashing moves ~1/N keys; new nodes start cold: warm gradually, throttle misses to the DB.
- **Failure handling**: client timeouts and circuit breaker; on node loss requests fall through to DB (protect DB with rate limits); replicas promote.
- **Multi-tenancy**: namespaces, per-tenant quotas, memory limits, isolation of noisy neighbours.
- **Observability**: hit ratio, evictions, latency percentiles, memory fragmentation, top keys, connection count.
- **Security**: network isolation, auth/TLS.

## Follow-ups

- Implement LRU in O(1) (hash map + doubly linked list).
- How do you support atomic multi-key operations across shards?
- Cross-region replication of cache? (Usually avoid: invalidate via events rather than replicate.)
