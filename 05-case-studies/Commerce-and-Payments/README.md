# 🛒 Commerce and Payments — High Level Design

Systems where **correctness beats throughput**: contention on a few rows, reservations, idempotent
money movement.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 14 | [Ticket Booking](TicketBooking/README.md) | Seat state machine, conditional updates, hold expiry, waiting room, refund saga | [DB fundamentals](../../02-core-concepts/04-database-fundamentals.md), [Saga](../../04-patterns/02-saga.md) |
| 15 | [Flash Sale / Inventory](FlashSaleInventory/README.md) | Request funnel, Redis gate + DB authority, reservations, bucketed hot stock | [Fan-out & hot keys](../../04-patterns/04-fanout-and-hot-keys.md), [Redis](../../03-technologies/01-redis.md) |
| 16 | [Payment System](PaymentSystem/README.md) | Idempotency keys, unknown-outcome handling, double-entry ledger, outbox, reconciliation | [Idempotency](../../04-patterns/01-idempotency.md), [Security](../../02-core-concepts/14-security-basics.md) |

⬅️ Previous category: [Search and Discovery](../Search-and-Discovery/README.md) · ➡️ Next category: [Distributed Infrastructure](../Distributed-Infrastructure/README.md)
