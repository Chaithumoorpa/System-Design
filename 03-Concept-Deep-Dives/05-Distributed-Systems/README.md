# Distributed Systems

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Advanced

⬅️ Previous: [Database Design](../04-database-design.md) · 🏠 [Concept Deep Dives](../README.md) · ➡️ Next: [PostgreSQL](../../04-Technology-Deep-Dives/01-postgresql.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../../CREDITS.md).
<!-- nav:end -->

A distributed system is a set of machines that appear to users as one system. The difficulty is not
the number of machines; it is that **parts fail independently, networks are unreliable, and there is
no shared clock**. This chapter is the map; the linked notes are the detail.

## The eight fallacies (why it is hard)

The network is reliable · latency is zero · bandwidth is infinite · the network is secure · topology
never changes · there is one administrator · transport cost is zero · the network is homogeneous.
Every technique below exists because one of these is false.

## Chapter map

| Topic | You will learn | Note |
|---|---|---|
| Replication | Leader/follower, multi-leader, leaderless, lag, failover, split brain, CDC | [Replication](01-replication.md) |
| Partitioning | Range/hash/directory, shard keys, hot shards, resharding | [Sharding and partitioning](02-sharding-partitioning.md) |
| Consistency | CAP, PACELC, consistency models, quorums, consensus, clocks, 2PC/saga | [Consistency and CAP](03-consistency-and-cap.md) |
| Placement | Consistent hashing, virtual nodes, rendezvous hashing | [Consistent hashing](04-consistent-hashing.md) |
| Messaging | Queues vs logs, delivery semantics, ordering, DLQ | [Messaging and streaming](../../_Reference/messaging-and-streaming.md) |
| Resilience | Timeouts, retries, circuit breakers, bulkheads, load shedding | [Surviving component failures](../../05-Interview-Patterns/09-surviving-component-failures.md) |
| Coordination | Leader election, locks, leases, fencing | [ZooKeeper](../../04-Technology-Deep-Dives/12-zookeeper.md) |

## The five questions to ask of any distributed design

1. **What is the unit of partitioning, and is load even?** (shard key, hot keys)
2. **What is replicated, how, and what happens on failover?** (sync/async, lag, data loss)
3. **What consistency does each operation need?** (strong for money; eventual for feeds)
4. **What happens on retry or duplicate delivery?** (idempotency)
5. **What happens when the network splits or a node is slow?** (timeouts, quorum, fencing)

## Core ideas in one page

### Partial failure and detection
A node cannot distinguish "dead" from "slow". Failure detectors use timeouts/heartbeats
(phi-accrual gives a suspicion level rather than a binary answer). Design for false positives:
operations must be safe if a "dead" node comes back.

### Time and ordering
Wall clocks drift and can jump. Use **logical clocks** (Lamport) for causal order, **vector clocks**
to detect concurrency, per-partition **sequence numbers** or log offsets for total order within a
partition, and bounded-uncertainty clocks (TrueTime) only when you have them.

### Consensus
Raft/Paxos let a majority agree on a sequence of values, tolerating f failures with 2f+1 nodes. Use
for metadata, leader election and configuration, not for the bulk data path across continents.

### Consistency spectrum
Linearizable → sequential → causal → session guarantees (read-your-writes, monotonic reads) → eventual.
Stronger costs latency and availability. Choose per operation.

### Exactly-once is an effect, not a delivery guarantee
At-least-once delivery + idempotent processing (dedupe key, conditional write, transactional outbox)
gives the *effect* of exactly-once.

### Distributed transactions
2PC blocks and reduces availability; sagas give eventual atomicity with compensations; the outbox
pattern makes "update DB and publish event" reliable. See
[Coordinating Transactions](../../05-Interview-Patterns/12-coordinating-transactions-across-services.md).

## Failure-mode cheat sheet

| Failure | Symptom | Standard defence |
|---|---|---|
| Node crash | Requests error | Replicas, health checks, failover |
| Slow node | Tail latency, thread exhaustion | Timeouts, hedging, bulkheads, load shedding |
| Network partition | Split brain, divergent data | Quorums, fencing tokens, leases |
| Duplicate delivery | Double effects | Idempotency keys, dedupe |
| Reordering | Stale overwrites | Version numbers, per-key partitioning |
| Clock skew | Wrong "latest" | Logical clocks, avoid LWW for critical data |
| Overload | Cascading failure | Rate limits, backpressure, autoscaling |
| Bad deploy | Correlated failure | Canary, rollback, feature flags |

## Interview questions (with answers)

**Q1. What is the difference between availability and durability?**
Availability: can you serve requests now. Durability: is committed data safe over time. A system can be down but not lose data, or up but lose recent writes (async replication).

**Q2. Why 2f+1 nodes for consensus?**
Progress needs a majority; with 2f+1 nodes, f can fail and f+1 remain to form a majority. Any two majorities overlap, preserving agreement.

**Q3. Explain split brain and how to prevent it.**
Two nodes both believe they are leader after a partition. Prevent with quorum-based election (only the majority side elects), leases with expiry, and fencing tokens so a stale leader's writes are rejected.

**Q4. Why is "last write wins" dangerous?**
Clock skew or concurrent updates cause silent data loss. Prefer version vectors, CRDTs, or app-level merge for important data.

## Last-minute revision

Failures are partial; clocks lie; retries duplicate. Use **partitioning for scale, replication for
availability, quorums/consensus for agreement, idempotency for retries, and fencing for safety**.
