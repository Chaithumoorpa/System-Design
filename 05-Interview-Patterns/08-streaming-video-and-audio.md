# Pattern: Streaming Video and Audio

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Advanced

⬅️ Previous: [Uploading and Serving Large Files](07-uploading-and-serving-large-files.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Surviving Component Failures](09-surviving-component-failures.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Deliver continuous media to millions of viewers on heterogeneous devices and networks
with fast start, minimal buffering, and acceptable cost. Two flavours: **on-demand (VOD)** and **live**.

## Recognise it when

YouTube, Netflix, Spotify, Twitch, Zoom, podcasts, live events. Bandwidth and storage dominate cost.

## VOD pipeline

```
Upload → raw store → transcode DAG → renditions + manifests → origin store → CDN → player (ABR)
```

### Key ideas
1. **Segmenting**: media is cut into 2–10 s chunks; each chunk is a separate small HTTP object, hence cacheable and seekable.
2. **Multiple renditions (bitrate ladder)**: 240p…4K (video) or 64–320 kbps (audio), several codecs (H.264 for compatibility; VP9/AV1/HEVC for efficiency).
3. **Manifest** lists renditions and segment URLs: HLS (`.m3u8`) or MPEG-DASH (`.mpd`).
4. **Adaptive bitrate (ABR)**: the player measures throughput and buffer, switching renditions per segment. Start low for fast start, climb as buffer grows.
5. **Parallel transcoding**: split into GOP-aligned segments, encode in parallel across workers, then stitch manifests.
6. **CDN**: multi-tier (edge, regional shield, origin); pre-position popular titles; ISP-embedded caches for the largest services.
7. **DRM + signed URLs** for protected content.

## Audio (Spotify-like)

- Smaller files (a few MB/track): cache aggressively at CDN, prefetch the next track.
- Multiple bitrates; offline downloads encrypted per device.
- Catalogue and playlists are metadata problems (sharded DB, cache); streaming is CDN-driven.

## Live streaming

```
Camera/encoder → RTMP/SRT/WebRTC ingest → live transcoder/packager → short segments (1–4 s) → CDN → players
```
- Latency ladder: traditional HLS (20–30 s) → Low-Latency HLS/CMAF (2–5 s) → WebRTC (<1 s, expensive at scale).
- Trade-off: lower latency ⇒ smaller segments ⇒ more requests and higher rebuffer risk.
- DVR window keeps recent segments for rewind; recorded as VOD afterwards.
- Chat/reactions are a separate real-time fan-out system ([Pushing Real-time Updates](05-pushing-realtime-updates.md)).

## Interactive/conferencing (Zoom-like)

- **WebRTC** with signalling server; NAT traversal via STUN/TURN.
- **SFU** (selective forwarding unit) forwards each sender's stream to receivers without decoding; scales better than **MCU** (server mixing) which uses heavy CPU; peer-to-peer only for 1:1.
- Simulcast/SVC: senders publish multiple qualities; SFU picks per receiver.
- Priorities: audio > video; drop frames rather than delay.

## Cost levers

| Lever | Effect |
|---|---|
| Better codecs/per-title encoding | 20–50% less bandwidth |
| CDN hit ratio, ISP caches | Lower egress |
| Storage tiering, delete unused renditions | Lower storage |
| Encode popular content richly, long tail sparsely | Compute savings |
| Adaptive quality caps on mobile | Bandwidth |

## Player and QoE metrics

Startup time, rebuffer ratio, average bitrate, bitrate switches, error rate; feed back into ABR
tuning, CDN selection and encoding ladders.

## Pitfalls

- Serving one big file (no seek, no adaptation).
- Transcoding synchronously in the upload request.
- Ignoring the thundering herd on a viral title (use origin shield and request coalescing).
- Underestimating storage growth from many renditions.

## Interview questions (with answers)

**Q1. Why HLS/DASH instead of one MP4?** Small cacheable segments enable CDN caching, seeking, and adaptive bitrate switching; one file cannot adapt to changing bandwidth.

**Q2. How would you reduce startup time?** Small first segment/low initial rendition, preconnect and prefetch manifest, CDN close to users, keep-alive/HTTP/2-3, and edge caching.

**Q3. SFU vs MCU?** SFU forwards streams (scalable, low CPU, client decodes several); MCU mixes into one stream (simple clients, heavy server CPU).

**Q4. How do you deliver live video with low latency at scale?** LL-HLS/CMAF with chunked transfer through a CDN for seconds-level latency; WebRTC for sub-second at limited scale/cost.

## Last-minute revision

Segments + manifest + ABR + multi-rendition + CDN; parallel transcode DAG; live = short segments and a latency/stability trade-off; conferencing = WebRTC with SFU.

Related: [YouTube](../10-Media-Streaming-and-Delivery/YouTube/README.md) · [Netflix](../10-Media-Streaming-and-Delivery/Netflix/README.md) · [Zoom](../08-Real-Time-Communication/Zoom/README.md) · [CDN](../_Reference/cdn-and-storage.md)
