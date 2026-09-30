# Study Plan

<!-- nav:start -->
⬅️ Previous: [Expectations by Level/YoE](03-expectations-by-level.md) · 🏠 [Introduction](README.md) · ➡️ Next: [Concepts](../02-Must-Know-Topics/01-concepts.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Pick a track based on how long until your interview. A "session" is about 90 minutes. Chapter names match the [course roadmap](../README.md).

## 4-week track (experienced, revising)

| Week | Focus | Chapters |
|---|---|---|
| 1 | Framework, estimation, must-know topics, caching, database design, API design | [Introduction](README.md), [Must-Know Topics](../02-Must-Know-Topics/README.md), [Answering Framework](../06-Interview-Tips/01-answering-framework.md), [Concept Deep Dives](../03-Concept-Deep-Dives/README.md) |
| 2 | Distributed systems + the patterns that recur in every design | [Distributed Systems](../03-Concept-Deep-Dives/05-Distributed-Systems/README.md), [Interview Patterns](../05-Interview-Patterns/README.md), Redis, Kafka, DynamoDB/Cassandra |
| 3 | 8 high-priority questions cold, then compare | URL Shortener, Rate Limiter, WhatsApp, FB News Feed, YouTube, Uber, Payment System, Movie Booking |
| 4 | 6 more questions + mock interviews + rapid-fire | Distributed Cache, Notification Service, Search Autocomplete, Web Crawler, Ad Click Aggregator, Key-Value Store |

## 8-week track (building from scratch)

| Week | Focus |
|---|---|
| 1 | [Introduction](README.md), [Networking](../03-Concept-Deep-Dives/01-networking.md), [API Design](../03-Concept-Deep-Dives/03-api-design.md), [Estimation](../06-Interview-Tips/02-estimation-cheatsheet.md) |
| 2 | [Caching](../03-Concept-Deep-Dives/02-caching.md), load balancing, CDN, [Scaling Read Traffic](../05-Interview-Patterns/01-scaling-read-traffic.md) |
| 3 | [Database Design](../03-Concept-Deep-Dives/04-database-design.md), [Choosing the Right Database](../06-Interview-Tips/04-choosing-the-right-database.md), PostgreSQL, MongoDB, DynamoDB, Cassandra |
| 4 | [Distributed Systems](../03-Concept-Deep-Dives/05-Distributed-Systems/README.md): replication, sharding, consistency, consistent hashing |
| 5 | Messaging (Kafka, RabbitMQ, SQS), Flink, patterns: duplicates, failures, transactions, keeping data in sync |
| 6 | Remaining patterns + S3, ZooKeeper, Elasticsearch, Redis |
| 7 | Design questions: Basic, Real-Time, Social, Media, Location |
| 8 | Design questions: Search, E-commerce, Payments, Infrastructure, Counting, Async, Specialized + mocks |

## Weekly rhythm

- **Two days:** learn a chapter, then write a 10-line summary from memory.
- **Two days:** one design question, cold attempt (35 min), then compare with the write-up.
- **One day:** rapid-fire questions from [`_Reference/interview-questions/`](../_Reference/interview-questions/02-rapid-fire.md).
- **One day:** a mock interview with a peer, or record yourself, using the [rubric](../_Reference/interview-questions/03-mock-interview-rubric.md).

## Self-check before the interview

You are ready when you can, without notes:

- [ ] Run a full 45-minute interview using the [answering framework](../06-Interview-Tips/01-answering-framework.md).
- [ ] Do back-of-envelope math for QPS, storage and bandwidth in under 3 minutes.
- [ ] Explain when to pick SQL vs NoSQL and which shard key you would use, with reasons.
- [ ] Name two failure modes for every box on your diagram, and how you would handle them.
- [ ] Discuss at least three trade-offs per design (consistency vs availability, latency vs cost, simplicity vs scale).
