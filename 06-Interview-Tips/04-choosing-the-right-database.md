# Choosing the Right Database

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Diagramming Tips](03-diagramming-tips.md) · 🏠 [Interview Tips](README.md) · ➡️ Next: [Design URL Shortener](../07-Basic-Questions/URL-Shortener/README.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

"Which database?" appears in every design. The best answers start from **access patterns and
constraints**, not from product names.

## Decision procedure

1. **List the top access patterns** with frequency and latency needs ("get post by id", "latest 20 messages of a conversation", "search by text").
2. **Classify data shape**: relational, aggregate/document, key-value, wide-column time series, graph, blob, text.
3. **State consistency and transaction needs**: must two rows change atomically? Can reads be stale?
4. **Estimate scale**: data size, read/write QPS, growth, hot keys.
5. **Pick the simplest store that satisfies all of the above**; add specialised stores as *derived* views.

## Quick decision table

| If you need… | Choose | Why |
|---|---|---|
| Transactions, joins, constraints, ad hoc queries | PostgreSQL / MySQL | ACID, mature, flexible |
| Flexible nested documents, rich queries | MongoDB | Aggregates, secondary indexes |
| Predictable low latency KV at any scale, low ops | DynamoDB | Managed partitioning |
| Extreme write volume, multi-region, time-series/messages | Cassandra | LSM, masterless, tunable consistency |
| Sub-ms reads, counters, leaderboards, ephemeral state | Redis | In-memory structures |
| Full-text, relevance, facets, geo + filters | Elasticsearch / OpenSearch | Inverted index |
| Blobs (images, video, backups) | S3 / GCS | Cheap, durable |
| Analytics over huge data | BigQuery / Snowflake / ClickHouse | Columnar, scans |
| Metrics/time series | Prometheus/TSDB/InfluxDB/TimescaleDB | Time-partitioned, compressed |
| Relationship traversals (friends of friends) | Graph DB (Neo4j) or SQL with limits | Traversal cost |
| Coordination, config, locks | etcd / ZooKeeper | Consensus, small data |
| Event log with replay | Kafka | Durable ordered log |

## SQL vs NoSQL: how to argue it

**Prefer SQL when:** data is relational; you need multi-row transactions (payments, inventory); queries are varied; scale fits one primary + replicas (tens of TB, thousands of QPS goes far with indexes, caching, partitioning).

**Prefer NoSQL when:** a specific pressure justifies it:
- write throughput or dataset size exceeds what a sharded SQL setup can reasonably handle;
- access is by known key with predictable patterns;
- schema evolves rapidly or data is naturally document-shaped;
- multi-region active-active availability is required.

Say which pressure applies. "NoSQL scales better" alone is a weak answer.

## Polyglot persistence (the usual real answer)

```
PostgreSQL (source of truth)
   ├─ CDC → Elasticsearch (search)
   ├─ cache → Redis (hot reads, counters)
   ├─ events → Kafka → analytics warehouse
   └─ blobs → S3 (+ CDN)
```

One store is the **system of record**; others are **derived**, rebuildable, and eventually consistent.

## Worked choices

| System | Data | Choice and reason |
|---|---|---|
| URL shortener | code → URL | KV store (DynamoDB/Cassandra) or sharded SQL; single-key access, huge read fan-out; Redis cache |
| Chat messages | conv_id, time-ordered | Cassandra/DynamoDB/HBase: write-heavy, partition by conversation, sort by time |
| Payments & ledger | Money movement | PostgreSQL/MySQL: ACID, constraints, audit |
| Product catalogue | Nested attributes | MongoDB or PostgreSQL JSONB, plus Elasticsearch for search |
| Leaderboard | Rank by score | Redis sorted set |
| Ride locations | Ephemeral positions | In-memory geo index (Redis/custom); history to Kafka/S3 |
| Social graph | Follow relationships | Adjacency lists in KV/wide-column; SQL until huge |
| Metrics | Time series | TSDB; downsample and tier |

## Pitfalls

- Choosing a store for a feature rather than the access pattern.
- Using a cache as the only copy of important data.
- Using the search engine as the system of record.
- Forgetting secondary access patterns (query by owner, by time).
- Ignoring hot keys and partition size limits.
- Picking a distributed database when a single well-indexed Postgres would do.

## Interview questions (with answers)

**Q1. SQL or NoSQL for a chat app?** Messages: wide-column/KV (Cassandra/DynamoDB) partitioned by conversation for write volume and ordered reads. Users, groups and memberships: relational or KV. Media: object storage.

**Q2. Design storage for "orders" needing strong consistency and reporting.** PostgreSQL for orders (ACID); CDC to a warehouse (BigQuery/ClickHouse) for reporting so analytics don't load the primary.

**Q3. Why not put everything in Postgres?** You can, until a specific limit (write throughput, size, latency, search relevance) appears; then add a targeted store as a derived view rather than migrating everything.

**Q4. How do you choose a partition key?** High cardinality, even access, aligns with the dominant query so most requests hit one partition.

## Last-minute revision

Access patterns → data shape → consistency → scale → simplest fit. Default to PostgreSQL; add Redis,
Elasticsearch, S3, Kafka as **derived** stores with clear reasons; know one clear "why not" for each.
