# Apache Flink (Stream Processing)

<!-- nav:start -->
🏷️ **Priority:** Low · **Difficulty:** Advanced

⬅️ Previous: [SQS](09-sqs.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [S3](11-s3.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Flink is a distributed engine for **stateful computation over unbounded streams** with low latency
and strong correctness guarantees (exactly-once state consistency). It is the usual answer when an
interview needs windowed aggregation over events: ad clicks, trending topics, fraud signals, metrics.

## Why stream processing

| Batch (Spark, MapReduce) | Stream (Flink) |
|---|---|
| Bounded data, periodic | Unbounded, continuous |
| Latency minutes–hours | Latency ms–seconds |
| Simple recovery (rerun) | Needs state and checkpoints |
| Backfills, reports | Real-time dashboards, alerts, pipelines |

## Programming model

```
Source (Kafka) → map/filter → keyBy(key) → window(...) → aggregate/process → Sink (DB, Kafka, Redis)
```

- **DataStream API** (low-level, flexible), **Table/SQL API** (declarative), and connectors for Kafka, files, JDBC, Elasticsearch, etc.
- **keyBy** partitions the stream so each key is handled by one parallel task, enabling per-key state and ordering.
- **Parallelism**: operators run as many parallel subtasks spread over task managers.

## Time and windows

- **Event time** (when it happened) vs **processing time** (when we saw it). Use event time for correct results with out-of-order data.
- **Watermarks** declare "no more events older than T are expected"; a window fires when the watermark passes its end. **Allowed lateness** and **side outputs** handle late events.
- Windows: **tumbling** (fixed, non-overlapping), **sliding** (overlapping), **session** (gap-based), **global** (custom triggers).

```
events per minute per ad:  keyBy(adId).window(TumblingEventTimeWindows.of(1 min)).sum(clicks)
```

## State and fault tolerance

- **Keyed state** (value, list, map) stored on the task manager (RocksDB backend for large state) and snapshotted.
- **Checkpoints**: periodic, asynchronous distributed snapshots (Chandy–Lamport style barriers) written to durable storage (S3/HDFS). On failure Flink restores the last checkpoint and replays the source from the checkpointed offsets, yielding **exactly-once state semantics**.
- **Savepoints**: manual, portable snapshots for upgrades and rescaling.
- **End-to-end exactly-once** requires a transactional/idempotent sink (Kafka transactions with two-phase commit sink, or idempotent upserts).

## Common design patterns

| Need | Flink approach |
|---|---|
| Deduplicate events | Keyed state of seen event IDs with TTL |
| Top-K over window | Per-key counts → window aggregate → global top-K (or Count-Min Sketch) |
| Join streams | Interval join / windowed join / temporal join to a changelog table |
| Enrichment | Broadcast state or async I/O lookups (cache in state) |
| Sessionisation | Session windows with gap |
| CDC to search index | Source from Debezium/Kafka, upsert into Elasticsearch |
| Alerting | CEP patterns or rule evaluation over keyed state |

## Scaling and operations

- Scale by increasing parallelism (rescale from savepoint); parallelism ≤ Kafka partitions for source throughput.
- **Backpressure**: slow operators propagate pressure upstream through bounded buffers; monitor it.
- **Data skew** (hot keys) makes one subtask a bottleneck: pre-aggregate locally, salt keys, two-phase aggregation.
- Watch: checkpoint duration and size, state size, watermark lag, consumer lag.

## Flink vs Spark Streaming vs Kafka Streams

| | Flink | Spark Structured Streaming | Kafka Streams |
|---|---|---|---|
| Model | True streaming | Micro-batch (with continuous mode) | Library inside your app |
| Latency | Lowest | Higher | Low |
| State | Rich, RocksDB, large | Good | Local RocksDB + changelog topics |
| Deployment | Cluster (YARN/K8s/managed) | Cluster | Just a JVM app |
| Best for | Complex stateful, event-time | Unified batch+stream ML/ETL | Simple Kafka-to-Kafka transforms |

## When to choose it

Real-time aggregation, windowed analytics, streaming ETL/CDC, fraud detection, complex event
processing. In an interview, mention it (or "a stream processor") when the design needs windowing and
stateful aggregation; you rarely need to go deeper than checkpoints, watermarks and keyed state.

## Interview questions (with answers)

**Q1. How does Flink achieve exactly-once?** Barrier-based distributed checkpoints capture operator state and source offsets consistently; on failure it restores both and replays. Sinks must be transactional or idempotent for end-to-end exactly-once.

**Q2. What is a watermark and why is it needed?** A monotonic marker of event-time progress that lets windows close despite out-of-order arrival; events later than the watermark are late (dropped, side-output, or within allowed lateness).

**Q3. How do you handle a hot key in an aggregation?** Two-stage aggregation: pre-aggregate with a random salt in parallel, then merge partial results by the real key.

**Q4. How would you count ad clicks per minute exactly once?** Kafka source with event-time tumbling windows keyed by ad ID, dedupe by click ID in keyed state, checkpointing, and an idempotent/transactional sink. See [Ad Click Aggregator](../12-Search-and-Aggregation-Systems/Ad-Click-Aggregator/README.md).

## Last-minute revision

keyBy → windows on **event time** with **watermarks** → keyed state → **checkpoints** (exactly-once state) → transactional/idempotent sinks; watch backpressure and skew.

## References

- Apache Flink documentation; Carbone et al., *State Management in Apache Flink*.
