# 🔎 Search and Discovery — High Level Design

Systems that **find and index information**: precomputed lookups, crawling and freshness.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 12 | [Typeahead](Typeahead/README.md) | Trie with precomputed top-k, offline snapshot build + atomic swap, freshness layer, edge caching | [Search & geospatial](../../02-core-concepts/15-search-and-geospatial.md), [Caching](../../02-core-concepts/03-caching.md) |
| 13 | [Web Crawler](WebCrawler/README.md) | URL frontier with per-host politeness, Bloom-filter dedupe, SimHash, host-partitioned crawling | [Consistent hashing](../../02-core-concepts/08-consistent-hashing.md), [Probabilistic structures](../../03-technologies/06-coordination-and-misc.md) |

⬅️ Previous category: [Location-Based Services](../Location-Based-Services/README.md) · ➡️ Next category: [Commerce and Payments](../Commerce-and-Payments/README.md)
