# Must-Know Trade-offs

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Technologies](02-technologies.md) · 🏠 [Must-Know Topics](README.md) · ➡️ Next: [Data Structures](04-data-structures.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Every design decision gives something up. Strong answers name the trade-off out loud:
**"X because Y, at the cost of Z."** This chapter is a catalogue of the trade-offs that appear most often.

## The template

> "I'll choose **A** over **B** because our requirement is **R**. The cost is **C**, which we accept because **reason**. If **condition** changes, I would revisit."

## Core trade-off pairs

| Trade-off | Option A | Option B | Decide by |
|---|---|---|---|
| Consistency vs availability (CAP) | Refuse/lag to stay consistent | Answer possibly stale | Cost of a wrong answer vs an error (money vs likes) |
| Consistency vs latency (PACELC) | Sync replication, quorum | Async replication | Tolerance for stale reads and data loss on failover |
| Latency vs throughput | Small batches, immediate | Big batches, delayed | Interactive vs bulk workload |
| Read cost vs write cost | Precompute on write (fan-out on write) | Compute on read | Read:write ratio, skew (celebrities) |
| Space vs time | Precompute, index, denormalise | Compute, normalise | Memory/storage budget |
| Normalisation vs denormalisation | Integrity, simple writes | Fast reads, complex writes | Access pattern frequency |
| SQL vs NoSQL | Transactions, joins | Scale, flexible access | Need for ACID and query flexibility |
| Push vs pull | Server pushes (low latency) | Client polls (simple, robust) | Number of clients, freshness need |
| Sync vs async | Simple, immediate result | Decoupled, resilient, eventual | Whether caller needs the result now |
| Monolith vs microservices | Simplicity, one deploy | Independent scaling/teams | Team size and domain boundaries |
| Build vs buy | Control, fit | Speed, maintenance | Core differentiator or commodity? |
| Strong durability vs speed | fsync each write, sync replicas | Buffered writes | Data-loss tolerance |
| Accuracy vs cost | Exact counts | Approximate (HLL, sketches) | Business need for exactness |
| Simplicity vs flexibility | Hard-coded, fewer parts | Generic, configurable | Rate of change expected |
| Freshness vs load | Short TTL, frequent refresh | Long TTL | Staleness tolerance |
| Availability vs cost | Multi-AZ/region active-active | Single region | RTO/RPO, revenue impact |
| Ordering vs parallelism | Single partition/consumer | Many partitions | Whether order matters per entity |
| Security vs usability | Strict auth, short tokens | Convenience | Threat model |

## Worked examples

### Example 1: news feed fan-out
Fan-out on write gives O(1) reads, but a celebrity post causes millions of writes. Fan-out on read is
cheap to write, slow to read. **Hybrid**: push for normal users, pull for celebrities. Cost: two code
paths and merge logic.

### Example 2: cache TTL
Long TTL means fewer DB hits and more staleness; short TTL means fresher data and more load. For a
product price shown on a listing, 60 s staleness is acceptable; for checkout, read the source.

### Example 3: rate limiter store
Central Redis: accurate, one hop, single dependency. Local counters: fast, approximate.
Hybrid: local allowance replenished from Redis in chunks.

### Example 4: message ordering
Global order needs a single writer and caps throughput; per-key order via partitioning gives
parallelism while preserving what actually matters.

## How to talk about trade-offs in an interview

1. **State the requirement that decides it** ("we can tolerate a few seconds of staleness").
2. **Name what you give up** (complexity, cost, consistency).
3. **Give a trigger to revisit** ("if we need cross-region writes, I would move to X").
4. **Do not pretend a choice is free.**

## Anti-patterns

- "We'll use X" with no alternative considered.
- Listing pros only.
- Choosing the consistent option for everything (or the available one for everything).
- Trading away durability silently (async writes to a cache used as the only copy).

## Interview questions (with answers)

**Q1. Why might you choose eventual consistency for a like counter but not for account balances?**
A stale count harms no one and scales cheaply; a stale balance can permit overdrafts. Correctness cost differs.

**Q2. Push vs pull for notifications to mobile apps?**
Push (APNs/FCM) for timeliness while the app is closed; pull/sync on open as the fallback and source of truth.

**Q3. When is denormalisation a mistake?**
When data changes frequently and consistency across copies is hard to maintain, or reads aren't actually the bottleneck.

## Last-minute revision

Say **"because / at the cost of / revisit if"** for every major choice. Know the top ten pairs above cold.
