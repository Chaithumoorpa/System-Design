# Pattern: Handling Long-Running Tasks

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Preventing Double Booking](14-preventing-double-booking.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Scheduling Delayed and Recurring Jobs](16-scheduling-delayed-and-recurring-jobs.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Some work takes seconds to hours (video transcoding, report generation, ML inference, bulk
imports, exports, PDF rendering, code execution). Holding an HTTP request open is fragile and wastes
resources.

## Recognise it when

"Upload and process", "generate report", "export data", "run submitted code", "transcode", any step
that exceeds a normal request timeout (30–60 s) or is CPU/IO heavy.

## The standard shape: accept, queue, work, report

```
Client → API: POST /jobs → 202 Accepted { job_id }
API → DB: job(status=QUEUED) + enqueue message
Workers ← queue → process → update status/progress → store result (S3)
Client → GET /jobs/{id} (poll) | webhook | SSE/WebSocket | push notification
```

| Element | Notes |
|---|---|
| **202 + job id + status endpoint** | Never block the request |
| **Durable queue** | SQS/RabbitMQ/Kafka; work survives crashes |
| **Job table** | `QUEUED → RUNNING → SUCCEEDED/FAILED/CANCELLED`, progress %, attempt count, result pointer, error |
| **Workers** | Stateless pool; autoscale on queue age/depth |
| **Result delivery** | Poll, webhook, SSE/WebSocket, email/push; results in object storage with a signed URL |

## Reliability

- **At-least-once** execution: use **visibility timeout/lease + heartbeat**; if a worker dies, the task reappears.
- **Idempotent tasks**: pass `job_id`/attempt id downstream; write results atomically (temp then rename/commit).
- **Retries** with exponential backoff and jitter; classify transient vs permanent failures; max attempts; **DLQ** for poison jobs.
- **Timeouts** per job class; kill runaway tasks.
- **Checkpointing** for very long jobs: persist progress so a retry resumes rather than restarts.
- **Cancellation**: cooperative flag checked by workers; propagate to child tasks.

## Scaling and fairness

- Split work into **subtasks** (map-reduce style/fan-out) for parallelism and shorter retries (e.g. per video segment, per data shard).
- Separate queues by **priority** and **tenant**; weighted consumption to avoid starvation; per-tenant concurrency caps.
- Right-size worker pools by job type (CPU, GPU, memory-heavy); spot instances for retryable work.
- Backpressure: bounded queues, admission control, reject or delay when overloaded.

## Workflow engines

For multi-step processes with retries, timers, and compensation (order fulfilment, onboarding),
use a durable workflow engine (Temporal, Cadence, AWS Step Functions, Airflow for data DAGs). They persist
state, so orchestration code survives crashes and deploys.

```
Workflow: validate → charge → reserve → ship → notify   (each step retried; compensations defined)
```

## Progress and UX

Return quick acknowledgement; show progress; provide ETA; allow cancel; send completion notification;
clean up temporary artefacts (TTL).

## Worked example: code execution (LeetCode-style)

Submission → queue → sandboxed worker (container/gVisor/Firecracker, CPU/memory/time limits, no network)
→ run tests → store verdict → notify via WebSocket. See [LeetCode](../18-Specialized-Systems/LeetCode/README.md).

## Pitfalls

- Long synchronous HTTP requests, load balancer timeouts.
- Non-idempotent tasks with at-least-once delivery.
- Visibility timeout shorter than the task (duplicate concurrent runs).
- No DLQ or alerting; unbounded retries.
- Storing large results in the queue message.

## Interview questions (with answers)

**Q1. A user requests a 10-minute report. Design the flow.** `POST /reports` returns 202 + id; enqueue; worker generates and uploads to S3; status endpoint/notification; signed download link with expiry.

**Q2. How do you avoid duplicate processing if a worker is slow?** Heartbeat/extend the lease, make the task idempotent, and use a unique constraint/conditional update when committing the result.

**Q3. How do you handle a job that keeps failing?** Retry with backoff up to a limit, then DLQ with the error and context; alert; provide tooling to inspect and redrive.

**Q4. When would you use a workflow engine instead of plain queues?** Multi-step flows with timers, branching, human approval, and compensation, where durable orchestration state and visibility matter.

## Last-minute revision

202 + job id → durable queue → idempotent workers with leases/heartbeats → status via poll/webhook/push → retries + DLQ → split into subtasks → workflow engine for complex flows.

Related: [SQS](../04-Technology-Deep-Dives/09-sqs.md) · [Scheduling Delayed and Recurring Jobs](16-scheduling-delayed-and-recurring-jobs.md) · [Job Scheduler](../17-Asynchronous-Systems/Job-Scheduler/README.md)
