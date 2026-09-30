# Must-Know Technologies

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: [Concepts](01-concepts.md) · 🏠 [Must-Know Topics](README.md) · ➡️ Next: [Tradeoffs](03-tradeoffs.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

You do not need to know every product. You need one or two representatives of each **category**,
understood well enough to explain why you'd choose them and how they fail.

## The category map

| Category | Representatives | Reach for it when | Deep dive |
|---|---|---|---|
| Relational database | PostgreSQL, MySQL | Transactions, joins, relational data; default choice | [PostgreSQL](../04-Technology-Deep-Dives/01-postgresql.md) |
| Document store | MongoDB | Nested aggregates, flexible schema, rich queries | [MongoDB](../04-Technology-Deep-Dives/02-mongodb.md) |
| Key-value / serverless NoSQL | DynamoDB | Known access patterns, massive scale, low ops | [DynamoDB](../04-Technology-Deep-Dives/04-dynamodb.md) |
| Wide-column | Cassandra | Huge write volume, multi-region, time-series/messaging | [Cassandra](../04-Technology-Deep-Dives/05-cassandra.md) |
| In-memory store | Redis, Memcached | Caching, counters, leaderboards, locks, rate limits | [Redis](../04-Technology-Deep-Dives/03-redis.md) |
| Search engine | Elasticsearch, OpenSearch | Full-text, faceted and geo search, log analytics | [Elasticsearch](../04-Technology-Deep-Dives/06-elasticsearch.md) |
| Distributed log | Kafka | Event streams, CDC, replayable pipelines | [Kafka](../04-Technology-Deep-Dives/07-kafka.md) |
| Message broker | RabbitMQ | Task queues, routing, per-message ack | [RabbitMQ](../04-Technology-Deep-Dives/08-rabbitmq.md) |
| Managed queue | SQS (+SNS) | Simple durable queue with no servers | [SQS](../04-Technology-Deep-Dives/09-sqs.md) |
| Stream processor | Flink, Spark Streaming | Windowed aggregation, stateful streaming | [Flink](../04-Technology-Deep-Dives/10-flink.md) |
| Object storage | S3, GCS | Media, backups, data lakes | [S3](../04-Technology-Deep-Dives/11-s3.md) |
| Coordination | ZooKeeper, etcd | Leader election, config, locks, membership | [ZooKeeper](../04-Technology-Deep-Dives/12-zookeeper.md) |
| CDN | CloudFront, Cloudflare, Akamai | Static and cacheable content at the edge | [CDN and storage](../_Reference/cdn-and-storage.md) |
| Load balancer / gateway | Nginx, Envoy, ALB | Traffic distribution, TLS, routing | [Load balancing](../_Reference/load-balancing.md) |
| OLAP / warehouse | BigQuery, Snowflake, ClickHouse, Redshift | Analytics over large data | [Time Series DB](../15-Distributed-Infrastructure/Time-Series-Database/README.md) |

## One-line decision rules

- Not sure? **PostgreSQL** until a specific need proves otherwise.
- Need sub-millisecond reads on hot data? **Redis** in front of the database.
- Need to store files? **Object storage**, with a pointer in the database.
- Need search relevance, typo tolerance or facets? **Elasticsearch**, fed from the primary store.
- Need to decouple services and absorb bursts? A **queue** (SQS/RabbitMQ) or a **log** (Kafka).
- Need to replay history or fan out to many consumers? **Kafka**.
- Need one leader among many nodes? **etcd/ZooKeeper** lease, not homemade locks.
- Need a scalable KV with predictable latency and little ops? **DynamoDB**.
- Need to ingest millions of writes per second, multi-region? **Cassandra**.

## What to be able to say about any technology

1. **Data model** and access patterns it is built for.
2. **How it scales** (partitioning, replication) and its failure behaviour.
3. **Consistency and durability** guarantees (and their defaults).
4. **Limits** (item size, hot partitions, write amplification, memory).
5. **When not to use it.**

## Common pairings

| Pairing | Why |
|---|---|
| PostgreSQL + Redis | Truth in the DB, speed from the cache |
| PostgreSQL + Elasticsearch (via CDC) | Transactions plus search |
| Kafka + Flink | Durable stream plus stateful processing |
| S3 + CDN + metadata DB | Media at scale |
| DynamoDB + SQS/SNS | Serverless pipelines |
| Cassandra + Kafka | High-volume ingest with replay |

## Interview questions (with answers)

**Q1. Why not use Kafka as the database?**
Kafka is a log optimised for sequential append and consumption, not random key lookups, ad hoc queries or transactions. It can be a source of truth for events, but you materialise queryable views elsewhere.

**Q2. When would you choose Cassandra over PostgreSQL?**
When write throughput, multi-region availability and linear horizontal scale outweigh joins and transactions, and access patterns are known (messages by conversation, time series).

**Q3. When is Redis not enough as a primary store?**
When data must survive failures with no loss (async replication can lose recent writes), exceeds memory economically, or needs complex queries.

## Last-minute revision

Memorise the **category → representative → when to use** table; for each, know scaling, consistency and a "when not".
