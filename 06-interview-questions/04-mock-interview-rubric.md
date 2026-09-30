# Mock Interview Rubric and Checklists

Use with a peer, or self-review from a recording. Score each row 1 (weak) to 4 (strong).

## Scorecard

| Area | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Requirements | Started designing immediately | Some questions, no scope | Clear functional/NFR list | Prioritised, scoped, stated assumptions |
| Estimation | None | Numbers without conclusions | Correct math | Numbers drove design decisions |
| API & data model | Missing | Partial | Clear endpoints and schema | Access patterns justify storage and keys |
| High-level design | Confusing | Boxes, no flow | Clear flow, sensible components | Requests traced; every component justified |
| Deep dive | Surface only | One area with some depth | Two areas with trade-offs | Internals, alternatives, failure modes |
| Trade-offs | Not discussed | Mentioned by name | Compared options | Chose and stated what was sacrificed |
| Scalability & reliability | Ignored | Generic ("add replicas") | Specific bottlenecks and remedies | SPOFs, hot spots, DR, monitoring covered |
| Communication | Silent or rambling | Follows, unstructured | Structured, signposts | Collaborative, uses hints, manages time |

Rough bar: average 3+ across rows with no 1s is a hire signal at most companies; senior and staff roles expect 4s in deep dive, trade-offs and reliability.

## Level expectations

| Level | What is expected |
|---|---|
| Mid (SDE-2) | Solid fundamentals, working design for a scoped problem, knows common components, some trade-offs |
| Senior (SDE-3) | Drives the conversation, quantifies, deep in 2+ areas, anticipates failures, pragmatic simplicity |
| Staff+ | Frames ambiguous problems, cross-system and org concerns, migration and evolution, cost, operational maturity, multiple viable architectures compared |

## During-interview checklist

- [ ] Restated the problem and confirmed scope
- [ ] Listed functional and non-functional requirements
- [ ] Did estimation and stated the implication
- [ ] Defined APIs and data model
- [ ] Drew a diagram and traced read and write requests
- [ ] Picked 2-3 deep dives and compared alternatives
- [ ] Discussed failures, hot spots, consistency and idempotency
- [ ] Covered monitoring, security and privacy briefly
- [ ] Summarised design and open issues at the end

## Trade-off prompts to practise

For any design, answer these aloud:

1. What would break first at 10x load?
2. What is the biggest single point of failure?
3. Which data can be stale, and for how long?
4. What is the most expensive component, and how would you cut cost 30%?
5. How would you migrate from the old system with no downtime?
6. What would you build first for an MVP, and what would you postpone?
7. How would you test this system, including failure injection?

## Feedback template

```
Prompt:                Date:
Strong points:
Missed requirements / assumptions:
Estimation accuracy:
Weakest deep dive:
Unstated trade-offs:
Time management (per phase actuals):
One thing to fix next time:
```

## Behavioural crossover

System design rounds often include questions about past projects. Prepare 3 stories using the STAR format (Situation, Task, Action, Result) covering: a scaling problem you solved, an outage you handled, and a design disagreement you resolved. Quantify results (latency, cost, availability).
