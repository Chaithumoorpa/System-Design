# Pattern: Absorbing Traffic Spikes

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Handling Hot Keys](03-handling-hot-keys.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Pushing Real-time Updates](05-pushing-realtime-updates.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Load can jump 10–100× in seconds (flash sale, ticket on-sale, viral event, breaking news,
top-of-hour cron, marketing push). Provisioning for the peak is wasteful; provisioning for average means outages.

## Recognise it when

- The prompt mentions "sale", "on-sale", "campaign", "viral", "Black Friday", "launch".
- Traffic is predictable (scheduled) or unpredictable (viral).
- Downstream systems (DB, payment provider) have hard capacity limits.

## Strategy: shape → absorb → protect → scale

```
Edge: CDN, WAF, rate limits, waiting room
  ↓ shed & shape
Buffer: queue / log
  ↓ smooth
Compute: autoscaled stateless workers
  ↓ bulkheads, circuit breakers
Data: bounded concurrency, caching, read replicas
```

## Techniques

| Technique | What it does | Notes |
|---|---|---|
| **CDN + static offload** | Serve the herd from the edge | Pre-render pages; cache aggressively |
| **Rate limiting / quotas** | Cap per client and globally | [Rate Limiter](../15-Distributed-Infrastructure/Rate-Limiter/README.md) |
| **Load shedding** | Reject low-priority work early (fail fast, 429/503) | Protect the core path; return Retry-After |
| **Virtual waiting room** | Admit users at a controlled rate | Fairness, honest progress |
| **Queue-based load leveling** | Accept fast, process at sustainable rate | Async UX ("order received") |
| **Autoscaling** | Add capacity on CPU/queue depth/age | Slow to react (minutes); combine with pre-warming |
| **Pre-scaling** | Provision before scheduled events | Cheapest for predictable spikes |
| **Caching and precompute** | Reduce per-request work | Hot key handling |
| **Backpressure** | Propagate limits upstream (bounded queues) | Prevents memory blow-up |
| **Graceful degradation** | Turn off non-essential features (recommendations) | Feature flags |
| **Bulkheads** | Isolate spike traffic from the rest of the site | Separate cluster/DB for the sale |
| **Client behaviour** | Exponential backoff with jitter; avoid retry storms | SDK defaults matter |

## Queue-based load leveling in detail

Producers enqueue; consumers pull at a rate the database can sustain. Monitor **queue age**, not just
depth. Bound the queue; when full, shed load rather than accept work you cannot finish in time.
Give users a status endpoint or notification when processing completes.

## Autoscaling caveats

- Reaction time (minutes) is slower than a spike (seconds): buffers absorb the gap.
- Cold instances have cold caches and connection pools; slow-start traffic.
- Scale the bottleneck, not just the web tier: DB connections, downstream API quotas.
- Set maximum limits to avoid a bill or downstream stampede.

## Worked example: concert on-sale

1. Event page and seat map on CDN with short-TTL cache.
2. Waiting room admits e.g. 2,000 users/s using signed tokens.
3. Booking service rate-limited per user; seat holds via conditional DB updates (see [Preventing Double Booking](14-preventing-double-booking.md)).
4. Payment calls queued and throttled to the provider's limits.
5. Pre-scaled infrastructure; separate cluster from the main site.

## Pitfalls

- Unbounded queues (latency grows unnoticed, memory exhaustion).
- Retries without jitter multiplying load.
- Autoscaling alone for sub-minute spikes.
- Letting the spike hit the shared database used by the whole product.

## Interview questions (with answers)

**Q1. 2M users for 10k items at 10:00. Design?** Waiting room + CDN + rate limits at the edge; cheap atomic stock gate (Redis) to reject losers; queue to authoritative DB updates; async confirmation. See [Flash Sale](../13-E-commerce-and-Marketplace/Flash-Sale/README.md).

**Q2. Why monitor queue age over depth?** Depth ignores processing rate; age tells you the user-visible delay and whether you meet your SLO.

**Q3. What is load shedding and when is it better than queueing?** Rejecting excess requests immediately. Prefer it when work is time-sensitive (stale results are useless) or queues would grow unboundedly.

## Last-minute revision

Edge shed/shape → queue to smooth → autoscale/pre-scale → bulkhead the core → degrade gracefully → clients back off with jitter.

Related: [Surviving Component Failures](09-surviving-component-failures.md) · [SQS](../04-Technology-Deep-Dives/09-sqs.md) · [Kafka](../04-Technology-Deep-Dives/07-kafka.md)
