# Fan-out, Hot Keys and Other Scale Patterns

## Fan-out on write vs on read

For content delivered to many followers (feeds, notifications):

| | Fan-out on write (push) | Fan-out on read (pull) |
|---|---|---|
| When work happens | At post time, write to every follower's inbox | At read time, gather from followees |
| Read latency | Very low | Higher (merge many sources) |
| Write cost | Huge for users with many followers | Trivial |
| Wasted work | Inactive followers get writes | None |
| Good for | Typical users | Celebrities |

**Hybrid**: push for normal users, pull for high-follower accounts and merge at read time; skip inactive users; cap inbox size.

## Hot key mitigation

- **Local cache with short TTL** in app servers for extremely popular keys.
- **Key splitting**: `counter#0..#N-1`, write to a random suffix, sum on read.
- **Replicate hot data** to more nodes and read from any.
- **Request coalescing** (single-flight) so one fetch serves many waiters.
- **Isolate**: dedicated shard for known large tenants or celebrities.

## Counting at scale

- Naive `UPDATE count = count + 1` on a hot row causes lock contention.
- Options: sharded counters, buffer increments in memory/Redis and flush in batches, stream events and aggregate (Kafka + Flink), approximate counts (HyperLogLog, Count-Min Sketch) when exactness is unnecessary.

## Precompute vs compute on demand

Precompute when reads dominate and staleness is tolerable (feeds, recommendations, aggregates). Compute on demand when the space of queries is huge or freshness is critical. Often combine: precompute a candidate set, refine at request time.

## Batching and coalescing

Group small writes into larger ones (bulk inserts, Kafka batching, write coalescing in caches). Trade a little latency for a lot of throughput.

## Bounded queues and admission control

Reject or shed early rather than queue unboundedly; unbounded queues turn overload into latency blowups and memory exhaustion.

## Lease and heartbeat

Ownership of a resource (leader, partition, job) is held via a time-limited **lease** renewed by heartbeats; expiry lets others take over. Combine with fencing tokens.

## Gossip protocols

Nodes periodically exchange state with random peers; membership and failure information spreads epidemically. Scalable, decentralised, eventually consistent (Cassandra, Consul).

## Interview questions

1. A user with 50M followers posts. What happens in your design?
2. Design a like counter for a viral post receiving 100k likes/s.
3. When do you choose precomputation over on-demand computation?
