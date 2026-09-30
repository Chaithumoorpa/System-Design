# Back-of-the-Envelope Estimation

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Beginner

⬅️ Previous: [Answering Framework](01-answering-framework.md) · 🏠 [Interview Tips](README.md) · ➡️ Next: [Diagramming Tips](03-diagramming-tips.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

Goal: decide the **shape** of the system (one box or many, cache or not, shard or not) with rough numbers.

## Numbers worth memorising

| Quantity | Value |
|---|---|
| Seconds per day | ~86,400 (use 10^5) |
| Seconds per month | ~2.5 million |
| 1 million req/day | ~12 QPS |
| 1 billion req/day | ~12,000 QPS |
| Peak factor | 2-5x average (state your choice) |

Powers of two: 2^10 = 1 KB (thousand), 2^20 = 1 MB (million), 2^30 = 1 GB (billion), 2^40 = 1 TB (trillion).

### Latency (order of magnitude)

| Operation | Time |
|---|---|
| L1/L2 cache reference | 1-10 ns |
| Main memory read | ~100 ns |
| SSD random read | ~100 µs |
| Same-datacenter round trip | ~0.5 ms |
| Read 1 MB sequentially from memory | ~10-50 µs range |
| Read 1 MB sequentially from SSD | ~0.5-1 ms |
| Spinning disk seek | ~10 ms |
| Cross-continent round trip | ~100-150 ms |

Takeaways: memory is ~1000x faster than SSD random access; network hops are expensive; avoid cross-region calls on the hot path.

### Typical single-machine capacities (rough)

| Component | Rough capacity |
|---|---|
| Web/app server | 1k-10k simple req/s |
| Relational DB (well-indexed) | few thousand to ~10k QPS, tens of TB with care |
| Redis node | 50k-100k+ ops/s |
| Kafka broker | hundreds of MB/s throughput |

## Method

1. **Users**: total, DAU, peak concurrent.
2. **Actions per user per day** for each core operation.
3. **QPS** = DAU x actions / 86,400. Peak = QPS x factor.
4. **Read:write ratio** decides caching and replication needs.
5. **Object size** x objects per day x retention = storage. Add replication factor (usually 3).
6. **Bandwidth** = QPS x payload size, in and out.
7. **Memory for cache** = hot fraction (e.g. 20% of daily data) x size.

## Worked example: photo sharing

Assumptions: 100M DAU, each uploads 0.2 photos/day, views 50 photos/day, average photo 500 KB, metadata 1 KB.

- Upload QPS: 100M x 0.2 / 10^5 = 200 QPS (peak ~600).
- View QPS: 100M x 50 / 10^5 = 50,000 QPS (peak ~150k). Read:write = 250:1, so CDN and caching are essential.
- Storage per day: 20M photos x 500 KB = 10 TB/day, ~3.6 PB/year raw, ~11 PB with 3x replication. Needs object storage and tiering, not a database.
- Egress: 50k QPS x 500 KB = 25 GB/s. That is CDN territory; origin must serve only cache misses.
- Metadata: 20M x 1 KB = 20 GB/day, fine for a sharded DB.

Conclusion you can state: "Photos in object storage behind a CDN, metadata in a sharded store, upload path is small, read path is the scaling problem."

## Availability math

| Availability | Downtime per year |
|---|---|
| 99% | ~3.65 days |
| 99.9% | ~8.8 hours |
| 99.99% | ~53 minutes |
| 99.999% | ~5 minutes |

Serial dependencies multiply (0.999 x 0.999 = 0.998); redundant parallel components improve availability.

## Tips

- Round: 86,400 becomes 100,000; 1.2 becomes 1.
- Say the unit every time. Most mistakes are KB vs MB or per-day vs per-second.
- Stop once you know the design implication. Do not compute for its own sake.
- Sanity-check against known systems (e.g. a single Redis handles ~100k ops/s, so 50k QPS needs few nodes).

## Practice

1. Twitter-like: 300M DAU, 2 tweets/day, 100 reads/day. Compute write QPS, read QPS, and yearly text storage (280 bytes/tweet).
2. Video platform: 50M DAU, each watches 30 minutes at 2 Mbps. Compute peak egress.
3. Chat: 500M DAU, 40 messages/day, 100 bytes each. Compute QPS and 5-year storage.
4. Log pipeline: 10,000 servers, each emitting 100 lines/s of 200 bytes. Compute ingest MB/s and daily storage.

---

## 🔗 Used in these case studies

- [Video Streaming](../10-Media-Streaming-and-Delivery/YouTube/README.md)
- [Chat System](../08-Real-Time-Communication/WhatsApp/README.md)
- [URL Shortener](../07-Basic-Questions/URL-Shortener/README.md)
