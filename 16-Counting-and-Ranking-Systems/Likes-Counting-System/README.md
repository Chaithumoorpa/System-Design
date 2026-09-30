# 👍 Design a Likes Counting System — High Level Design

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Intermediate

⬅️ Previous: [Design Locking Service](../../15-Distributed-Infrastructure/Locking-Service/README.md) · 🏠 [Counting & Ranking Systems](../README.md) · ➡️ Next: [Design Real Time Leaderboard](../Real-Time-Leaderboard/README.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../../CREDITS.md).
<!-- nav:end -->

> "Count likes" is a hot-key problem in disguise: a viral post gets 100k likes/s on a single counter, every like must be
> deduplicated per user, and everyone wants to see the number instantly and to know whether **they** already liked it.

## 1. Clarifying Requirements

| Candidate asks | Interviewer answers | Design impact |
|---|---|---|
| Actions? | Like/unlike posts (and comments); show count and "liked by me". | Idempotent toggle. |
| Uniqueness? | One like per user per post. | Unique `(post,user)`. |
| Accuracy? | Displayed count can lag a few seconds, must converge to exact. | Eventual consistency. |
| Scale? | 5B likes/day, 100k likes/s on viral posts; 100B likes stored. | Hot key + huge storage. |
| Reads? | Every feed item shows count + my-like state (1M reads/s). | Batched multi-get. |
| Extras? | "Who liked" list, notifications. | Secondary indexes. |
| Abuse? | Bots, like farms. | Rate limits, detection. |

**Functional:** like/unlike, get count(s), check liked-by-me for many posts, list likers (paginated), notify author.
**Non-functional:** very high write throughput, low-latency reads, no double counting, tolerance for staleness, eventual exactness, hot-key resilience.

## 2. Back-of-the-Envelope Estimation

| Quantity | Working | Result |
|---|---|---|
| Likes | 5B/day | **~58k/s avg**, peak ~150–300k/s |
| Like record | (post 8 B, user 8 B, ts 8 B) ≈ 32 B | 160 GB/day; 58 TB/yr |
| Counters | 5B posts × 8 B | 40 GB (in memory feasible when sharded) |
| Reads | Feed items 1M/s × (count + liked-by-me) | Cache/batch essential |
| Hot post | 100k likes/s to one key | 1 Redis shard can't take it ⇒ split |

## 3. Core APIs

```http
PUT    /v1/posts/{id}/like            (idempotent: like)   → 204   {liked: true, count: 12034}
DELETE /v1/posts/{id}/like            (unlike)
GET    /v1/posts/counts?ids=1,2,3     → {1: 12034, 2: 88, 3: 2M}
POST   /v1/posts/liked-by-me {ids[]}  → {1: true, 2: false, ...}
GET    /v1/posts/{id}/likers?cursor=  → users (paginated)
```
Use `PUT/DELETE` for idempotency: retries don't double count.

## 4. High-Level Design

```mermaid
flowchart LR
    C[Client] --> API[Like API] --> LS[(Like store: (post,user) unique)]
    API --> K[[Kafka: like events by post_id]]
    K --> AGG[Aggregator: batch deltas per post/second] --> CTR[(Counter store: sharded Redis / DB)]
    K --> NT[Notifications, activity feed]
    API --> RC[(Redis: my-likes cache / Bloom)]
    R[Read path] --> CC[(Count cache)] --> CTR
    R --> RC & LS
    BATCH[Reconciliation job] --> LS & CTR
```

### 4.1 Write path
1. Insert `(post_id, user_id)` into the like store with a **unique constraint** (`INSERT ... ON CONFLICT DO NOTHING`); if it was new, emit `LikeAdded`. Unlike deletes and emits `LikeRemoved` (only if a row was deleted).
2. Event stream drives counter updates and notifications asynchronously. The API can return the optimistic count immediately.

### 4.2 Read path
Counts come from the counter cache (sharded counters summed or a periodically refreshed total); "liked by me" from a per-user cache/Bloom filter and the like store (batched multi-get by `(user, post_ids)`).

## 5. Database Design

```text
likes         PK (post_id, user_id) → created_at                      -- wide-column/KV partitioned by post_id (likers list)
user_likes    PK (user_id, post_id) → created_at                      -- reverse index for liked-by-me and "posts I liked" (partitioned by user_id)
counters      post_id → total (persisted); Redis: likes:{post}:{shard 0..N-1} for hot posts
events        Kafka topic like_events (key = post_id) → retention 3–7 days; archive to lake for reconciliation
```
Two writes (post-partitioned and user-partitioned) are made through the event stream or a transactional outbox so both indexes eventually agree.

## 6. Design Deep Dive

### 6.1 Deduplication (idempotency)
The unique `(post,user)` row *is* the truth: count = number of rows. Making the insert conditional guarantees at-most-once counting per user despite retries. For extreme scale, use a Bloom filter (or per-user recent-likes set) as a fast pre-check
to avoid hitting the store for already-liked items, with the store as the authority. See [Preventing Duplicate Processing](../../05-Interview-Patterns/10-preventing-duplicate-processing.md).

### 6.2 Counter strategies
| Strategy | Pros | Cons |
|---|---|---|
| `UPDATE count = count+1` per like | Exact, simple | Hot-row contention; low throughput |
| **Sharded counters** (`k` sub-counters, random increment, sum on read) | Removes contention | Read cost ×k; cache the sum |
| Buffer in memory/Redis and flush batches | Cuts DB writes 100–1000× | Loss window (mitigate via event log) |
| **Stream aggregation** (Kafka → aggregate deltas per post per second → update) | Exactness via replay, backpressure | Slight delay |
| Count from likes table on demand | Always exact | Too slow at scale |
Combine: sharded Redis counters for immediate display + stream aggregation persisting exact totals + periodic reconciliation.

### 6.3 Hot keys
A viral post overloads one partition/counter: shard counters by `post_id#rand(0..N)` **only for hot posts** (detect via sampling, or shard everything above a threshold); local in-process aggregation on API servers (sum deltas for 200 ms then send one increment);
cache count reads with a short TTL and serve slightly stale numbers ("1.2M"). See [Handling Hot Keys](../../05-Interview-Patterns/03-handling-hot-keys.md).

### 6.4 Display formatting and consistency
Users don't need exact numbers for big counts: show abbreviations ("1.2M"); the author's own like (optimistic UI) is shown immediately; eventual convergence within seconds. Consistency need is low; correctness need is on **uniqueness** and **eventual exactness**.

### 6.5 Liked-by-me at feed scale
Feed loads 20–50 posts: one batched call `MGET user_likes:{user}:{post}` or a per-user Bloom/set cache of recent likes; fall back to the reverse index (`user_likes`) point reads by `(user, post)` in a multi-get; cache results per session.

### 6.6 Reconciliation and repair
Nightly job recomputes counts from the immutable like log/table and corrects counters (compare, fix with adjustment). Detect drift (>0.1%) and alert. Deleted posts/accounts trigger cleanup jobs (remove likes, decrement counters, purge caches).

### 6.7 Abuse controls
Per-user like rate limits, bot/like-farm detection (velocity, graph clustering), delayed/quarantined counting for suspicious accounts, ability to retract fraudulent likes (events remove rows and adjust counters).

## 7. Follow-ups (with answers)

**7.1 How do you prevent a user from liking twice under concurrent requests?** The unique `(post,user)` constraint: only one insert succeeds; the second is a no-op, and no second event is emitted.

**7.2 How do you keep counts accurate if the aggregator crashes?** Kafka retains events; the consumer replays from the last committed offset; idempotent updates (apply delta by event id/offset or recompute from source) plus the nightly reconciliation.

**7.3 How do you show the count on 50 posts per feed load cheaply?** Batch `MGET` on count cache keys, populated by the aggregator; misses fall back to the counter store in one batched query.

**7.4 How would you support "list of likers" for a post with 5M likes?** Paginated range scan on `(post_id, created_at)` partition (bucketed by time to bound partition size); cache the first page; don't allow arbitrary deep pagination.

**7.5 What if you need an exact count for billing/reporting?** Use the immutable events/likes table with a batch aggregation (Spark) as the source of truth; the online counter is a display cache.

**7.6 How do you count views (much higher volume than likes)?** Same pattern but weaker uniqueness: sampled or approximate counting, HyperLogLog for unique viewers, batching aggressively; views rarely need dedupe per user.

## 🧪 Practice Round

<details><summary>Why PUT/DELETE rather than POST for likes?</summary>
They are idempotent by definition: repeating "like" yields the same state, so retries are harmless.
</details>

<details><summary>Why can the displayed count lag but uniqueness cannot?</summary>
Users tolerate a slightly stale number, but double-counting or losing a like corrupts the data permanently; the unique row keeps truth intact while counters converge.
</details>

## 📝 Last-Minute Revision

Truth = unique `(post,user)` rows (both directions indexed); events via Kafka → **batched delta aggregation** into **sharded counters**; count cache + Bloom/set for liked-by-me; hot-post shard splitting and local aggregation; nightly reconciliation; approximate display for big numbers.

Related: [Counting at Scale](../../05-Interview-Patterns/20-counting-at-scale.md) · [Handling Hot Keys](../../05-Interview-Patterns/03-handling-hot-keys.md) · [Instagram](../../09-Social-Media-Systems/Instagram/README.md)
