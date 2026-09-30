# Pattern: Scheduling Delayed and Recurring Jobs

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [Handling Long-Running Tasks](15-handling-long-running-tasks.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Search and Typeahead](17-search-and-typeahead.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Run something later ("send reminder in 24 h", "expire this hold in 8 minutes", "retry in
30 s") or repeatedly ("every day at 9:00 IST"), reliably, at scale, without double-firing.

## Recognise it when

Reminders, TTL expiry of reservations, retry with delay, cron-like reports, subscription renewals,
scheduled posts, notification campaigns.

## Building blocks

| Mechanism | Fits | Notes |
|---|---|---|
| **DB table with `run_at` index** | Up to millions of jobs, moderate precision | Poll `WHERE run_at <= now AND status='SCHEDULED'`, claim with `SKIP LOCKED` |
| **Redis sorted set** (score = due time) | Fast, simple | Poll `ZRANGEBYSCORE`; move to working list atomically (Lua); persistence caveats |
| **Queue with delay** (SQS ≤15 min, RabbitMQ TTL+DLX, Kafka + delay topics) | Short delays | Long delays need re-queue loops |
| **Timing wheel** (in memory) | Millions of short timers | Hierarchical wheels; combine with DB for durability |
| **Workflow engine timers** (Temporal) | Long, durable timers | Days/months timers with state |
| **OS cron / Kubernetes CronJob** | Few, coarse jobs | Not a distributed multi-tenant scheduler |
| **Cloud schedulers** (EventBridge Scheduler, Cloud Scheduler) | Managed | Limits per account |

## Architecture (multi-tenant scheduler)

```
API → Job store (definition, schedule, next_run_at)
Scheduler nodes (own hash slots) → find due jobs → claim → enqueue task
Workers ← queue → execute (lease + heartbeat) → report → compute next_run_at
Reaper → requeue expired leases
```
Full design: [Job Scheduler](../17-Asynchronous-Systems/Job-Scheduler/README.md).

## Exactly one trigger per tick

1. **Atomic claim**: `UPDATE … SET status='CLAIMED' WHERE id=? AND version=?` or `SKIP LOCKED`.
2. **Unique key `(job_id, scheduled_time)`** on executions makes creation idempotent.
3. **Partition ownership** (hash slots) with leader election/leases so two schedulers don't own one job; overlaps remain safe due to (1)–(2).
4. Handlers are **idempotent** (at-least-once delivery).

## Recurring jobs

- Store `cron_expr` + IANA time zone; compute next fire time with a tz-aware library; DST: define behaviour for skipped/duplicated local times.
- **Missed run policy** after downtime: run once, catch up all, or skip.
- **Overlap policy** if the previous run is still going: skip, queue, or cancel previous.
- Jitter non-critical jobs to avoid thundering herds at :00.

## Delayed retries and expirations

- Retry with exponential backoff + jitter using a delay mechanism; cap attempts; DLQ.
- Expiry (holds, OTPs, sessions): use store TTLs **plus** a re-check at use time; TTL deletion is delayed and best-effort. Never rely on expiry events alone for correctness.

## Precision vs scale

| Need | Approach |
|---|---|
| Seconds precision, millions of jobs | Index scan every 1 s + in-memory heap/wheel for the next minute |
| Sub-second | In-memory timing wheel on the owner node; durable backing store |
| Long horizon (months) | Store in DB; load into memory as it approaches |

## Pitfalls

- Polling with `SELECT` without locking ⇒ double execution.
- Single scheduler = SPOF and bottleneck.
- Ignoring time zones/DST.
- Using in-memory timers without persistence (lost on restart).
- Redis lists/sets losing scheduled tasks on failover without durability configuration.

## Interview questions (with answers)

**Q1. Fire an email 24 hours after signup, for 5M users/day.** Store `(user, send_at)` in a partitioned table (or workflow timers); scheduler polls due rows with `SKIP LOCKED`, enqueues sends, idempotent by `(user, email_type)`.

**Q2. How do you prevent two scheduler nodes from running the same job?** Atomic claim (conditional update/SKIP LOCKED) + unique `(job_id, tick)` constraint + slot ownership with leases.

**Q3. How would you release a ticket hold after 8 minutes?** Store `expires_at`; every claim/confirm query compares against `now()`; a sweeper reclaims rows and emits events; optional Redis TTL for UX only.

**Q4. Delayed messages of 3 days on SQS?** Not native (15 min max): store in DB/timers, or use a scheduler that enqueues at due time; or Step Functions/EventBridge Scheduler.

## Last-minute revision

`run_at` index + atomic claim + unique tick + leases; timers hierarchy for precision; time zones/DST; idempotent handlers; TTL ≠ correctness.

Related: [Job Scheduler](../17-Asynchronous-Systems/Job-Scheduler/README.md) · [Handling Long-Running Tasks](15-handling-long-running-tasks.md) · [ZooKeeper](../04-Technology-Deep-Dives/12-zookeeper.md)
