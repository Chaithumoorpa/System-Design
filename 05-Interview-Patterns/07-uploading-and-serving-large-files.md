# Pattern: Uploading and Serving Large Files

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [Fanning Out Updates](06-fanning-out-updates.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Streaming Video and Audio](08-streaming-video-and-audio.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Users upload/download images, videos, documents or backups (MBs to GBs) over unreliable
networks. App servers must not become a byte pipe; uploads must be resumable; downloads must be fast
and cheap.

## Recognise it when

- Instagram/YouTube/Drive/Slack attachments, profile photos, exports, backups.
- Files larger than a few MB, mobile networks, global users.

## Upload architecture

```
Client → API (authN/authZ, create upload record) → returns presigned URL(s)
Client → Object storage (direct, multipart, parallel, resumable)
Object storage event → queue → workers (scan, validate, thumbnail, transcode, index)
Workers → metadata DB status = READY → notify client
```

| Technique | Why |
|---|---|
| **Presigned URLs** | Bytes bypass your servers; short-lived, scoped credentials |
| **Multipart/chunked upload** | Parallelism, per-chunk retry, resume after failure |
| **Content hash (checksum)** | Integrity check; dedupe; skip already-uploaded chunks |
| **Resumable protocol (tus / S3 multipart)** | Continue after interruption |
| **Size and type limits** | Abuse and cost control; validate server-side (magic bytes, not just extension) |
| **Async processing** | Keep the request short; process via queue |
| **Virus/malware scan, moderation** | Before making content public |
| **Upload status API** | UI shows progress and final state |

### State machine
`INITIATED → UPLOADING → UPLOADED → PROCESSING → READY | FAILED`. Abandoned uploads are cleaned by
lifecycle rules (abort incomplete multipart uploads after N days).

## Download / serving architecture

```
Client → CDN (edge cache) → origin shield → object storage
```

- **CDN** with long TTL for immutable, versioned/hash-named objects.
- **Signed URLs/cookies** for private content, short expiry.
- **Range requests** for resume and seeking; **compression** for text; **image resizing** on the fly or precomputed variants (WebP/AVIF, responsive sizes).
- Serve **derived renditions** (thumbnails, transcoded video) not originals.
- Storage tiers and lifecycle rules for cold content.

## Consistency and metadata

Blob in object storage; metadata (owner, name, size, hash, status, ACL) in a database. Commit
metadata **after** the blob exists so metadata never points to nothing; background reconciliation
finds orphans.

## Large-file specifics

| Scenario | Approach |
|---|---|
| 50 GB file, flaky network | Chunks (e.g. 8–64 MB), parallel, retry per chunk, resumable, checksum per chunk |
| Very many small files | Batch/zip client-side; avoid per-object overhead |
| Desktop sync | Content-defined chunking, dedupe, delta sync ([Google Drive](../10-Media-Streaming-and-Delivery/Google-Drive/README.md)) |
| Video | Segment and transcode ([YouTube](../10-Media-Streaming-and-Delivery/YouTube/README.md)) |
| Global uploads | Transfer acceleration/regional upload endpoints |

## Security

Authorise before issuing URLs; scope URLs to a single key and size; expire quickly; scan content;
serve user content from a separate domain (avoid XSS/cookie issues); encrypt at rest; log access.

## Pitfalls

- Proxying uploads through app servers (memory, timeouts, cost).
- No resume ⇒ users retry entire uploads.
- Trusting client-declared content type/size.
- Public buckets; predictable object keys for private data.
- Serving originals to mobile clients.

## Interview questions (with answers)

**Q1. How would you handle a 2 GB video upload from mobile?** Presigned multipart upload with parallel resumable chunks and checksums; status polling/notification; async processing after completion.

**Q2. Why not upload through your API servers?** They become a bandwidth/memory bottleneck, scale poorly and add latency; direct-to-storage offloads them entirely.

**Q3. How do you prevent orphaned blobs?** Track upload records with expiry, abort stale multipart uploads via lifecycle, reconcile metadata vs storage periodically.

**Q4. How do you serve private files securely at scale?** Authorise in the API, return time-limited signed CDN/S3 URLs (or signed cookies), scoped to the object.

## Last-minute revision

Presigned + multipart + resumable up; queue-driven processing; metadata in DB; CDN + signed URLs +
range requests down; serve renditions; lifecycle for cost/orphans.

Related: [S3](../04-Technology-Deep-Dives/11-s3.md) · [CDN and storage](../_Reference/cdn-and-storage.md) · [Streaming Video and Audio](08-streaming-video-and-audio.md)
