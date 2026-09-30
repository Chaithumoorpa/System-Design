# RabbitMQ

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [Kafka](07-kafka.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [SQS](09-sqs.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

A mature **message broker** implementing AMQP: producers publish to **exchanges**, which route
messages to **queues** according to bindings; consumers pull or receive messages and acknowledge
them. Its strength is flexible routing and per-message delivery control.

## Core model

```
Producer → Exchange --(binding key / pattern)--> Queue → Consumer(s)
```

| Exchange type | Routing rule | Use |
|---|---|---|
| Direct | Exact routing key match | Task types, per-service queues |
| Topic | Pattern match (`orders.*.created`) | Selective pub/sub |
| Fanout | All bound queues | Broadcast, cache invalidation |
| Headers | Match on message headers | Rare, attribute routing |

- **Queue**: FIFO buffer, can be durable, exclusive, auto-delete, with TTL and max length.
- **Consumers** on a queue compete (work distribution); use **prefetch** (QoS) to bound in-flight messages per consumer.
- **Ack/nack/reject**: message removed only after `ack`; unacked messages return to the queue if the consumer dies.

## Reliability features

- **Durable queues + persistent messages** survive broker restart (write to disk).
- **Publisher confirms** tell producers the broker accepted (and persisted) the message.
- **Dead-letter exchanges (DLX)** capture rejected, expired or overflowed messages.
- **Retry pattern**: DLX with per-message TTL delays and re-routing, or delayed-message plugin.
- **Quorum queues** (Raft-replicated) provide replicated, safe queues; classic mirrored queues are deprecated.
- **Streams**: append-only log with replay, closer to Kafka semantics.

## Delivery semantics

At-least-once by default with acks and confirms; duplicates possible on redelivery, so consumers must
be idempotent. At-most-once with auto-ack. Ordering is preserved per queue with a single consumer;
multiple consumers or redelivery can reorder.

## Scaling and clustering

- A cluster shares metadata; each queue lives on a node (quorum queues replicated across nodes).
- Scale consumers horizontally per queue; scale queues by sharding (consistent-hash exchange plugin).
- Throughput is typically tens of thousands of messages/s per node: lower than Kafka, but with rich
  routing and lower per-message latency.
- Backpressure: memory/disk alarms block publishers; use queue length limits and consumer scaling.

## RabbitMQ vs Kafka vs SQS

| | RabbitMQ | Kafka | SQS |
|---|---|---|---|
| Model | Broker routes to queues | Partitioned log | Managed queue |
| Retention | Until consumed (streams: retention) | Time/size, replayable | Up to 14 days, no replay |
| Routing | Very flexible | By topic/partition key | None (with SNS fan-out) |
| Ordering | Per queue | Per partition | FIFO queues optional |
| Throughput | Moderate | Very high | High (managed) |
| Ops | Self-run/managed | Self-run/managed | None |
| Best for | Task queues, RPC, complex routing | Event streaming, replay, CDC | Simple durable decoupling |

## When to choose it

Background jobs, work queues with priorities, request/reply, complex routing rules, moderate
throughput with strict per-message ack. Avoid when you need replay, very high throughput, or
long retention: use [Kafka](07-kafka.md).

## Interview questions (with answers)

**Q1. How do you avoid losing a task when a worker crashes?** Manual ack after processing; unacked message is requeued; use durable queues, persistent messages and publisher confirms.

**Q2. How do you implement retry with backoff?** Reject to a DLX bound to a delay queue with TTL that routes back to the main queue; increment an attempt header; after max attempts route to a parked (dead-letter) queue.

**Q3. Why set a prefetch count?** Without it the broker pushes unlimited messages to a consumer, causing memory pressure and uneven distribution; small prefetch gives fair dispatch.

**Q4. How do you preserve order with multiple workers?** You cannot on one queue; partition by key into multiple queues (one consumer each) using a consistent-hash exchange.

## Last-minute revision

Exchanges route, queues buffer, consumers ack; durable + confirms + DLX for reliability; competing
consumers with prefetch; not a log, so no replay.

## References

- RabbitMQ documentation (AMQP concepts, reliability guide, quorum queues).
