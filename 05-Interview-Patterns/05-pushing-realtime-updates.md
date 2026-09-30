# Pattern: Pushing Real-time Updates

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Absorbing Traffic Spikes](04-absorbing-traffic-spikes.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Fanning Out Updates](06-fanning-out-updates.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Clients need new data within milliseconds to seconds without polling: chat, live scores,
notifications, collaborative cursors, dashboards, live comments, driver location.

## Recognise it when

- The prompt says "real time", "live", "instantly", "notifications", "presence".
- Staleness of more than a second or two breaks the experience.
- The server must initiate the message.

## Transport options

| Option | How | Pros | Cons | Use |
|---|---|---|---|---|
| Short polling | Client asks every N s | Trivial, stateless | Wasteful, delayed | Low-frequency, low-stakes |
| Long polling | Server holds request until data/timeout | Works everywhere | Connection churn, one response per request | Fallback, moderate scale |
| **Server-Sent Events (SSE)** | One-way stream over HTTP | Simple, auto-reconnect, proxies OK | Server→client only, text | Feeds, dashboards, live comments |
| **WebSocket** | Full-duplex over one TCP connection | Low latency, bi-directional | Stateful, LB/proxy care | Chat, games, collaboration |
| Mobile push (APNs/FCM) | OS-level push | Works when app closed | Not instant/guaranteed, quotas | Notifications |
| WebRTC | Peer/relay media & data | Very low latency media | Complex signalling/NAT | Calls, video |

## Architecture

```
Clients ⇄ (WebSocket/SSE) ⇄ Gateway fleet ⇄ Pub/Sub or routing layer ⇄ Backend services
                                 │
                        Session registry (user → gateway)
```

### Connection tier
- Gateways hold many connections (100k+ each with tuned OS/async I/O); mostly stateless except sockets.
- Load balance by least connections; use sticky routing only if needed.
- Heartbeats/ping-pong detect dead peers; TCP alone is too slow.
- **Reconnect with jittered exponential backoff** to avoid thundering herds after a gateway or regional failure; resync from a cursor.

### Delivering a message to the right gateway
- **Registry lookup**: `user_id → gateway_id` in Redis with TTL; forward via internal RPC.
- **Pub/sub topics**: gateways subscribe to channels for their connected users/rooms (Redis Pub/Sub, NATS, Kafka per-gateway topic).
- For rooms: one subscription per room per gateway (not per user) then local fan-out.

### Reliability
Push is best effort. Combine with:
- **Sequence numbers/cursors** so clients detect gaps and request missing data.
- **Persist first**, push second; the database (or log) is the source of truth.
- Ack-based retry for messages that must arrive; idempotent client handling by message ID.

### Scaling fan-out
- Hot rooms (live events with 1M viewers): sample, batch and coalesce updates (send a snapshot per 200 ms), hierarchical fan-out (edge relays), or downgrade to polling/CDN-cached snapshots.
- Backpressure: drop or coalesce for slow clients; cap per-connection buffers.

## Choosing SSE vs WebSocket

| Need | Pick |
|---|---|
| Client only listens (live comments view, scores) | SSE |
| Client sends frequent messages (chat, game input) | WebSocket |
| Must traverse strict corporate proxies | SSE/long polling |
| Binary data, lowest overhead | WebSocket |

## Pitfalls

- Treating the socket as durable: messages lost on disconnect without cursor-based resync.
- One giant pub/sub channel for everything.
- Sticky sessions that prevent rebalancing, or no way to drain gateways during deploys (send "reconnect" hints).
- Ignoring auth on long-lived connections (token expiry mid-connection).

## Interview questions (with answers)

**Q1. How do you deliver a message to a user connected on a different server?** Look up the recipient's gateway in the session registry and forward via internal RPC or pub/sub; if offline, persist and send mobile push.

**Q2. WebSocket vs SSE for live comments?** SSE: one-way stream, simple and proxy-friendly; comments are posted via normal HTTP. WebSocket only if you need low-latency bi-directional traffic.

**Q3. What happens when a gateway crashes with 100k connections?** Clients reconnect with jitter to other gateways, re-auth, and resume from their last cursor; registry TTL expires stale entries; capacity headroom and admission control absorb the reconnection wave.

**Q4. How do you support 1M viewers in one live room?** Publish once to a topic; edge/regional relays fan out; coalesce updates into periodic snapshots; consider CDN-cached snapshots for the long tail.

## Last-minute revision

SSE for one-way, WebSocket for two-way, mobile push when offline; gateway + registry/pub-sub; **cursor-based
resync** because sockets drop; jittered reconnect; coalesce for hot rooms.

Related: [WhatsApp](../08-Real-Time-Communication/WhatsApp/README.md) · [Networking](../03-Concept-Deep-Dives/01-networking.md) · [Fanning Out Updates](06-fanning-out-updates.md)
