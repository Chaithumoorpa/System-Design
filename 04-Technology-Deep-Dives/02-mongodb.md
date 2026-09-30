# MongoDB

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [PostgreSQL](01-postgresql.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [Redis](03-redis.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Document database storing JSON-like (BSON) documents. Flexible schema, rich queries, secondary
indexes, replica sets, and horizontal scaling through sharding.

## Data model

- **Database → collection → document.** A document is a nested structure, up to 16 MB.
- **Embed** data read together and owned by the parent (order with line items). **Reference** data that is large, shared, or changes independently (user referenced by many posts).
- Model for **read patterns first**: one read should return what a screen needs.

```json
{ "_id": "order_981", "user_id": 42, "status": "PAID",
  "items": [ {"sku":"A1","qty":2,"price":499}, {"sku":"B7","qty":1,"price":1299} ],
  "shipping": { "city": "Pune", "pin": "411001" }, "created_at": "2026-09-30T10:00:00Z" }
```

## Indexing and querying

- B-tree indexes: single field, compound (order matters: equality → sort → range, "ESR"), multikey (arrays), text, geospatial (2dsphere), TTL, partial and sparse.
- Aggregation pipeline (`$match`, `$group`, `$lookup`, `$sort`) for analytics; `$lookup` is a limited join and costly at scale.
- Use `explain()` to confirm an index is used; avoid unbounded arrays inside documents.

## Replication

- **Replica set**: one primary, several secondaries, automatic election via a Raft-like protocol; typical 3 or 5 members.
- **Write concern** (`w:1`, `w:majority`, journal) controls durability; **read concern** (`local`, `majority`, `linearizable`) and **read preference** (primary, secondary) control staleness.
- Async replication means `w:1` writes can be rolled back on failover; use `w:majority` for important data.

## Sharding

- **mongos** routers, **config servers**, shards (each a replica set).
- Shard key choice is critical and hard to change: high cardinality, even distribution, matches queries.
  - **Hashed** key: even writes, no range queries.
  - **Ranged** key: efficient ranges but hot spots on monotonic keys (timestamps, ObjectIds).
- Balancer moves chunks; targeted queries include the shard key, otherwise scatter-gather.

## Transactions

Multi-document ACID transactions exist (replica sets and sharded clusters) but cost performance;
prefer single-document atomicity by embedding related data.

## Strengths and limits

| Strengths | Limits |
|---|---|
| Flexible schema, rapid iteration | Joins are weak; data duplication needed |
| Rich queries and secondary indexes | Shard key mistakes are costly |
| Good developer ergonomics | Large documents/unbounded arrays hurt |
| Horizontal scale via sharding | Cross-shard transactions and scatter-gather are slow |

## When to choose it

Catalogues, content management, user profiles, event/IoT data with evolving structure, prototypes
that need schema agility. Avoid when you need heavy relational integrity, complex joins, or
predictable single-digit-ms key-value at extreme scale (consider [DynamoDB](04-dynamodb.md)).

## Interview questions (with answers)

**Q1. Embed or reference?** Embed for one-to-few, read together, bounded size; reference for one-to-many with growth, shared entities, or independent updates.

**Q2. Why is a timestamp a bad ranged shard key?** New writes all hit the newest chunk (hot shard). Use a hashed key or a compound key with a well-distributed prefix.

**Q3. What happens on primary failure?** Secondaries elect a new primary (majority vote); writes acknowledged only at `w:1` and not yet replicated may be rolled back; drivers retry with retryable writes.

**Q4. How to model a social profile with posts?** Profile document with recent posts embedded (bounded), full posts in their own collection referenced by user id and indexed on `(user_id, created_at)`.

## Last-minute revision

Documents model aggregates; index for queries (ESR); replica sets for HA (`w:majority` for safety); shard key is the make-or-break decision.

## References

- MongoDB official documentation (data modelling, replication, sharding).
