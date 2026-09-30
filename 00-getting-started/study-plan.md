# Study Plan

Pick a track based on how long until your interview. Each "session" is about 90 minutes.

## 4-week track (experienced, revising)

| Week | Focus | Sessions |
|---|---|---|
| 1 | Framework, estimation, API design, caching, load balancing, DB scaling | Foundations + concepts 01-06 |
| 2 | Consistency, messaging, rate limiting, failure handling, technologies | Concepts 07-14, Redis, Kafka |
| 3 | 8 case studies (1, 2, 4, 6, 8, 10, 14, 16) | Attempt cold, then compare |
| 4 | 6 more case studies + mock interviews + rapid-fire | Timed, out loud |

## 8-week track (building from scratch)

| Week | Focus |
|---|---|
| 1 | Networking basics, HTTP/REST/gRPC, API design, estimation |
| 2 | Scaling, load balancing, caching, CDN |
| 3 | Data storage: indexes, SQL vs NoSQL, sharding, replication |
| 4 | Consistency, CAP/PACELC, consensus, distributed transactions |
| 5 | Messaging, streams, idempotency, retries, resilience, observability |
| 6 | Technologies (Redis, Kafka, Cassandra/Dynamo, Elasticsearch, S3) and patterns |
| 7 | Case studies 1-12 |
| 8 | Case studies 13-20, mocks, weak-area review |

## Weekly rhythm

- **Two days:** learn a concept, then write a 10-line summary from memory.
- **Two days:** one case study, cold attempt, then compare.
- **One day:** rapid-fire questions from `06-interview-questions/`.
- **One day:** a mock interview with a peer, or record yourself.

## Self-check before the interview

You are ready when you can, without notes:

- [ ] Run a full 45-minute interview using the framework in this folder.
- [ ] Do back-of-envelope math for QPS, storage and bandwidth in under 3 minutes.
- [ ] Explain when to pick SQL vs NoSQL, and which sharding key you would use, with reasons.
- [ ] Name two failure modes for every box on your diagram, and how you would handle them.
- [ ] Discuss at least three trade-offs per design (consistency vs availability, latency vs cost, simplicity vs scale).
