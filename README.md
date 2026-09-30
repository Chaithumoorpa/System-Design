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
| [`05-case-studies/`](05-case-studies/) | 20 classic design problems, each with requirements, estimates, design, deep dives, follow-ups |
| [`06-interview-questions/`](06-interview-questions/) | Concept Q&A, rapid-fire drills, "design X" prompt bank, mock interview rubric |

## Suggested path

1. Read [`00-getting-started/study-plan.md`](00-getting-started/study-plan.md) and pick a 4, 6 or 8-week track.
2. Learn foundations and core concepts first. Do not start case studies before caching, sharding, replication and queues feel comfortable.
3. For each case study: **read the prompt only, attempt it on paper for 35 minutes, then compare** with the write-up.
4. Use the question banks in `06-interview-questions/` for spaced repetition.

## Case study index

Basics: [URL shortener](05-case-studies/01-url-shortener.md) · [Rate limiter](05-case-studies/02-rate-limiter.md) · [Unique ID generator](05-case-studies/03-unique-id-generator.md)
Real-time: [Chat system](05-case-studies/04-chat-system.md) · [Notification service](05-case-studies/05-notification-service.md)
Social: [News feed](05-case-studies/06-news-feed.md) · [Trending topics / Top-K](05-case-studies/07-top-k-trending.md)
Media: [Video streaming](05-case-studies/08-video-streaming.md) · [File storage and sync](05-case-studies/09-file-storage-sync.md)
Location: [Ride hailing](05-case-studies/10-ride-hailing.md) · [Nearby places](05-case-studies/11-nearby-places.md)
Search: [Typeahead](05-case-studies/12-typeahead.md) · [Web crawler](05-case-studies/13-web-crawler.md)
Commerce: [Ticket booking](05-case-studies/14-ticket-booking.md) · [Flash sale / inventory](05-case-studies/15-flash-sale-inventory.md)
Payments: [Payment system](05-case-studies/16-payment-system.md)
Infrastructure: [Distributed cache](05-case-studies/17-distributed-cache.md) · [Key-value store](05-case-studies/18-key-value-store.md) · [Job scheduler](05-case-studies/19-job-scheduler.md) · [Metrics and logging pipeline](05-case-studies/20-metrics-logging-pipeline.md)
