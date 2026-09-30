# Resilience and Failure Handling

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Streaming Video and Audio](08-streaming-video-and-audio.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Preventing Duplicate Processing](10-preventing-duplicate-processing.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Distributed systems fail partially and unpredictably. Design for it explicitly.

## Failure types

Crash, slow node (worse than dead), network partition, packet loss and reordering, disk corruption, dependency outage, bad deploy, overload, clock skew, human error.

## Core techniques

| Technique | Purpose | Notes |
|---|---|---|
| **Timeouts** | Never wait forever | Set per call, shorter than caller's own deadline; propagate deadlines |
| **Retries with exponential backoff + jitter** | Ride out transient errors | Retry only idempotent operations; cap attempts; use retry budgets |
| **Idempotency** | Make retries safe | Idempotency keys, upserts, dedupe tables |
| **Circuit breaker** | Stop calling a failing dependency | Closed, open (fail fast), half-open (probe) |
| **Bulkheads** | Isolate resources per dependency/tenant | Separate thread pools, connection pools, queues |
| **Load shedding** | Reject excess work to protect core | Prioritise critical traffic |
| **Backpressure** | Slow producers when consumers lag | Bounded queues, credit-based flow |
| **Graceful degradation** | Serve reduced functionality | Stale cache, hide recommendations, read-only mode |
| **Fallbacks** | Alternate path on failure | Default value, cached copy |
| **Hedged requests** | Cut tail latency | Send a duplicate to another replica after a delay; cancel loser |

### Retry storms

If every layer retries 3 times across 3 layers, a failure amplifies load 27x. Retry at one layer, use budgets (e.g. retries <= 10% of requests), and jitter to avoid synchronised waves.

## Redundancy and isolation

- Multiple instances across **availability zones**; multiple **regions** for disaster recovery.
- **Cells / shards of failure**: partition users into independent cells so an outage affects a fraction.
- Avoid shared fate: separate control and data planes, and no single global dependency on the hot path.

## Disaster recovery

- **RPO** (recovery point objective): how much data loss is tolerable.
- **RTO** (recovery time objective): how long recovery may take.
- Strategies: backup and restore, pilot light, warm standby, active-active. Cost rises as RPO/RTO shrink. Test restores and failover regularly.

## Safe deployments

Canary releases, blue-green, feature flags, automatic rollback on SLO burn, gradual regional rollout, backward-compatible schema migrations (expand then contract).

## Observability

- **Metrics**: the four golden signals: latency, traffic, errors, saturation. Track percentiles (p50, p95, p99), not averages.
- **Logs**: structured, with request IDs.
- **Traces**: distributed tracing to find slow hops.
- **SLI / SLO / SLA**: indicator (measured), objective (target), agreement (contract). Alert on **error-budget burn**, not raw thresholds.
- Health endpoints, synthetic probes, runbooks, on-call.

## Interview questions

1. Service A calls B, which is slow but not down. Describe every protection you would apply.
2. Why is a slow dependency more dangerous than a dead one?
3. Describe circuit breaker states and how you would tune them.
4. Define RPO and RTO for a payment system and pick a DR strategy.

---

## 🔗 Used in these case studies

- [Rate Limiter](../15-Distributed-Infrastructure/Rate-Limiter/README.md)
- [Notification Service](../17-Asynchronous-Systems/Notification-Service/README.md)
- [Flash Sale / Inventory](../13-E-commerce-and-Marketplace/Flash-Sale/README.md)
- [Metrics and Logging Pipeline](../17-Asynchronous-Systems/Monitoring-and-Alerting/README.md)
