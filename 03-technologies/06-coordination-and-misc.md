# Coordination Services and Other Building Blocks

## ZooKeeper / etcd / Consul

Small, strongly consistent, replicated stores (ZAB/Raft consensus) for **metadata and coordination**, not bulk data.

Uses:
- **Leader election** (ephemeral node or lease; the lowest sequence node wins).
- **Service discovery and health** (ephemeral registrations that vanish when a session dies).
- **Distributed locks** and barriers (with fencing tokens to protect against paused clients).
- **Configuration** with watches for change notification.
- **Cluster membership and partition assignment** (Kafka controller, HBase, Kubernetes state in etcd).

Limits: low write throughput, small values, 3 or 5 nodes (odd, majority quorum), keep off the request hot path.

**Fencing token**: a monotonically increasing number issued with each lock or lease; the resource rejects operations with a lower token than one it has seen, protecting against a stalled ex-leader.

## Probabilistic data structures

| Structure | Answers | Trade-off |
|---|---|---|
| **Bloom filter** | "Is x in set?" (no false negatives, some false positives) | Space-efficient; cannot delete (use counting variant) |
| **Count-Min Sketch** | Approximate frequency counts | Overestimates; used for top-k heavy hitters |
| **HyperLogLog** | Approximate distinct count | ~1% error, KBs of memory |
| **Cuckoo filter** | Set membership with deletion | Slightly more complex |

Used for: skip disk lookups for missing keys (LSM stores), cache penetration guards, crawler seen-URL sets, unique visitor counts, trending items.

## Batch and stream processing

- **Batch** (Spark, MapReduce): large, periodic, high throughput, high latency. Good for backfills, ML features, reports.
- **Stream** (Flink, Kafka Streams, Spark Streaming): continuous, low latency, windowing, state, watermarks for late data.
- **Lambda architecture**: batch layer + speed layer + serving; **Kappa**: everything is a stream, replay the log to reprocess.
- **Windowing**: tumbling, sliding, session windows; event time vs processing time.

## Workflow / orchestration

Durable workflow engines (Temporal, Cadence, AWS Step Functions) persist state of long-running processes with retries and timers; ideal for sagas, order fulfilment, onboarding.

## Containers and platforms (mention level)

Containers package apps; Kubernetes schedules them, restarts failures, rolls out deployments, scales on metrics, and provides service discovery. Know: pods, deployments, services, HPA, readiness/liveness probes.

## Interview questions

1. How does a lock service prevent two leaders from acting at once after a network pause?
2. Which probabilistic structure would you use to dedupe billions of URLs in a crawler?
3. Batch vs stream for computing daily and near-real-time metrics; how do you unify them?
