# Data Structures Behind Distributed Systems

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [Tradeoffs](03-tradeoffs.md) · 🏠 [Must-Know Topics](README.md) · ➡️ Next: [Networking](../03-Concept-Deep-Dives/01-networking.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

System design leans on a small set of data structures. Knowing *why* they are used lets you explain
how databases, caches and queues work internally.

## Quick map

| Structure | Where you meet it | Key property |
|---|---|---|
| Hash table | Caches, indexes, dedupe sets | O(1) average lookup |
| B-tree / B+tree | Relational DB indexes | Balanced, sorted, range scans, read-optimised |
| LSM tree (memtable + SSTables) | Cassandra, RocksDB, HBase | Sequential writes, compaction |
| Skip list | Redis sorted sets, memtables | Sorted with simple concurrency |
| Heap / priority queue | Schedulers, top-K, timers | O(log n) min/max |
| Trie / radix tree | Autocomplete, routing tables | Prefix lookups |
| Inverted index | Search engines | Term → document list |
| Bloom filter | LSM reads, crawlers, cache guards | No false negatives, tunable false positives |
| Count-Min Sketch | Heavy hitters, frequency | Approximate counts, fixed memory |
| HyperLogLog | Unique counts | ~1% error in KBs |
| Merkle tree | Anti-entropy repair, Git, blockchains | Compare large datasets by hash |
| Consistent hash ring | Sharding, caches | Minimal remapping |
| Linked list + hash map | LRU cache | O(1) get/put/evict |
| Ring buffer | Logs, bounded queues | Fixed memory, fast append |
| Timing wheel | Timers at scale | O(1) schedule/expire |
| Geohash / quadtree / S2 / H3 | Location services | Map 2D to 1D or hierarchical cells |
| Vector clocks | Dynamo-style conflict detection | Detect concurrent writes |
| CRDTs | Collaborative editing, counters | Merge without coordination |

## Details worth knowing

### B-tree vs LSM tree
- **B+tree**: pages updated in place; predictable reads; write amplification from random page writes; good for read-heavy OLTP.
- **LSM**: writes go to a WAL and in-memory memtable, flushed as immutable sorted files; compaction merges them. Great write throughput; reads may consult several files (Bloom filters help); space and write amplification from compaction.

### Bloom filter
`m` bits, `k` hashes. Insert sets k bits; membership tests check k bits. False-positive rate ≈ (1 − e^(−kn/m))^k. Use for "definitely not present" fast paths: skip disk reads for missing keys, avoid re-crawling URLs, block cache penetration. Cannot delete (use a counting or cuckoo filter).

### Count-Min Sketch
A `d × w` table of counters with d hash functions; increment one cell per row; estimate = min across rows. Overestimates only. With `w = e/ε`, `d = ln(1/δ)`: error ≤ ε·N with probability ≥ 1 − δ. Mergeable by adding tables.

### HyperLogLog
Hash each item; track the maximum leading-zero run per bucket; harmonic-mean estimate of distinct count. Mergeable by max per bucket. Redis: 12 KB per counter, standard error ~0.81%.

### LRU in O(1)
Doubly linked list ordered by recency + hash map key → node. `get`: move node to head. `put`: insert at head; evict tail if full.

### Heaps for top-K
Maintain a min-heap of size K: for each item, push if larger than the heap minimum, pop the smallest. O(n log K). For streams, combine with Count-Min Sketch for frequencies.

### Trie with top-k
Store, at each node, the precomputed top-k completions so prefix lookup is O(length). See [Search Autocomplete](../12-Search-and-Aggregation-Systems/Search-Autocomplete/README.md).

### Merkle tree
Leaves hash data blocks; parents hash children. Two replicas compare root hashes; if different, descend to find the differing range. Used for anti-entropy in [Cassandra](../04-Technology-Deep-Dives/05-cassandra.md).

### Timing wheel
Array of buckets for future ticks; a pointer advances each tick and fires that bucket. Hierarchical wheels cover long horizons. Used for millions of timers (timeouts, delayed jobs).

## Choosing quickly

| Need | Use |
|---|---|
| Exact key lookup | Hash table |
| Range or ordered scan | B-tree / sorted structure |
| Heavy write ingestion | LSM tree |
| "Have I seen this?" at huge scale | Bloom filter |
| Top-K frequent | Count-Min + heap |
| Distinct count | HyperLogLog |
| Prefix search | Trie |
| Text search | Inverted index |
| Timers | Heap or timing wheel |
| Nearby points | Geohash / S2 / H3 |

## Interview questions (with answers)

**Q1. Why do LSM stores use Bloom filters?**
A read may need to check many SSTables; a Bloom filter cheaply proves a key is absent from a file, avoiding disk seeks.

**Q2. Why can't you delete from a standard Bloom filter?**
Bits are shared among items; clearing them could create false negatives. Counting filters keep counters instead.

**Q3. How would you find the top 10 most frequent items in a stream too large for memory?**
Count-Min Sketch (or Space-Saving) for approximate frequencies plus a size-10 min-heap of candidates.

**Q4. Why is a hash ring better than `hash % N`?**
Adding/removing a node moves only ~1/N of keys instead of nearly all.

## Last-minute revision

Bloom = "maybe/no", CMS = "at least this many", HLL = "about this many distinct", LSM = "fast writes, compaction",
B-tree = "fast reads, ranges", Trie = "prefix", Heap = "top-K/timers", Merkle = "find the difference".
