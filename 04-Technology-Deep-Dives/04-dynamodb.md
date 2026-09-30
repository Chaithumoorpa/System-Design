# DynamoDB

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Redis](03-redis.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [Cassandra](05-cassandra.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Fully managed key-value and document database on AWS, designed for **single-digit-millisecond
latency at any scale** with essentially no servers to manage. Inspired by the Dynamo paper, but a
different product (managed, with a leader per partition).

## Data model

- **Table** of **items** (up to 400 KB), each with a **primary key**:
  - **Partition key (PK)** only, or
  - **PK + sort key (SK)**: items with the same PK are stored together sorted by SK, enabling range queries within a partition.
- Attributes are schemaless beyond the key. Types: string, number, binary, sets, lists, maps.
- Requests: `GetItem`, `PutItem`, `UpdateItem`, `DeleteItem`, `Query` (PK + SK condition), `Scan` (avoid), `BatchGet/Write`, `TransactGet/Write`.

## Partitioning and capacity

- Items are spread across partitions by a hash of the PK; each partition serves a bounded throughput (~3,000 RCU / 1,000 WCU) and ~10 GB.
- **Capacity modes**: provisioned (with auto scaling) or on-demand (pay per request).
- **Hot partition** problem: a skewed PK throttles even if the table has spare capacity. Fix with high-cardinality keys, write sharding (`PK#0..N`), caching (DAX/Redis).

## Secondary indexes

| | GSI (global) | LSI (local) |
|---|---|---|
| Key | Different PK and SK | Same PK, different SK |
| Consistency | Eventually consistent | Strong or eventual |
| Creation | Anytime | Only at table creation |
| Capacity | Own throughput | Shares table's |

Access patterns not served by the base key are served by a GSI. Each GSI is asynchronous and doubles
storage of projected attributes.

## Single-table design

Store several entity types in one table using overloaded keys so one `Query` returns related items:

| PK | SK | Data |
|---|---|---|
| `USER#42` | `PROFILE` | name, email |
| `USER#42` | `ORDER#2026-09-30#981` | total, status |
| `USER#42` | `ORDER#2026-09-30#982` | total, status |

Query `PK = USER#42 AND SK begins_with ORDER#` returns a user's orders in time order. Trade-off: less
flexible for new access patterns; requires up-front modelling.

## Consistency and transactions

- Reads are **eventually consistent** by default; `ConsistentRead=true` for strongly consistent reads from the leader replica (2× RCU cost; not available on GSIs).
- **Conditional writes** (`attribute_not_exists`, version checks) give optimistic concurrency and idempotency.
- **Transactions** (`TransactWriteItems`, up to 100 items) provide ACID across items/tables at 2× cost.

## Other features

- **TTL**: automatic item expiry (deletion is delayed, so filter expired items in queries).
- **Streams**: ordered change log per item (24 h) to trigger Lambda, feed search indexes, replicate, or build materialised views.
- **Global tables**: multi-region active-active with last-writer-wins conflict resolution.
- **DAX**: in-memory cache in front for microsecond reads.
- Backups: on-demand and point-in-time recovery.

## Limits and gotchas

- Query flexibility is limited; no joins; `Scan` is expensive.
- Item size 400 KB; large blobs belong in [S3](11-s3.md) with a pointer.
- 1 MB result page limit per `Query`; paginate with `LastEvaluatedKey`.
- Cost model surprises: GSIs, strongly consistent reads, transactions, and large items multiply cost.

## When to choose it

Known access patterns; spiky or huge scale; little ops; serverless stacks; sessions, carts, user
profiles, metadata, idempotency tables, leaderboards keyed by user. Avoid for ad hoc analytics or
heavy relational queries.

## Interview questions (with answers)

**Q1. Why can DynamoDB throttle when the table has unused capacity?** Capacity is per partition; a hot key exhausts one partition's limit. Distribute keys or shard hot keys.

**Q2. How do you model "latest 20 messages in a conversation"?** PK = `conv_id` (or `conv_id#bucket`), SK = timestamp/sequence; `Query` with `ScanIndexForward=false, Limit=20`.

**Q3. How do you implement an idempotency store?** `PutItem` with `attribute_not_exists(idempotency_key)`; on conflict return the stored result; TTL for cleanup.

**Q4. GSI vs LSI?** GSI: any alternate key, eventually consistent, created anytime; LSI: same PK, alternate SK, allows strong reads, created at table creation only.

**Q5. How do you guarantee atomic updates across two items?** `TransactWriteItems` (all-or-nothing) or restructure so they share one item.

## Last-minute revision

PK spreads load, SK orders within it; design tables **from access patterns**; GSIs for extra patterns;
conditional writes for concurrency/idempotency; watch hot partitions and cost multipliers.

## References

- AWS DynamoDB Developer Guide; DeCandia et al., *Dynamo* (SOSP 2007) for the original ideas.
