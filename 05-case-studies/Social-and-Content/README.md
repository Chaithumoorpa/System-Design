# 🌐 Social and Content — High Level Design

Read-heavy content systems where **fan-out, ranking and approximate counting** dominate.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 6 | [News Feed](NewsFeed/README.md) | Hybrid push/pull fan-out, timeline cache, cursor pagination, ranking service | [Fan-out & hot keys](../../04-patterns/04-fanout-and-hot-keys.md), [Caching](../../02-core-concepts/03-caching.md) |
| 7 | [Top-K / Trending](TopKTrending/README.md) | Kafka partition by key, sliding windows, Count-Min Sketch, velocity scoring, lambda-style correction | [Messaging](../../02-core-concepts/09-messaging-and-streaming.md), [Probabilistic structures](../../03-technologies/06-coordination-and-misc.md) |

⬅️ Previous category: [Real-Time Communication](../Real-Time-Communication/README.md) · ➡️ Next category: [Media and Storage](../Media-and-Storage/README.md)
