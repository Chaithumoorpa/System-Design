# 🔒 Design a Distributed Locking Service — High Level Design

<!-- nav:start -->
🏷️ **Priority:** Low · **Difficulty:** Advanced

⬅️ Previous: [Design Time Series Database](../Time-Series-Database/README.md) · 🏠 [Distributed Infrastructure](../README.md) · ➡️ Next: [Design Likes Counting System](../../16-Counting-and-Ranking-Systems/Likes-Counting-System/README.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../../CREDITS.md).
<!-- nav:end -->

> "Only one worker may do X at a time" is easy on one machine and treacherous across many: processes pause, networks partition, clocks drift.
> A correct lock service is really **consensus + leases + fencing tokens**.

## 1. Clarifying Requirements

| Candidate asks | Interviewer answers | Design impact |
|---|---|---|
| Use cases? | Leader election, mutual exclusion for jobs, resource ownership. | Lease-based locks. |
| Safety? | At most one holder at any time (mutual exclusion). | Consensus/fencing. |
| Liveness? | Lock is released if holder dies; no deadlock. | Leases with TTL. |
| Scale? | 100k locks, 50k lock ops/s, low latency < 10 ms. | Small consensus cluster. |
| Fairness? | FIFO waiting nice-to-have. | Wait queues. |
| Reentrancy? | Optional. | Owner IDs. |
| Availability? | Survive minority node failures. | 3/5-node quorum. |

**Functional:** acquire (with timeout), release, renew/extend lease, try-lock, watch (notify on release), read-write locks (optional), leader election, semaphores.
**Non-functional:** correctness first (safety), fault tolerance, bounded lock hold on failure, moderate throughput, clear semantics under partitions.

## 2. Back-of-the-Envelope Estimation

| Quantity | Working | Result |
|---|---|---|
| Locks | 100k active | State tiny: 100k × 200 B = 20 MB (fits in memory) |
| Ops | 50k/s acquire/release + heartbeats 100k clients × 1 per 5 s = 20k/s | ~70k/s ⇒ need batching/sharding |
| Consensus write cost | Raft commit ≈ 1–5 ms in-DC | ~10–50k writes/s per group |
| Cluster | 5 nodes (tolerate 2 failures) | Dedicated small cluster (etcd/ZooKeeper) |

If lock ops exceed one group's throughput, **shard lock namespaces** across multiple consensus groups.

## 3. Core APIs

```text
Acquire(lock_name, owner_id, ttl, wait_timeout) → { granted: bool, lease_id, fencing_token }
Release(lock_name, lease_id)                    → ok
Renew(lock_name, lease_id, ttl)                 → ok | expired
Watch(lock_name)                                → stream of {released|acquired} events
Election: Campaign(election_name, candidate) / Resign / Observe → current leader
Session API: CreateSession(ttl) → session_id; KeepAlive(session_id); locks tied to session (auto-released on expiry)
```

## 4. High-Level Design

```mermaid
flowchart LR
    C1[Client A] & C2[Client B] --> SDK[Client library: session, keepalive, retries]
    SDK --> LS[Lock service nodes]
    subgraph Consensus cluster: Raft / Paxos, 5 nodes
      L[Leader] --- F1[Follower] & F2[Follower] & F3[Follower] & F4[Follower]
      SM[(Replicated state machine: locks table, sessions, wait queues, fencing counter)]
    end
    LS --> L
    L -->|committed events| WATCH[Watch/notify stream] --> SDK
    C1 -->|"operation + fencing token"| RES[Protected resource: verifies token]
```

### 4.1 Acquire flow
Client sends `Acquire` to the leader (followers redirect). The leader proposes the operation to the Raft log; on majority commit, the state machine grants the lock if free (records owner, lease expiry, and increments a **global fencing token**),
otherwise enqueues the waiter or returns failure. Response includes the lease id and fencing token.

### 4.2 Keepalive and expiry
Sessions renew leases via heartbeats (also replicated). If the client stops heartbeating, the lease expires (time measured by the leader; expiry itself is committed through the log), and the lock is released and the next waiter granted.

## 5. Database Design

Replicated state machine in memory + Raft log/snapshots on disk:

```text
locks(name PK) → { owner_session, lease_id, fencing_token, acquired_at, expires_at, waiters[FIFO] }
sessions(session_id PK) → { client_id, ttl, last_renewed_at, owned_locks[] }
fencing_counter → monotonically increasing integer (per lock name or global)
raft log: entries (term, index, command) ; snapshots every N entries for compaction
watches(name) → subscribers
```

## 6. Design Deep Dive

### 6.1 Why naive locks are unsafe
Redis `SET key val NX PX 30000` gives a lease, but: (1) a client can **pause** (GC, VM stall) beyond the TTL, lose the lock, then wake and still act on the protected resource while another client holds the lock;
(2) with failover of an async-replicated Redis, the lock can be granted twice; (3) clock jumps break TTL assumptions. Lease-based locks without a fencing check cannot guarantee mutual exclusion for correctness-critical work.

### 6.2 Fencing tokens (the fix)
Each grant returns a strictly increasing **fencing token**. The protected resource (DB, storage, downstream service) remembers the highest token seen and **rejects any operation carrying a lower token**. A paused old holder wakes up with token 33
after the new holder already used 34 ⇒ its writes are rejected. This makes safety independent of clock/pause behaviour.

### 6.3 Consensus-backed state
Use Raft/Paxos (etcd, ZooKeeper/ZAB, Consul) so lock state survives minority failures and has a single linearisable order. All lock decisions are commands in the replicated log; leader failover preserves granted locks (state is in the log).
Reads that must be fresh go through the leader (or read-index); watches deliver committed events.

### 6.4 Leases, sessions and time
Prefer **sessions with TTL**: locks tied to a session that must be kept alive; expiry is decided by the leader's monotonic clock and committed through the log. Clients treat a lock as lost if they cannot renew within TTL (stop work, conservative safety margin
`renew_interval ≪ ttl`); still require fencing for resources. Avoid wall-clock comparisons across machines.

### 6.5 Waiting and fairness
FIFO queue per lock: on release, the next waiter is granted (ZooKeeper recipe: ephemeral sequential nodes, each waiter watches its predecessor only ⇒ avoids herd). Timeouts remove waiters. Try-lock returns immediately.

### 6.6 Leader election
Election = a lock with a value: the winner is leader; others watch. Leaders must handle **loss of leadership** (session expiry) immediately by stepping down, and use fencing tokens (epoch/term) when writing to shared state.
Term numbers also prevent split-brain writes.

### 6.7 Performance and scaling
Lock traffic is small but latency-sensitive; consensus commits cost a network round trip to a majority: batch operations, pipeline, keep cluster in one region/low-latency AZs. Scale by sharding lock names across independent consensus groups (consistent hashing)
and by making clients avoid excessive locking (coarser locks, optimistic concurrency, partitioned ownership).

### 6.8 When not to use distributed locks
Prefer designs that avoid them: **optimistic concurrency/conditional writes**, idempotent operations, partitioning so a single owner handles each key (queue per key/consumer group), or database constraints. Locks add latency, failure modes and coupling.

## 7. Follow-ups (with answers)

**7.1 Is Redlock safe?** It relies on timing assumptions (bounded delays and clock drift) that can be violated by pauses/clock jumps; for correctness-critical mutual exclusion use a consensus system plus fencing tokens; Redis locks are fine for efficiency-only cases (duplicate work is harmless).

**7.2 What happens if the client holding the lock crashes?** Its session stops heartbeating; after the TTL the lease expires and the lock is released; fencing protects against the crashed-but-only-paused case.

**7.3 What happens on a network partition?** The minority side cannot commit operations (no lock grants/renewals) so its clients lose their leases; the majority side continues; clients on the minority must stop work when renewals fail.

**7.4 How do you avoid the thundering herd on release?** Each waiter watches only its predecessor in the queue (ZooKeeper sequential nodes) or the server grants directly to the next waiter and notifies only it.

**7.5 How would you implement a read-write lock?** Track a set of readers or one writer; writers wait for readers to drain; enqueue fairly to avoid writer starvation; fencing tokens for each mode.

**7.6 How do you make lock acquisition time-bounded?** `wait_timeout` on acquire and TTL on leases; deadlock prevention through ordering or timeouts; monitoring for long-held locks.

## 🧪 Practice Round

<details><summary>Why isn't a TTL alone enough?</summary>
The holder may pause and resume after expiry while believing it still holds the lock; only the protected resource rejecting stale fencing tokens guarantees safety.
</details>

<details><summary>Why run the lock service on a consensus cluster?</summary>
A single node is a SPOF, and naive replication can grant the lock twice on failover; consensus gives a single linearisable history tolerating minority failures.
</details>

## 📝 Last-Minute Revision

Locks = **leases via sessions** in a **Raft/ZAB-replicated state machine**; every grant returns a monotonic **fencing token** checked by the resource; expiry decided through the log; FIFO waiters watching predecessors; leader election = lock + term; avoid locks when possible (optimistic concurrency, single-owner partitioning).

Related: [ZooKeeper](../../04-Technology-Deep-Dives/12-zookeeper.md) · [Consistency and CAP](../../03-Concept-Deep-Dives/05-Distributed-Systems/03-consistency-and-cap.md) · [Preventing Double Booking](../../05-Interview-Patterns/14-preventing-double-booking.md)
