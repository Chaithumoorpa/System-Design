# Messaging and Streaming

Asynchronous messaging decouples producers from consumers, absorbs bursts, and enables retries and fan-out.

## Why use a queue

- **Decoupling**: producer does not know or wait for consumers.
- **Load leveling**: bursts are buffered; workers drain at their own pace.
- **Reliability**: work survives consumer crashes and can be retried.
- **Fan-out**: one event, many independent consumers.
- **Cost**: added latency, operational complexity, and harder debugging and ordering.

## Queue vs log

| | Message queue (RabbitMQ, SQS) | Distributed log (Kafka, Pulsar, Kinesis) |
|---|---|---|
| Model | Broker tracks per-message state; message removed after ack | Append-only partitioned log; consumers track offsets |
| Replay | Generally no | Yes, within retention |
| Ordering | Per queue (FIFO variants) | Per partition |
| Throughput | Good | Very high |
| Consumers | Competing consumers share work | Consumer groups; each group sees all events |
| Best for | Task/job distribution, per-message routing | Event streams, pipelines, CDC, event sourcing |

## Delivery semantics

- **At-most-once**: may lose messages, never duplicates.
- **At-least-once**: never loses, may duplicate. The default in practice.
- **Exactly-once**: effectively achieved by at-least-once delivery plus **idempotent consumers** (dedupe by message ID) or transactional writes. True end-to-end exactly-once across arbitrary systems does not exist.

## Kafka-style essentials

- Topic split into **partitions**; ordering only within a partition. Choose the message key so related events share a partition.
- **Consumer group**: each partition is consumed by exactly one member; max parallelism = partitions.
- **Offsets** committed after processing (at-least-once) or before (at-most-once).
- **Replication** with leader/followers per partition; `acks=all` plus `min.insync.replicas` for durability.
- **Retention** by time/size; **log compaction** keeps the latest value per key.

## Patterns

- **Pub/sub fan-out**: notifications, cache invalidation, search indexing.
- **Work queue**: image processing, emails. Scale by adding workers.
- **Dead-letter queue (DLQ)**: park messages that fail repeatedly for inspection.
- **Retry with backoff**: retry queues or delay topics; cap attempts.
- **Priority queues**: separate queues per priority to avoid starvation.
- **Backpressure**: bound queue length, throttle producers, autoscale consumers on lag.
- **Outbox + CDC**: reliably publish events from a DB transaction.

## Ordering and duplicates

- Need per-entity order? Partition by entity ID, and process one partition sequentially.
- Consumer retries and rebalances cause duplicates: make handlers idempotent (unique message ID stored with the effect, or naturally idempotent upserts).
- Poison messages block a partition unless you route them to a DLQ.

## Monitoring

Consumer lag, throughput, error and retry rates, DLQ depth, oldest message age, rebalance frequency.

## Interview questions

1. Kafka or SQS for an order pipeline with multiple downstream consumers? Justify.
2. How do you guarantee an email is not sent twice, given at-least-once delivery?
3. A consumer group has 12 consumers but the topic has 8 partitions. What happens?
4. How do you handle a poison message?

---

## 🔗 Used in these case studies

- [Notification Service](../05-case-studies/Real-Time-Communication/NotificationService/README.md)
- [Chat System](../05-case-studies/Real-Time-Communication/ChatSystem/README.md)
- [Job Scheduler](../05-case-studies/Distributed-Infrastructure/JobScheduler/README.md)
- [Metrics and Logging Pipeline](../05-case-studies/Distributed-Infrastructure/MetricsLoggingPipeline/README.md)
- [Top-K / Trending](../05-case-studies/Social-and-Content/TopKTrending/README.md)
