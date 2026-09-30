# Kafka

Distributed, replicated, partitioned commit log for high-throughput event streaming.

## Architecture

- **Broker**: server storing partitions. **Cluster** coordinated by KRaft (Raft-based controller; older versions used ZooKeeper).
- **Topic** split into **partitions**; each partition is an ordered, immutable sequence with an **offset** per record.
- Each partition has a **leader** and follower replicas (**ISR**: in-sync replicas).
- **Producers** choose a partition (by key hash, round robin, or custom).
- **Consumer groups**: partitions are divided among group members. Different groups consume independently.

## Why it is fast

Sequential disk I/O, OS page cache, batching and compression, zero-copy (`sendfile`), and partition-level parallelism.

## Durability and delivery

| Setting | Effect |
|---|---|
| `acks=0/1/all` | Wait for none / leader / all in-sync replicas |
| `replication.factor=3`, `min.insync.replicas=2` | Tolerate one broker loss without losing acked data |
| Idempotent producer | Broker dedupes retries per producer session, no duplicates within partition |
| Transactions | Atomic writes across partitions; enables exactly-once stream processing (read-process-write) |
| Consumer offset commit | After processing gives at-least-once |

## Ordering

Guaranteed only within a partition. To order per entity, key by entity ID. Increasing partition count later changes key-to-partition mapping, so plan capacity upfront.

## Consumer group behaviour

- Rebalances on member join/leave pause consumption briefly; cooperative rebalancing reduces this.
- Parallelism limited by partition count.
- **Lag** = latest offset minus committed offset; the key health metric.

## Retention and compaction

Time/size retention deletes old segments. **Compacted topics** retain the latest record per key (changelogs, state). Tombstones (null value) delete keys.

## Ecosystem

Kafka Connect (source/sink connectors, CDC via Debezium), Kafka Streams / Flink / Spark for stream processing, Schema Registry (Avro/Protobuf) for compatible schemas.

## When to use

Event pipelines, CDC, log aggregation, activity tracking, decoupling microservices, stream processing, event sourcing.
When not: simple task queue with per-message ack/retry semantics, tiny scale, request-response, or when you need very low latency per message with complex routing (RabbitMQ/SQS may be simpler).

## Failure scenarios

- Broker dies: new leader elected from ISR; producers/consumers retry.
- Consumer crashes: group rebalances; uncommitted messages reprocessed (duplicates).
- Hot partition: bad key choice; add salting or change key.
- Slow consumer: lag grows; add consumers up to partition count, or optimise handler.

## Interview questions

1. How does Kafka preserve order, and what breaks it?
2. Explain how to get effectively-once processing.
3. Topic has 6 partitions and lag is growing with 6 consumers. What now?
4. Kafka vs SQS vs RabbitMQ.

---

## 🔗 Used in these case studies

- [Metrics and Logging Pipeline](../05-case-studies/Distributed-Infrastructure/MetricsLoggingPipeline/README.md)
- [Top-K / Trending](../05-case-studies/Social-and-Content/TopKTrending/README.md)
- [Notification Service](../05-case-studies/Real-Time-Communication/NotificationService/README.md)
