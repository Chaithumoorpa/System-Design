# 🏗️ Distributed Infrastructure — High Level Design

Building blocks that **other systems depend on**: caches, stores, schedulers and telemetry.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 17 | [Distributed Cache](DistributedCache/README.md) | Hash slots / consistent hashing, approximate LRU/LFU, lazy + active expiry, replicas, hot-key handling | [Caching](../../02-core-concepts/03-caching.md), [Consistent hashing](../../02-core-concepts/08-consistent-hashing.md) |
| 18 | [Key-Value Store](KeyValueStore/README.md) | Ring + vnodes, quorums, hinted handoff, Merkle repair, LSM engine, tombstones | [Consistency & CAP](../../02-core-concepts/07-consistency-and-cap.md), [NoSQL stores](../../03-technologies/04-nosql-stores.md) |
| 19 | [Job Scheduler](JobScheduler/README.md) | Due-job index/timing wheel, atomic claims, unique tick constraint, leases + heartbeats, retries | [Messaging](../../02-core-concepts/09-messaging-and-streaming.md), [Coordination](../../03-technologies/06-coordination-and-misc.md) |
| 20 | [Metrics and Logging Pipeline](MetricsLoggingPipeline/README.md) | Agents → Kafka → TSDB/log index, Gorilla compression, cardinality control, tiered retention, alerting | [Kafka](../../03-technologies/02-kafka.md), [Elasticsearch](../../03-technologies/05-elasticsearch.md) |

⬅️ Previous category: [Commerce and Payments](../Commerce-and-Payments/README.md) · 🏠 [All HLD problems](../README.md)
