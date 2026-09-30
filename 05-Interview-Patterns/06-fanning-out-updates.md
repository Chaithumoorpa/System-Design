# Pattern: Fanning Out Updates

<!-- nav:start -->
🏷️ **Priority:** High · **Difficulty:** Intermediate

⬅️ Previous: [Pushing Real-time Updates](05-pushing-realtime-updates.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Uploading and Serving Large Files](07-uploading-and-serving-large-files.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** One event must reach many recipients: a post to followers, a price change to watchers,
a notification to a segment, an invalidation to all caches.

## Recognise it when

- "Followers", "subscribers", "notify everyone", "timeline", "broadcast".
- Recipient counts vary wildly (most have 100, a few have 50M).

## Two basic strategies

| | Fan-out on write (push) | Fan-out on read (pull) |
|---|---|---|
| Work done | At publish time: write to each recipient's inbox | At read time: gather from sources |
| Read latency | Very low (one lookup) | Higher (merge many sources) |
| Write cost | O(followers) | O(1) |
| Wasted work | Writes for inactive recipients | None |
| Storage | Duplicates per recipient (ids only) | Minimal |
| Best for | Typical users, read-heavy | Celebrities, rarely-read data |

## Hybrid (the usual answer)

- **Push** for authors under a follower threshold (say 10k–100k).
- **Pull/merge** at read time for high-follower authors.
- **Skip inactive users** (no login in N days); rebuild their inbox on return.
- Bound inbox size (e.g. 800 ids); older content served by pull.

```
publish → Kafka(post_created) → fan-out workers → page followers → write ids to Redis timelines
read → timeline ids (push part) + recent posts of followed celebrities (pull part) → hydrate → rank
```

## Fan-out via messaging systems

| Need | Mechanism |
|---|---|
| Independent consumers (billing, email, analytics) | Pub/sub topic with a subscription (queue) per consumer (SNS→SQS, Kafka consumer groups) |
| Broadcast to online users | Pub/sub per room/topic + gateway local fan-out |
| Broadcast to mobile devices | Push provider topics (FCM topics) or sharded workers |
| Cache invalidation | Fan-out invalidation messages to all app servers (pub/sub) |

## Making fan-out workers robust

- Partition by author/entity for ordering; **batch followers** (10k per page) to avoid huge in-memory lists.
- **Idempotent writes** (adding an id to a sorted set twice is harmless).
- Rate limit and prioritise (VIP recipients first, or recent-active first).
- Retry with backoff; DLQ; track progress so a crash resumes where it stopped.
- Backpressure through queue lag; autoscale workers.

## Ordering and freshness

Timelines sort by time or rank score. Late fan-out may insert older items after newer; use score-based
sorted sets, not append-only lists. Accept seconds of delay; show "new posts" banners.

## Deletes, unfollows, privacy

Filter at read time (authoritative), clean inboxes lazily. Never rely on fan-out cleanup for correctness.

## Amplification math (do it out loud)

`writes/s = posts/s × avg followers`. Example: 1.2k posts/s × 200 = 240k inbox writes/s (fine);
one 50M-follower post = 50M writes, which the hybrid avoids.

## Pitfalls

- Fan-out synchronously in the request path.
- Storing full post bodies in every inbox (store ids).
- No cap on inbox length; no strategy for inactive users.
- Treating pull as free (celebrity reads still need heavy caching).

## Interview questions (with answers)

**Q1. A user with 50M followers posts. What happens?** Not fanned out; stored once; readers merge that author's recent posts at read time from a heavily cached source; push continues for others.

**Q2. Why store only post IDs in timelines?** Small, dedupe-friendly; bodies are fetched from a post cache, so edits/deletes apply everywhere instantly.

**Q3. How do you fan out a notification to 10M users without melting providers?** Shard the audience across many workers with per-provider rate limits, prioritise by segment, use provider topic broadcasts where available, and track progress for pause/resume.

## Last-minute revision

Push vs pull → **hybrid** with a celebrity threshold, skip inactive, bounded inboxes; store ids; idempotent batched workers; filter at read time.

Related: [FB News Feed](../09-Social-Media-Systems/FB-News-Feed/README.md) · [Notification Service](../17-Asynchronous-Systems/Notification-Service/README.md) · [Fan-out notes](../_Reference/fanout-and-hot-keys.md)
