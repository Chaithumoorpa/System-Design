# Pattern: Keeping Data in Sync

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Coordinating Transactions Across Services](12-coordinating-transactions-across-services.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Preventing Double Booking](14-preventing-double-booking.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** The same information lives in several places: primary DB, cache, search index,
analytics warehouse, another service's database. How do you keep the copies consistent without
distributed transactions?

## Recognise it when

- "Update search when a product changes", "keep cache fresh", "replicate to the data warehouse", "microservice needs a copy of user data".
- Any derived view: timelines, materialised views, denormalised counts.

## The wrong way: dual writes

```
app: write DB;  write Elasticsearch;  write cache
```
If the second write fails (or the process crashes between), copies diverge silently. Ordering races
also produce stale overwrites. Avoid dual writes from application code.

## Right ways

### 1. Change Data Capture (CDC) from the source's log
Read the database's WAL/binlog (Debezium, DMS, native logical replication) and publish changes to a
log (Kafka). Consumers update caches, search indexes, warehouses, other services.
- Source of truth = the primary DB; the log is ordered per key.
- Consumers are idempotent (upsert by primary key + version).
- Can **reindex from scratch** by replaying/snapshotting.

### 2. Transactional outbox
In the same local transaction as the business change, insert an event row into an `outbox` table. A
relay/CDC publishes it, at-least-once. Guarantees "if the state changed, the event will be published".

```sql
BEGIN;
  UPDATE products SET price = 999 WHERE id = 7;
  INSERT INTO outbox(id, aggregate_id, type, payload) VALUES (gen_random_uuid(), 7, 'PriceChanged', '{...}');
COMMIT;
```

### 3. Event-driven propagation (events as the source)
Services publish domain events; others build local read models (CQRS). See
[CQRS notes](../_Reference/cqrs-event-sourcing.md).

### 4. Cache invalidation strategies
- Delete-on-write + TTL safety net (simple).
- CDC-driven invalidation (covers all writers).
- Versioned keys (`product:7:v42`) to avoid races.
- Write-through when a single writer owns the cache.

### 5. Periodic reconciliation
A background job compares source and copy (checksums, counts, sampled rows) and repairs drift.
Essential safety net even with CDC.

## Handling ordering, duplicates and lag

| Issue | Handling |
|---|---|
| Duplicate events | Idempotent consumers; upsert by key |
| Out-of-order events | Version/sequence numbers; ignore stale (`WHERE version < new`) |
| Consumer lag | Monitor lag; users may see stale data; show "updating…" where needed |
| Deletes | Tombstones; propagate deletes explicitly |
| Schema changes | Versioned schemas (Avro/Protobuf + registry), backward-compatible evolution |
| Initial load / backfill | Snapshot + stream from an offset without gaps (Debezium snapshotting) |
| Poison message | DLQ, alert, fix and replay |

## Consistency expectations

Copies are **eventually consistent**. Decide what "fresh enough" means per view (search: seconds;
warehouse: minutes-hours; cache: TTL). For read-your-writes on the acting user, return the result
directly or read from the source briefly after a write.

## Worked example: product search

```
Postgres (truth) → Debezium → Kafka → indexer (upsert by product_id + version) → Elasticsearch
                                     ↘ cache invalidator → Redis
```
Reindex: create new index, replay a snapshot, swap alias.

## Pitfalls

- Treating the search index/cache as authoritative.
- Not versioning events ⇒ stale overwrites.
- Publishing before commit (event for a rolled-back change).
- CDC consumers that are not idempotent.
- No reconciliation job.

## Interview questions (with answers)

**Q1. Why is "write DB then publish event" unsafe?** A crash between the two loses the event (or publishing first exposes an event for a change that then fails). Use the outbox or CDC.

**Q2. How do you keep Elasticsearch in sync with Postgres?** CDC into Kafka, idempotent indexer using document version, alias-swap reindexing, periodic reconciliation.

**Q3. How do you avoid a stale cache being repopulated after an invalidation?** TTL as backstop, versioned values, or delayed double-delete; better: CDC-driven invalidation with versions.

## Last-minute revision

No dual writes. **Outbox or CDC → log → idempotent, version-aware consumers.** Reconcile periodically; expect eventual consistency.

Related: [Coordinating Transactions](12-coordinating-transactions-across-services.md) · [Kafka](../04-Technology-Deep-Dives/07-kafka.md) · [Elasticsearch](../04-Technology-Deep-Dives/06-elasticsearch.md)
