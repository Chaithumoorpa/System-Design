# Sharding and Partitioning

Partitioning splits a dataset across nodes so no single machine holds or serves everything. (Sharding usually means partitioning across separate database instances.)

## Strategies

| Strategy | How | Pros | Cons |
|---|---|---|---|
| Range | Key ranges (A-F, G-M) or time ranges | Efficient range scans | Hot spots (recent times, popular ranges) |
| Hash | `hash(key) % N` | Even distribution | No range scans; resharding moves most keys |
| Consistent hashing | Ring; keys map to nearest node | Adding/removing node moves ~1/N of keys | Needs virtual nodes for balance |
| Directory / lookup | Table maps key to shard | Flexible, easy rebalancing | Lookup service is a dependency |
| Geo | By region | Data locality, compliance | Cross-region queries |

## Choosing a shard key

Good keys have **high cardinality**, **even access distribution**, and **match the dominant query** so most requests hit a single shard.

| System | Likely key | Watch out for |
|---|---|---|
| Chat messages | conversation_id | Very active group chat becomes hot |
| Orders | user_id (for "my orders") | Merchant-side queries need a second index |
| Timeline / events | user_id, with time as sort key inside | Time as the *partition* key creates a hot recent shard |
| Multi-tenant SaaS | tenant_id | One huge tenant dominates; split large tenants |

## Problems introduced

- **Cross-shard queries and joins**: scatter-gather is slow; denormalise or maintain global secondary indexes (local index per shard = scatter-gather reads; global index = extra write cost).
- **Cross-shard transactions**: need 2PC or sagas; try to design so transactions stay within one shard.
- **Hot shards / hot keys**: add salt (`key#0..k`), split hot keys, cache in front, or isolate heavy tenants.
- **Resharding**: use many small logical partitions (e.g. 1024) mapped to fewer physical nodes so rebalancing moves whole partitions. Avoid `hash % N` with changing N.
- **Unique IDs and auto-increment**: need globally unique ID generation (see [ID generator](../05-case-studies/03-unique-id-generator.md)).
- **Operational load**: backups, schema changes, monitoring times N.

## Partitioning vs replication

They combine: each partition is replicated (e.g. 3 copies) across nodes. Partitioning scales capacity and throughput; replication gives availability and durability.

## Vertical (functional) partitioning

Split by feature or table group across databases (users DB, orders DB). Simple first step before horizontal sharding, and aligns with microservice ownership.

## Interview questions

1. Why is `hash(key) % N` a poor choice when N changes? What is better?
2. You shard orders by user_id but the merchant dashboard needs orders by merchant. Options?
3. How do you handle a celebrity account that overloads its shard?
4. When would you avoid sharding entirely?
