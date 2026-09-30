# Design Typeahead / Autocomplete

**Prompt:** As a user types, suggest the most relevant completions within milliseconds.

## Requirements

- Functional: top ~5-10 suggestions per prefix, ranked by popularity (and optionally personalisation, freshness), multilingual.
- Non-functional: p99 < 50-100 ms end to end, extremely read-heavy, suggestions can lag real-time popularity by minutes to hours, high availability.

## Estimates

- 500M searches/day, each ~10 keystrokes -> ~5B suggestion requests/day = ~60k/s avg, peak 150-200k/s (mitigate with client debounce and caching). Distinct queries in the index: tens to hundreds of millions; top prefixes fit in memory.

## Design

```
Client (debounce 100-200 ms, local cache) -> CDN/edge cache -> Suggestion service (in-memory tries) 
Offline: search logs -> Kafka -> aggregation (frequency per query) -> build trie snapshots -> distribute to servers
Real-time trending layer: streaming counts -> small "fresh" index merged at serve time
```

## Data structure

**Trie** where each node stores the **top-k completions** for its prefix (precomputed), so lookup is O(length of prefix) with no subtree traversal. Memory-optimised via compressed (radix) trie, limiting to prefixes with enough traffic, and storing query IDs rather than strings.

Alternative: key-value map `prefix -> top-k list` in Redis; simple, larger footprint, easy sharding.

## Building and updating

- Aggregate query frequencies with time-decay (recent counts weigh more) in batch (hourly/daily).
- Build a new trie snapshot offline, ship to servers, atomically swap (blue-green style). Avoid in-place updates on the serving path.
- Streaming layer for breaking news: small fresh trie/KV overlaid at query time.
- Filter offensive, illegal or low-quality queries; honour removal requests quickly (blocklist applied at serve time).

## Scaling

- Shard by first characters or prefix hash; replicate for availability; each shard's data fits in memory.
- Cache hot prefixes at CDN/edge with short TTL (popular short prefixes like "a", "am" get huge hit rates).
- Client optimisations: debounce, cancel stale requests, cache previous responses, prefetch.

## Ranking

Score = popularity x recency decay + personalisation boost (recent user searches) + language/location relevance. Personal suggestions from a per-user store merged with global.

## Follow-ups

- Typo tolerance? (Edit-distance candidate generation, or phonetic matching.)
- Multi-language / non-space languages? (Tokenisation, per-language tries.)
- How to measure quality? (CTR on suggestions, keystrokes saved, latency.)
