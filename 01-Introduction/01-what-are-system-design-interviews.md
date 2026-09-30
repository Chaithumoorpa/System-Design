# What are System Design Interviews?

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: *(start)* · 🏠 [Introduction](README.md) · ➡️ Next: [Types of System Design Questions](02-types-of-system-design-questions.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

## The one-paragraph answer

A system design interview is a 45–60 minute conversation in which you design the architecture of a
large software system (a chat app, a video platform, a payment service) on a whiteboard or shared
canvas. There is no single correct answer. The interviewer is evaluating **how you think**:
whether you can turn a vague request into requirements, reason with numbers, pick components for
stated reasons, and discuss trade-offs and failure the way an experienced engineer would.

## Why companies ask it

| What they want to learn | How the interview reveals it |
|---|---|
| Can you handle ambiguity? | You get a one-line prompt ("Design Instagram") and must scope it yourself. |
| Do you understand scale? | Your estimates shape whether you need one database or a hundred shards. |
| Do you know the building blocks? | Caches, queues, load balancers, databases, CDNs, and when each fits. |
| Can you reason about trade-offs? | Every choice costs something; do you name the cost? |
| Can you communicate? | Explaining a design to a colleague is most of an engineer's senior work. |
| Do you have depth somewhere? | Deep dives probe whether "I'd use Kafka" is backed by understanding. |
| How do you collaborate? | Do you take hints, defend choices calmly, change your mind with evidence? |

## What it is *not*

- Not a memory test of a famous architecture. Interviewers see through recited diagrams.
- Not a coding test. You may write a schema, a query or a snippet of pseudo-code, but the focus is design.
- Not about the "best" technology. It is about **justified** technology.
- Not a monologue. It is a conversation; check in often.

## Anatomy of a typical round (45 minutes)

| Minutes | Phase | Your output |
|---|---|---|
| 0–5 | Clarify requirements | Functional list, non-functional list, scope cuts |
| 5–9 | Estimate scale | QPS, storage, bandwidth, and the design implication |
| 9–14 | APIs and data model | Endpoints, entities, storage choice |
| 14–24 | High-level design | Diagram plus a walk through one write and one read |
| 24–40 | Deep dives | 2–3 hard components with alternatives |
| 40–45 | Wrap-up | Bottlenecks, failures, monitoring, extensions |

Detailed guidance: [Answering Framework](../06-Interview-Tips/01-answering-framework.md).

## Where it sits in the hiring loop

- **Mid-level and above** (roughly 3+ years) at product companies almost always includes at least one round.
- Junior loops may replace it with an object-oriented design round (see the companion
  [Low-Level-Design](https://github.com/Chaithumoorpa/Low-Level-Design) repo).
- Staff-level loops may include two rounds, or a deeper one on architecture and cross-team trade-offs.
- Outcomes are usually a rating on a rubric (e.g. strong hire / hire / lean no hire / no hire) rather than a pass/fail on any single detail.

## HLD vs LLD

| | High-Level Design (this repo) | Low-Level Design |
|---|---|---|
| Question | "Design Twitter" | "Design a parking lot" |
| Unit of thought | Services, databases, queues, networks | Classes, interfaces, methods |
| Focus | Scale, availability, data flow | Object model, patterns, extensibility |
| Deliverable | Architecture diagram and reasoning | Class diagram and code |

## Common misconceptions

1. **"I must design everything."** You can't in 45 minutes. Scoping down is a skill that is graded.
2. **"More boxes mean a better answer."** Complexity without a reason is a red flag.
3. **"I should name the fanciest technology."** Choose boring, well-understood tools and justify them.
4. **"The interviewer will tell me if I'm wrong."** Often they stay neutral. Ask, "Is this the level of depth you want?"
5. **"There's a perfect answer I need to match."** There are many good designs; the reasoning is the deliverable.

## How to prepare (overview)

1. Learn the vocabulary: [Must-Know Topics](../02-Must-Know-Topics/README.md).
2. Learn the mechanics: [Concept Deep Dives](../03-Concept-Deep-Dives/README.md) and [Technology Deep Dives](../04-Technology-Deep-Dives/README.md).
3. Learn reusable solutions: [Interview Patterns](../05-Interview-Patterns/README.md).
4. Practise problems out loud with a timer: [Basic Questions](../07-Basic-Questions/README.md) onward.
5. Get feedback from a peer, or record yourself, using the [mock-interview rubric](../_Reference/interview-questions/03-mock-interview-rubric.md).

## Interview questions (with answers)

**Q1. What is the most common reason strong engineers fail this round?**
Jumping into solutions without clarifying requirements or quantifying scale, then being unable to justify choices when challenged.

**Q2. How is "senior" different from "mid-level" in this round?**
Seniors drive the conversation, quantify early, go deep in more than one area, anticipate failure modes, and prefer pragmatic simplicity. See [Expectations by Level](03-expectations-by-level.md).

**Q3. What if I don't know a technology the interviewer mentions?**
Say so, then reason from first principles about what problem it solves ("It sounds like a partitioned log; here's how I would think about ordering and consumption"). Honesty plus reasoning beats bluffing.

## Last-minute revision

- It is a **structured conversation** about trade-offs at scale, not a trivia test.
- Time-box phases, state assumptions, quantify, justify, and check in with the interviewer.
- Simple first; add complexity only when a requirement or number demands it.
