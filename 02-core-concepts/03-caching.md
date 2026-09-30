# Caching

A cache stores computed or fetched data closer to the consumer to cut latency and backend load. It trades **freshness and complexity** for speed.

## Where to cache

| Layer | Example | Notes |
|---|---|---|
| Browser | HTTP cache headers | Cheapest; controlled by `Cache-Control`, `ETag` |
| CDN | Static assets, video segments, cacheable API responses | Global edge |
| Reverse proxy | Nginx/Varnish | Shared per-region |
| Application (local) | In-process map (Caffeine, Guava) | Fastest, per-instance, inconsistent across nodes |
| Distributed cache | Redis, Memcached | Shared, network hop |
| Database | Buffer pool, query cache | Automatic |

## Read strategies

- **Cache-aside (lazy loading)**: app checks cache; on miss reads DB and fills the cache. Simple, resilient to cache failure, but first read is slow and stale data is possible.
- **Read-through**: cache library loads from DB on miss; app talks only to cache.

## Write strategies

| Strategy | Behaviour | Trade-off |
|---|---|---|
| Write-through | Write to cache and DB synchronously | Consistent, slower writes |
| Write-back (write-behind) | Write to cache, flush to DB later | Fast writes; risk of loss if cache dies |
| Write-around | Write to DB, skip cache | Avoids caching write-once data; first read misses |
| Invalidate on write | Update DB, delete cache key | Common and simple; watch races |

### The classic race

Cache-aside with delete-on-write: Reader misses and reads old value from DB; writer updates DB and deletes key; reader then writes the old value into the cache. Now the cache is stale indefinitely. Mitigations: short TTLs, versioned values, delayed double delete, or change-data-capture driven invalidation.

## Eviction policies

LRU (least recently used, common default), LFU (least frequently used, better for stable hot sets), FIFO, TTL-based expiry, random. Pick by access pattern; combine TTL with LRU.

## Cache failure modes

| Problem | What happens | Fixes |
|---|---|---|
| **Cache stampede / thundering herd** | Hot key expires, thousands of requests hit the DB | Request coalescing (single-flight), locks, jittered TTLs, refresh-ahead, serve stale while revalidating |
| **Cache penetration** | Requests for keys that never exist bypass cache | Cache negative results with short TTL, Bloom filter, input validation |
| **Cache avalanche** | Many keys expire together or cache node dies | Randomise TTLs, replicas, gradual warm-up |
| **Hot key** | One key overloads a single cache node | Local in-process cache for hot keys, replicate key with suffixes (`key#1..N`) |
| **Inconsistency** | Cache and DB disagree | TTLs, CDC invalidation, accept eventual consistency |

## Sizing and hit ratio

Effective latency = hit% x cache latency + miss% x (cache + DB latency). Even 90% to 99% hit rate cuts DB load 10x. Monitor hit ratio, evictions, memory, and per-key hotness.

## HTTP caching cheat sheet

- `Cache-Control: max-age=3600, public` for static assets; use fingerprinted filenames to cache forever.
- `ETag` / `If-None-Match` for conditional requests (304 responses).
- `private` for user-specific responses; `no-store` for sensitive data.
- `stale-while-revalidate` for smooth refresh.

## What not to cache

Highly personalised data with low reuse, rapidly changing values needing strict consistency (account balance for authorisation), or data where a stale read is unacceptable.

## Interview questions

1. Cache-aside vs write-through: choose for a product catalogue and for a shopping cart.
2. A celebrity profile expires and your DB melts. Explain and fix.
3. How do you keep a cache consistent with a database without distributed transactions?
4. How would you size a Redis cluster for 500 GB of hot data at 200k ops/s?

---

## 🔗 Used in these case studies

- [URL Shortener](../05-case-studies/Basics/URLShortener/README.md)
- [News Feed](../05-case-studies/Social-and-Content/NewsFeed/README.md)
- [Distributed Cache](../05-case-studies/Distributed-Infrastructure/DistributedCache/README.md)
- [Flash Sale / Inventory](../05-case-studies/Commerce-and-Payments/FlashSaleInventory/README.md)
