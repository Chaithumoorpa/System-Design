# Consistent Hashing

## Problem

With `node = hash(key) % N`, changing N remaps almost every key. For a cache that means a near-total miss storm; for a database, massive data movement.

## Idea

Place both nodes and keys on a hash ring (0 to 2^32 - 1). A key belongs to the first node found moving clockwise. When a node joins or leaves, only the keys between it and its predecessor move: about **K/N** keys on average.

```
        node A
   .-----o------.
  /              \
 o node D         o node B     key k -> first node clockwise
  \              /
   '-----o------'
        node C
```

## Virtual nodes

Plain placement gives uneven load (random gaps) and a failed node dumps its whole range onto one neighbour. Fix: give each physical node many points (e.g. 100-500 virtual nodes) on the ring.

- Better balance statistically.
- Failed node's load spreads across many nodes.
- Weighted capacity: bigger machines get more vnodes.

## Replication on the ring

Store each key on the next R distinct physical nodes clockwise (Dynamo, Cassandra). Skip vnodes belonging to the same machine or rack to keep replicas in separate failure domains.

## Implementation sketch

1. Hash each `node_id#i` to a point; keep points in a sorted structure.
2. To locate a key: hash it, binary search for the first point >= hash (wrap to the first).
3. Add/remove node: insert/remove its points; migrate only the affected ranges.

## Where it is used

Distributed caches (client-side sharding of Memcached/Redis), Dynamo/Cassandra partitioning, CDNs, load balancers with affinity, sharded databases.

## Alternatives and related

- **Rendezvous (HRW) hashing**: score each node with `hash(key, node)`; pick the highest. Simple, balanced, O(N) lookup.
- **Jump consistent hash**: minimal memory, only supports append-style node numbering.
- **Fixed logical partitions** (Redis Cluster uses 16384 hash slots): map keys to slots, slots to nodes; rebalance by moving slots.
- **Bounded-load consistent hashing**: caps load per node to handle skew.

## Caveats

Does not solve hot keys. Data movement still needs orchestration (dual reads or writes during migration). Replica placement and metadata (who owns what) must be propagated reliably, often via gossip or a coordination service.

## Interview questions

1. Why virtual nodes? What happens with too few or too many?
2. Node C dies in a 4-node ring with replication factor 3. Which data is affected and how does the cluster recover?
3. Compare consistent hashing with fixed hash slots.

---

## 🔗 Used in these case studies

- [Distributed Cache](../../15-Distributed-Infrastructure/Distributed-Cache/README.md)
- [Key-Value Store](../../15-Distributed-Infrastructure/Key-Value-Store/README.md)
- [Web Crawler](../../12-Search-and-Aggregation-Systems/Web-Crawler/README.md)
- [URL Shortener](../../07-Basic-Questions/URL-Shortener/README.md)
