# Must-Know Concepts

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: [Study Plan (bonus)](../01-Introduction/04-study-plan.md) · 🏠 [Must-Know Topics](README.md) · ➡️ Next: [Technologies](02-technologies.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

A one-page map of the vocabulary that appears in nearly every system design interview. For each
concept: what it is, why it matters, and where to go deeper.

## Scaling and performance

| Concept | One-liner | Deeper |
|---|---|---|
| Latency vs throughput | Time per request vs requests per second; optimising one can hurt the other | [Estimation](../06-Interview-Tips/02-estimation-cheatsheet.md) |
| Percentiles (p50/p95/p99) | Tail latency is what users feel; averages hide it | [Failures](../05-Interview-Patterns/09-surviving-component-failures.md) |
| Vertical vs horizontal scaling | Bigger machine vs more machines | [Scalability](../_Reference/scalability.md) |
| Statelessness | Any instance can serve any request; state lives elsewhere | [Scalability](../_Reference/scalability.md) |
| Load balancing | Spread requests across instances (L4/L7, algorithms, health checks) | [Load balancing](../_Reference/load-balancing.md) |
| Caching | Keep hot data close; cache-aside, write-through, eviction, invalidation | [Caching](../03-Concept-Deep-Dives/02-caching.md) |
| CDN | Cache content at the network edge | [CDN and storage](../_Reference/cdn-and-storage.md) |
| Batching and async | Trade latency for throughput; decouple with queues | [Messaging](../_Reference/messaging-and-streaming.md) |

## Data

| Concept | One-liner | Deeper |
|---|---|---|
| ACID | Atomicity, consistency, isolation, durability of transactions | [Database design](../03-Concept-Deep-Dives/04-database-design.md) |
| Indexes | Trade write cost and space for read speed (B-tree, LSM, inverted) | [Database design](../03-Concept-Deep-Dives/04-database-design.md) |
| Normalisation vs denormalisation | Integrity vs read speed | [Database design](../03-Concept-Deep-Dives/04-database-design.md) |
| SQL vs NoSQL | Relational guarantees vs horizontal scale and flexible access | [Choosing a database](../06-Interview-Tips/04-choosing-the-right-database.md) |
| Replication | Copies for availability, durability, read scale | [Replication](../03-Concept-Deep-Dives/05-Distributed-Systems/01-replication.md) |
| Sharding / partitioning | Split data across nodes | [Sharding](../03-Concept-Deep-Dives/05-Distributed-Systems/02-sharding-partitioning.md) |
| Consistent hashing | Minimal data movement when nodes change | [Consistent hashing](../03-Concept-Deep-Dives/05-Distributed-Systems/04-consistent-hashing.md) |
| Object storage | Cheap, durable blobs behind an HTTP API | [S3](../04-Technology-Deep-Dives/11-s3.md) |

## Distributed systems

| Concept | One-liner | Deeper |
|---|---|---|
| CAP / PACELC | Under partition choose consistency or availability; otherwise latency vs consistency | [Consistency and CAP](../03-Concept-Deep-Dives/05-Distributed-Systems/03-consistency-and-cap.md) |
| Consistency models | Strong, causal, read-your-writes, eventual | same |
| Consensus (Raft/Paxos) | Agreement on a value/log despite failures | same |
| Leader election and leases | One owner at a time, with fencing | [ZooKeeper](../04-Technology-Deep-Dives/12-zookeeper.md) |
| Idempotency | Repeating an operation has the same effect as once | [Duplicate processing](../05-Interview-Patterns/10-preventing-duplicate-processing.md) |
| Delivery semantics | At-most-once, at-least-once, "exactly-once" effect | [Messaging](../_Reference/messaging-and-streaming.md) |
| Sagas and outbox | Multi-service workflows without 2PC | [Transactions](../05-Interview-Patterns/12-coordinating-transactions-across-services.md) |
| Backpressure and load shedding | Protect a system by refusing work early | [Failures](../05-Interview-Patterns/09-surviving-component-failures.md) |
| Retries, timeouts, circuit breakers | Make failure survivable without amplifying it | same |

## Networking and APIs

| Concept | One-liner | Deeper |
|---|---|---|
| DNS, TCP, TLS, HTTP/2/3 | How a request reaches a server | [Networking](../03-Concept-Deep-Dives/01-networking.md) |
| REST, gRPC, GraphQL | API styles and when to use each | [API design](../03-Concept-Deep-Dives/03-api-design.md) |
| WebSocket, SSE, long polling | Real-time delivery options | [Pushing real-time updates](../05-Interview-Patterns/05-pushing-realtime-updates.md) |
| Pagination | Cursor beats offset for changing data | [API design](../03-Concept-Deep-Dives/03-api-design.md) |
| Rate limiting | Cap usage per client | [Rate Limiter](../15-Distributed-Infrastructure/Rate-Limiter/README.md) |

## Operations

Observability (metrics, logs, traces), SLI/SLO/SLA, RPO/RTO, canary/blue-green deploys, feature flags,
autoscaling, capacity planning. See [Monitoring and Alerting](../17-Asynchronous-Systems/Monitoring-and-Alerting/README.md).

## Self-test (answer aloud in 20 seconds each)

1. Why is p99 latency more useful than the mean?
2. When is a cache harmful?
3. What does "R + W > N" guarantee?
4. Why can't you get exactly-once delivery over a network?
5. What breaks when you scale a stateful service horizontally?

<details><summary>Answers</summary>

1. Users experience the tail; averages hide slow outliers, and fan-out makes tail latency dominate.
2. When data is rarely reused, must always be fresh, or the added invalidation complexity outweighs the gain.
3. Read and write replica sets overlap, so a read hits at least one replica with the latest acknowledged write.
4. Messages and acks can be lost, so senders must retry; you get at-least-once, and dedupe for effectively-once.
5. Requests need the same instance (stickiness), state migration on scale events, and failover loses state.
</details>

## Last-minute revision

Know each concept in **one sentence, one trade-off, one example**. The pages linked above expand each.
