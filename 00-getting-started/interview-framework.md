# The Interview Framework

A 45-minute round is won by structure. Interviewers grade **how you think**, not whether you match a reference design.

## Time budget (45 min)

| Phase | Minutes | Output |
|---|---|---|
| 1. Clarify requirements | 5 | Functional list, non-functional list, scope cuts |
| 2. Estimate scale | 3-4 | QPS, storage, bandwidth, read/write ratio |
| 3. API and data model | 5 | Endpoints, core entities, DB choice |
| 4. High-level design | 8-10 | Box-and-arrow diagram, request flow walkthrough |
| 5. Deep dives | 15 | 2-3 hardest components in detail |
| 6. Bottlenecks and wrap-up | 5 | Failures, scaling, monitoring, extensions |

## Phase 1: Clarify

Ask, don't assume. Good questions:

- Who are the users and what are the top 2-3 use cases? (Scope down aggressively.)
- Scale: DAU, peak traffic, data volume, growth.
- Read-heavy or write-heavy? Latency targets? Global or single region?
- Consistency: is stale data acceptable? For how long?
- Availability target, durability requirements, compliance constraints.

Write down **in scope / out of scope** explicitly. It protects your time.

## Phase 2: Estimate

State assumptions out loud, round aggressively, and keep units visible. See [`01-foundations/01-estimation.md`](../01-foundations/01-estimation.md). The goal is to decide **what kind of system** this is (single node vs sharded, cache needed or not), not to get exact numbers.

## Phase 3: API and data model

- Sketch 3-6 endpoints with key parameters and response shape.
- List entities and their relationships, then choose storage per access pattern.
- Decide keys and indexes now. They drive sharding later.

## Phase 4: High-level design

Start with the simplest thing that satisfies requirements (client, LB, service, DB), then **walk one write request and one read request end to end**. Add components only when a requirement or estimate justifies them (cache because reads dominate, queue because work is slow or bursty).

## Phase 5: Deep dives

Let the interviewer steer, but proactively pick the hardest parts. For each:

1. State the problem in one sentence.
2. Give 2-3 options.
3. Compare on the dimension that matters (consistency, latency, cost, complexity).
4. Pick one and say why. Name what you gave up.

## Phase 6: Wrap-up

- Single points of failure and how to remove them.
- Hot keys, thundering herds, retry storms.
- Monitoring: golden signals, SLOs, alerts.
- Multi-region, data migration, privacy, cost.

## What interviewers score

| Signal | Strong looks like | Weak looks like |
|---|---|---|
| Problem exploration | Asks scoping questions, states assumptions | Jumps straight to boxes |
| Structure | Signposts phases, manages time | Wanders, gets lost in one component |
| Technical depth | Explains internals and trade-offs | Name-drops technologies |
| Trade-off reasoning | "X because Y, at the cost of Z" | "We'll use Kafka" with no reason |
| Communication | Thinks aloud, checks in, takes hints | Silent, defensive |
| Practicality | Simple first, evolves | Over-engineered from minute one |

## Common mistakes

- Designing for Google scale when the prompt is a 100k-user product.
- Choosing a technology before stating the access pattern.
- Ignoring failure, retries, duplicates and ordering.
- Drawing a diagram and never tracing a request through it.
- Treating the interviewer's hint as criticism instead of direction.

## Useful phrases

- "Before I go deeper, is this the part you want me to focus on?"
- "The main trade-off here is ___ versus ___. Given our requirement of ___, I would pick ___."
- "This becomes a bottleneck at roughly ___ QPS. If we get there, we would ___."
