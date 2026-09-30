# Design a Distributed Job Scheduler

**Prompt:** Users schedule one-off and recurring jobs (cron-like); the system runs them reliably at the right time across many workers.

## Requirements

- Functional: create/update/cancel jobs, one-time and cron schedules, retries, priorities, job status and history, timeouts.
- Non-functional: run each job on time (within seconds), **at-least-once** execution (with ability to make effectively-once), survives node failures, scales to millions of jobs, no duplicate triggering of the same schedule tick.

## Estimates

- 10M scheduled jobs, ~5k executions/s at peak minute boundaries (cron jobs cluster on the hour). Job metadata small; execution history grows quickly, so keep it in append-optimised storage with retention.

## Architecture

```
API -> Job store (DB: job definition, schedule, next_run_at, status)
Scheduler (leader-elected or partitioned) -> scans due jobs -> enqueues to Task queue (Kafka/SQS partitioned by priority)
Workers (pull) -> lease task -> execute -> report result -> update state, compute next_run_at
Heartbeats + lease expiry -> reaper requeues stuck tasks
```

## Deep dives

- **Finding due jobs efficiently**: index on `next_run_at`; scheduler polls `WHERE next_run_at <= now AND status='SCHEDULED' LIMIT n`. Partition jobs across scheduler instances by hash of job_id (each owns a range/slot set) instead of a single leader for scale; use leader election (etcd lease) to assign slots.
- **Avoiding double enqueue**: claim with an atomic conditional update (`UPDATE ... SET status='QUEUED', lease=... WHERE id=? AND status='SCHEDULED'`), or `SELECT FOR UPDATE SKIP LOCKED`. Unique key `(job_id, scheduled_time)` on executions makes ticks idempotent.
- **Execution guarantees**: worker takes a **lease** with a visibility timeout and renews with heartbeats. If the worker dies, the lease expires and another picks it up (at-least-once). Jobs should be idempotent; pass `execution_id` to downstream calls.
- **Recurring jobs**: after each execution compute next fire time; handle missed runs on downtime with a policy (run once, run all, skip). Time zones and DST care.
- **Retries**: exponential backoff with jitter, max attempts, DLQ; separate retry state from schedule state.
- **Priorities and fairness**: separate queues per priority and per tenant with weighted consumption to prevent one tenant starving others.
- **Timers at scale**: hierarchical timing wheels in memory for sub-second precision on near-future tasks; DB for the long horizon; load next hour's tasks into memory periodically.
- **Long-running jobs**: heartbeats, checkpoints, cancellation signals, max runtime.
- **Dependencies (DAGs)**: workflow engine tracks upstream completion (Airflow/Temporal style).
- **Observability**: lag between scheduled and actual start, failure rate, queue depth, stuck-lease count.

## Follow-ups

- Thundering herd at :00 every hour? (Spread with jitter, capacity for peaks.)
- Exactly-once execution? (Not possible in general; idempotency plus dedupe keys.)
- Multi-region scheduler failover without double-running?
