# 🎮 Design Twitch — High Level Design

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Advanced

⬅️ Previous: [Design Gmail](../Gmail/README.md) · 🏠 [Media Streaming & Delivery](../README.md) · ➡️ Next: [Design Airbnb](../../11-Location-Based-Services/Airbnb/README.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../../CREDITS.md).
<!-- nav:end -->

> Twitch is **live video to a huge audience with interactive chat**. Two hard real-time systems run side by side: a
> low-latency video pipeline (ingest → transcode → CDN) and a massive chat fan-out. The streamer's upload is tiny; the
> audience's download is enormous.

## 1. Clarifying Requirements

| Candidate asks | Interviewer answers | Design impact |
|---|---|---|
| Core features? | Go live, watch live, chat, follow/subscribe, VOD/clips. | Live + VOD. |
| Latency? | Glass-to-glass 2–5 s (low-latency mode). | LL-HLS/CMAF. |
| Scale? | 9M streamers/month, 2–3M concurrent viewers avg, peaks 10M+; top channels 500k+. | Fan-out. |
| Quality? | Source up to 1080p60 → transcoded ladder; adaptive bitrate. | Live transcoding cost. |
| Chat? | Real-time, moderation, emotes, rate limits. | Chat fan-out system. |
| Recording? | Auto-save VODs, clip creation. | Segment archive. |
| Monetisation? | Subs, bits, ads. | Entitlement & events. |

**Functional:** broadcast (RTMP/SRT/WebRTC ingest), watch live with ABR, chat, follows/notifications, VOD, clips, moderation.
**Non-functional:** low latency, resilience to streamer/network glitches, elasticity for spikes (raids/events), cost control.

## 2. Back-of-the-Envelope Estimation

| Quantity | Working | Result |
|---|---|---|
| Concurrent streamers | ~100k at peak | Ingest 100k × 6 Mbps = **600 Gbps** |
| Concurrent viewers | 5M peak (typical) | Egress 5M × 4 Mbps = **20 Tbps** |
| Transcoding | Top channels get full ladder; others source-only or limited | Live encoder farm (CPU/GPU/ASIC) |
| Chat messages | Avg 100k viewers/chan × …; global ~300k msgs/s peak | Partitioned chat clusters |
| VOD storage | 100k streams × 3 h × 6 Mbps ≈ 0.8 PB/day if all kept | Retention limits (14–60 d) |

## 3. Core APIs

```http
Ingest:  rtmp://ingest.region.example/live/{stream_key}     (or SRT/WebRTC WHIP)
GET  /v1/channels/{id}/live → {status, viewers, playlist_url (LL-HLS), chat_endpoint}
GET  <CDN>/live/{channel}/master.m3u8        segments *.m4s (~2 s) / partial segments
WS   wss://chat.example  → JOIN #channel · PRIVMSG · events (sub, raid, ban)
POST /v1/follows  ·  POST /v1/clips {channel, start, end}  ·  GET /v1/vods/{id}
```

## 4. High-Level Design

```mermaid
flowchart LR
    S[Streamer OBS] -->|RTMP/SRT| ING[Ingest edge PoPs] --> RT[Live transcoders: 1080p/720p/480p/160p]
    RT --> PKG[Packager: LL-HLS/CMAF segments] --> ORG[Origin cache] --> CDN[CDN edges] --> V[Viewers]
    PKG --> REC[VOD recorder] --> OBJ[(Object storage)] --> VOD[VOD/clip service]
    V <-->|WebSocket| CH[Chat edge → chat servers]
    CH --> MOD[Moderation / AutoMod] --> CHK[[Kafka: chat events]] --> ARC[(Chat archive)]
    META[Channel service: live state, viewers, recommendations] --- ING
    NOT[Notification: "X is live"] --- META
```

### 4.1 Live video path
Streamer connects to the nearest **ingest PoP**; stream is forwarded to a transcoding cluster in the region; renditions are
packaged into short segments (1–2 s, with partial chunks for LL-HLS) and pushed to origin caches; CDN edges pull and serve
viewers. Viewers' players use ABR over the manifest that updates every segment.

### 4.2 Chat path
Viewers open WebSocket connections to chat edge servers; messages are validated (auth, slow mode, AutoMod), published to a
per-channel partition and fanned out to all subscribed servers, each pushing to its local connections. See [Live Comments](../../08-Real-Time-Communication/Live-Comments/README.md).

## 5. Database Design

```text
channels     channel_id PK, owner, title, category, stream_key_hash, status, created_at              (SQL/KV)
live_state   channel_id → {live, started_at, ingest_node, viewer_count(approx), bitrate}            (Redis/etcd, TTL heartbeat)
follows/subs (user_id, channel_id) both directions                                                  (KV/wide-column)
vod          vod_id → {channel, segments manifest in object storage, duration, expires_at}
chat archive Cassandra: PK (channel_id, hour_bucket) CLUSTER ts    — sampled/retained per policy
clips        clip_id → {vod_id, start, end, object_key}
events       Kafka → analytics (viewership, revenue)
```

## 6. Design Deep Dive

### 6.1 Ingest and live transcoding
Ingest PoPs terminate RTMP/SRT close to streamers, forward over an optimised backbone. Transcoding is the largest cost: encode a
ladder only for channels that justify it (partners/popular), offer source-quality passthrough for others; use hardware encoders (GPU/ASIC);
keep ingest stateless where possible, handle streamer reconnects (grace period) without ending the broadcast; failover between
redundant ingest/transcode paths by keyframe-aligned switching.

### 6.2 Latency vs stability
Traditional HLS ~15–30 s (6 s segments × 3). **LL-HLS/CMAF chunked transfer** with 2 s segments and 200–500 ms parts gets 2–5 s.
Trade-off: smaller units increase request rate and rebuffer risk; tuning player buffer target; WebRTC only for ultra-low latency at limited scale.

### 6.3 CDN and viral spikes
Manifests change constantly (short TTL, request coalescing at edge, origin shield); segments are immutable (cacheable). A raid/event
can move 100k viewers to a channel in seconds: pre-warm edges for the channel, distribute across multiple CDNs, capacity headroom,
graceful downgrade of top quality if saturated.

### 6.4 Chat at scale
- Large channels (500k viewers): a single room's fan-out is the bottleneck. Shard the room's audience across many chat servers; messages
  flow producer → partition → all servers (or via hierarchical relays) → connections.
- **AutoMod** and rate limits reduce volume; slow mode/emote-only/followers-only modes; sampling of what each viewer sees at extreme rates.
- IRC-compatible protocol details aside, treat as pub/sub with per-connection backpressure and drop policies.
- Persistent archive optional; moderation actions (ban, timeout) are broadcast events and enforced at ingestion.

### 6.5 VOD and clips
Recorder archives segments as the stream progresses; VOD playlist references the same segments, so VOD is available instantly when
the stream ends; clips reference (vod, start, end) and are extracted/transcoded asynchronously for stable links. Retention by tier.

### 6.6 Viewer counts and discovery
Approximate viewer counts via heartbeats/sampled aggregation (HyperLogLog-like or per-server counters summed); directory ranking by
viewers, category, tags, personalisation; "went live" notifications fan-out to followers (segmented, rate-limited).

### 6.7 Reliability and abuse
Redundant ingest paths; stream-key security and rotation; DMCA/audio fingerprinting on VODs; DDoS protection at edge; incident
response for illegal content (fast takedown, stream kill switch).

## 7. Follow-ups (with answers)

**7.1 Why does live latency matter to Twitch specifically?** Chat interaction: streamers respond to chat, so a 30 s delay breaks the conversation; hence low-latency modes.

**7.2 How do you cut transcoding cost?** Limit ladders by channel tier and audience size, use hardware encoders, transcode on demand for low-viewer channels (only when viewers with bandwidth needs appear), tune presets, reuse encodes across regions.

**7.3 How do you notify millions of followers when a big streamer goes live?** Fan-out via a notification pipeline with batching and provider rate limits, prioritise engaged/subscribed followers, and use topic-based push for scale. See [Notification Service](../../17-Asynchronous-Systems/Notification-Service/README.md).

**7.4 What if the streamer's connection drops?** Ingest holds the channel in a "reconnecting" state for a grace period; players show a buffering slate; on resume, splice at keyframe; VOD marks the gap.

**7.5 How do you ensure chat order for all viewers?** Per-channel partition sequence gives a total order; viewers may see small skew because of fan-out latency; acceptable.

**7.6 How would you support ads?** Server-side ad insertion (SSAI) stitches ad segments into the manifest per viewer/cohort, or client-side markers (SCTE-35) triggering ad players; entitlement decides who sees ads.

## 🧪 Practice Round

<details><summary>Why can't live video be served like VOD?</summary>
Content doesn't exist yet: segments are generated continuously, manifests update every segment, and end-to-end latency is a first-class metric.
</details>

<details><summary>What limits chat scale?</summary>
Fan-out of each message to every viewer connection; solved by sharding audiences, hierarchical relays, moderation and rate controls.
</details>

## 📝 Last-Minute Revision

Ingest PoP → live transcode ladder → packager (LL-HLS/CMAF, 1–2 s segments) → origin/shield → CDN; separate chat fan-out cluster with AutoMod; VOD = same segments; clips by (vod,start,end); pre-warm for raids; latency vs stability trade-off; transcode selectively for cost.

Related: [Streaming Video and Audio](../../05-Interview-Patterns/08-streaming-video-and-audio.md) · [Live Comments](../../08-Real-Time-Communication/Live-Comments/README.md) · [Netflix](../Netflix/README.md)
