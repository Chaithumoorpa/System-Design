# Pattern: Preventing Double Booking

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Keeping Data in Sync](13-keeping-data-in-sync.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Handling Long-Running Tasks](15-handling-long-running-tasks.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** A scarce resource (seat, room, driver, inventory unit, appointment slot, username) must
be assigned to at most one party even when many requests race, retry, or arrive from different servers.

## Recognise it when

Ticketing, hotel/Airbnb booking, calendar slots, flash sales, ride assignment, unique constraints.

## Core principle

The check and the claim must be **one atomic operation** at the source of truth. "Read, then write" from
the application creates a race (check-then-act).

## Techniques

### 1. Atomic conditional update (usually best)
```sql
UPDATE seats SET status='HELD', held_by=:u, expires_at=now()+interval '8 min'
WHERE event_id=:e AND seat_id=:s AND (status='AVAILABLE' OR expires_at < now());
-- affected rows = 1 → success, 0 → someone else got it
```

### 2. Unique constraint / insert-if-absent
`UNIQUE(room_id, night)` on a bookings table; the second insert fails. Works for date-range problems by
inserting one row per unit of time (per night, per slot).

### 3. Pessimistic locking
`SELECT … FOR UPDATE` locks the rows until commit. Simple and safe; contention causes waits, deadlocks
possible (lock in consistent order), poor with long user think-time (never hold locks while the user
decides).

### 4. Optimistic concurrency
Read with a `version`; update `WHERE version = :v`; retry on conflict. Good when conflicts are rare.

### 5. Exclusion constraints (ranges)
PostgreSQL `EXCLUDE USING gist (room WITH =, during WITH &&)` prevents overlapping time ranges
declaratively, ideal for calendars and hotel stays.

### 6. Distributed lock / single-writer partition
Route all requests for a resource to one owner (partition by resource id, single consumer, or a lease).
Serialises without DB locks; needs fencing tokens if using an external lock. Redis locks alone are not
safe for correctness-critical guarding.

### 7. Reservation (hold) then confirm
Hold for a short TTL, then confirm on payment. Expiry must be checked **in the conditional update**
(timestamp compare), not only by a background sweeper. See [Movie Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md).

## Multi-resource bookings

- Book all-or-nothing in one transaction; lock/claim in a **consistent order** to avoid deadlocks.
- Across services (flight + hotel): [saga](12-coordinating-transactions-across-services.md) with compensations and holds.

## Idempotency and retries

Attach a booking/idempotency key so client retries or double clicks don't create two bookings; store
it with a unique constraint. See [Preventing Duplicate Processing](10-preventing-duplicate-processing.md).

## Handling contention spikes

Waiting room, rate limits, a fast cache gate to reject hopeless requests, then the authoritative DB
check. See [Absorbing Traffic Spikes](04-absorbing-traffic-spikes.md).

## Overbooking as a business choice

Airlines intentionally overbook using statistics; the system enforces a policy (limit = capacity × factor)
and handles compensation. State the requirement before assuming zero tolerance.

## Choosing quickly

| Situation | Choice |
|---|---|
| Single resource unit, high contention | Conditional update |
| Date ranges | Unit-per-night rows with unique key, or exclusion constraint |
| Low contention, long workflows | Optimistic versioning |
| Multi-row atomic | Transaction with ordered locks |
| Cross-service | Holds + saga |

## Pitfalls

- Trusting a cache for the availability decision.
- Holding DB locks during user interaction or payment.
- Sweeper-only expiry (stale holds block or double-sell).
- No idempotency ⇒ duplicate bookings on retry.
- Sharding by a key that splits a single resource's contention across nodes.

## Interview questions (with answers)

**Q1. Two users click the last seat at once. What happens?** Both send a conditional update; the database serialises them; exactly one affects a row, the other gets 0 rows and a "seat unavailable" response.

**Q2. How to prevent overlapping hotel bookings?** One row per room-night with a unique key, all nights inserted in a single transaction; or a Postgres exclusion constraint on the date range.

**Q3. Optimistic vs pessimistic?** Optimistic for rare conflicts (retry on failure); pessimistic when conflicts are common and retry storms would be worse; never hold locks over network round trips to users.

**Q4. Can a Redis lock alone guarantee no double booking?** No. Failover, pauses and expiry can let two holders proceed; the database's atomic constraint (or a fencing token) must be the final arbiter.

## Last-minute revision

Atomic check-and-claim in the DB (conditional update / unique / exclusion), holds with expiry checked in SQL, idempotency keys, ordered locks, saga across services.

Related: [Movie Booking](../13-E-commerce-and-Marketplace/Movie-Booking/README.md) · [Flash Sale](../13-E-commerce-and-Marketplace/Flash-Sale/README.md) · [Database design](../03-Concept-Deep-Dives/04-database-design.md)
