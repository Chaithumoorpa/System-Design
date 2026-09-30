# Pattern: Search and Typeahead

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Scheduling Delayed and Recurring Jobs](16-scheduling-delayed-and-recurring-jobs.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Finding and Tracking Locations](18-finding-and-tracking-locations.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Users need to find things by text ("red running shoes"), with typo tolerance, relevance
ranking, filters, and instant suggestions as they type.

## Recognise it when

E-commerce search, message/email search, log search, maps search, autocomplete, "search bar" anywhere.

## Full-text search building blocks

### Inverted index
Map **term → posting list** (document ids, positions, frequencies).

```
"running" → [doc3, doc9, doc17]     "shoes" → [doc3, doc4, doc17]
query "running shoes" → intersect lists → rank → top-k
```

**Analysis pipeline** (at index and query time): tokenise → lowercase → remove stop words → stem/lemmatise → synonyms → n-grams (for prefix/partial).

### Ranking
- **BM25** (successor of TF-IDF): term frequency, inverse document frequency, length normalisation.
- Blend business signals: popularity, recency, price, availability, personalisation; later a learning-to-rank model.
- Typo tolerance: fuzzy queries (edit distance), phonetic matching, "did you mean".
- Facets/filters: keyword fields with doc values; aggregations for counts.

### Distributed search (Elasticsearch/OpenSearch/Solr)
- Index split into **shards** with replicas; a query fans out to all shards; each returns top-k; coordinator merges.
- Near-real-time (refresh ~1 s); segments are immutable and merged in the background.
- Deep pagination is costly (`search_after`/PIT instead of large `from`).
- Shard sizing: tens of GB per shard; time-based indices for logs.
- See [Elasticsearch](../04-Technology-Deep-Dives/06-elasticsearch.md).

## Pipeline architecture

```
Source DB (truth) → CDC/events → Kafka → indexer (idempotent, versioned) → search cluster
Client → Search API → query rewrite (spell, synonyms, filters) → cluster → rank/re-rank → results
```
The index is **derived**: rebuildable via reindex + alias swap. See [Keeping Data in Sync](13-keeping-data-in-sync.md).

## Typeahead / autocomplete

**Requirements:** <100 ms end to end, extremely high QPS (keystrokes), suggestions from popular queries.

| Approach | Notes |
|---|---|
| **Trie with precomputed top-k per node** | O(prefix length) lookup; in-memory; rebuilt offline from query logs |
| Prefix → top-k in KV store (Redis/DynamoDB) | Simple, shardable; larger footprint |
| Elasticsearch completion suggester / edge n-grams | Good for catalogue-based suggestions |
| Hybrid | Global popular queries + personal history + fresh trending overlay |

Serving tips: client debounce (100–200 ms), cancel stale requests, cache responses for short prefixes
at CDN/edge, replicate snapshots to identical servers, swap versions atomically. Filtering: blocklist,
minimum frequency thresholds (privacy). Details: [Search Autocomplete](../12-Search-and-Aggregation-Systems/Search-Autocomplete/README.md).

## Relevance vs speed vs freshness

| Lever | Effect |
|---|---|
| More shards/replicas | Latency/throughput up, cost up |
| Precomputed popularity signals | Cheaper ranking |
| Shorter refresh interval | Fresher results, more indexing load |
| Result caching (popular queries) | Fast, staleness |
| Two-stage ranking (cheap recall → expensive rerank) | Quality without scanning everything |

## Special search types

- **Geo search**: combine geo filter with text; see [Finding and Tracking Locations](18-finding-and-tracking-locations.md).
- **Semantic/vector search**: embeddings + approximate nearest neighbour (HNSW/IVF); combine with keyword search (hybrid) for best relevance.
- **Log/observability search**: time-partitioned indices, hot/warm/cold tiers.
- **Personal/private search** (mail, chat): per-user index/partitioning and access control filters.

## Pitfalls

- Using the search cluster as the system of record.
- Indexing everything (mapping explosions, cost).
- Deep pagination; unbounded aggregations.
- Ignoring analysis differences between index and query time.
- No plan for reindexing (schema/analyzer changes).

## Interview questions (with answers)

**Q1. How would you build product search with typo tolerance and filters?** Elasticsearch index fed via CDC; analyzers with stemming/synonyms; fuzzy matching; keyword fields for filters/facets; BM25 + popularity signals; alias-swap for reindexing.

**Q2. Why is a trie with top-k at each node fast?** Lookup is O(prefix length) and returns precomputed results; no subtree traversal at query time.

**Q3. How do you keep suggestions fresh?** Offline aggregation with time decay to build snapshots plus a streaming layer for trending queries merged at serve time.

**Q4. Why is deep pagination a problem in distributed search?** Each shard must return `from + size` results to the coordinator to sort globally; cost grows with depth. Use `search_after`.

## Last-minute revision

Inverted index + analyzers + BM25; sharded scatter-gather; index is derived (CDC + reindex); typeahead = precomputed top-k (trie/KV) + edge cache + debounce; hybrid keyword+vector for semantic.

Related: [Search and geospatial notes](../_Reference/search-and-geospatial.md) · [Google Search](../12-Search-and-Aggregation-Systems/Google-Search/README.md) · [Search Autocomplete](../12-Search-and-Aggregation-Systems/Search-Autocomplete/README.md)
