# Search and Geospatial Indexing

## Full-text search

**Inverted index**: maps each term to the list of documents (and positions) containing it.

Pipeline: tokenise, lowercase, remove stop words, stem/lemmatise, index. Query goes through the same analysis, then posting lists are intersected/merged and **ranked** (TF-IDF, BM25, plus signals like popularity, recency, personalisation).

Architecture (Elasticsearch/OpenSearch/Solr):
- Index split into **shards** (each a Lucene index), each with replicas.
- Query fans out to all shards, each returns top-k, coordinator merges.
- Near-real-time: new docs become searchable after a refresh interval (~1 s).
- **Search is a derived view**: source of truth stays in the primary DB; feed the index via CDC or events, and be able to reindex from scratch.
- Do not use the search engine as the primary store for transactional data.

Features to know: fuzzy matching (edit distance), prefix/autocomplete (edge n-grams or tries), facets/aggregations, synonyms, highlighting, pagination limits (deep paging is expensive; use search-after).

## Typeahead structures

- **Trie** with top-k completions cached at each node.
- Precompute popular queries offline; serve from memory/cache; update periodically. See [typeahead](../05-case-studies/12-typeahead.md).

## Geospatial indexing

Problem: "find things within r km of (lat, lon)" quickly.

| Structure | Idea | Notes |
|---|---|---|
| **Geohash** | Interleave lat/lon bits into a string; shared prefix means nearby | Simple, works with any sorted store; edge effects, so query neighbouring cells |
| **Quadtree** | Recursively split map into 4 cells until each holds few points | Adapts to density; in-memory service |
| **S2 (Google)** | Sphere mapped to hierarchical cells on a Hilbert curve | Good coverage, used in production maps |
| **H3 (Uber)** | Hexagonal hierarchical grid | Uniform neighbour distance, good for surge pricing |
| **R-tree** | Bounding boxes in a tree | Used inside PostGIS |

Query flow: compute the cells covering the search circle, fetch points from those cells, filter by exact distance, sort. For moving objects (drivers) keep positions in an in-memory grid/Redis geo index with TTLs, rather than writing every update to a disk database.

## Interview questions

1. How would you keep an Elasticsearch index in sync with a SQL database?
2. Why does geohash need to check neighbouring cells?
3. Why is deep pagination slow in a sharded search index?
4. Design storage for driver locations updating every 4 seconds for 1M drivers.
