# 🏛️ High Level Design — Interview Practice

20 classic system design problems written the way you would present them in an interview:

**Clarify → Estimate → Core APIs → High-Level Design → Database Design → Deep Dive → Follow-ups (all answered) → Practice → Revision**

Each problem has Mermaid diagrams, a sample interviewer conversation, answered follow-ups, a practice
round, and links to the concept notes it depends on. Problems are chained with ⬅️ / ➡️ links so you can
read them in order.

## 📂 Categories

| Category | Problems |
|---|---|
| [🧩 Basics](Basics/README.md) | URL Shortener, Rate Limiter, Unique ID Generator |
| [💬 Real-Time Communication](Real-Time-Communication/README.md) | Chat System, Notification Service |
| [🌐 Social and Content](Social-and-Content/README.md) | News Feed, Top-K / Trending |
| [🎞️ Media and Storage](Media-and-Storage/README.md) | Video Streaming, File Storage and Sync |
| [🗺️ Location-Based Services](Location-Based-Services/README.md) | Ride Hailing, Nearby Places |
| [🔎 Search and Discovery](Search-and-Discovery/README.md) | Typeahead, Web Crawler |
| [🛒 Commerce and Payments](Commerce-and-Payments/README.md) | Ticket Booking, Flash Sale / Inventory, Payment System |
| [🏗️ Distributed Infrastructure](Distributed-Infrastructure/README.md) | Distributed Cache, Key-Value Store, Job Scheduler, Metrics and Logging Pipeline |

## 🧭 Recommended order

| # | Problem | Level | Main lesson |
|---|---|---|---|
| 1 | [URL Shortener](Basics/URLShortener/README.md) | Easy–Med | ID generation, caching, read-heavy design |
| 2 | [Rate Limiter](Basics/RateLimiter/README.md) | Medium | Algorithms, atomicity, failure policy |
| 3 | [Unique ID Generator](Basics/UniqueIdGenerator/README.md) | Medium | Coordination-free uniqueness |
| 4 | [Chat System](Real-Time-Communication/ChatSystem/README.md) | Hard | Connections, ordering, delivery |
| 5 | [Notification Service](Real-Time-Communication/NotificationService/README.md) | Medium | Queues, priority isolation |
| 6 | [News Feed](Social-and-Content/NewsFeed/README.md) | Hard | Fan-out trade-offs |
| 7 | [Top-K / Trending](Social-and-Content/TopKTrending/README.md) | Hard | Streaming aggregation, sketches |
| 8 | [Video Streaming](Media-and-Storage/VideoStreaming/README.md) | Hard | Pipelines, CDN, ABR |
| 9 | [File Storage and Sync](Media-and-Storage/FileStorageSync/README.md) | Hard | Chunking, sync, conflicts |
| 10 | [Ride Hailing](Location-Based-Services/RideHailing/README.md) | Hard | Geo index, matching |
| 11 | [Nearby Places](Location-Based-Services/NearbyPlaces/README.md) | Medium | Spatial indexing |
| 12 | [Typeahead](Search-and-Discovery/Typeahead/README.md) | Medium | Precomputation, tries |
| 13 | [Web Crawler](Search-and-Discovery/WebCrawler/README.md) | Hard | Frontier, politeness, dedupe |
| 14 | [Ticket Booking](Commerce-and-Payments/TicketBooking/README.md) | Hard | Contention, holds |
| 15 | [Flash Sale / Inventory](Commerce-and-Payments/FlashSaleInventory/README.md) | Hard | Load funnel, hot rows |
| 16 | [Payment System](Commerce-and-Payments/PaymentSystem/README.md) | Hard | Idempotency, ledger |
| 17 | [Distributed Cache](Distributed-Infrastructure/DistributedCache/README.md) | Hard | Partitioning, eviction |
| 18 | [Key-Value Store](Distributed-Infrastructure/KeyValueStore/README.md) | Hard | Quorums, LSM |
| 19 | [Job Scheduler](Distributed-Infrastructure/JobScheduler/README.md) | Hard | Timers, leases |
| 20 | [Metrics and Logging Pipeline](Distributed-Infrastructure/MetricsLoggingPipeline/README.md) | Hard | Ingest at scale, cardinality |

## 🔗 Companion repository

Object-oriented (low-level) versions of several of these live in the
[Low-Level-Design repo](https://github.com/Chaithumoorpa/Low-Level-Design): Rate Limiter, LRU/LFU Cache,
Search Autocomplete, Notification System, Pub-Sub, Chat Application, Payment Gateway, Movie Booking,
Inventory Management and Ride-Sharing.

> Personal learning project. Section layout is inspired by publicly visible course outlines; all
> text, numbers, tables and diagrams are original. Not affiliated with AlgoMaster.io.

⬅️ [Back to the main README](../README.md)
