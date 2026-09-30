# Design a Nearby Places Service (Yelp / Google Maps Places style)

**Prompt:** Given a location and radius, return nearby businesses, filterable by category, rating and open now.

## Requirements

- Functional: search nearby (radius, category, rating filters), business details, add/update business, reviews (brief).
- Non-functional: p99 < 200 ms, read-heavy, businesses change rarely, 200M places, 100M DAU, eventual consistency for updates fine.

## Estimates

- 100M DAU x 5 searches = 500M/day = ~6k/s avg, ~20k/s peak. Places data: 200M x 1 KB = 200 GB: fits comfortably in memory across a few nodes; the index itself is small.

## Design

```
Client -> LB -> Search service -> Geo index (sharded) + attribute filters -> Ranker
Business service (CRUD) -> DB of record -> CDC -> index builders -> geo index / Elasticsearch
Read replicas + cache for details; CDN for photos
```

## Geo indexing options

| Option | Query | Trade-off |
|---|---|---|
| Geohash column + B-tree/index | Compute covering prefixes at chosen precision, `WHERE geohash LIKE 'abc%'` for cell and 8 neighbours, filter exact distance | Simple, works in SQL/Redis; fixed precision, edge cases |
| Quadtree (in memory) | Traverse to cells intersecting circle | Adaptive to density (dense cities split deeper); rebuild/updates need care |
| S2 / H3 cells | Cover circle with cells at a level, look up each | Uniform, hierarchical, production proven |
| Elasticsearch geo queries | `geo_distance` filter plus text/category filters, sorted by score | One system for text + geo + filters |

Recommended: Elasticsearch (or PostGIS for smaller scale) for combined filter + geo + ranking; or geohash/S2 cell to business-ID lists in a KV store for ultra-fast simple lookups.

## Deep dives

- **Radius search**: choose cell precision so the cell size is about the radius; query the center cell + neighbours; post-filter by haversine distance; if too few results, expand ring by ring.
- **Density skew**: Manhattan vs rural: quadtree splits until <= N places per node, or variable radius expansion with a result cap.
- **Sharding**: by region (geohash prefix) rather than by business ID, so a query hits one or few shards. Watch hot regions (big cities): split them further and replicate.
- **Freshness**: businesses rarely move; update index near real time via CDC; rebuild periodically.
- **Ranking**: distance, rating, popularity, open now, personalisation, sponsored placements.
- **Caching**: cache results by (cell, filters) for short TTL; popular areas benefit greatly.

## Follow-ups

- Moving objects instead of static places? (See ride-hailing: in-memory grid with TTL.)
- Global search by name + location? (Text + geo boost.)
- Keeping the index consistent after a business is deleted?
