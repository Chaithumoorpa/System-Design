# Pattern: Finding and Tracking Locations

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Search and Typeahead](17-search-and-typeahead.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Generating Unique IDs](19-generating-unique-ids.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Answer "what is near (lat, lng)?" quickly (static places) and "where is everything right
now?" continuously (moving drivers, couriers, devices), at high update rates.

## Recognise it when

Nearby places/restaurants, ride hailing, food delivery, dating apps (nearby users), geofencing, fleet
tracking, maps.

## Two workloads

| | Static places (Yelp) | Moving objects (Uber drivers) |
|---|---|---|
| Update rate | Rare | Every few seconds |
| Storage | Durable index (DB/ES) | In-memory with TTL |
| Consistency | Eventual OK | Latest position matters, old positions worthless |
| History | Not needed | Stream to cold storage for analytics |

## Spatial indexing options

| Structure | Idea | Pros | Cons |
|---|---|---|---|
| **Geohash** | Interleave lat/lng bits into base-32 string; shared prefix ⇒ near | Works in any sorted store; easy | Edge effects; cells uneven near poles; must query neighbours |
| **Quadtree** | Recursively split into 4 until ≤ N points | Adapts to density | In-memory; update/rebalance logic |
| **S2** (Google) | Sphere → hierarchical cells on a Hilbert curve | Accurate, region coverings | Learning curve |
| **H3** (Uber) | Hexagonal hierarchical grid | Uniform neighbour distances, good for aggregation (surge) | Cells don't nest perfectly |
| **R-tree / GiST** | Bounding boxes tree | Rich queries in PostGIS | Write-heavy loads |
| **Elasticsearch geo_point** | BKD tree | Geo + text + filters | Heavier infrastructure |

## Radius query algorithm

1. Choose a cell level so cell size ≈ search radius.
2. Compute the covering cells (center cell + neighbours, or S2 region covering).
3. Fetch candidates from those cells; filter by exact **haversine** distance; rank; paginate.
4. If too few, expand ring by ring; if too many (dense area), cap and rank first.

## Tracking moving objects

```
Device → gateway (batched, adaptive frequency) → in-memory geo index (cells → objects, TTL)
                                     ↘ Kafka → history/analytics store
Consumers subscribe to cells or objects (pub/sub) for live tracking on maps.
```

- **Sharding**: by cell range/region so a query hits one or few shards; hot cities are split finer.
- **Update path**: object moves between cells ⇒ remove from old, add to new; TTL removes stale objects.
- **Adaptive frequency**: fast when on a trip or moving, slow when idle; delta encoding; batching.
- **Smoothing**: map-matching to roads, dead reckoning, filtering GPS noise.
- **Push to viewers**: subscribe rider to driver's channel; downsample to 1–2 s.
- **Geofencing**: index polygons (cells covering); on each update test entry/exit.

## Ranking by ETA, not distance

Road network, one-ways, rivers and traffic make straight-line distance misleading. Two-stage: fetch
candidates by cell (cheap), rank top N by routing-engine ETA (expensive).

## Sharding and scale considerations

- Regional isolation (per city) contains failures and load.
- Replicate hot shards; consider write-through of location to the owning shard only.
- Loss of an in-memory shard is recoverable: clients re-report within seconds.
- Privacy: coarsen locations for others (fuzzing), short retention, access control.

## Pitfalls

- Storing every ping in the transactional database.
- Ignoring boundary cells in geohash queries.
- Uniform cell size across dense cities and empty regions.
- Using lat/lng bounding boxes near the date line or poles.
- Ranking purely by straight-line distance.

## Interview questions (with answers)

**Q1. Why check neighbouring geohash cells?** Points just across a cell boundary can be closer than points in your own cell, and adjacent cells don't necessarily share prefixes.

**Q2. Store driver locations for 1M drivers updating every 4 s?** ~250k writes/s ⇒ in-memory grid/Redis GEO sharded by cell with TTL; history to Kafka/object storage; no disk DB on the hot path.

**Q3. Quadtree vs geohash?** Quadtree adapts to density (dense cities get finer cells) but is an in-memory structure; geohash is simple and works in any ordered store but has fixed cell sizes and edge effects.

**Q4. How do you notify a rider of nearby drivers on a map?** Subscribe the client to the cells in their viewport via pub/sub; push deltas at low frequency.

## Last-minute revision

Cells (geohash/S2/H3) ⇒ candidates ⇒ exact distance ⇒ ETA ranking. Static ⇒ durable index; moving ⇒ **in-memory + TTL**, history via stream. Shard by region; expand rings; handle boundaries and density.

Related: [Uber](../11-Location-Based-Services/Uber/README.md) · [Nearby Places](../11-Location-Based-Services/Nearby-Places-Bonus/README.md) · [Google Maps](../11-Location-Based-Services/Google-Maps/README.md)
