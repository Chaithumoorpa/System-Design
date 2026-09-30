# Concept Questions with Model Answers

Cover the answer, attempt it aloud, then compare. Answers are intentionally compact: expand with examples in a real interview.

## Scaling and architecture

**Q1. Vertical vs horizontal scaling. When do you pick each?**
Vertical is simpler and avoids distribution problems but has a ceiling and is a single point of failure. Horizontal scales further and tolerates failure but needs stateless design, load balancing and data partitioning. Start vertical while cheap, go horizontal when limits, cost or availability demand it.

**Q2. What makes a service stateless and why does it matter?**
No request-specific state is kept in process memory between requests; state lives in shared stores or tokens. Any instance can serve any request, enabling autoscaling, rolling deploys and easy failover.

**Q3. How do you find and fix a bottleneck?**
Measure (metrics, traces, profiling) across CPU, memory, disk, network and lock contention, and dependencies. Fix by caching, batching, indexing, async processing, partitioning or removing work. Verify with load tests.

**Q4. Monolith or microservices for a new startup?**
A modular monolith first. Microservices bring network failure, distributed transactions and operational overhead; extract services when team scale, independent deployment or divergent scaling needs justify it.

## Caching

**Q5. Explain cache-aside, write-through and write-back.**
Cache-aside: app reads cache, on miss loads DB and populates. Write-through: writes go to cache and DB synchronously (consistent, slower). Write-back: write to cache, flush later (fast, risk of loss).

**Q6. What is a cache stampede and how do you prevent it?**
Many requests miss simultaneously on an expired hot key and hammer the DB. Prevent with single-flight/locks, jittered TTLs, refresh-ahead, stale-while-revalidate.

**Q7. How do you keep cache and database consistent?**
You cannot guarantee strict consistency without coordination. Use invalidate-on-write with TTL as a safety net, versioned values, or CDC-driven invalidation; accept bounded staleness where allowed.

**Q8. LRU vs LFU?**
LRU evicts the least recently used: good for recency-biased access. LFU evicts the least frequently used: better for stable popular sets but slow to adapt (needs decay).

## Databases

**Q9. SQL or NoSQL?**
Default SQL for relational data and transactions. Choose NoSQL for a specific need: massive horizontal write scale, simple key access, flexible schema, or multi-region availability. Justify by access patterns, not fashion.

**Q10. Explain database indexing and its cost.**
An index (usually a B-tree) speeds up reads by avoiding full scans. It costs storage and slows writes since each write updates indexes. Composite index order follows the query's equality then range columns.

**Q11. How do you shard, and how do you choose the shard key?**
Partition by hash, range, or directory. Key should have high cardinality, spread load evenly and match the main query so requests hit one shard. Watch for hot shards and cross-shard queries.

**Q12. Why is `hash(key) % N` bad for changing clusters?**
Changing N remaps almost all keys. Consistent hashing (with virtual nodes) or fixed slots moves only about 1/N of the keys.

**Q13. How do you prevent overselling under concurrency?**
Atomic conditional update (`qty = qty - 1 WHERE qty > 0`), row locks, optimistic versioning, or serialising per-item operations through a queue. Add reservations with expiry for multi-step flows.

**Q14. Explain isolation levels and one anomaly each guards against.**
Read committed prevents dirty reads; repeatable read prevents non-repeatable reads; serializable prevents phantoms and write skew. Higher isolation costs concurrency.

## Distributed systems

**Q15. State the CAP theorem correctly.**
During a network partition, a system must choose consistency (refuse or error) or availability (respond, maybe stale). Without a partition both are achievable. PACELC adds the latency vs consistency trade-off in normal operation.

**Q16. What does quorum R + W > N give you?**
Read and write sets overlap, so a read sees at least one replica with the latest acknowledged write (absent failures during concurrent activity/sloppy quorums). It does not by itself give linearizability.

**Q17. How does leader election work?**
Nodes use a consensus protocol (Raft/Paxos) or a coordination service (etcd/ZooKeeper leases). The leader holds a time-limited lease; epochs/terms and fencing tokens prevent an old leader from acting.

**Q18. What is split brain?**
Two nodes both believe they are leader after a partition, causing divergent writes. Prevent with quorum-based election, leases, and fencing.

**Q19. Explain eventual consistency and where it is acceptable.**
Replicas converge if updates stop. Acceptable for feeds, counters, search indexes; not for balances, unique constraints, inventory decisions.

**Q20. Why is exactly-once delivery a myth, and what do you do instead?**
Networks and crashes force retries, so at-least-once is the realistic guarantee. Achieve exactly-once *effect* with idempotent operations and dedupe keys, or transactional writes.

**Q21. 2PC vs saga?**
2PC gives atomic commit but blocks and reduces availability. Saga chains local transactions with compensations: available and scalable but only eventually consistent, and needs idempotent steps.

**Q22. How do clocks affect distributed systems?**
Physical clocks drift and skew, so timestamps from different nodes cannot order events reliably. Use logical clocks, per-partition sequence numbers, or bounded-uncertainty clocks (TrueTime).

## Messaging and async

**Q23. Why use a message queue?**
Decoupling, load leveling, retry/durability and fan-out, at the cost of latency and complexity.

**Q24. How does Kafka guarantee ordering?**
Only within a partition. Use the entity key so all its events land on one partition, and one consumer per partition per group processes them in order.

**Q25. How do you handle a poison message?**
Limit retries with backoff, then route to a dead-letter queue with metadata for inspection and replay; alert on DLQ growth.

**Q26. How do you handle backpressure?**
Bound queues, throttle or reject producers, scale consumers on lag, shed low-priority load, and use flow control in streaming protocols.

## Reliability and operations

**Q27. What are retry storms and how do you avoid them?**
Layers retrying failures amplify load and prevent recovery. Retry at one layer, use exponential backoff with jitter, retry budgets, and circuit breakers.

**Q28. Explain circuit breakers.**
Track failures to a dependency; after a threshold, open the circuit to fail fast; after a cool-down, half-open to probe; close on success. Prevents cascading failure and gives the dependency room to recover.

**Q29. RPO vs RTO?**
RPO is maximum tolerable data loss (time); RTO is maximum tolerable downtime. They drive backup frequency, replication mode and standby strategy.

**Q30. How do you deploy safely?**
Canary or blue-green, feature flags, automated health checks and rollback, backward-compatible schema changes (expand, migrate, contract), gradual regional rollout.

**Q31. What do you monitor?**
Golden signals (latency percentiles, traffic, errors, saturation), business metrics, queue lag, dependency health; alert on SLO burn rate; traces and structured logs with correlation IDs.

## Networking and APIs

**Q32. WebSocket, SSE or long polling?**
WebSocket for bi-directional low-latency, SSE for simple server push, long polling as a universal fallback. WebSockets are stateful: plan for connection registry, reconnect with jitter, and resync.

**Q33. Offset vs cursor pagination?**
Offset is simple but slow on deep pages and unstable under inserts. Cursor (keyset) uses the last seen sort key: stable and fast.

**Q34. How do you design idempotent APIs?**
Idempotency-Key header; store key with result atomically with the effect; return the stored response on retries; reject key reuse with a different payload.

**Q35. How does a CDN help beyond static files?**
Edge caching of cacheable API responses, TLS termination near users, DDoS absorption, connection reuse, and origin offload with shield tiers.

## Security

**Q36. JWT vs sessions?**
JWTs are stateless and scale easily but are hard to revoke; use short lifetimes and refresh tokens. Server sessions are easy to revoke but need shared storage.

**Q37. How do you let users upload large files safely?**
Authenticate, issue short-lived pre-signed multipart upload URLs, upload directly to object storage, verify with checksums, then scan and process asynchronously.
