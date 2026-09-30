# Database Fundamentals

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [API Design](03-api-design.md) · 🏠 [Concept Deep Dives](README.md) · ➡️ Next: [Distributed Systems](05-Distributed-Systems/README.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

## SQL vs NoSQL

| | Relational (Postgres, MySQL) | NoSQL families |
|---|---|---|
| Model | Tables, joins, schema | Key-value, document, wide-column, graph |
| Transactions | Strong ACID, multi-row | Often limited to single key/partition (some now support more) |
| Scaling | Vertical + replicas; sharding is manual | Built for horizontal partitioning |
| Query flexibility | Ad hoc queries, joins | Query by key/known access paths |
| Best for | Money, inventory, relational data | Massive scale, simple access patterns, flexible schema |

Rule of thumb: default to a relational database. Move to NoSQL when a **specific** need (scale, latency, schema flexibility, access pattern) justifies it, and say which.

| NoSQL family | Example | Fit |
|---|---|---|
| Key-value | Redis, DynamoDB | Sessions, caches, carts, counters |
| Document | MongoDB | Nested aggregates like profiles, catalogues |
| Wide-column | Cassandra, HBase, Bigtable | Time series, messaging, high write volume |
| Graph | Neo4j | Relationship traversal, recommendations |
| Search | Elasticsearch, OpenSearch | Full-text and faceted search |
| Time series | InfluxDB, TimescaleDB | Metrics |

## ACID

- **Atomicity**: all or nothing.
- **Consistency**: constraints hold before and after.
- **Isolation**: concurrent transactions do not see each other's partial work.
- **Durability**: committed data survives crashes (write-ahead log).

## Isolation levels and anomalies

| Level | Prevents | Still allows |
|---|---|---|
| Read uncommitted | nothing | dirty reads |
| Read committed | dirty reads | non-repeatable reads |
| Repeatable read | non-repeatable reads | phantoms (in standard definition); write skew in snapshot isolation |
| Serializable | all of the above | lowest concurrency |

Practical tools: `SELECT ... FOR UPDATE` (pessimistic lock), **optimistic concurrency** with a version column (`UPDATE ... WHERE id=? AND version=?`), unique constraints, and atomic conditional updates (`UPDATE stock SET qty = qty - 1 WHERE id=? AND qty > 0`).

## Indexes

An index is an auxiliary structure that speeds up lookups at the cost of extra storage and slower writes.

- **B-tree / B+tree**: balanced, sorted; supports equality, range and ordering. Default in most RDBMS. Good for read-heavy workloads.
- **LSM tree** (Cassandra, RocksDB, LevelDB): writes go to memtable and WAL, flushed to immutable sorted files (SSTables), merged by compaction. Very high write throughput; reads may check multiple files (Bloom filters help).
- **Hash index**: O(1) equality only.
- **Inverted index**: term to document list, for text search.
- **Geospatial**: geohash, quadtree, R-tree, S2/H3 cells.

Index design tips:

- **Composite index** column order matters: equality columns first, then range, following the leftmost prefix rule.
- **Covering index** includes all queried columns, avoiding table lookups.
- Every index slows writes and uses space; do not index everything.
- Low-cardinality columns (boolean) are poor index candidates alone.

## Normalisation vs denormalisation

Normalise to avoid duplication and anomalies. Denormalise for read performance (precomputed counts, embedded author names in posts), accepting write complexity and the need to keep copies in sync (events, CDC, or periodic jobs).

## OLTP vs OLAP

OLTP: many small transactions, row stores. OLAP: large scans and aggregates, columnar stores (Redshift, BigQuery, ClickHouse, Snowflake). Feed analytics from OLTP via CDC or event streams, not by running heavy queries on the primary.

## Write-ahead log and durability

Changes are appended to a log before being applied, so after a crash the DB replays the log. The same log powers replication and change data capture.

## Interview questions

1. Why might a query still be slow with an index on each column separately?
2. Explain how you would prevent overselling the last ticket under concurrency, with two different mechanisms.
3. B-tree vs LSM-tree: which for a write-heavy metrics store, and why?
4. When is denormalisation the right call, and how do you keep it correct?

---

## 🔗 Used in these case studies

- [Ticket Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md)
- [Flash Sale / Inventory](../13-E-commerce-and-Marketplace/Flash-Sale/README.md)
- [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md)
