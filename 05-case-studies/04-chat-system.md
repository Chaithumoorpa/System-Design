# Design a Chat System (WhatsApp / Messenger style)

**Prompt:** 1:1 and group messaging, delivery status, presence, media, multi-device.

## Requirements

- Functional: 1:1 and group (up to ~500) chat, sent/delivered/read receipts, offline delivery, message history, media sharing, presence.
- Non-functional: low latency (<200 ms online), no message loss, per-conversation ordering, 500M DAU, high availability.
- Scope out: voice/video calls, end-to-end encryption internals (mention Signal protocol, keys on device).

## Estimates

- 500M DAU x 40 messages = 20B/day = ~230k msgs/s avg, ~700k peak. At 100 bytes: 2 TB/day text.
- Concurrent connections: ~100-200M. At 100k connections per gateway host: ~1,000-2,000 gateway servers.

## High-level design

```
Client <-WebSocket-> Chat Gateway ---> Chat Service ---> Message Store (Cassandra/HBase)
                          |                 |
                    Session Registry   Kafka (fan-out, push, indexing)
                    (Redis)                 -> Push service (APNs/FCM)
Media: client -> presigned URL -> object store -> CDN; message carries media ID
```

## Message flow (1:1)

1. Sender's app sends message (client-generated `message_id`) over its WebSocket.
2. Gateway forwards to the chat service; message is **persisted first**, then acked to sender ("sent").
3. Service looks up recipient's gateway in the session registry; if online, forwards; recipient acks -> "delivered".
4. If offline: message stays in the recipient's inbox; push notification sent; delivered on reconnect.
5. Read receipts travel the opposite way as small events.

## Data model and storage

- Messages table (wide-column): partition key `conversation_id` (bucketed by time window for huge chats), clustering `message_seq DESC`. Access pattern: latest N messages, paginate backwards.
- Per-user inbox / sync cursor for offline delivery and multi-device.
- Conversations and membership in a relational or KV store; users' profile elsewhere.

## Deep dives

- **Ordering**: assign a per-conversation increasing sequence (single partition owner, or Lamport-style counter at the conversation's home shard). Clients sort by sequence; retries dedupe by `message_id`.
- **Group messaging**: store one copy of the message per conversation; deliver to each member's connection. Small groups: fan-out on write to each member's inbox. Large groups/channels: fan-out on read with per-member last-read cursors.
- **Connection management**: gateway is stateless apart from sockets; registry maps `user -> gateway` with TTL heartbeat; on gateway crash, clients reconnect (jittered backoff) and sync from last seen sequence.
- **Presence**: heartbeat every ~5 s, TTL in Redis; publish changes only to online contacts who are viewing; last-seen persisted lazily.
- **Multi-device**: each device has its own inbox cursor; message fan-out to all of a user's devices.
- **Delivery guarantees**: at-least-once with client dedupe; server retries until ack; inbox retention (e.g. 30 days) for offline users.
- **Media**: upload to object storage, generate thumbnails asynchronously, send only URL/metadata in message.
- **Encryption**: E2E means server stores ciphertext and cannot index content; key exchange via prekeys.

## Failure scenarios

Gateway dies (reconnect + sync), message store shard lag (quorum writes), duplicate sends (message_id dedupe), push provider outage (queue and retry), thundering herd on reconnect after regional outage (jitter, admission control).

## Follow-ups

- Support message search? (Index only for non-E2E, or on-device.)
- Edit/delete/reactions? (Events referencing message_id.)
- Multi-region users? (Home region per user, cross-region relay.)
- How do you guarantee "exactly once" display?
