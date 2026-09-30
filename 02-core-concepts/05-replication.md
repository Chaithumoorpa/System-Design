# Replication

Replication keeps copies of data on multiple nodes for **availability**, **durability** and **read scaling**, and to place data near users.

## Models

| Model | How it works | Pros | Cons |
|---|---|---|---|
| Single-leader (primary/replica) | Writes go to leader; followers replicate | Simple, no write conflicts | Leader is write bottleneck and failover point |
| Multi-leader | Several nodes accept writes, sync with each other | Multi-region writes, offline clients | Write conflicts need resolution |
| Leaderless (Dynamo-style) | Any replica accepts writes; quorum reads/writes | High availability, no failover | Conflicts, read repair, tunable consistency |

## Sync vs async replication

- **Synchronous**: leader waits for follower ack. No data loss on failover, but higher latency and availability is tied to follower health.
- **Asynchronous**: leader acks immediately. Fast, but replicas lag and a leader crash can lose recent writes.
- **Semi-sync**: wait for at least one follower; common compromise.

## Replication lag problems

| Symptom | Cause | Fix |
|---|---|---|
| User posts then does not see it | Read hit a lagging replica | **Read-your-writes**: read from leader for recent writers, or track write timestamp/LSN |
| Data goes "back in time" across refreshes | Reads hit different replicas | **Monotonic reads**: pin a user to one replica |
| Reply appears before the question | Causality lost across partitions | Causal consistency, same partition for related data |

## Failover

1. Detect leader failure (heartbeats/timeouts; avoid false positives).
2. Elect a new leader (most up-to-date replica), often via consensus.
3. Reconfigure clients and old leader. Beware **split brain**: two nodes both think they are leader. Fence the old one (epoch/term numbers, STONITH, leases).

## Leaderless quorums

With N replicas, write to W and read from R. If **R + W > N**, reads overlap the latest write. Example N=3, W=2, R=2. Extras: read repair, hinted handoff, anti-entropy with Merkle trees, and sloppy quorums for availability. Conflicts resolved by last-write-wins (timestamps, can lose data), vector clocks, or CRDTs.

## Conflict resolution in multi-leader

Last-write-wins, application merge logic, CRDTs (counters, sets), or avoid conflicts by routing each record's writes to one home region.

## Change data capture (CDC)

Stream the database's log (Debezium on binlog/WAL) to downstream systems: caches, search indexes, analytics, other services. Prefer CDC over dual-writes from application code, which can diverge on partial failure.

## Interview questions

1. A user updates their profile and then sees the old profile. Why, and how do you fix it?
2. Explain split brain and how to prevent it.
3. Choose N, R, W for a shopping cart (available) versus a bank ledger (consistent).
4. Why is async replication risky for failover, and when is it still acceptable?
