# "Design X" Prompt Bank

Use these for timed practice (35-45 minutes). Each lists difficulty (E/M/H), the core challenge to spot, and key things a strong answer covers. Items marked with a link have a full worked example.

## Basics

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 1 | [URL shortener](../05-case-studies/Basics/URLShortener/README.md) | E | Unique code generation, read-heavy | KGS/ranges, cache, 301 vs 302, analytics async |
| 2 | [Rate limiter](../05-case-studies/Basics/RateLimiter/README.md) | M | Distributed counters | Token bucket, Redis Lua, fail-open |
| 3 | [Unique ID generator](../05-case-studies/Basics/UniqueIdGenerator/README.md) | M | Coordination-free uniqueness | Snowflake bits, clock skew |
| 4 | Pastebin | E | Blob + metadata, expiry | Object store, TTL, abuse controls |
| 5 | Key-value store with TTL (single node) | M | Data structures | Hash map + heap/wheel for TTL, persistence |
| 6 | API gateway | M | Edge concerns | Auth, routing, rate limits, plugins |

## Real-time and social

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 7 | [Chat system](../05-case-studies/Real-Time-Communication/ChatSystem/README.md) | H | Delivery, ordering, connections | WebSocket gateways, registry, sequence numbers |
| 8 | [Notification service](../05-case-studies/Real-Time-Communication/NotificationService/README.md) | M | Multi-channel, priority | Queues per priority, prefs, retries |
| 9 | [News feed](../05-case-studies/Social-and-Content/NewsFeed/README.md) | H | Fan-out | Hybrid push/pull, ranking |
| 10 | [Trending / Top-K](../05-case-studies/Social-and-Content/TopKTrending/README.md) | H | Streaming aggregation | Count-Min sketch, windows |
| 11 | Instagram / photo sharing | M | Media + feed | Object store, CDN, feed |
| 12 | Live comments / live reactions | H | Fan-out to viewers in real time | Pub/sub tiers, sampling, batching |
| 13 | Presence service | M | Approximate state at scale | Heartbeats, TTL, selective fan-out |
| 14 | Collaborative document editor | H | Concurrent edits | OT/CRDT, sessions, persistence |
| 15 | Social graph (friends, mutuals) | M | Graph queries | Adjacency lists, sharding, caching |

## Media and storage

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 16 | [Video streaming](../05-case-studies/Media-and-Storage/VideoStreaming/README.md) | H | Transcode + delivery | ABR, CDN tiers, DAG pipeline |
| 17 | [File storage and sync](../05-case-studies/Media-and-Storage/FileStorageSync/README.md) | H | Chunking, sync, conflicts | Dedupe, change log, versions |
| 18 | Music streaming (Spotify) | M | Catalogue + playlists + offline | CDN, metadata, playlist consistency |
| 19 | Image upload & processing service | M | Async pipeline | Presigned upload, queue, thumbnails |
| 20 | Distributed file system (GFS/HDFS) | H | Metadata vs data | Master, chunk servers, replication |

## Location and marketplace

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 21 | [Ride hailing](../05-case-studies/Location-Based-Services/RideHailing/README.md) | H | Geo index + matching | Cells, in-memory index, offer locking |
| 22 | [Nearby places](../05-case-studies/Location-Based-Services/NearbyPlaces/README.md) | M | Geo search | Geohash/S2/quadtree, ES |
| 23 | Food delivery | H | 3-sided marketplace | Dispatch, ETAs, order state machine |
| 24 | Hotel / airline booking | H | Inventory + payments | Holds, idempotency, overbooking policy |
| 25 | [Ticket booking](../05-case-studies/Commerce-and-Payments/TicketBooking/README.md) | H | Seat contention | Conditional updates, waiting room |
| 26 | [Flash sale](../05-case-studies/Commerce-and-Payments/FlashSaleInventory/README.md) | H | Hot row, spikes | Redis gate, queue, reservations |
| 27 | Shopping cart and checkout | M | Availability vs correctness | Cart in KV, checkout saga |
| 28 | Auction system | H | Concurrent bidding | Ordered bid log, close time, sniping rules |

## Search and data

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 29 | [Typeahead](../05-case-studies/Search-and-Discovery/Typeahead/README.md) | M | Latency, prefix data | Trie top-k, offline build |
| 30 | [Web crawler](../05-case-studies/Search-and-Discovery/WebCrawler/README.md) | H | Frontier, politeness | Bloom filter, host partitioning |
| 31 | Search engine (simplified) | H | Index build + query | Inverted index, sharding, ranking |
| 32 | Analytics dashboard / clickstream | H | High-volume ingest | Kafka, stream + batch, OLAP store |
| 33 | Recommendation system (high level) | H | Candidate gen + ranking | Offline/online split, feature store |

## Payments and infrastructure

| # | Prompt | Level | Core challenge | Strong answers cover |
|---|---|---|---|---|
| 34 | [Payment system](../05-case-studies/Commerce-and-Payments/PaymentSystem/README.md) | H | Correctness | Idempotency, ledger, reconciliation |
| 35 | Digital wallet / money transfer | H | Atomic transfers | Double entry, single-shard txns, saga |
| 36 | [Distributed cache](../05-case-studies/Distributed-Infrastructure/DistributedCache/README.md) | H | Partitioning, eviction | Hashing, replication, hot keys |
| 37 | [Distributed KV store](../05-case-studies/Distributed-Infrastructure/KeyValueStore/README.md) | H | AP design | Quorums, hinted handoff, Merkle trees |
| 38 | [Job scheduler](../05-case-studies/Distributed-Infrastructure/JobScheduler/README.md) | H | Timers, leases | Due index, claiming, retries |
| 39 | [Metrics / logging pipeline](../05-case-studies/Distributed-Infrastructure/MetricsLoggingPipeline/README.md) | H | Ingest at scale | Kafka, TSDB, cardinality |
| 40 | Distributed lock service | H | Safety under failure | Leases, fencing, consensus |
| 41 | CDN design | H | Caching hierarchy | Edge/regional/origin, invalidation |
| 42 | Feature flag / config service | M | Propagation and safety | Push/poll, versioning, rollout |
| 43 | Email service | M | Deliverability, queues | SMTP, bounces, reputation, retries |
| 44 | Pub/sub system | H | Broker internals | Partitions, offsets, retention |
| 45 | Multi-region active-active data store | H | Conflicts, latency | Home region, CRDTs, replication |

## How to practise a prompt

1. Set a 40-minute timer. Use paper or a whiteboard.
2. Follow [the framework](../00-getting-started/interview-framework.md); speak aloud.
3. Compare with the worked example or, for unlinked prompts, self-review against the "strong answers cover" column.
4. Write down the two things you missed and the trade-off you failed to state.
5. Redo the same prompt a week later without notes.
