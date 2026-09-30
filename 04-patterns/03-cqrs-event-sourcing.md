# CQRS and Event Sourcing

## CQRS (Command Query Responsibility Segregation)

Separate the **write model** (commands, validation, transactions) from one or more **read models** (queries, optimised views).

```
Command -> Write DB (normalised) --events/CDC--> Read store(s) (denormalised, cache, search) <- Query
```

- Use when read and write shapes or scale differ sharply (feeds, dashboards, search).
- Read models are eventually consistent; handle read-your-writes for the acting user (return the result, or read from the write side briefly).
- Cost: extra components, sync pipeline, lag monitoring, rebuild tooling. Do not use for simple CRUD.

## Event sourcing

Store the **sequence of events** that happened, not just current state. State = fold over events.

- Benefits: full audit trail, temporal queries ("balance at 10:00"), replay to rebuild views or fix bugs, natural fit with event-driven systems.
- Costs: event schema evolution (versioning/upcasting), eventual consistency, learning curve, replay time (mitigate with **snapshots**), harder ad hoc queries (project into read models), privacy deletion is difficult.
- Great fit: ledgers, order lifecycle, collaborative editing. Poor fit: simple CRUD.

Example ledger: events `Deposited(100)`, `Withdrawn(30)`; balance = sum. Events are immutable; corrections are new compensating events.

## Materialised views

Precomputed query results maintained from events or CDC (per-user timeline, counts, leaderboards). Can be rebuilt from the log, which is a strong operational property.

## Interview questions

1. When does CQRS earn its complexity? Give a counterexample.
2. How do you show a user their own new post immediately in a CQRS system?
3. What are the drawbacks of event sourcing, and how do snapshots help?
