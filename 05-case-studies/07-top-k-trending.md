# Design Trending Topics / Top-K Service

**Prompt:** Show the top K most popular hashtags/searches/videos in the last hour/day, near real time.

## Requirements

- Functional: top K (e.g. 10-100) items over sliding windows (1 min, 1 h, 24 h), per region or category optional.
- Non-functional: freshness within ~1 minute, 100k+ events/s, approximate answers acceptable, low read latency.

## Estimates

- 200k events/s (views, searches). Distinct keys: hundreds of millions. Exact counts per key per window is heavy; approximations suffice.

## Design

```
Events -> Kafka (partitioned by key) -> Stream processors (Flink) -> windowed partial counts
      -> merge partial top-K -> Serving store (Redis / cache) -> Top-K API
Batch path: raw events -> object store -> Spark -> corrected daily/hourly aggregates
```

## Approaches

| Approach | Notes |
|---|---|
| Exact counts in a sorted set (Redis ZINCRBY) | Simple for moderate scale; hot keys and memory limit |
| **Count-Min Sketch + min-heap of size K** | Approximate counts in fixed memory; heap tracks candidates. Sketch overestimates slightly |
| Space-Saving / Misra-Gries | Deterministic heavy-hitter algorithms, bounded error |
| Map-reduce style | Partition by key, count locally, merge top-K per partition into global top-K |

## Deep dives

- **Windowing**: tumbling windows (per minute buckets) summed over a sliding range; keep 60 one-minute buckets for an hour view, subtract expiring bucket. Use event time with watermarks to handle late events.
- **Two-level aggregation**: each partition computes local top-K (K x safety margin), a merger combines. Keys are hash-partitioned so one key lives in one partition, making local counts exact per key.
- **Hot keys** (viral topic): pre-aggregate on producers or in the first stage before shuffling; use key-splitting then merge.
- **Serving**: write final top-K per window to Redis; API reads a small list; cache at CDN with a few seconds TTL.
- **Trending vs popular**: compare current rate to a historical baseline (e.g. z-score or ratio) to surface *rising* items rather than perennially large ones.
- **Spam and manipulation**: dedupe per user per key, bot filtering, anomaly detection.
- **Accuracy vs cost**: exact counts via batch for history, approximate streaming for freshness (lambda-style).

## Follow-ups

- Top-K per country? (Add region to the key; more partitions.)
- Support arbitrary time ranges? (Store minute-level rollups, merge on demand; sketches are mergeable.)
- What is the error bound of a Count-Min sketch with width w and depth d?
