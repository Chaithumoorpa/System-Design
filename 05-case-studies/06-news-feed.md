# Design a News Feed (Twitter / Instagram style)

**Prompt:** Users post content, follow others, and see a ranked timeline of posts from people they follow.

## Requirements

- Functional: create post (text/media), follow/unfollow, home timeline, user timeline, like/comment (brief).
- Non-functional: feed load < 200 ms, heavily read-biased, eventual consistency acceptable (a post can appear seconds late), highly available, celebrities with tens of millions of followers.

## Estimates

- 300M DAU, feed opens 10/day = 3B feed reads/day = ~35k/s (peak ~100k/s). Posts: 100M/day = ~1.2k/s. Read:write ~ 30:1 at feed level, but fan-out amplifies writes.
- Average 200 followers: fan-out on write = 240k timeline inserts/s. Celebrity with 50M followers would be 50M writes per post; requires hybrid.

## High-level design

```
Post service -> Post store (sharded, by post_id) + Media -> Object store/CDN
     |-> Kafka "post_created" -> Fan-out workers -> Timeline cache (Redis: list of post_ids per user)
Follow graph service (sharded by user_id) for follower lists
Feed service: read timeline ids -> hydrate posts/users (multi-get from caches) -> rank -> return
```

## Deep dive 1: fan-out strategy

- **Push (on write)**: on post, write post_id into each follower's timeline list (bounded, e.g. last 800). Feed read is one cache lookup. Great for normal users.
- **Pull (on read)**: gather recent posts from each followee and merge. Needed for celebrities.
- **Hybrid** (recommended): push for accounts below a follower threshold; for celebrities, don't fan out. At read time, fetch the user's precomputed timeline and merge in recent posts from followed celebrities. Also skip fan-out to inactive users (no login in N days) and rebuild lazily when they return.

## Deep dive 2: storage

- Posts: KV/wide-column by `post_id`; user posts index `(user_id, time)`.
- Timeline: Redis list/sorted set of `(post_id, score)`; persisted as backup or rebuilt from post index.
- Follow graph: `followers(user_id -> list)` and `following(user_id -> list)`; paginated; graph DB not required.
- Counters (likes, comments): sharded counters or async aggregation; approximate display.

## Deep dive 3: ranking

Chronological is simplest. Ranked feed: candidate generation (timeline ids) -> features (affinity, recency, engagement, media type) -> lightweight model score -> diversity/dedupe filters. Keep ranking in a separate service; precompute features offline, look up online.

## Feed read path

1. Get timeline ids from cache (cursor pagination by post_id/score, not offset).
2. Merge celebrity posts.
3. Batch fetch post objects, author info, counters (cache multi-get).
4. Rank/filter (blocked users, deleted posts).
5. Return page with next cursor.

## Failure and edge cases

- Cache node loss: rebuild timeline from post index.
- Deleted or private posts: filter at read time (tombstones), async cleanup.
- Unfollow: remove from timeline lazily or filter at read.
- Hot posts: local caching, CDN for media, sharded counters.
- New user cold start: trending/suggested content.

## Follow-ups

- How do you keep timelines fresh for users following many celebrities?
- How would you add "For You" recommendations?
- What is the threshold for a celebrity and how do you pick it?
