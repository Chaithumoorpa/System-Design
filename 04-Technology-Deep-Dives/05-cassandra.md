# Cassandra

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Advanced

⬅️ Previous: [DynamoDB](04-dynamodb.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [Elasticsearch](06-elasticsearch.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Distributed, masterless **wide-column** database built for very high write throughput, linear
scalability and multi-datacenter availability. Combines Dynamo's distribution model (ring, gossip,
tunable consistency) with Bigtable's storage model (LSM tree, column families).

## Architecture

- **Peer-to-peer ring**: no leader; any node can coordinate a request.
- **Partitioner** hashes the partition key to a token; nodes own token ranges (with **virtual nodes**).
- **Replication factor (RF)**: each partition is stored on RF nodes (e.g. RF=3), chosen along the ring, rack- and DC-aware.
- **Gossip** spreads membership and health; a phi-accrual detector marks nodes down.
- **Snitch/topology** keeps replicas in different racks/AZs.

## Data model (query-first)

```sql
CREATE TABLE messages_by_conversation (
  conv_id uuid, bucket int, sent_at timeuuid, sender uuid, body text,
  PRIMARY KEY ((conv_id, bucket), sent_at)
) WITH CLUSTERING ORDER BY (sent_at DESC);
```

- **Primary key = partition key + clustering columns.** The partition key decides *where* data lives; clustering columns decide *sort order within* the partition.
- **One table per query pattern**; denormalise freely. No joins; no ad hoc filtering without indexes or `ALLOW FILTERING` (avoid).
- Keep partitions bounded (<~100 MB, <~100k cells): add a **bucket** (day/month) to the key for unbounded growth.

## Write path (why writes are fast)

1. Append to the **commit log** (sequential, durable).
2. Update the in-memory **memtable**.
3. When full, flush to an immutable **SSTable**.
4. **Compaction** merges SSTables (size-tiered, leveled, time-window) and purges tombstones.

No read-before-write and no random I/O on the write path.

## Read path

Coordinator asks replicas (per consistency level); each replica checks memtable then SSTables, using
**Bloom filters**, partition index and caches to minimise disk reads; results merged by timestamp;
**read repair** fixes stale replicas.

## Tunable consistency

| Level | Meaning |
|---|---|
| `ONE` / `LOCAL_ONE` | Fastest; may be stale |
| `QUORUM` / `LOCAL_QUORUM` | Majority of replicas (of the DC); `R+W>RF` with QUORUM/QUORUM |
| `ALL` | Every replica; lowest availability |
| `SERIAL` / LWT | Paxos-based compare-and-set (`IF NOT EXISTS`), slow; use sparingly |

## Failure handling and repair

- **Hinted handoff**: coordinator stores writes for a down replica and replays them.
- **Read repair** and scheduled **anti-entropy repair** (Merkle trees) converge replicas.
- **Tombstones** mark deletes and persist for `gc_grace_seconds`; repair within that window or deleted data can resurrect. Excess tombstones slow reads.

## Operational notes

- Add nodes by bootstrapping (streaming token ranges); no downtime.
- Compaction and repair need spare disk (keep ~50% headroom for size-tiered) and I/O budget.
- TTL on columns/rows for expiring data (time series, sessions).
- Avoid: large partitions, unbounded collections, secondary indexes on high-cardinality columns, frequent deletes/updates on the same cells, `SELECT *` scans.

## When to choose it

Heavy write workloads (messaging, IoT, activity/event logs, time series), multi-region active-active,
known query patterns, need for linear scaling and always-on availability. Avoid for ad hoc queries,
strong multi-row transactions, or small datasets where PostgreSQL is simpler.

## Cassandra vs neighbours

| | Cassandra | DynamoDB | PostgreSQL |
|---|---|---|---|
| Ops | Self-run (or managed) | Fully managed | Self-run/managed |
| Consistency | Tunable | Eventual/strong per read | Strong |
| Transactions | LWT only | Item transactions | Full ACID |
| Multi-region | Native | Global tables (LWW) | Complex |
| Query flexibility | Low | Low | High |

## Interview questions (with answers)

**Q1. Model messages per conversation.** Partition `(conv_id, bucket)`, cluster by `sent_at DESC`; bucket by time to bound partition size; read latest N from the newest bucket, then older buckets on scroll.

**Q2. Why are Cassandra writes fast?** Append-only commit log + memtable; sequential I/O; no read-modify-write; compaction deferred to the background.

**Q3. What can go wrong with deletes?** Tombstones accumulate and slow reads; if a replica misses the tombstone and it is purged after `gc_grace_seconds`, the deleted data returns. Run repair regularly.

**Q4. QUORUM reads and writes at RF=3: guarantee?** Read and write sets overlap (2+2>3), so a read sees the latest acknowledged write, barring concurrent writes and clock issues; not linearizable.

**Q5. How do you avoid hot partitions?** Add buckets or salt to the partition key; pick keys with even access; cache hot items.

## Last-minute revision

Ring + vnodes, RF=3, tunable consistency; LSM (commit log → memtable → SSTable → compaction); **model
tables per query**, bound partition size; tombstones + repair; great for writes, weak for ad hoc queries.

## References

- Lakshman & Malik, *Cassandra: A Decentralized Structured Storage System*; Apache Cassandra documentation.
