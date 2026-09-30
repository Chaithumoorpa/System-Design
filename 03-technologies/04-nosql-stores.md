# NoSQL Stores: Cassandra, DynamoDB, MongoDB

## Cassandra (wide-column, leaderless)

- Peer-to-peer ring, consistent hashing with vnodes, tunable consistency (`ONE`, `QUORUM`, `ALL`, `LOCAL_QUORUM`).
- **Write path**: commit log + memtable, flushed to SSTables, compaction merges. Extremely fast writes.
- **Data model is query-first**: design one table per access pattern; denormalise freely. No joins.
- **Primary key = partition key + clustering columns**. Partition key decides placement; clustering columns sort within a partition. Keep partitions bounded (e.g. bucket by day) to avoid huge partitions.
- Anti-entropy: read repair, hinted handoff, Merkle-tree repair. Tombstones for deletes (excess tombstones hurt reads).
- Strengths: write-heavy, multi-region, always-on. Weaknesses: no ad hoc queries, weak transactions (lightweight transactions via Paxos are slow), operational tuning.
- Good for: messaging history, time series, activity feeds, IoT.

## DynamoDB (managed key-value/document)

- Partition key (+ optional sort key). Single-digit ms latency at any scale, serverless capacity modes.
- Items up to 400 KB. **GSI** (global secondary index, eventually consistent) and **LSI** for alternate access patterns.
- Consistency: eventually consistent reads by default; strongly consistent reads optional (per-partition); transactions supported across items.
- Hot partitions throttle; design high-cardinality keys. Adaptive capacity helps but is not magic.
- Streams for CDC; TTL for expiry; global tables for multi-region active-active with last-writer-wins.
- Single-table design: model multiple entity types with overloaded keys to serve access patterns in one query.

## MongoDB (document)

- JSON-like documents; embed related data for one-read access, reference for large or shared data.
- Replica sets (primary + secondaries, automatic election) and sharded clusters (mongos + config servers), hashed or ranged shard keys.
- Rich queries and secondary indexes, aggregation pipeline; multi-document transactions available with a cost.
- Good for: catalogues, content, profiles, evolving schemas.

## Choosing

| Need | Lean towards |
|---|---|
| Joins, transactions, ad hoc queries | Relational |
| Massive writes, known access patterns, multi-region | Cassandra / DynamoDB |
| Managed, zero-ops KV at scale on AWS | DynamoDB |
| Flexible nested documents with rich queries | MongoDB |
| Sub-ms latency, ephemeral or derived data | Redis |

## Design questions to ask yourself

1. What are the exact queries, ranked by frequency?
2. What is the partition key, and is it evenly accessed?
3. How large can one partition or item become?
4. What consistency does each read need?
5. How will secondary access patterns be served (GSI, denormalised table, search index)?

## Interview questions

1. Model "messages in a conversation, newest first" in Cassandra. What is the partition key and why do you bucket?
2. Why can DynamoDB throttle even when total capacity is available?
3. Compare quorum settings for reads and writes and their consequences.
