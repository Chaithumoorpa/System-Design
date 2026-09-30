# 🗺️ Location-Based Services — High Level Design

Systems built around **where things are**: spatial indexes, moving vs static objects, regional isolation.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 10 | [Ride Hailing](RideHailing/README.md) | In-memory cell index with TTL, ETA-ranked matching, atomic offer locks, trip state machine, surge | [Search & geospatial](../../02-core-concepts/15-search-and-geospatial.md), [Saga](../../04-patterns/02-saga.md) |
| 11 | [Nearby Places](NearbyPlaces/README.md) | Geohash/S2/quadtree/ES, query centre + neighbours, region sharding, CDC-fed index | [Elasticsearch](../../03-technologies/05-elasticsearch.md), [Caching](../../02-core-concepts/03-caching.md) |

⬅️ Previous category: [Media and Storage](../Media-and-Storage/README.md) · ➡️ Next category: [Search and Discovery](../Search-and-Discovery/README.md)
