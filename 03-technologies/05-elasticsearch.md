# Elasticsearch / OpenSearch

Distributed search and analytics engine built on Lucene.

## Concepts

- **Index** = logical collection; split into **primary shards**, each with **replicas**.
- Documents are JSON; **mappings** define field types (`text` analysed for full-text, `keyword` exact for filters/aggregations).
- **Analyzers**: tokenizer + filters (lowercase, stemming, synonyms, n-grams).
- **Segments** are immutable; writes go to a buffer, `refresh` (default 1 s) makes them searchable, merges combine segments, deletes are markers.
- **Translog** provides durability between flushes.

## Query execution

Coordinator node fans out to relevant shards; each returns top-k with scores; coordinator merges. Filters (`bool`/`filter`) are cacheable and unscored; queries score by BM25. Aggregations power facets and analytics.

## Sizing and scaling

- Shard size in the tens of GB is a common target; too many small shards waste overhead, too few limit parallelism. Shard count is fixed at index creation (reindex or split to change).
- Time-based indices (daily/weekly) for logs, with lifecycle management: hot, warm, cold, delete.
- Replicas add read capacity and availability.
- Separate master, data, and coordinating roles at scale.

## Common architecture

```
Primary DB --CDC/events--> Queue --> Indexer --> Elasticsearch <-- Search API
```

- Source of truth stays in the DB; the index is rebuildable.
- Handle out-of-order and duplicate events with document versions (external versioning).
- Use aliases to reindex with zero downtime: build the new index, swap the alias.

## Pitfalls

- Not a transactional database: eventual visibility, no multi-doc transactions.
- Deep pagination is costly: use `search_after` or scroll/PIT.
- Mapping explosions from dynamic fields; heavy aggregations on high-cardinality fields cost memory.
- Split-brain avoidance needs proper master quorum configuration.

## Interview questions

1. How would you support product search with typo tolerance, filters, and popularity ranking?
2. How do you reindex a live index without downtime?
3. Why is the data not immediately searchable after write, and is that a problem?

---

## 🔗 Used in these case studies

- [Nearby Places](../05-case-studies/Location-Based-Services/NearbyPlaces/README.md)
- [Metrics and Logging Pipeline](../05-case-studies/Distributed-Infrastructure/MetricsLoggingPipeline/README.md)
