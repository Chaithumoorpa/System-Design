# System Design Interview Prep

Study material and practice questions for system design rounds at product-based companies (FAANG-style, unicorns, and strong startups). All content is original and written for revision: dense, example-driven, and interview-oriented.

## How the material is organised

| Folder | What it covers |
|---|---|
| [`00-getting-started/`](00-getting-started/) | Study plan, interview framework, how interviewers score you |
| [`01-foundations/`](01-foundations/) | Estimation, requirements, API design, networking basics |
| [`02-core-concepts/`](02-core-concepts/) | Scaling, caching, sharding, replication, consistency, messaging, and more |
| [`03-technologies/`](03-technologies/) | Redis, Kafka, SQL/NoSQL stores, Elasticsearch, object storage, coordination services |
| [`04-patterns/`](04-patterns/) | Reusable design patterns (idempotency, saga, CQRS, fan-out, and others) |
| [`05-case-studies/`](05-case-studies/README.md) | 20 High Level Design problems in 8 categories. Each: clarify → estimate → APIs → HLD → database → deep dive → answered follow-ups → practice → revision |
| [`06-interview-questions/`](06-interview-questions/) | Concept Q&A, rapid-fire drills, "design X" prompt bank, mock interview rubric |

## Suggested path

1. Read [`00-getting-started/study-plan.md`](00-getting-started/study-plan.md) and pick a 4, 6 or 8-week track.
2. Learn foundations and core concepts first. Do not start case studies before caching, sharding, replication and queues feel comfortable.
3. For each case study: **read the prompt only, attempt it on paper for 35 minutes, then compare** with the write-up.
4. Use the question banks in `06-interview-questions/` for spaced repetition.

## Case study index (full list with levels: [`05-case-studies/README.md`](05-case-studies/README.md))

Basics: [URL shortener](05-case-studies/Basics/URLShortener/README.md) · [Rate limiter](05-case-studies/Basics/RateLimiter/README.md) · [Unique ID generator](05-case-studies/Basics/UniqueIdGenerator/README.md)
Real-time: [Chat system](05-case-studies/Real-Time-Communication/ChatSystem/README.md) · [Notification service](05-case-studies/Real-Time-Communication/NotificationService/README.md)
Social: [News feed](05-case-studies/Social-and-Content/NewsFeed/README.md) · [Trending topics / Top-K](05-case-studies/Social-and-Content/TopKTrending/README.md)
Media: [Video streaming](05-case-studies/Media-and-Storage/VideoStreaming/README.md) · [File storage and sync](05-case-studies/Media-and-Storage/FileStorageSync/README.md)
Location: [Ride hailing](05-case-studies/Location-Based-Services/RideHailing/README.md) · [Nearby places](05-case-studies/Location-Based-Services/NearbyPlaces/README.md)
Search: [Typeahead](05-case-studies/Search-and-Discovery/Typeahead/README.md) · [Web crawler](05-case-studies/Search-and-Discovery/WebCrawler/README.md)
Commerce: [Ticket booking](05-case-studies/Commerce-and-Payments/TicketBooking/README.md) · [Flash sale / inventory](05-case-studies/Commerce-and-Payments/FlashSaleInventory/README.md)
Payments: [Payment system](05-case-studies/Commerce-and-Payments/PaymentSystem/README.md)
Infrastructure: [Distributed cache](05-case-studies/Distributed-Infrastructure/DistributedCache/README.md) · [Key-value store](05-case-studies/Distributed-Infrastructure/KeyValueStore/README.md) · [Job scheduler](05-case-studies/Distributed-Infrastructure/JobScheduler/README.md) · [Metrics and logging pipeline](05-case-studies/Distributed-Infrastructure/MetricsLoggingPipeline/README.md)

Companion repo for object-oriented design: [Low-Level-Design](https://github.com/Chaithumoorpa/Low-Level-Design).
