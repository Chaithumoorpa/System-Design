# Real-Time, Sync and Scheduling Patterns

## Presence and connection management

- Users connect to a gateway over WebSocket. A **session registry** (Redis) maps `user_id -> gateway_id`, refreshed by heartbeat with TTL.
- Delivering a message: look up recipient's gateway, forward through internal pub/sub or RPC. If offline, persist and send a push notification.
- Presence ("online") is approximate: derive from heartbeats, fan out changes only to interested friends, and debounce flapping.

## Ordering and delivery in messaging

- Assign a **per-conversation monotonically increasing sequence number** (or use a single-partition log) to give total order within a conversation.
- Clients ack; server retries until ack (at-least-once); clients dedupe by message ID.
- Sync on reconnect: client sends last seen sequence number and the server returns the gap.

## Collaborative editing (mention level)

- **Operational Transformation (OT)**: central server transforms concurrent operations.
- **CRDTs**: data types that merge deterministically without coordination; suits peer-to-peer and offline use.
- Both target convergence; CRDTs trade memory for simplicity of merging.

## Delta sync and resumable transfers

- Split files into chunks, hash each chunk, upload only chunks the server does not have (dedupe and delta).
- Resumable uploads: track completed chunk indices.
- Sync clients keep a **change log cursor** and apply remote changes since last cursor.

## Scheduling and delayed jobs

- **Timing wheel / delay queue** in memory for many short timers.
- **Sorted set by due time** (Redis ZSET) polled by workers; or a DB table with `run_at` index and `SKIP LOCKED` claims.
- Ensure **at-least-once execution** with visibility timeouts and idempotent jobs; heartbeat for long tasks.
- Avoid double-scheduling cron jobs by leader election or unique job keys.

## Time-based expiry

Reservations (ticket holds), sessions, OTP codes: use TTLs in the store plus a sweeper for cleanup, and never rely on expiry alone for correctness (re-check state at commit time).

## Geo-distribution patterns

- **Home-region** ownership: each user's data has one writable home; others read replicas.
- **Active-active** with conflict resolution for availability-critical data.
- **Geo-routing** via DNS/anycast; data residency constraints shape placement.

## Interview questions

1. How do you deliver a chat message to a user connected to a different server?
2. How would clients resync after being offline for a day?
3. Design a delayed job system that fires 10M timers per day accurately.

---

## 🔗 Used in these case studies

- [Chat System](../05-case-studies/Real-Time-Communication/ChatSystem/README.md)
- [File Storage and Sync](../05-case-studies/Media-and-Storage/FileStorageSync/README.md)
- [Job Scheduler](../05-case-studies/Distributed-Infrastructure/JobScheduler/README.md)
