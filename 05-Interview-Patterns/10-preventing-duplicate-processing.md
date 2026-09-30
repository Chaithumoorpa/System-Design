# Idempotency

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Surviving Component Failures](09-surviving-component-failures.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Running Across Multiple Regions](11-running-across-multiple-regions.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

An operation is idempotent if performing it many times has the same effect as performing it once. It is what makes retries, at-least-once delivery, and client timeouts safe.

## Why it matters

A client sends `POST /payments`, the server charges the card, and the response is lost. The client cannot tell success from failure and retries. Without idempotency, the customer is charged twice.

## Naturally idempotent

`PUT` (replace), `DELETE`, `SET x = 5`, upserts, "mark as shipped". Not idempotent: `INCR`, "append", "charge $10", "send email".

## Idempotency key pattern

1. Client generates a unique key (UUID) per logical operation and sends it (`Idempotency-Key` header). Retries reuse the same key.
2. Server, **atomically**, inserts `(key, request_hash, status=IN_PROGRESS)` with a unique constraint.
   - Insert fails, and the stored result is complete: return the stored response.
   - Insert fails, and the result is in progress: return 409 or wait.
   - Insert succeeds: process, then store the response with the key.
3. Keys expire after a window (e.g. 24 hours).
4. Reject a reused key with a different request body.

Store the key and the business effect **in the same transaction** when possible, so a crash cannot leave one without the other. When the effect is in another system (payment provider), pass the key downstream too.

## Consumers of messages

- Store processed message IDs (with unique constraint) in the same transaction as the side effect.
- Or use versioned/natural-key upserts.
- Or conditional writes (`WHERE version = ?`).

## Pitfalls

- Check-then-act without atomicity (two concurrent retries both pass the check).
- Key scoped globally instead of per user or tenant.
- Dedupe window shorter than the longest possible retry.
- Idempotent handler that still triggers non-idempotent side effects (emails) outside the guarded section.

## Interview questions

1. Design idempotent payment creation across an API server and a payment provider.
2. How do you make an "increment counter" consumer idempotent?
3. Two identical requests arrive at the same time on different servers. What guarantees only one executes?

---

## 🔗 Used in these case studies

- [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md)
- [Notification Service](../17-Asynchronous-Systems/Notification-Service/README.md)
- [Ticket Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md)
