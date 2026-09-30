# Design a Video Streaming Platform (YouTube / Netflix style)

**Prompt:** Users upload (or the platform ingests) videos and millions watch them with smooth playback on any device.

## Requirements

- Functional: upload, process, watch (adaptive quality), search/browse, resume position, (recommendations out of depth).
- Non-functional: fast start (<2 s), minimal buffering, global reach, high availability for playback, upload reliability, cost control (storage and egress dominate).

## Estimates

- 100M DAU x 30 min at avg 3 Mbps: peak concurrent maybe 20M streams -> ~60 Tbps egress. Only a CDN can serve this; origin sees a small fraction.
- Uploads: 500k videos/day x 500 MB raw = 250 TB/day raw, multiplied by transcoded renditions (~2-3x). Storage grows to hundreds of PB: tiering is essential.

## High-level design

```
Upload: client -> API (auth, metadata) -> resumable multipart upload -> object store (raw)
   -> Kafka/queue -> Transcoding pipeline (DAG of workers) -> renditions + HLS/DASH manifests -> object store
   -> metadata DB updated (READY) -> CDN warm for popular titles
Watch: client -> API (metadata, manifest URL, signed) -> CDN edge -> (miss) regional cache -> origin object store
```

## Deep dive 1: upload and processing

- Chunked, resumable upload directly to object storage via pre-signed URLs; client retries failed chunks only.
- **Transcoding pipeline** (parallel DAG): split into GOP-aligned segments, encode each segment into multiple resolutions/bitrates (240p to 4K) and codecs (H.264, VP9/AV1, HEVC) in parallel on a worker fleet, then assemble; also thumbnails, audio tracks, subtitles, DRM packaging.
- Queue-based, autoscaled, idempotent tasks with retries; priority for new uploads of popular creators.
- Content moderation and copyright fingerprinting as pipeline stages.

## Deep dive 2: adaptive bitrate streaming

- Video cut into 2-10 s segments per rendition; a **manifest** (HLS `.m3u8` / DASH `.mpd`) lists them.
- The player measures throughput and buffer, and switches rendition per segment. Segments are plain HTTP objects, so highly cacheable.
- Start with a low rendition for fast start, then step up.

## Deep dive 3: delivery

- Multi-tier CDN (edge -> regional -> origin shield). Popular content pre-positioned; long tail served from origin/regional.
- Large providers embed cache appliances inside ISPs (Open Connect style) to cut backbone cost.
- Signed, expiring URLs and tokens for access control; DRM for premium content.
- Cache key by segment path; long TTLs (immutable).

## Metadata and other services

- Metadata (title, owner, renditions, status): sharded SQL/NoSQL; view counts via streamed aggregation, not per-view DB writes.
- Search via inverted index fed by CDC. Watch history/resume position in a KV store, written with debouncing.
- Recommendations: offline candidate generation + online ranking (mention only).

## Cost levers

Encode popular videos at more renditions, rarely watched at fewer; move cold originals to cheaper tiers; per-title encoding; peer/ISP caches.

## Follow-ups

- Live streaming? (Low-latency ingest via RTMP/WebRTC, segmenter, shorter segments, CDN fan-out, latency vs stability.)
- Viral video suddenly popular? (Origin shield, request coalescing, prewarm.)
- Resume playback across devices? (Position events to KV, latest-wins.)
