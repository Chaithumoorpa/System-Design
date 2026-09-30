# Saga and the Outbox Pattern

## Problem

A business workflow spans services, each with its own database (order, payment, inventory). A single ACID transaction is not available; 2PC is fragile and blocks.

## Saga

A saga is a sequence of **local transactions**. Each step publishes an event or triggers the next. If a step fails, **compensating transactions** undo prior steps (cancel reservation, refund).

Example: place order
1. Order service: create order (PENDING).
2. Inventory: reserve items. *Compensation: release.*
3. Payment: charge. *Compensation: refund.*
4. Order: mark CONFIRMED. If payment fails: release inventory, mark order CANCELLED.

### Two styles

| | Choreography | Orchestration |
|---|---|---|
| Control | Services react to each other's events | Central orchestrator commands each step |
| Pros | Loose coupling, no central point | Clear flow, easy to reason about and monitor |
| Cons | Hard to follow, cyclic dependencies | Orchestrator is more logic and must be resilient |

Use orchestration (Temporal, Step Functions, or a state machine in a table) for complex flows.

### Requirements and caveats

- Steps and compensations must be **idempotent** and retryable.
- Compensation is semantic, not a rollback: some effects cannot be undone (email sent). Order steps so irreversible ones come last.
- Intermediate states are visible (isolation is lost): use PENDING states, reservations with expiry, and countermeasures like semantic locks.
- Persist saga state so a crash resumes correctly; add timeouts.

## Outbox pattern

**Problem**: "update DB and publish event" is a dual write; one can succeed and the other fail.

**Solution**: in the same local transaction, write the business change and an `outbox` row. A relay (poller or CDC such as Debezium) reads the outbox and publishes to the broker, marking rows sent. Delivery is at-least-once, so consumers must be idempotent.

```
BEGIN;
  UPDATE orders SET status='PAID' WHERE id=42;
  INSERT INTO outbox(id, topic, payload) VALUES (uuid, 'order.paid', '{...}');
COMMIT;
-- relay publishes outbox rows, then marks or deletes them
```

## Related: Two-phase commit (for contrast)

Coordinator asks all participants to **prepare** (lock and promise), then **commit**. Guarantees atomicity but blocks if the coordinator dies, holds locks, and reduces availability. Acceptable inside a single database cluster; avoid across independently owned services.

## Interview questions

1. Walk through a saga for booking a flight + hotel + car, including failure of the car step.
2. Why does the outbox pattern beat "write DB, then publish"?
3. Choreography or orchestration for a 7-step fulfilment flow? Why?

---

## 🔗 Used in these case studies

- [Payment System](../05-case-studies/Commerce-and-Payments/PaymentSystem/README.md)
- [Ticket Booking](../05-case-studies/Commerce-and-Payments/TicketBooking/README.md)
- [Ride Hailing](../05-case-studies/Location-Based-Services/RideHailing/README.md)
