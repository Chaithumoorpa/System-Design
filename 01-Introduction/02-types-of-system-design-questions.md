# Types of System Design Questions

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: [What are System Design Interviews?](01-what-are-system-design-interviews.md) · 🏠 [Introduction](README.md) · ➡️ Next: [Expectations by Level/YoE](03-expectations-by-level.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Most prompts fall into a handful of families. Recognising the family tells you which ideas to reach
for first and which trade-offs the interviewer probably wants to hear.

## 1. Product / application design ("Design X")

Full user-facing systems: WhatsApp, Instagram, Uber, YouTube, Airbnb.

- **Skill tested:** decomposing a product into services, choosing storage per access pattern, handling read/write asymmetry.
- **Typical deep dives:** feed fan-out, connection management, geo-indexing, media pipelines.
- **Strategy:** pick 2–3 core features, cut the rest explicitly, then design the hardest one properly.
- **Examples in this repo:** [WhatsApp](../08-Real-Time-Communication/WhatsApp/README.md), [FB News Feed](../09-Social-Media-Systems/FB-News-Feed/README.md), [Uber](../11-Location-Based-Services/Uber/README.md).

## 2. Infrastructure / building-block design

The tools other engineers use: rate limiter, key-value store, cache, message queue, load balancer, CDN, scheduler.

- **Skill tested:** internals and first principles: data structures, consistency, failure, replication.
- **Typical deep dives:** partitioning, eviction, quorums, leader election, durability.
- **Strategy:** define the API and guarantees first (what does "delivered" mean?), then the architecture.
- **Examples:** [Rate Limiter](../15-Distributed-Infrastructure/Rate-Limiter/README.md), [Key-Value Store](../15-Distributed-Infrastructure/Key-Value-Store/README.md), [Distributed Cache](../15-Distributed-Infrastructure/Distributed-Cache/README.md).

## 3. Data-intensive / pipeline design

Ingesting, processing and serving large data: ad click aggregation, metrics pipeline, log search, top-K, analytics.

- **Skill tested:** streaming vs batch, exactly-once effects, windowing, storage choice for analytics.
- **Typical deep dives:** late data, deduplication, hot keys, approximate algorithms, cost.
- **Examples:** [Top K](../16-Counting-and-Ranking-Systems/Top-K/README.md), [Monitoring and Alerting](../17-Asynchronous-Systems/Monitoring-and-Alerting/README.md).

## 4. Transactional / correctness-critical design

Money and inventory: payments, wallets, booking, auctions, flash sales, stock exchange.

- **Skill tested:** idempotency, consistency, concurrency control, audit, failure recovery.
- **Typical deep dives:** double-spend/double-booking, sagas, ledgers, reconciliation.
- **Examples:** [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md), [Movie Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md).

## 5. Real-time / collaborative design

Live systems: chat, comments, presence, collaborative docs, video calls, multiplayer games.

- **Skill tested:** persistent connections, ordering, conflict resolution, latency budgets.
- **Typical deep dives:** WebSocket fleets, pub/sub fan-out, OT/CRDT, media relays (SFU).

## 6. Improvement / scaling of an existing system

"Our API has 200 ms p99 and traffic doubles; what would you do?" or "Here is a diagram; find the problems."

- **Skill tested:** diagnosis, prioritisation, measuring before optimising.
- **Strategy:** ask for metrics, find the bottleneck, propose the cheapest effective change first, state the trade-off.

## 7. Estimation-first and trade-off questions

"Estimate storage for 5 years of tweets", "SQL or NoSQL for this workload and why?"

- **Skill tested:** numeracy and decision-making. See [Estimation Cheatsheet](../06-Interview-Tips/02-estimation-cheatsheet.md) and [Choosing the Right Database](../06-Interview-Tips/04-choosing-the-right-database.md).

## Mapping prompts to families

| Prompt | Family | First ideas to reach for |
|---|---|---|
| URL shortener | Product (small) | ID generation, cache, read-heavy |
| Rate limiter | Infrastructure | Token bucket, atomic counters, failure policy |
| Instagram | Product | Object storage + CDN, feed fan-out |
| Payment system | Transactional | Idempotency, ledger, reconciliation |
| Ad click aggregator | Data pipeline | Kafka, windowed aggregation, dedupe |
| Google Docs | Real-time | OT/CRDT, WebSocket, snapshots |
| Distributed cache | Infrastructure | Partitioning, eviction, replication |

## Questions the interviewer may ask inside any family

1. What happens when this component fails?
2. How does this behave at 10× traffic?
3. Where might data become inconsistent?
4. How would you monitor it?
5. What would you change for a global user base?
6. What would you build first for an MVP?

## Interview questions (with answers)

**Q1. The prompt is only "Design Uber". What do you do first?**
Clarify: rider or driver side? ride types? which cities/scale? Decide scope (request ride, match, track, pay), state NFRs (match in seconds, lossy location OK, trips durable), then estimate.

**Q2. How do you recognise an infrastructure question vs a product question?**
The "user" is another engineer and the emphasis is on guarantees (durability, ordering, throughput) rather than features.

**Q3. What if the interviewer gives an existing design and asks for improvements?**
Ask for numbers (QPS, latency, error rates), locate the bottleneck, propose targeted changes (cache, index, queue, shard), and state expected impact and cost.

## Last-minute revision

- Identify the **family** in the first minute; it tells you the deep dives to expect.
- Product ⇒ features + scale; Infra ⇒ guarantees + internals; Pipeline ⇒ streaming semantics; Transactional ⇒ correctness.
