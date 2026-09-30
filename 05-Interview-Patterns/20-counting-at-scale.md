# Pattern: Counting at Scale

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Advanced

⬅️ Previous: [Generating Unique IDs](19-generating-unique-ids.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Answering Framework](../06-Interview-Tips/01-answering-framework.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Count things (likes, views, clicks, unique visitors, rate-limit tokens, inventory) at
millions of events per second without hot rows, double counting, or unaffordable storage.

## Recognise it when

Like/view counters, ad click aggregation, analytics dashboards, unique visitors, trending, leaderboards,
rate limiters, metrics.

## Choose the right kind of count

| Kind | Example | Technique |
|---|---|---|
| **Exact, low-volume** | Inventory, balances | DB row with atomic update / ledger |
| **Exact, high-volume** | Total likes on a viral post | Sharded counters + async aggregation; dedupe set |
| **Approximate frequency** | Top-K searches | Count-Min Sketch, Space-Saving |
| **Approximate distinct** | Unique visitors | HyperLogLog |
| **Windowed** | Clicks per minute | Stream processing with event-time windows |
| **Rate** | Requests/sec per key | Token/leaky bucket, sliding window counter |
| **Ranking** | Leaderboard | Sorted set / ordered store |

## Techniques

### 1. Sharded (striped) counters
```
INCR likes:{post}:{rand(0..15)}       // write to a random shard
total = SUM(likes:{post}:0..15)       // read (or aggregate periodically)
```
Removes single-row contention. Trade-off: reads cost N lookups or cache the sum.

### 2. Buffer and flush
Accumulate in memory/Redis and write batches to the database every few seconds. Loss window on crash
(mitigate with a durable log). Batching turns 100k writes/s into hundreds.

### 3. Event streaming + aggregation
Emit `like`/`click` events to Kafka; stream job (Flink) aggregates by key and window; sink to a
store. Enables late data handling, replay and exactness. See [Flink](../04-Technology-Deep-Dives/10-flink.md).

### 4. Deduplication (idempotent counting)
Counting "unique" or preventing double likes: unique key `(user, item)` in a KV/DB, Bloom filter as a
fast pre-check, or event IDs in stream state with TTL. Count = number of distinct keys.

### 5. Probabilistic structures
| | Answer | Size | Error |
|---|---|---|---|
| HyperLogLog | Distinct count | ~12 KB | ~0.8% |
| Count-Min Sketch | Frequency of any key | Fixed table | Overestimates ≤ εN |
| Bloom filter | Seen before? | ~10 bits/item at 1% FP | False positives |
| Space-Saving | Top-K heavy hitters | O(K/ε) | Bounded |

### 6. Rollups and tiered storage
Minute → hour → day aggregates; keep raw events short-term, rollups long-term.

### 7. Lambda-style correction
Fast approximate streaming path + periodic exact batch recompute that overwrites.

## Accuracy vs freshness vs cost

Ask what the product needs: a like count can be a few seconds stale and ±1 off; ad billing must be
exact and auditable (dedupe, reconciliation, immutable event log). State this before choosing.

## Worked example: like counter

1. `POST /like` writes `(user, post)` with a unique constraint (idempotent).
2. Emit `LikeAdded` to Kafka.
3. Redis sharded counters updated for immediate display; stream job persists exact totals per post to DB.
4. UI reads cached total; personalised "liked by you" from the `(user, post)` set/Bloom filter.
See [Likes Counting System](../16-Counting-and-Ranking-Systems/Likes-Counting-System/README.md).

## Pitfalls

- `UPDATE … SET n = n + 1` on a hot row.
- Counting duplicates from retries/at-least-once delivery.
- HyperLogLog for anything needing exactness or deletes (it can't remove).
- Averaging percentiles or ratios instead of merging sketches/sums.
- Time zone/window boundary bugs; late events dropped silently.

## Interview questions (with answers)

**Q1. Count unique daily visitors for 1B page views.** HyperLogLog per page per day (12 KB each), mergeable across servers/days; exact only if required using dedupe sets and heavier storage.

**Q2. How to keep exact like counts with 100k likes/s on one post?** Idempotent like records (unique constraint) + sharded counters or stream aggregation, persisted periodically; display slightly stale totals.

**Q3. Top 10 trending hashtags in the last hour?** Partition by tag, per-minute buckets, Count-Min/heap for candidates, merge partitions into global top-K, cache results.

**Q4. Why is exactly-once counting hard?** Retries and duplicates from at-least-once pipelines; solve with idempotency keys/dedupe in the aggregator or transactional sinks.

## Last-minute revision

Pick exact vs approximate; shard hot counters; buffer/stream; dedupe with unique keys/Bloom; HLL for distinct, CMS for frequency; rollups; reconcile with batch.

Related: [Handling Hot Keys](03-handling-hot-keys.md) · [Top K](../16-Counting-and-Ranking-Systems/Top-K/README.md) · [Ad Click Aggregator](../12-Search-and-Aggregation-Systems/Ad-Click-Aggregator/README.md)
