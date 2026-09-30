# Amazon SQS (and SNS)

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [RabbitMQ](08-rabbitmq.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [Flink](10-flink.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**SQS** is a fully managed, durable message queue. **SNS** is managed pub/sub. Together they give
serverless decoupling, buffering and fan-out with no brokers to run.

## SQS essentials

| Property | Standard queue | FIFO queue |
|---|---|---|
| Throughput | Nearly unlimited | 300 msg/s per API (3,000 with batching; higher with high-throughput mode) |
| Ordering | Best effort | Strict within a **message group ID** |
| Delivery | At-least-once (duplicates possible) | Exactly-once processing via dedupe ID (5-minute window) |
| Use | Most workloads | Ordering or dedupe needed |

- **Visibility timeout**: after a consumer receives a message it is hidden for N seconds. If not deleted in time it reappears, hence at-least-once. Set it longer than processing time; extend for long jobs.
- **Long polling** (`WaitTimeSeconds` up to 20): reduces empty responses and cost.
- **Delete after success**: the consumer must explicitly delete the message.
- **Retention**: 1 minute to 14 days. **Max size**: 256 KB (use S3 for larger payloads with a pointer).
- **Delay queues / message timers**: up to 15 minutes.
- **Dead-letter queue**: after `maxReceiveCount` failed receives, move to a DLQ; redrive after fixing.

## Scaling and consumption pattern

```
Producers → SQS → consumers (EC2/ECS/Lambda) — scale on ApproximateNumberOfMessages / age
```

- Lambda triggers poll SQS and scale concurrency automatically; report partial batch failures to avoid reprocessing entire batches.
- Autoscale workers on queue depth per instance or **age of oldest message**.
- Batch send/receive/delete (up to 10) for throughput and cost.

## SNS + SQS fan-out

```
Publisher → SNS topic → SQS queue A (billing)
                      → SQS queue B (email)
                      → Lambda / HTTP / other
```

Each subscriber has its own queue: independent retry, backpressure and DLQ. Use SNS filter policies
so subscribers receive only relevant messages.

## Reliability and idempotency

- Consumers must be **idempotent** (duplicates and redelivery happen). Store processed message IDs or use conditional writes.
- Poison messages: cap receives, DLQ, alarm on DLQ depth.
- Ordering with standard queues: include sequence numbers and reorder or ignore stale updates.

## SQS vs Kafka vs RabbitMQ

| | SQS | Kafka | RabbitMQ |
|---|---|---|---|
| Ops | None | High | Medium |
| Replay | No | Yes | Streams only |
| Ordering | FIFO groups | Per partition | Per queue |
| Consumer model | Competing consumers | Consumer groups per topic | Competing consumers |
| Ideal | Simple buffering, serverless | Event streaming | Rich routing |

## Limits and gotchas

- No native fan-out (add SNS/EventBridge); no replay; message size 256 KB; standard-queue duplicates and reordering.
- Visibility timeout too short ⇒ duplicate processing; too long ⇒ slow recovery from failures.
- FIFO throughput limits and single hot message group serialise processing.

## When to choose it

Decoupling microservices, absorbing traffic spikes ([Absorbing Traffic Spikes](../05-Interview-Patterns/04-absorbing-traffic-spikes.md)),
background work ([Long-Running Tasks](../05-Interview-Patterns/15-handling-long-running-tasks.md)), any AWS
workload needing a queue without operations.

## Interview questions (with answers)

**Q1. Why might a message be processed twice?** Visibility timeout expired before delete, consumer crash after side effect but before delete, or standard-queue duplicate delivery. Make handlers idempotent.

**Q2. How do you process an order stream in order per customer?** FIFO queue with `MessageGroupId = customer_id`; messages within a group are delivered in order, groups processed in parallel.

**Q3. How do you handle a 50 MB payload?** Store it in S3, send the S3 key in the message (extended client library pattern).

**Q4. How do you scale workers?** Scale on queue backlog or oldest-message age; use long polling and batching; set concurrency to what downstream dependencies tolerate.

## Last-minute revision

Visibility timeout ⇒ at-least-once ⇒ idempotent consumers; DLQ for poison messages; FIFO groups for
per-key order; SNS→SQS for fan-out; no replay.

## References

- AWS documentation: SQS Developer Guide; SNS Developer Guide.
