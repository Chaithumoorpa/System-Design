# Consistency, CAP and PACELC

## CAP theorem

In the presence of a **network partition**, a distributed data store must choose between **consistency** (every read sees the latest write or an error) and **availability** (every non-failing node answers). Partitions are unavoidable, so the real choice is CP vs AP *during a partition*.

- **CP** (e.g. ZooKeeper, etcd, HBase, Spanner-style): refuse or block some requests to stay consistent.
- **AP** (e.g. Cassandra, DynamoDB default, Riak): keep answering, possibly stale, reconcile later.

Common misreading to avoid: CAP is not "pick any two" at all times. Without a partition you can have both.

## PACELC

If there is a **P**artition, choose **A** or **C**; **E**lse (normal operation), choose **L**atency or **C**onsistency. This captures that replication for consistency costs latency even when nothing is broken. Example: Dynamo-style is PA/EL; Spanner is PC/EC.

## Consistency models (strong to weak)

| Model | Guarantee |
|---|---|
| Linearizable (strong) | Operations appear to happen at one instant in real-time order |
| Sequential | All see the same order, not necessarily real time |
| Causal | Causally related operations seen in order |
| Read-your-writes / monotonic reads | Session guarantees per client |
| Eventual | Replicas converge if writes stop |

Stronger models cost latency and availability. Pick per use case, even per operation.

## Choosing by use case

| Use case | Need | Choice |
|---|---|---|
| Bank balance, inventory decrement, unique username | Strong | Single leader, quorum, or consensus |
| Social likes, view counts, feeds | Eventual is fine | Async replication, caches |
| Chat | Per-conversation ordering, delivery guarantees | Partition by conversation, sequence numbers |
| Shopping cart | High availability | AP with merge |

## Consensus (Raft / Paxos in brief)

Consensus lets nodes agree on a value/log despite failures, using majority quorums. **Raft**: one elected leader per term appends entries and replicates them to followers; an entry is committed once a majority stores it; a new leader must have the latest committed log. Tolerates f failures with 2f+1 nodes. Used in etcd, Consul, and many databases for metadata, leader election and config. Not for high-throughput data path across the globe: each commit needs a majority round trip.

## Time and ordering

- Physical clocks drift; NTP is not enough for ordering events across nodes.
- **Lamport clocks** give a logical order consistent with causality; **vector clocks** detect concurrency.
- Spanner's **TrueTime** bounds clock uncertainty and waits it out to get external consistency.
- Prefer per-partition sequence numbers or a log offset for ordering.

## Distributed transactions

- **2PC**: coordinator asks participants to prepare then commit. Atomic but blocking if coordinator fails and holds locks.
- **Saga**: sequence of local transactions with compensating actions. Available and scalable, but only eventually consistent and requires idempotent, compensatable steps. See [saga pattern](../../05-Interview-Patterns/12-coordinating-transactions-across-services.md).
- **Outbox pattern**: write the event to an outbox table in the same local transaction; publish it asynchronously. Avoids dual-write inconsistency.

## Interview questions

1. Explain CAP with a concrete partition scenario for a chat system.
2. What does R + W > N guarantee, and what does it not guarantee?
3. Why is 2PC rarely used across microservices?
4. Where would you accept eventual consistency in an e-commerce system, and where not?

---

## 🔗 Used in these case studies

- [Key-Value Store](../../15-Distributed-Infrastructure/Key-Value-Store/README.md)
- [Unique ID Generator](../../05-Interview-Patterns/19-generating-unique-ids.md)
- [Payment System](../../14-Payment-and-Financial-Systems/Payment-System/README.md)
