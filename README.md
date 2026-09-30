# 🏗️ System Design Interviews — Study Guide

Study material, deep dives and worked interview questions for **system design rounds at product-based
companies**, organised as a course. Every problem follows the same flow:
**Clarify → Estimate → Core APIs → High-Level Design → Database Design → Deep Dive → Follow-ups (answered) → Practice → Revision**.

> 📚 **Credit:** The course outline (chapter selection, order, and priority/difficulty tags) and the
> choice of interview questions are credited to
> [AlgoMaster.io — System Design Interviews](https://algomaster.io/learn/system-design-interviews/course-roadmap).
> All text, numbers, tables and diagrams in this repository were written with Claude for personal
> interview preparation; the premium lesson content was **not** accessed or reproduced.
> Not affiliated with AlgoMaster.io: please support the original at [algomaster.io](https://algomaster.io).
> See [CREDITS.md](CREDITS.md).

**Progress: 105/105 chapters written.** ✅ written · 🚧 planned

## How to study

1. Start with [Introduction](01-Introduction/README.md) and the [study plan](01-Introduction/04-study-plan.md).
2. Learn the **Must-Know Topics**, **Concept** and **Technology** deep dives.
3. Learn the **Interview Patterns** (reusable solutions to recurring problems).
4. Practise the **Design Questions**: read only the prompt, attempt it for 35 minutes, then compare.
5. Use [`_Reference/`](_Reference/README.md) for quick-revision Q&A, rapid-fire drills and the mock-interview rubric.

Priority = how often the topic appears in interviews; difficulty = how hard it is to learn.
Tools: `python3 tools/build.py` regenerates navigation, indexes and this table.


## [Introduction](01-Introduction/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [What are System Design Interviews?](01-Introduction/01-what-are-system-design-interviews.md) | High | Beginner | ✅ |
| [Types of System Design Questions](01-Introduction/02-types-of-system-design-questions.md) | High | Beginner | ✅ |
| [Expectations by Level/YoE](01-Introduction/03-expectations-by-level.md) | High | Beginner | ✅ |
| [Study Plan (bonus)](01-Introduction/04-study-plan.md) | — | — | ✅ |

## [Must-Know Topics](02-Must-Know-Topics/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Concepts](02-Must-Know-Topics/01-concepts.md) | High | Beginner | ✅ |
| [Technologies](02-Must-Know-Topics/02-technologies.md) | High | Beginner | ✅ |
| [Tradeoffs](02-Must-Know-Topics/03-tradeoffs.md) | High | Intermediate | ✅ |
| [Data Structures](02-Must-Know-Topics/04-data-structures.md) | Medium | Intermediate | ✅ |

## [Concept Deep Dives](03-Concept-Deep-Dives/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Networking](03-Concept-Deep-Dives/01-networking.md) | High | Beginner | ✅ |
| [Caching](03-Concept-Deep-Dives/02-caching.md) | High | Intermediate | ✅ |
| [API Design](03-Concept-Deep-Dives/03-api-design.md) | High | Intermediate | ✅ |
| [Database Design](03-Concept-Deep-Dives/04-database-design.md) | High | Intermediate | ✅ |
| [Distributed Systems](03-Concept-Deep-Dives/05-Distributed-Systems/README.md) | High | Advanced | ✅ |

## [Technology Deep Dives](04-Technology-Deep-Dives/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [PostgreSQL](04-Technology-Deep-Dives/01-postgresql.md) | High | Intermediate | ✅ |
| [MongoDB](04-Technology-Deep-Dives/02-mongodb.md) | Medium | Intermediate | ✅ |
| [Redis](04-Technology-Deep-Dives/03-redis.md) | High | Intermediate | ✅ |
| [DynamoDB](04-Technology-Deep-Dives/04-dynamodb.md) | High | Intermediate | ✅ |
| [Cassandra](04-Technology-Deep-Dives/05-cassandra.md) | High | Advanced | ✅ |
| [Elasticsearch](04-Technology-Deep-Dives/06-elasticsearch.md) | High | Intermediate | ✅ |
| [Kafka](04-Technology-Deep-Dives/07-kafka.md) | High | Intermediate | ✅ |
| [RabbitMQ](04-Technology-Deep-Dives/08-rabbitmq.md) | Medium | Intermediate | ✅ |
| [SQS](04-Technology-Deep-Dives/09-sqs.md) | Medium | Intermediate | ✅ |
| [Flink](04-Technology-Deep-Dives/10-flink.md) | Low | Advanced | ✅ |
| [S3](04-Technology-Deep-Dives/11-s3.md) | High | Intermediate | ✅ |
| [ZooKeeper](04-Technology-Deep-Dives/12-zookeeper.md) | Medium | Advanced | ✅ |

## [Interview Patterns](05-Interview-Patterns/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Scaling Read Traffic](05-Interview-Patterns/01-scaling-read-traffic.md) | High | Intermediate | ✅ |
| [Scaling Write Traffic](05-Interview-Patterns/02-scaling-write-traffic.md) | High | Intermediate | ✅ |
| [Handling Hot Keys](05-Interview-Patterns/03-handling-hot-keys.md) | High | Intermediate | ✅ |
| [Absorbing Traffic Spikes](05-Interview-Patterns/04-absorbing-traffic-spikes.md) | High | Intermediate | ✅ |
| [Pushing Real-time Updates](05-Interview-Patterns/05-pushing-realtime-updates.md) | High | Intermediate | ✅ |
| [Fanning Out Updates](05-Interview-Patterns/06-fanning-out-updates.md) | High | Intermediate | ✅ |
| [Uploading and Serving Large Files](05-Interview-Patterns/07-uploading-and-serving-large-files.md) | Medium | Intermediate | ✅ |
| [Streaming Video and Audio](05-Interview-Patterns/08-streaming-video-and-audio.md) | High | Advanced | ✅ |
| [Surviving Component Failures](05-Interview-Patterns/09-surviving-component-failures.md) | High | Intermediate | ✅ |
| [Preventing Duplicate Processing](05-Interview-Patterns/10-preventing-duplicate-processing.md) | High | Intermediate | ✅ |
| [Running Across Multiple Regions](05-Interview-Patterns/11-running-across-multiple-regions.md) | Medium | Advanced | ✅ |
| [Coordinating Transactions Across Services](05-Interview-Patterns/12-coordinating-transactions-across-services.md) | Medium | Advanced | ✅ |
| [Keeping Data in Sync](05-Interview-Patterns/13-keeping-data-in-sync.md) | High | Intermediate | ✅ |
| [Preventing Double Booking](05-Interview-Patterns/14-preventing-double-booking.md) | High | Intermediate | ✅ |
| [Handling Long-Running Tasks](05-Interview-Patterns/15-handling-long-running-tasks.md) | High | Intermediate | ✅ |
| [Scheduling Delayed and Recurring Jobs](05-Interview-Patterns/16-scheduling-delayed-and-recurring-jobs.md) | Medium | Intermediate | ✅ |
| [Search and Typeahead](05-Interview-Patterns/17-search-and-typeahead.md) | High | Intermediate | ✅ |
| [Finding and Tracking Locations](05-Interview-Patterns/18-finding-and-tracking-locations.md) | High | Intermediate | ✅ |
| [Generating Unique IDs](05-Interview-Patterns/19-generating-unique-ids.md) | Medium | Intermediate | ✅ |
| [Counting at Scale](05-Interview-Patterns/20-counting-at-scale.md) | Medium | Advanced | ✅ |

## [Interview Tips](06-Interview-Tips/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Answering Framework](06-Interview-Tips/01-answering-framework.md) | High | Beginner | ✅ |
| [Estimation Cheatsheet](06-Interview-Tips/02-estimation-cheatsheet.md) | High | Beginner | ✅ |
| [Diagramming Tips](06-Interview-Tips/03-diagramming-tips.md) | High | Beginner | ✅ |
| [Choosing the Right Database](06-Interview-Tips/04-choosing-the-right-database.md) | High | Intermediate | ✅ |

## [Basic Questions](07-Basic-Questions/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design URL Shortener](07-Basic-Questions/URL-Shortener/README.md) | High | Beginner | ✅ |
| [Design Pastebin](07-Basic-Questions/Pastebin/README.md) | Medium | Beginner | ✅ |

## [Real-Time Communication](08-Real-Time-Communication/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design WhatsApp](08-Real-Time-Communication/WhatsApp/README.md) | High | Intermediate | ✅ |
| [Design Slack](08-Real-Time-Communication/Slack/README.md) | Medium | Intermediate | ✅ |
| [Design Live Comments](08-Real-Time-Communication/Live-Comments/README.md) | Medium | Intermediate | ✅ |
| [Design Google Docs](08-Real-Time-Communication/Google-Docs/README.md) | High | Advanced | ✅ |
| [Design Zoom](08-Real-Time-Communication/Zoom/README.md) | Medium | Advanced | ✅ |

## [Social Media Systems](09-Social-Media-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Instagram](09-Social-Media-Systems/Instagram/README.md) | High | Intermediate | ✅ |
| [Design FB News Feed](09-Social-Media-Systems/FB-News-Feed/README.md) | High | Intermediate | ✅ |
| [Design TikTok](09-Social-Media-Systems/TikTok/README.md) | Medium | Intermediate | ✅ |
| [Design Reddit](09-Social-Media-Systems/Reddit/README.md) | Medium | Intermediate | ✅ |
| [Design Tinder](09-Social-Media-Systems/Tinder/README.md) | Medium | Intermediate | ✅ |

## [Media Streaming & Delivery](10-Media-Streaming-and-Delivery/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Spotify](10-Media-Streaming-and-Delivery/Spotify/README.md) | Medium | Intermediate | ✅ |
| [Design YouTube](10-Media-Streaming-and-Delivery/YouTube/README.md) | High | Intermediate | ✅ |
| [Design Netflix](10-Media-Streaming-and-Delivery/Netflix/README.md) | High | Intermediate | ✅ |
| [Design Google Drive](10-Media-Streaming-and-Delivery/Google-Drive/README.md) | High | Intermediate | ✅ |
| [Design Gmail](10-Media-Streaming-and-Delivery/Gmail/README.md) | Low | Advanced | ✅ |
| [Design Twitch](10-Media-Streaming-and-Delivery/Twitch/README.md) | Medium | Advanced | ✅ |

## [Location-Based Services](11-Location-Based-Services/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Airbnb](11-Location-Based-Services/Airbnb/README.md) | Medium | Intermediate | ✅ |
| [Design Food Delivery Service](11-Location-Based-Services/Food-Delivery-Service/README.md) | Medium | Intermediate | ✅ |
| [Design Uber](11-Location-Based-Services/Uber/README.md) | High | Advanced | ✅ |
| [Design Google Maps](11-Location-Based-Services/Google-Maps/README.md) | Medium | Advanced | ✅ |
| [Design Nearby Places / Yelp (bonus)](11-Location-Based-Services/Nearby-Places-Bonus/README.md) | — | — | ✅ |

## [Search & Aggregation Systems](12-Search-and-Aggregation-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Search Autocomplete System](12-Search-and-Aggregation-Systems/Search-Autocomplete/README.md) | High | Beginner | ✅ |
| [Design News Aggregator](12-Search-and-Aggregation-Systems/News-Aggregator/README.md) | Low | Intermediate | ✅ |
| [Design Web Crawler](12-Search-and-Aggregation-Systems/Web-Crawler/README.md) | High | Intermediate | ✅ |
| [Design Google Search](12-Search-and-Aggregation-Systems/Google-Search/README.md) | Medium | Advanced | ✅ |
| [Design Ad Click Aggregator](12-Search-and-Aggregation-Systems/Ad-Click-Aggregator/README.md) | Medium | Advanced | ✅ |

## [E-commerce & Marketplace](13-E-commerce-and-Marketplace/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Amazon](13-E-commerce-and-Marketplace/Amazon/README.md) | Medium | Intermediate | ✅ |
| [Design Shopify](13-E-commerce-and-Marketplace/Shopify/README.md) | Low | Intermediate | ✅ |
| [Design Flash Sale](13-E-commerce-and-Marketplace/Flash-Sale/README.md) | Medium | Advanced | ✅ |
| [Design Online Auction System](13-E-commerce-and-Marketplace/Online-Auction-System/README.md) | Low | Advanced | ✅ |
| [Design Movie Booking System](13-E-commerce-and-Marketplace/Movie-Booking/README.md) | Medium | Advanced | ✅ |

## [Payment & Financial Systems](14-Payment-and-Financial-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Payment System](14-Payment-and-Financial-Systems/Payment-System/README.md) | High | Intermediate | ✅ |
| [Design Digital Wallet](14-Payment-and-Financial-Systems/Digital-Wallet/README.md) | Medium | Advanced | ✅ |
| [Design Stock Exchange](14-Payment-and-Financial-Systems/Stock-Exchange/README.md) | Low | Advanced | ✅ |

## [Distributed Infrastructure](15-Distributed-Infrastructure/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Load Balancer](15-Distributed-Infrastructure/Load-Balancer/README.md) | High | Intermediate | ✅ |
| [Design API Gateway](15-Distributed-Infrastructure/API-Gateway/README.md) | High | Intermediate | ✅ |
| [Design Rate Limiter](15-Distributed-Infrastructure/Rate-Limiter/README.md) | High | Intermediate | ✅ |
| [Design Key-Value Store](15-Distributed-Infrastructure/Key-Value-Store/README.md) | High | Advanced | ✅ |
| [Design Distributed Cache](15-Distributed-Infrastructure/Distributed-Cache/README.md) | High | Advanced | ✅ |
| [Design CDN](15-Distributed-Infrastructure/CDN/README.md) | Medium | Advanced | ✅ |
| [Design Object Storage like S3](15-Distributed-Infrastructure/Object-Storage-S3/README.md) | Medium | Advanced | ✅ |
| [Design Messaging Queue](15-Distributed-Infrastructure/Messaging-Queue/README.md) | Medium | Advanced | ✅ |
| [Design Time Series Database](15-Distributed-Infrastructure/Time-Series-Database/README.md) | Low | Advanced | ✅ |
| [Design Locking Service](15-Distributed-Infrastructure/Locking-Service/README.md) | Low | Advanced | ✅ |

## [Counting & Ranking Systems](16-Counting-and-Ranking-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Likes Counting System](16-Counting-and-Ranking-Systems/Likes-Counting-System/README.md) | Medium | Intermediate | ✅ |
| [Design Real Time Leaderboard](16-Counting-and-Ranking-Systems/Real-Time-Leaderboard/README.md) | Medium | Intermediate | ✅ |
| [Design Top K](16-Counting-and-Ranking-Systems/Top-K/README.md) | Medium | Advanced | ✅ |

## [Asynchronous Systems](17-Asynchronous-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design Notification Service](17-Asynchronous-Systems/Notification-Service/README.md) | High | Intermediate | ✅ |
| [Design Job Scheduler](17-Asynchronous-Systems/Job-Scheduler/README.md) | Medium | Intermediate | ✅ |
| [Design CI/CD Pipeline](17-Asynchronous-Systems/CI-CD-Pipeline/README.md) | Low | Intermediate | ✅ |
| [Design Monitoring and Alerting System](17-Asynchronous-Systems/Monitoring-and-Alerting/README.md) | Medium | Intermediate | ✅ |

## [Specialized Systems](18-Specialized-Systems/README.md)

| Chapter | Priority | Difficulty | Status |
|---|---|---|---|
| [Design LeetCode](18-Specialized-Systems/LeetCode/README.md) | Medium | Intermediate | ✅ |
| [Design Calendar System](18-Specialized-Systems/Calendar-System/README.md) | Low | Advanced | ✅ |
| [Design Online Chess](18-Specialized-Systems/Online-Chess/README.md) | Low | Advanced | ✅ |

## 🔗 Companion repository

Object-oriented (low-level) design: [Low-Level-Design](https://github.com/Chaithumoorpa/Low-Level-Design).
