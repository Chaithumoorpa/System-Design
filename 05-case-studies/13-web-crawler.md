# Design a Web Crawler

**Prompt:** Crawl the web at scale to feed a search index, being polite and efficient.

## Requirements

- Functional: start from seed URLs, fetch pages, extract links, store content, re-crawl to keep fresh.
- Non-functional: scalable (billions of pages), polite (robots.txt, per-host rate), robust to bad HTML/traps, extensible (new content types), deduplicating.

## Estimates

- 1B pages/month = ~400 pages/s. Average page 100 KB compressed -> 100 TB/month raw. Fetch bandwidth: ~40 MB/s sustained (scale by 5-10x for peak, retries and re-crawl).

## Architecture

```
Seed URLs -> URL Frontier (priority + politeness queues) -> Fetcher workers (DNS cache, HTTP)
   -> Content store (object storage) + parser -> extracted links -> URL filter/normalise/dedupe (Bloom filter + DB)
   -> back to Frontier
   -> content dedupe (hash/simhash) -> indexer pipeline
```

## Components

- **URL frontier**: the heart. Two-tier queues: front queues by **priority** (importance, change frequency), back queues **one per host** to enforce politeness (min delay between requests to same host, respecting `Crawl-delay`). A scheduler maps ready hosts to fetcher workers.
- **Fetchers**: async I/O, many concurrent connections, timeouts, retries with backoff, honour robots.txt (cached per host), user-agent identification.
- **DNS resolver cache**: DNS lookups are a bottleneck; local caching and batching.
- **Parser**: extract text, links, metadata; handle malformed HTML; JavaScript-rendered pages need a headless browser pool (expensive, used selectively).
- **Normalisation**: canonicalise URLs (lowercase host, remove fragments, sort params, resolve relative links), respect `rel=canonical`.

## Deep dives

- **URL dedupe**: billions of URLs; use a **Bloom filter** in memory in front of a persistent store (false positives skip a few new URLs; acceptable), or a sharded KV of URL hash.
- **Content dedupe**: exact via content hash; near-duplicate via SimHash/MinHash.
- **Spider traps** (infinite calendars, session IDs in URLs): depth limits, per-host page caps, URL pattern heuristics.
- **Freshness / re-crawl**: adaptive intervals from observed change rate; prioritise high PageRank/news sites; use `If-Modified-Since`/ETag; sitemaps.
- **Distribution**: partition the frontier by host hash so each host is handled by one crawler node (natural politeness); consistent hashing for node changes.
- **Fault tolerance**: frontier state checkpointed; workers are stateless; at-least-once processing with dedupe.
- **Storage**: raw pages in object storage keyed by URL hash; metadata (last crawled, checksum, status) in a wide-column store.
- **Ethics and limits**: robots.txt, rate limits, legal constraints, avoid overloading small sites.

## Follow-ups

- How to crawl 10x faster without violating politeness? (More hosts in parallel, not more per host.)
- Prioritise fresh news? (Dedicated priority queue and frequent re-crawl of feeds.)
- Detect and handle duplicate content across mirrors?
