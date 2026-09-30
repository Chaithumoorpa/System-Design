# 💬 Real-Time Communication — High Level Design

Systems that **move messages to people**: persistent connections, ordering, delivery guarantees,
queues, retries and priority isolation. Pairs with the LLD repo's *Chat Application* and
*Notification System*.

| # | Problem | Key ideas | Concepts to read first |
|---|---|---|---|
| 4 | [Chat System](ChatSystem/README.md) | WebSocket gateways, session registry, per-conversation sequence, persist-then-ack, sync cursors, watermark receipts | [Networking](../../01-foundations/03-networking-basics.md), [Messaging](../../02-core-concepts/09-messaging-and-streaming.md), [Real-time patterns](../../04-patterns/05-realtime-and-sync-patterns.md) |
| 5 | [Notification Service](NotificationService/README.md) | Priority-isolated queues, preferences, retries + DLQ, provider failover, campaigns | [Messaging](../../02-core-concepts/09-messaging-and-streaming.md), [Idempotency](../../04-patterns/01-idempotency.md) |

⬅️ Previous category: [Basics](../Basics/README.md) · ➡️ Next category: [Social and Content](../Social-and-Content/README.md)
