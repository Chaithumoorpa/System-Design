# Design File Storage and Sync (Dropbox / Google Drive style)

**Prompt:** Users store files in the cloud, sync across devices, and share with others.

## Requirements

- Functional: upload/download, automatic multi-device sync, sharing with permissions, version history, offline edits.
- Non-functional: reliability (never lose data), efficient sync (bandwidth), large files, eventual consistency across devices with conflict handling, 500M users.

## Estimates

- 50M DAU, 2 changes/day = 100M sync ops/day (~1.2k/s). Storage: 500M users x 5 GB avg = 2.5 EB raw (chunk dedupe and tiering reduce this). Metadata is small relative to blobs.

## High-level design

```
Client (watcher + chunker + local DB) <-> API/Sync service -> Metadata DB (sharded SQL)
          |                                     |-> Notification service (long poll/WebSocket "changes available")
          '-- chunks --> Block/Object storage (dedup by hash) --> CDN for downloads
```

## Key ideas

1. **Chunking**: split files into fixed (e.g. 4 MB) or content-defined chunks; hash each chunk (SHA-256). A file is an ordered list of chunk hashes.
2. **Deduplication**: before uploading, client asks which hashes the server lacks; uploads only those. Identical chunks across files and users stored once (mind privacy: cross-user dedupe leaks existence; scope or use convergent encryption carefully).
3. **Delta sync**: editing part of a big file changes only a few chunks; only those upload.
4. **Metadata service**: tables for `files(id, parent, name, version, chunk_list, owner)`, `versions`, `shares/ACLs`, `devices`. Strong consistency here (relational, sharded by user or namespace).
5. **Sync protocol**: each device stores a cursor into a per-account change log. Notification says "new changes"; device calls `list_changes(cursor)`, downloads needed chunks, applies locally.

## Deep dives

- **Conflicts**: two devices edit offline. Use version vectors or compare base version; if concurrent, keep both ("conflicted copy") rather than silently overwriting; docs editors may use OT/CRDT.
- **Consistency of commit**: upload chunks first, then commit metadata atomically (file version points to chunk list). Partial uploads leave orphan chunks cleaned by GC.
- **Resumable uploads**: track received chunk indices.
- **Garbage collection**: chunk reference counts; delayed deletion; version retention policy.
- **Sharing and permissions**: ACLs on folders (inherit), link sharing with tokens and expiry; permission check on every metadata and download call; signed URLs for blob access.
- **Durability**: replication/erasure coding across zones, checksums verified on read, scrubbing.
- **Notification of changes**: long poll or WebSocket per device; fall back to periodic poll.
- **Scale**: shard metadata by namespace; hot shared folders need care; block store scales horizontally by chunk hash.

## Follow-ups

- Real-time collaborative doc editing? (OT/CRDT service.)
- Large file 50 GB on flaky network? (Chunk resume, parallel chunks.)
- Encrypted-at-rest and client-side encryption impact on dedupe?
