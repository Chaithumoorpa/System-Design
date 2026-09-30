# Relational Databases (PostgreSQL / MySQL)

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Database Design](../03-Concept-Deep-Dives/04-database-design.md) · 🏠 [Technology Deep Dives](README.md) · ➡️ Next: [Redis](03-redis.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

## Strengths

ACID transactions, joins, rich queries, mature tooling, strong constraints. The right default for most systems, and comfortably scales to large workloads with the techniques below.

## Scaling playbook (in order)

1. **Fix queries and indexes** (`EXPLAIN ANALYZE`; avoid N+1, full scans, unbounded `OFFSET`).
2. **Connection pooling** (PgBouncer, ProxySQL); connections are expensive.
3. **Cache** hot reads.
4. **Read replicas** for read scaling (mind replication lag).
5. **Vertical scaling** and better hardware.
6. **Partition large tables** (by time or key) within one instance: faster pruning, easier retention.
7. **Functional split** into separate databases per domain.
8. **Shard** horizontally (application-level, Vitess, Citus) as a last step.

## Internals worth knowing

- **MVCC**: readers do not block writers; old row versions retained until vacuumed (Postgres `VACUUM`, InnoDB undo logs).
- **WAL/redo log**: durability and replication source.
- **InnoDB** clustered index: table stored in primary key order, so secondary indexes point to the primary key. Postgres uses heap tables with separate indexes.
- **Locking**: row locks (`FOR UPDATE`, `SKIP LOCKED` for queue-like workloads), advisory locks, deadlocks (consistent lock ordering).
- **Query planner** relies on statistics; stale stats produce bad plans.

## Practical patterns

- **Optimistic locking** via version column.
- **Atomic conditional update** for inventory: `UPDATE items SET qty = qty - 1 WHERE id = ? AND qty > 0`.
- **Unique constraints** for idempotency and dedupe.
- **Outbox table** for reliable event publishing.
- **Soft deletes** with partial indexes; archival for old data.
- **JSONB** columns for semi-structured data with GIN indexes.
- **Postgres as a queue**: `SELECT ... FOR UPDATE SKIP LOCKED` works at modest scale.

## Schema migrations at scale

Expand-and-contract: add nullable column, deploy code writing both, backfill in batches, switch reads, drop old. Avoid long table locks; use online schema change tools.

## When not to use

Massive write throughput with simple key access, need for automatic multi-region writes, unstructured/wide time-series at huge scale, full-text at scale (use a search engine).

## Interview questions

1. A 2 TB orders table is slow. What do you do, in order?
2. How does `SKIP LOCKED` enable a job queue in SQL?
3. Explain MVCC and why long transactions hurt.
4. Design a safe zero-downtime column rename.

---

## 🔗 Used in these case studies

- [Ticket Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md)
- [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md)
- [Job Scheduler](../17-Asynchronous-Systems/Job-Scheduler/README.md)
