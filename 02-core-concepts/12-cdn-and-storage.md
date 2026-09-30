# CDN and Storage Systems

## CDN

A content delivery network is a globally distributed set of edge servers that cache content near users.

- **Pull CDN**: edge fetches from origin on first request, then caches by TTL. Easy, first request slow.
- **Push CDN**: you upload content to the CDN ahead of time. Good for large, predictable assets.
- Benefits: lower latency, offloaded origin, absorbs traffic spikes and DDoS, TLS at edge.
- Cache keys: URL plus selected headers/params. Avoid varying on cookies for public content.
- Invalidation: TTLs, purge APIs, or **versioned URLs** (best: `app.3fa9c.js`, cache forever).
- Dynamic acceleration: edge terminates TLS and uses optimised backbone paths; edge compute can personalise.
- Multi-tier caches (edge, regional shield, origin) reduce origin fetches.
- Video: segment media (HLS/DASH, a few seconds each) so segments are cacheable. See [video streaming](../05-case-studies/08-video-streaming.md).

## Storage types

| Type | Access | Examples | Use |
|---|---|---|---|
| Block | Raw volumes, low latency | EBS, local SSD | Databases, VMs |
| File | Hierarchical, POSIX/NFS | EFS, NFS | Shared file access |
| Object | Key to blob via HTTP API, flat namespace | S3, GCS, Azure Blob | Media, backups, data lakes |

## Object storage essentials

- Virtually unlimited, cheap, **11 nines durability** by replication or erasure coding across zones.
- Objects are immutable-ish (overwrite, no partial update); strong read-after-write consistency on major providers today.
- **Storage classes**: hot, infrequent access, archive; lifecycle rules move data automatically.
- **Pre-signed URLs**: clients upload/download directly to storage, keeping large bytes off your app servers.
- **Multipart upload**: split large files, upload in parallel, retry parts, then complete.
- **Erasure coding** (e.g. 10 data + 4 parity shards): tolerates several losses with less overhead than 3x replication, at higher CPU and repair cost.
- Store metadata (owner, name, permissions) in a database; blob content in object storage.

## Uploads pattern

1. Client requests an upload URL from your API (auth checked).
2. API returns pre-signed URL (or multipart parts).
3. Client uploads directly to object storage.
4. Storage event triggers processing (virus scan, thumbnails, transcoding) via queue.
5. Metadata row updated to "ready".

## Data lifecycle and cost

Tier by age and access frequency; compress; dedupe by content hash; set retention and deletion policies (legal requirements like GDPR deletion).

## Interview questions

1. How do you serve a 2 GB video upload reliably from flaky mobile networks?
2. Replication vs erasure coding: when would you choose each?
3. How do you invalidate CDN content quickly and safely?
4. Why not store images in the relational database?
