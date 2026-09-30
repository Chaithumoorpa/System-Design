# Requirements and API Design

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Caching](02-caching.md) · 🏠 [Concept Deep Dives](README.md) · ➡️ Next: [Database Design](04-database-design.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

## Functional vs non-functional

**Functional**: what the system does ("user can post a photo", "follow another user").
**Non-functional (NFRs)**: how well it does it.

| NFR | Question to ask | Design impact |
|---|---|---|
| Scalability | Users, QPS, data growth? | Sharding, caching, async |
| Latency | p50/p99 targets? | Cache, CDN, precompute |
| Availability | Nines? Tolerate region loss? | Replication, failover, multi-region |
| Consistency | Can users see stale data? | Sync vs async replication, quorum |
| Durability | Can we ever lose data? | Replication, backups, WAL |
| Ordering | Must events be ordered? | Partitioning key, sequence numbers |
| Security/privacy | PII, compliance? | Encryption, access control, retention |
| Cost | Budget constraints? | Storage tiers, compression |

Always pick the **2-3 NFRs that dominate** and say so ("this is read-heavy and latency-sensitive; eventual consistency is fine").

## API style choices

| Style | Good for | Notes |
|---|---|---|
| REST over HTTP/JSON | Public APIs, CRUD, cacheable reads | Resource-oriented, simple, human-readable |
| gRPC (HTTP/2 + protobuf) | Internal service-to-service, streaming | Compact, typed, low latency, harder from browsers |
| GraphQL | Varied client needs, mobile bandwidth | Client picks fields; watch N+1 and query cost |
| WebSocket | Bi-directional real-time | Stateful connections, need sticky routing or pub/sub |
| SSE | Server-to-client push only | Simple, auto-reconnect over HTTP |
| Webhooks | Server-to-server callbacks | Need retries, signatures, idempotency |

## REST design checklist

- Nouns for resources, verbs via HTTP methods: `POST /orders`, `GET /orders/{id}`.
- Correct status codes: 201 created, 400 bad input, 401/403 auth, 404, 409 conflict, 429 rate limited, 5xx server.
- **Idempotency**: PUT and DELETE idempotent by definition; make POST safe with an `Idempotency-Key` header.
- **Pagination**: prefer cursor-based (`?cursor=abc&limit=20`) over offset for large or changing data. Offset gets slower as it grows and skips or repeats rows on concurrent inserts.
- **Versioning**: `/v1/...` or header-based; never break existing clients.
- **Filtering and sorting** via query params; whitelist fields.
- **Rate limiting** headers, and consistent error shape.
- **Auth**: OAuth2 / JWT / API keys; never put secrets in URLs.

### Cursor pagination example

```
GET /v1/users/42/posts?limit=20&cursor=eyJ0cyI6MTcwMDAwMDAwMH0
200 OK
{ "items": [...], "next_cursor": "eyJ0cyI6MTY5OTk5OTk5OX0" }
```

The cursor encodes the last-seen sort key (for example timestamp + id), and the query becomes `WHERE (ts, id) < (?, ?) ORDER BY ts DESC, id DESC LIMIT 20`.

## Data modelling process

1. List entities and relationships (1:1, 1:N, N:M).
2. List **access patterns** in order of frequency ("get feed for user", "get post by id").
3. Choose storage to match: relational for joins and transactions, wide-column/KV for known-key scale, document for nested aggregates, graph for traversals, search index for text.
4. Decide primary key and secondary indexes per access pattern.
5. Decide what is denormalised and how it is kept in sync.

## Example: URL shortener API

```
POST /v1/urls      { "long_url": "...", "custom_alias": "opt", "expires_at": "opt" }
                   -> 201 { "short_url": "https://sho.rt/aZ3k9Q" }
GET  /{code}       -> 301/302 Location: long_url
DELETE /v1/urls/{code}
```

Interview point: 301 (permanent, browsers cache, fewer hits, no click analytics) vs 302 (temporary, every click hits you, enables analytics).

## Practice

1. Design the API for a ride-hailing app's "request ride" and "driver location update". Which is REST and which is not?
2. Why is offset pagination a problem on a feed with millions of rows and constant inserts?
3. A client retries `POST /payments` after a timeout. How does your API prevent double charges?

---

## 🔗 Used in these case studies

- [URL Shortener](../07-Basic-Questions/URL-Shortener/README.md)
- [Ride Hailing](../11-Location-Based-Services/Uber/README.md)
- [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md)
