# 🎞️ Media and Storage — High Level Design

Systems where **bytes are the product**: large objects, CDNs, pipelines and durability.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 8 | [Video Streaming](VideoStreaming/README.md) | Presigned multipart upload, segment-parallel transcoding DAG, HLS/DASH ABR, CDN tiers, tiered storage | [CDN & storage](../../02-core-concepts/12-cdn-and-storage.md), [Networking](../../01-foundations/03-networking-basics.md) |
| 9 | [File Storage and Sync](FileStorageSync/README.md) | Chunk hashing and dedupe, prepare/commit protocol, change log + cursors, conflicted copies, GC | [Replication](../../02-core-concepts/05-replication.md), [Real-time & sync patterns](../../04-patterns/05-realtime-and-sync-patterns.md) |

⬅️ Previous category: [Social and Content](../Social-and-Content/README.md) · ➡️ Next category: [Location-Based Services](../Location-Based-Services/README.md)
