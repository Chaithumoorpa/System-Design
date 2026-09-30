# Design a Ticket Booking System (BookMyShow / Ticketmaster style)

**Prompt:** Users browse events, pick seats, and book. Popular events cause huge spikes. No seat may be sold twice.

## Requirements

- Functional: browse/search events, view seat map, hold selected seats temporarily, pay, receive confirmation, cancel/refund.
- Non-functional: **no double booking** (strong consistency for seat state), fair handling of flash demand (100k users for 5k seats), search can be eventually consistent, high availability for browsing.

## Estimates

- Normal: browse-heavy, modest booking rate. Spike: 500k users hitting one event in the first minutes = a few thousand seat-hold attempts/s concentrated on a small set of rows: contention is the challenge, not raw volume.

## Design

```
Client -> CDN (static, event pages) -> API gateway -> Event/Search service (read replicas, cache, ES)
Booking flow: Waiting room/queue -> Booking service -> Seat inventory DB (strongly consistent, sharded by event_id)
    -> Payment service -> Confirm booking -> Notification (ticket, email)
Hold expiry: TTL / scheduled job releases unpaid holds
```

## Seat state machine

`AVAILABLE -> HELD (user, expires_at) -> BOOKED` or back to `AVAILABLE` on expiry/cancel.

## Deep dive 1: preventing double booking

- **Atomic conditional update** in the inventory DB:
  ```
  UPDATE seats SET status='HELD', held_by=?, hold_expires=now()+interval '8 min'
  WHERE event_id=? AND seat_id=? AND (status='AVAILABLE' OR (status='HELD' AND hold_expires < now()));
  -- rows_affected == 1 means success
  ```
- Alternatives: `SELECT ... FOR UPDATE` in a transaction (pessimistic), optimistic version check, or Redis `SET NX` with TTL for holds with the DB as final authority.
- Book multiple seats atomically in one transaction (all or nothing), ordering seat locks by ID to avoid deadlocks.
- Shard by event_id so one event's contention is in one place; that is fine because a single well-provisioned node can process thousands of conditional updates/s.

## Deep dive 2: hold, pay, confirm

1. Hold seats (TTL ~5-10 minutes) and show countdown.
2. Payment initiated with idempotency key; on success, transition `HELD -> BOOKED` conditioned on the hold still being owned by this user.
3. On payment failure/timeout: release hold. Late payment success after expiry: refund automatically or re-check availability (saga with compensation).
4. Expiry: lazy check on read + background sweeper; never rely solely on cache TTL.

## Deep dive 3: handling the spike

- **Virtual waiting room**: admit users at a controlled rate using a queue token; protects the DB, gives fairness.
- Serve seat maps from cache/CDN with short TTL; show approximate availability, confirm authoritatively at hold time.
- Rate limit and bot protection (CAPTCHA, per-account limits).
- Pre-scale infrastructure before scheduled on-sales.
- Separate read path (browsing) from booking path so browsing stays up.

## Consistency choices

Inventory: strong (single leader/shard, transactions). Search and listings: eventual. Booking history: durable, replicated.

## Follow-ups

- Waitlist when sold out? (Queue per event, notify on release.)
- Dynamic pricing?
- Best-available seat suggestion for a group of N? (Range query on contiguous seats, hold together.)
- What if the payment provider is slow, holding seats too long?
