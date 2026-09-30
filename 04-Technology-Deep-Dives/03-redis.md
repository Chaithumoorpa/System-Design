# Redis

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [MongoDB](02-mongodb.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [DynamoDB](04-dynamodb.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

In-memory data structure store; single-threaded command execution, extremely fast (~100k ops/s per node), optional persistence.

## Data structures and use cases

| Type | Use |
|---|---|
| String | Cache values, counters (`INCR`), locks (`SET key val NX PX ttl`) |
| Hash | Objects/sessions with fields |
| List | Simple queues, recent-items lists |
| Set | Unique members, tags, mutual friends (`SINTER`) |
| Sorted set (ZSET) | Leaderboards, rate limiting windows, delayed job queues by timestamp, feeds |
| Bitmap / HyperLogLog | Daily active flags; approximate distinct counts (12 KB, ~0.8% error) |
| Geo | `GEOADD`/`GEOSEARCH` on top of sorted sets |
| Streams | Log-like queue with consumer groups |
| Pub/Sub | Fire-and-forget messaging (no persistence) |

## Persistence

- **RDB snapshots**: periodic point-in-time; compact, can lose recent writes.
- **AOF**: append-only log of writes, fsync policy (always / every second / OS); more durable, larger.
- Often both. Cache-only deployments may disable persistence.

## Scaling and availability

- **Replication**: async leader-replica.
- **Sentinel**: monitoring and automatic failover for a single-shard setup.
- **Cluster**: 16384 hash slots spread across shards; clients route by slot (`MOVED` redirects); multi-key operations require keys in the same slot (hash tags `{user1}`).
- Managed offerings hide much of this.

## Patterns

- **Cache-aside** with TTL and jitter.
- **Distributed lock**: `SET lock token NX PX 30000`, release only if token matches (Lua). Single-node locks are not safe under failover or long pauses; use fencing tokens for correctness-critical cases. Redlock is debated; prefer a consensus system for strict guarantees.
- **Rate limiter**: `INCR` + `EXPIRE` or Lua token bucket.
- **Leaderboard**: `ZADD`, `ZREVRANGE`, `ZRANK`.
- **Session store**, **idempotency keys**, **job queues**.

## Pitfalls

- Memory is the limit and cost driver; set `maxmemory` and an eviction policy (`allkeys-lru`, `volatile-ttl`, etc.).
- Big keys and O(N) commands (`KEYS *`, huge `SMEMBERS`) block the event loop; use `SCAN`.
- Hot keys overload a single shard.
- Async replication means acknowledged writes can be lost on failover.
- Not a system of record unless you accept those durability semantics.

## Interview questions

1. Why is Redis fast despite being single-threaded?
2. Design a leaderboard for 50M players with rank lookup.
3. When is a Redis lock unsafe?
4. RDB vs AOF: choose for a session store and for a cache.

---

## 🔗 Used in these case studies

- [Rate Limiter](../15-Distributed-Infrastructure/Rate-Limiter/README.md)
- [Flash Sale / Inventory](../13-E-commerce-and-Marketplace/Flash-Sale/README.md)
- [Distributed Cache](../15-Distributed-Infrastructure/Distributed-Cache/README.md)
- [News Feed](../09-Social-Media-Systems/FB-News-Feed/README.md)
