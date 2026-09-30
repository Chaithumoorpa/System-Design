# Expectations by Level / Years of Experience

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: [Types of System Design Questions](02-types-of-system-design-questions.md) · 🏠 [Introduction](README.md) · ➡️ Next: [Study Plan (bonus)](04-study-plan.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Interviewers calibrate the same prompt to the candidate's level. The problem may be identical;
what changes is **who drives, how deep you go, and how you handle uncertainty**.

## Summary matrix

| Dimension | Junior / SDE-1 (0–2 yrs) | Mid / SDE-2 (3–5) | Senior / SDE-3 (6–9) | Staff+ (10+) |
|---|---|---|---|---|
| Round presence | Often absent (LLD/coding instead) | Usually 1 round | 1–2 rounds | 1–2, harder, more open-ended |
| Who drives | Interviewer guides | Shared | Candidate drives | Candidate frames the problem and constraints |
| Requirements | Answers what is asked | Asks good questions | Prioritises and cuts scope with reasons | Challenges the premise, considers org/product context |
| Estimation | May need hints | Correct and used | Drives decisions, sanity-checks | Includes cost and growth over years |
| Breadth | Core components | Common components correctly | Right component for the constraint | Multiple viable architectures compared |
| Depth | One area, basic | One area solidly | Two+ areas with internals and failure modes | Deep in several, plus cross-system interactions |
| Trade-offs | Names a few | Compares options | Quantifies and chooses under constraints | Frames strategy: build vs buy, migration, team ownership |
| Failure and ops | Rarely expected | Basics (replicas, retries) | Detailed: SLOs, degradation, DR, deploys | Reliability culture, incident lessons, evolution |
| Simplicity | OK | Good | Expected: simplest thing that works | Deliberately avoids over-engineering |

## What "good" looks like at each level

### Junior / SDE-1
- Produces a coherent basic design: client, server, database, maybe a cache.
- Understands read vs write paths and basic SQL vs NoSQL choices.
- Listens to hints and adapts.
- Not expected: sharding strategies, consensus, multi-region.

### Mid-level / SDE-2
- Structures the interview without prompting; asks clarifying questions; does basic estimation.
- Picks reasonable storage, adds caching/queues where justified, and explains why.
- Handles one deep dive (e.g. feed fan-out, rate limiting algorithm) correctly.
- Mentions failure handling at a basic level (replication, retries).

### Senior / SDE-3
- Leads the conversation; states assumptions; scopes ruthlessly.
- Estimation drives architecture (e.g. "this is 3 GB, so it fits in memory; no sharding needed").
- Goes deep into two or three areas: consistency, hot keys, ordering, idempotency, data modelling.
- Anticipates failure: partial failure, retry storms, thundering herds, backpressure.
- Talks about operations: monitoring, SLOs, rollout safety, cost.

### Staff+ / Principal
- Frames the problem (who are the stakeholders? what is the business constraint?).
- Compares architectures on cost, risk, team complexity, and time-to-market; recommends a phased path.
- Addresses migration, evolution and org boundaries (ownership, API contracts).
- Identifies the one or two decisions that are hard to reverse and treats them carefully.

## Signals that raise or lower the rating

| Raises | Lowers |
|---|---|
| Clarifies, states assumptions, and revisits them | Designs before understanding the problem |
| Uses numbers to make decisions | Numbers computed but never used |
| "X because Y, at the cost of Z" | Technology name-dropping |
| Traces a request end to end | Diagram with no flow |
| Volunteers failure modes | Waits to be asked about failure |
| Takes hints gracefully | Defensive, ignores hints |
| Keeps the design as simple as possible | Every fashionable component included |

## How to level-adjust your preparation

| If you are targeting | Emphasise |
|---|---|
| SDE-1/2 | Fundamentals, common components, 10–15 classic problems, clear communication |
| SDE-3 | Depth in consistency, partitioning, idempotency, failure handling; estimation driving design; 20+ problems; mock interviews |
| Staff | Trade-off framing, migrations, cost, multi-region, org-level concerns; teach-back practice |

## Interview questions (with answers)

**Q1. I'm mid-level. Should I discuss multi-region?**
Only if scale/requirements point to it. Mention it briefly as an extension; go deep on the core design first.

**Q2. As a senior, the interviewer keeps steering me. What am I doing wrong?**
You may not be driving. Announce a plan ("I'll cover APIs, then the write path, then two deep dives"), and choose the deep dives yourself.

**Q3. How do I show staff-level thinking in 45 minutes?**
Name the two or three irreversible decisions, compare alternatives on cost and risk, propose a phased rollout, and state what you would measure to know a decision was wrong.

## Last-minute revision

- Level changes **who drives, depth, and how you handle failure/ops**, not the prompt.
- Seniors: quantify, go deep in 2+ areas, anticipate failure, keep it simple.
- Staff: frame, compare architectures on cost/risk, plan the migration.
