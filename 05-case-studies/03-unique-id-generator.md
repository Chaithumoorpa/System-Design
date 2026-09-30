# Design a Distributed Unique ID Generator

**Prompt:** Generate unique IDs across many servers at high rate; IDs should ideally be sortable by time.

## Requirements

- Globally unique, 64-bit fits in a database `BIGINT`, roughly time-ordered (k-sortable), no central bottleneck, 10k+ IDs/s per node, survives node failures.

## Options

| Option | Pros | Cons |
|---|---|---|
| UUIDv4 | No coordination | 128-bit, random so poor index locality, not sortable |
| UUIDv7 / ULID | Time-ordered, no coordination | 128-bit |
| DB auto-increment | Simple | Single point and bottleneck; leaks volume; hard to shard |
| Multi-master auto-increment (step = N) | Some scale | Rebalancing pain, not time-ordered |
| Ticket server (Flickr-style) | Simple | Central dependency; add ranges/batching |
| **Snowflake-style** | 64-bit, sortable, decentralised | Depends on clocks, worker ID assignment |

## Snowflake layout (64 bits)

```
| 1 bit sign | 41 bits timestamp (ms since custom epoch) | 10 bits worker id | 12 bits sequence |
```

- 41 bits of ms is ~69 years. 12-bit sequence gives 4096 IDs per ms per worker (~4M/s).
- Worker ID (10 bits: e.g. 5 datacenter + 5 machine) assigned at startup via a coordination service (ZooKeeper/etcd lease) or config.
- Generation: `ts = now_ms; if ts == last_ts: seq = (seq+1) & 0xFFF; if seq == 0: wait next ms; else seq = 0`.

## Deep dives

- **Clock going backwards** (NTP adjustment): refuse to generate until clock catches up, or use the last timestamp and continue sequence, and alert. Never emit duplicates.
- **Worker ID uniqueness**: leases in etcd; do not reuse an ID while a stale process might still be running.
- **Ordering guarantee**: only roughly ordered across nodes (clock skew), strictly ordered per node. Not suitable when strict global ordering is required (use a sequencer or log for that).
- **Predictability**: IDs reveal creation time and volume; if sensitive, expose an opaque public ID.
- **Sharding benefit**: time-prefixed IDs give insert locality in B-trees; can embed shard information in the ID.
- **Alternative**: range allocation: a service hands each app server blocks of 10k sequential numbers; extremely simple, gaps on crash.

## Follow-ups

- How would you get IDs when 100k IDs/ms/node are needed?
- How would you use IDs for sharding, and how to route by ID?
- Design a globally monotonic sequence (answer: single leader with batching, or consensus log; trade throughput).
