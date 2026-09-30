# Rapid-Fire Drills

One-line answers. Aim to answer each in under 20 seconds. Answers follow the list; do not peek first.

## Questions

1. Why is a cache typically placed in front of a database rather than inside the app process only?
2. What problem do virtual nodes solve?
3. Name two ways to generate IDs without a central counter.
4. Why prefer cursor pagination over offset?
5. What does an idempotency key protect against?
6. What is the difference between a queue and a log?
7. How many partitions limit consumer parallelism in Kafka?
8. What is read-your-writes consistency?
9. What is the thundering herd problem?
10. What does `R + W > N` mean?
11. Why is a slow dependency worse than a failed one?
12. What is a dead-letter queue?
13. Name the four golden signals.
14. When would you pick 302 over 301 for a shortener?
15. What is a hot partition and one fix?
16. Why store money in integer minor units?
17. What is a Bloom filter's failure mode?
18. Why avoid long-running transactions?
19. What is the outbox pattern for?
20. What is a fencing token?
21. Difference between liveness and readiness probes?
22. Why is percentile latency preferred over the average?
23. What is head-of-line blocking?
24. What are compensating transactions?
25. Why is sticky routing needed for WebSockets, or is it?
26. What is backpressure?
27. What is the difference between horizontal and vertical partitioning?
28. What is eventual consistency's guarantee?
29. Why are secondary indexes hard in sharded databases?
30. What is change data capture?
31. What is a covering index?
32. Which structure gives approximate distinct counts?
33. Why use a CDN for APIs at all?
34. How do you avoid duplicate cron execution across nodes?
35. What is the purpose of a write-ahead log?

## Answers

1. A shared cache serves all instances and survives app restarts; local caches are per instance and inconsistent (use both in layers).
2. Uneven load and the lumpy redistribution when a node fails or joins.
3. Snowflake-style (time + worker + sequence), UUIDv4/v7/ULID; or pre-allocated ranges.
4. Stable under inserts and stays fast on deep pages.
5. Duplicate effects when a request is retried.
6. Queue: messages consumed and removed; log: retained, replayable by offset.
7. The number of partitions in the topic (per consumer group).
8. A user always sees their own completed writes.
9. Many clients simultaneously hit a resource (e.g. after cache expiry), overloading it.
10. Read and write quorums overlap, so reads see the latest acknowledged write.
11. It ties up threads, connections and queues, causing cascading failure; dead ones fail fast.
12. A holding queue for messages that repeatedly fail processing.
13. Latency, traffic, errors, saturation.
14. When you need click analytics or the ability to change/expire links, since browsers do not cache 302.
15. One partition receiving disproportionate load; fix by better key, key salting or splitting, caching.
16. Floating point cannot represent decimal money exactly.
17. False positives (never false negatives).
18. They hold locks, block vacuum/cleanup, and increase conflicts.
19. Atomically updating the DB and reliably publishing an event without dual writes.
20. A monotonically increasing token that lets a resource reject stale lock holders.
21. Liveness: process is alive (restart if not); readiness: ready to accept traffic.
22. Averages hide tail latency that users actually experience.
23. One slow/blocked item delays everything queued behind it on the same channel.
24. Actions that semantically undo previous local transactions in a saga.
25. WebSockets are long-lived connections, so once connected the client stays on one server; routing is per connection, and cross-server delivery needs a registry or pub/sub.
26. Signalling upstream to slow down when downstream cannot keep up.
27. Horizontal splits rows across nodes; vertical splits columns or tables by function.
28. If no new updates arrive, all replicas eventually converge to the same value.
29. Index entries may live on different shards from the data; queries either scatter-gather or need a global index with extra write cost.
30. Streaming committed database changes from its log to other systems.
31. An index that contains all columns a query needs, avoiding table lookups.
32. HyperLogLog.
33. Edge TLS termination, connection reuse, DDoS absorption, and caching of cacheable responses.
34. Leader election, a distributed lock with fencing, or unique `(job, tick)` constraint / conditional claim.
35. Durability and recovery: log changes before applying, replay after a crash; also feeds replication.
