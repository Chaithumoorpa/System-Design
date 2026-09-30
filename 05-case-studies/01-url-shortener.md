# Design a URL Shortener

**Prompt:** Users submit a long URL and get a short link that redirects to the original.

## Requirements

- Functional: create short URL (optional custom alias, expiry), redirect, optional click analytics, delete.
- Non-functional: very low redirect latency, high availability, read-heavy (~100:1), links must not collide, unpredictable codes preferred.
- Out of scope: user accounts UI, malware scanning (mention).

## Estimates

- 100M new URLs/month = ~40 writes/s; reads 100x = ~4,000/s average, ~20k/s peak.
- 5 years: 6B URLs x ~500 bytes = ~3 TB. Fits a modest sharded store; the cache holds hot links.
- Code length: base62, 7 chars = 62^7 ~ 3.5 trillion combinations, ample.

## API and data

```
POST /v1/urls {long_url, alias?, expires_at?} -> {short_url}
GET  /{code} -> 302 Location
```
Table `urls(code PK, long_url, user_id, created_at, expires_at)`. Access is key-value by `code`, so a KV/wide-column store (or sharded SQL) fits.

## High-level design

Client -> CDN/LB -> redirect service -> cache (Redis) -> DB. Create path: app -> ID/code generator -> DB.

## Deep dive 1: generating codes

| Approach | Pros | Cons |
|---|---|---|
| Hash long URL (MD5/SHA), take first 7 chars, resolve collisions | Stateless, same URL maps same code | Collisions need check and retry; predictable? no |
| Counter + base62 encode | No collisions, short | Sequential (guessable), central counter bottleneck |
| Pre-generated key pool (Key Generation Service) | Fast, no collision handling at write time | Extra service; must hand out keys atomically |
| Distributed unique ID (Snowflake) + base62 | Scalable, no coordination | Longer codes (~11 chars) |

Recommended: KGS hands out **ranges** of counter values to each app server (e.g. 1M at a time from a coordination store); each server encodes locally in base62 and optionally scrambles the number (bijective permutation) so codes are not sequential. Losing an unused range on crash is harmless.

## Deep dive 2: read path

- Cache-aside on `code -> long_url`, LRU, TTL. 80/20 rule: caching top 20% covers most traffic. Negative-cache misses.
- 301 vs 302: 301 is browser-cached (less load, no analytics); 302 keeps every click visible. Pick 302 if analytics matter.
- CDN can cache redirects for extremely popular links.

## Deep dive 3: analytics

Do not write to the DB on the redirect path. Emit a click event (code, time, user agent, coarse geo) to Kafka; stream-aggregate into a time-series/OLAP store. Redirect latency is unaffected.

## Expiry and cleanup

TTL on rows or a lazy check at read time; background job deletes expired links and recycles nothing (do not reuse codes quickly to avoid confusion).

## Failure and scaling

- Shard DB by `code` hash; replicate 3x; cache cluster sharded by consistent hashing.
- Abuse: rate limit creation per user/IP, blocklist domains, malware/phishing checks.
- Custom aliases: unique constraint returns 409 if taken.

## Follow-ups

- How do you avoid two users getting the same code under concurrency?
- Support link editing? (Invalidate cache on update.)
- Multi-region? (Replicate reads globally, writes to home region or use globally unique ranges.)
- What if the redirect service is 10x busier than estimated?
