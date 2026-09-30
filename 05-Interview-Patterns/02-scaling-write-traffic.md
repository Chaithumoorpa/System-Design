# Pattern: Scaling Write Traffic

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Scaling Read Traffic](01-scaling-read-traffic.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Handling Hot Keys](03-handling-hot-keys.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** The write rate (or write volume) exceeds what a single database primary can absorb:
messages, events, metrics, IoT, clickstreams, likes.

## Recognise it when

- Estimates show tens of thousands+ of writes per second, or TBs/day ingest.
- Writes are append-heavy (events/logs) or spread across many entities.
- A single primary shows CPU/IO/lock saturation, replication lag, or WAL pressure.

## The ladder

| Step | Technique | Notes |
|---|---|---|
| 1 | **Optimise the write path**: fewer indexes, batch inserts, prepared statements, right isolation level, SSD/NVMe | Cheap and effective |
| 2 | **Buffer with a queue/log** (Kafka/SQS) and write in batches | Smooths bursts; adds latency; needs idempotent consumers |
| 3 | **Batch and coalesce** updates (e.g. aggregate counters in memory, flush periodically) | Fewer, larger writes |
| 4 | **Partition/shard** by a well-distributed key | Linear write scale; cross-shard complexity |
| 5 | **Switch to write-optimised storage** (LSM: Cassandra, RocksDB; DynamoDB) | Sequential writes, compaction |
| 6 | **Reduce write volume**: sampling, aggregation, TTL, compress, don't store what you can derive | Often the best lever |
| 7 | **Async and eventual**: accept then process | Requires a status/notification story |

## Partitioning writes well

- Choose a key with **high cardinality and even traffic** (user_id, conversation_id), not time or a single tenant.
- **Time-ordered keys** create a hot shard on "now"; prefix with a hash or bucket (`hash(id) % N` + time).
- Use **many logical partitions** (e.g. 1024) mapped to fewer nodes so rebalancing moves whole partitions.
- Avoid cross-shard transactions; co-locate data that changes together.

## Batching and buffering

```
Clients → API (validate, ack quickly) → Kafka (partition by key) → Consumer (batch 500 rows) → DB
```
Trade-off: ack after enqueue (fast, eventual visibility) vs after persist (slower, durable). Use an
idempotency key so retries after partial batch failure do not duplicate.

## Write amplification to watch

Indexes, secondary indexes, replication, WAL, compaction (LSM), denormalised copies (fan-out on write).
Each logical write may become 5–20 physical writes; count them in your estimate.

## Counters and hot rows

`UPDATE counters SET n = n + 1` on one row serialises writers. Use sharded counters
(`counter#0..N`), Redis `INCR` with periodic flush, or streaming aggregation. See
[Counting at Scale](20-counting-at-scale.md) and [Handling Hot Keys](03-handling-hot-keys.md).

## Worked example: chat message ingest (700k msgs/s peak)

1. Gateways accept and forward; chat service assigns per-conversation sequence.
2. Messages written to Cassandra/DynamoDB partitioned by `(conversation_id, bucket)`.
3. Kafka side-channel for push notifications, search indexing, analytics (not on the write critical path).
4. Media bytes go to object storage, not the message store.

## Pitfalls

- Sharding on a skewed key; ignoring secondary index cost; unbounded partitions.
- Batching without idempotency; queue with no backpressure or DLQ.
- Assuming a bigger primary "fixes" it; vertical scaling has a ceiling.

## Interview questions (with answers)

**Q1. Postgres primary is at 90% write IOPS. Options?** Batch and reduce indexes; move append-only data (events) elsewhere; partition tables; shard by tenant/user; or move the write-heavy workload to an LSM store while keeping transactional data in Postgres.

**Q2. Why are LSM stores good for writes?** Writes are sequential appends to a log and memtable; random I/O is deferred to background compaction.

**Q3. How do you prevent a hot shard for time-series ingest?** Partition by `(entity_id, time_bucket)` so writes spread across entities, not just the newest time range.

## Last-minute revision

Optimise → buffer/batch → shard on a well-distributed key → LSM store → reduce volume. Count write amplification; make retries idempotent.

Related: [Kafka](../04-Technology-Deep-Dives/07-kafka.md) · [Cassandra](../04-Technology-Deep-Dives/05-cassandra.md) · [Sharding](../03-Concept-Deep-Dives/05-Distributed-Systems/02-sharding-partitioning.md)
