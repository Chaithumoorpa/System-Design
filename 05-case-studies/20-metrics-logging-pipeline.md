# Design a Metrics and Logging Pipeline (Datadog / ELK style)

**Prompt:** Collect metrics and logs from 100k servers, store them, and support dashboards, search and alerting.

## Requirements

- Functional: ingest metrics (counters, gauges, histograms) and logs, query with filters and aggregation, dashboards, alert rules, retention tiers.
- Non-functional: very high write throughput, near-real-time (<30 s to visible), reads are recent-biased, durable enough (some loss tolerable for metrics), cost-efficient long retention.

## Estimates

- Metrics: 100k hosts x 200 series x 1 point/10 s = 2M points/s. At ~16 bytes/point raw: ~30 MB/s, ~2.7 TB/day before compression (time-series compression gets 10x).
- Logs: 100k hosts x 50 lines/s x 200 bytes = 1 GB/s = ~86 TB/day. Logs dominate cost: sample, filter and tier aggressively.

## Architecture

```
Agents on hosts (buffer, batch, compress) -> Regional collectors/LB -> Kafka (partition by tenant/host)
   Metrics path: Stream aggregator (downsample/rollup) -> Time-series DB (TSDB)
   Logs path:    Parser/enricher -> Search index (hot) + Object storage (cold, Parquet)
Query service -> TSDB / index / cold store    Alert engine (evaluates rules on stream/queries) -> notifications
```

## Deep dives

- **Agent behaviour**: local buffering on disk during outages, batching, backoff, backpressure; push (agent sends) vs pull (Prometheus scrapes): pull gives service discovery and health for free, push suits short-lived jobs and firewalls.
- **Kafka as the buffer**: absorbs bursts, decouples ingest from storage, allows replay and multiple consumers.
- **TSDB design**: series identified by metric name + tag set; store `(series_id, timestamp, value)` in time-partitioned blocks; delta-of-delta timestamp and XOR float compression (Gorilla); in-memory recent window with WAL, flushed to immutable blocks.
- **Cardinality control**: high-cardinality tags (user_id, request_id) explode the series count and memory; enforce limits and drop or aggregate offending labels.
- **Rollups and retention**: raw 10 s data for days, 1 min for weeks, 1 h for a year; downsample on the stream or by background jobs.
- **Log storage**: hot tier in inverted index (Elasticsearch/OpenSearch) for ~7 days, warm/cold in object storage in columnar format with min/max and bloom indexes for cheap scanning (Loki/ClickHouse style indexes only labels).
- **Queries**: fan out by time range and shard; cache dashboard queries; query limits and timeouts to protect the store.
- **Alerting**: evaluate rules periodically over recent data or on the stream; dedupe, group, silence, escalation; avoid flapping with `for` durations; alert engine itself must be highly available and monitored independently (who monitors the monitor).
- **Multi-tenancy**: per-tenant quotas, isolation, and cost attribution.

## Failure and cost

Ingest overload: shed low-priority data first, sample debug logs. Collector down: agent buffers. Hot shard: partition by host + metric hash. Cost: compress, tier, TTL, and limit retention per class.

## Follow-ups

- Support percentiles across hosts? (Mergeable histograms/sketches like t-digest, DDSketch, not averaging percentiles.)
- Trace ingestion and sampling strategy (head vs tail-based)?
- How do you guarantee alerts fire when the pipeline itself is lagging?
