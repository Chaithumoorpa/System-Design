# Design a Distributed Key-Value Store (Dynamo-style)

**Prompt:** A highly available, horizontally scalable, durable key-value database.

## Requirements

- Functional: `put(key, value)`, `get(key)`, `delete(key)`; values up to ~1 MB.
- Non-functional: always writable (AP), low latency, linear scalability, tunable consistency, automatic recovery, multi-datacenter.

## Architecture (Dynamo/Cassandra lineage)

```
Client -> any node (coordinator) -> replicas chosen from consistent hash ring (N=3)
Each node: commit log + memtable + SSTables (LSM), Bloom filters, gossip, hinted handoff queue
```

## Techniques

| Concern | Technique |
|---|---|
| Partitioning | Consistent hashing with virtual nodes |
| Replication | Each key stored on N successive distinct nodes (rack/AZ aware) |
| Consistency | Quorum: choose R, W with R + W > N for strong-ish reads; R=1/W=1 for speed |
| Conflict detection | Vector clocks or version vectors; or last-write-wins timestamps |
| Failure detection | Gossip protocol with phi-accrual detector |
| Temporary failure | **Hinted handoff**: another node stores writes for the down node, replays on return; **sloppy quorum** improves availability |
| Permanent failure repair | **Anti-entropy** using Merkle trees to find and sync differing ranges; **read repair** on reads |
| Membership | Gossip spreads ring state; new node bootstraps by streaming its ranges |

## Write path

1. Client contacts coordinator (or token-aware driver picks a replica).
2. Coordinator forwards to the N replicas; waits for W acks.
3. Each replica appends to the **commit log** (durability), updates **memtable**; when full, flush to immutable **SSTable**.
4. Background **compaction** merges SSTables and drops overwritten values/tombstones.

## Read path

1. Coordinator queries R replicas (or one full read + digests from others).
2. Replica checks memtable, then SSTables newest-first, using **Bloom filters** to skip files and indexes to seek.
3. Coordinator reconciles versions; returns latest; triggers read repair on mismatch.

## Deep dives

- **Conflict resolution**: LWW is simple but can drop concurrent writes (clock skew); vector clocks surface siblings for the app to merge (shopping cart union); CRDTs for counters and sets.
- **Deletes**: tombstones retained until all replicas see them (grace period), else deleted data can resurrect.
- **Multi-DC**: `LOCAL_QUORUM` to avoid cross-DC latency, async replication across DCs.
- **Hot partitions and large values**: enforce size limits, chunk large blobs into object storage, store pointers.
- **Capacity/repair**: throttle streaming and compaction so they do not hurt foreground latency.
- **Alternative (CP)**: leader per partition with Raft (etcd, TiKV, Spanner-like): linearizable, at the cost of availability under partition and leader hot spots. Compare and choose by requirements.

## Follow-ups

- What happens with R=1, W=1, N=3 and a partition? Give an example anomaly.
- How would you add range scans? (Ordered partitioning within a partition key, secondary indexes.)
- How do you add a node with no downtime?
