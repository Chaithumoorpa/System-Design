# Design a Payment System

**Prompt:** Let merchants accept payments from customers via a payment service that integrates with card networks/PSPs and moves money correctly.

## Requirements

- Functional: create payment, authorise/capture, refund, webhook to merchants, payment status query, ledger of money movement, reconciliation.
- Non-functional: **correctness above all** (no double charge, no lost payment), idempotency, auditability, high availability, security/PCI compliance, exactly-once *effect*.

## Estimates

- 10M transactions/day = ~120/s avg, ~1-2k/s peak. Low volume compared to social apps; the difficulty is correctness, not scale.

## High-level design

```
Merchant/Client -> API gateway -> Payment service -> Payment DB (ACID) + Outbox
     -> PSP / acquirer adapters (Stripe-like, bank, card network) -> async webhooks back
     -> Ledger service (double-entry) -> Reconciliation & settlement jobs
     -> Event stream -> Notifications, fraud, analytics
Card data: Vault / tokenisation service (PCI scope isolated); client sends card directly to the vault, gets a token
```

## Payment flow

1. Client calls `POST /payments` with idempotency key, amount, currency, token.
2. Service creates payment record `CREATED` (unique on idempotency key), risk/fraud check.
3. Calls PSP to authorise, passing our idempotency key. Timeout or unknown result -> state `PENDING/UNKNOWN`, never assume failure.
4. Resolve unknowns: query PSP by reference, or process the async webhook. A recovery job retries status inquiries.
5. On success: `AUTHORISED -> CAPTURED`, ledger entries written, event published via outbox, merchant webhook sent (retries with backoff, signed).

## Deep dives

- **Idempotency**: key stored with request fingerprint and result; same key returns the same response. See [idempotency](../04-patterns/01-idempotency.md).
- **State machine**: explicit, persisted transitions with allowed-transition checks; every change appended to an immutable history table.
- **Double-entry ledger**: each transaction writes balanced debit and credit entries in one DB transaction; balances derived or updated atomically; entries immutable, corrections are new entries. Enables audit and reconciliation.
- **Consistency**: single relational DB (sharded by merchant or account) for payment + ledger to keep ACID; cross-system steps via saga/outbox, not 2PC with the PSP.
- **Reconciliation**: daily job compares internal records against PSP/bank settlement files; mismatches raise tickets; the source of truth for money movement is external.
- **Webhooks**: at-least-once delivery, signature, retries with exponential backoff, endpoint idempotency, replay tool.
- **Fraud/risk**: synchronous rules + async ML scoring; 3-D Secure step-up.
- **Security**: tokenisation, encryption at rest and in transit, HSMs for keys, strict access control, audit logs, PCI-DSS scoping.
- **Multi-currency and precision**: store minor units as integers (never floats), currency code alongside.
- **Retries and failover**: multiple PSPs with routing by cost/success rate and failover, only when it is safe to retry (idempotent with the PSP).

## Failure scenarios

- Timeout after PSP charge succeeded (unknown state) -> reconcile via inquiry.
- Duplicate webhook -> idempotent handler keyed by event ID.
- DB failover mid-transaction -> transaction atomicity ensures no half-written ledger.
- Merchant endpoint down -> retries plus dashboard for manual replay.

## Follow-ups

- Refund partial and multiple times? (Cap by captured amount, per-refund idempotency.)
- Wallet balance transfers between users with strong consistency?
- Support for subscriptions/recurring billing? (Scheduler + dunning.)
