# Design a Flash Sale / E-commerce Inventory System

**Prompt:** Millions of users try to buy a limited-stock item at the same moment. Do not oversell; stay up.

## Requirements

- Functional: product page, add to cart, checkout, stock decrement, order creation, cancel/return restocks.
- Non-functional: never oversell, survive 100x traffic spike, fair-ish, fast rejection of hopeless requests, eventual consistency for displays.

## Estimates

- 2M users in the first minute for 10k units: ~30k requests/s to the same product. Almost all should be rejected cheaply; only ~10k orders succeed.

## Layered design (filter the herd early)

```
CDN (static page, countdown) -> Rate limit / bot filter -> Waiting room / token bucket admission
 -> Stock pre-check in Redis (atomic DECR) -> Order queue (Kafka) -> Order workers -> Inventory DB (authoritative)
 -> Payment (with timeout) -> Confirm or release stock
```

## Deep dive 1: stock decrement

| Approach | Notes |
|---|---|
| DB row `UPDATE stock SET qty=qty-1 WHERE id=? AND qty>0` | Correct; hot-row contention limits throughput to a few thousand/s per row |
| **Redis atomic DECR / Lua** as gate | Very fast; reject when counter hits zero; DB remains source of truth and reconciles |
| Split stock into buckets (`stock#0..n`) | Reduces hot-row contention; buckets allocated across shards; handle imbalance by rebalancing |
| Queue serialised per product | One consumer per product processes orders in order; simple and consistent, bounded throughput |

Recommended: Redis gate (fast reject) -> queue -> DB conditional update. If the DB write fails, credit Redis back.

## Deep dive 2: correctness across systems

- Reserve stock at "order placed" with expiry (like holds); confirm on payment; release on failure/timeout (saga).
- Idempotency key per order attempt; one purchase per user rule via unique constraint `(user_id, product_id)`.
- Reconcile Redis vs DB periodically; the DB wins.
- Cache invalidation for displayed stock: approximate "few left", not exact.

## Deep dive 3: staying up

- Static content on CDN; sale-time API path minimal (no heavy joins).
- Return 429 / "sold out" quickly; client-side jitter on retry.
- Async order confirmation ("order received, confirming") via queue plus notification, rather than holding connections.
- Isolate flash sale infra (separate cluster/DB) from the rest of the store, bulkhead style.
- Graceful degradation: disable recommendations, reviews during the event.

## Anti-abuse

Bot detection, per-user/device limits, signed tokens to enter checkout, purchase quotas, delayed randomised admission for fairness.

## Follow-ups

- How do you avoid overselling if Redis fails over and loses a decrement? (DB is authoritative; reserve conditional at DB.)
- Multi-warehouse inventory allocation?
- How do you handle cart holds that expire during a sale?
