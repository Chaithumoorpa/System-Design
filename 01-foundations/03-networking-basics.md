# Networking Basics for System Design

## What happens when you open a URL

1. **DNS** resolves the hostname to an IP (browser cache, OS, resolver, root/TLD/authoritative servers). TTLs control caching.
2. **TCP handshake** (SYN, SYN-ACK, ACK), then **TLS handshake** for HTTPS.
3. **HTTP request** sent; may pass CDN, load balancer, reverse proxy, then app server.
4. Response returns; browser renders and fetches more assets.

Round trips add up, so connection reuse (keep-alive, HTTP/2, HTTP/3) matters.

## TCP vs UDP

| | TCP | UDP |
|---|---|---|
| Delivery | Reliable, ordered, retransmits | Best effort, unordered |
| Overhead | Handshake, congestion control | Minimal |
| Use | Web, DBs, file transfer | Live video/voice, gaming, DNS, QUIC underneath HTTP/3 |

## HTTP versions

- **HTTP/1.1**: one request per connection at a time (head-of-line blocking); browsers open several connections.
- **HTTP/2**: multiplexed streams over one connection, header compression; still suffers TCP-level head-of-line blocking.
- **HTTP/3**: over QUIC (UDP), avoids TCP head-of-line blocking, faster handshakes and connection migration.

## Real-time communication options

| Technique | How | Trade-off |
|---|---|---|
| Short polling | Client asks every N seconds | Simple, wasteful, delayed |
| Long polling | Server holds request until data or timeout | Works everywhere, one connection per waiting client |
| SSE | One-way server push over HTTP | Simple, no client-to-server channel |
| WebSocket | Full-duplex persistent connection | Stateful; needs connection registry and scaling plan |

Scaling WebSockets: connections are stateful, so an LB routes by connection (least connections, not per-request). To message user B connected on gateway 7, look up B's gateway in a presence/session store and forward via pub/sub or internal RPC.

## Proxies

- **Forward proxy**: sits in front of clients (anonymity, filtering, corporate egress).
- **Reverse proxy**: sits in front of servers (TLS termination, caching, compression, routing). Nginx, Envoy, HAProxy.
- **API gateway**: reverse proxy plus auth, rate limiting, routing, request shaping for microservices.

## Load balancing layers

- **L4** (TCP/UDP): fast, no content awareness.
- **L7** (HTTP): route by path, header, cookie; can terminate TLS, retry, do canaries. See [load balancing](../02-core-concepts/02-load-balancing.md).

## DNS in design

- Geo/latency-based routing to nearest region.
- Weighted records for gradual migration.
- Low TTL for failover, but resolvers may ignore it.
- DNS is a coarse tool for failover; pair with health checks and anycast.

## Common protocols cheat sheet

| Need | Reach for |
|---|---|
| Public API | REST/JSON |
| Internal RPC | gRPC |
| Client-server push | WebSocket or SSE |
| Async service decoupling | Message queue / log |
| Mobile push when app closed | APNs / FCM |
| Large file upload | Chunked or resumable upload directly to object storage via signed URL |

## Quick questions

1. Why does HTTP/2 not fully fix head-of-line blocking?
2. You need to push updates to 1M browsers. WebSocket or SSE, and how many gateway servers?
3. Why terminate TLS at the load balancer, and what is the security downside?
