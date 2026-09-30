# Design a Ride-Hailing Service (Uber / Lyft style)

**Prompt:** Riders request rides; nearby drivers are matched; trips are tracked and paid.

## Requirements

- Functional: rider requests ride, system finds nearby drivers, driver accepts, live tracking, ETA and fare, trip completion and payment.
- Non-functional: matching in seconds, very high location update rate, high availability, correctness (a driver gets one ride at a time), regional isolation.

## Estimates

- 1M concurrent drivers sending location every 4 s = 250k updates/s. Ride requests ~ few thousand/s peak. Location data is ephemeral: keep latest position in memory, archive samples for analytics.

## High-level design

```
Driver app --location--> Location service (gateway) --> In-memory geo index (sharded by cell/region)
                                  '--> Kafka -> trip trace store / analytics
Rider request -> Ride service -> Matching/Dispatch -> candidate drivers (geo query) -> offer to driver(s)
Trip service (state machine) <-> Payments, Pricing, Maps/ETA, Notifications
```

## Deep dive 1: location indexing

- Partition the world by geo cells (geohash prefix, S2, or H3). Each cell (or group) is owned by a shard holding an in-memory map of drivers in it. A driver's update moves it between cells.
- Nearby query: covering cells of radius around the pickup (plus neighbours), collect drivers, filter by availability, rank by ETA (road distance from a routing service, not straight line).
- Redis GEO / custom service; TTL removes stale drivers. Do not write every ping to a disk DB.
- Update volume: send location adaptively (more often when on trip, less when idle), batch over persistent connections.

## Deep dive 2: matching / dispatch

- Simple: nearest available driver. Better: minimise pickup ETA, consider driver rating, direction of travel, batching requests over a short window (a few seconds) for a global assignment (bipartite matching) across nearby riders and drivers.
- **Offer flow**: send offer to driver with timeout (~10-15 s); on decline/timeout go to the next candidate. Lock a driver while an offer is outstanding so two riders cannot get the same driver: atomic state transition `AVAILABLE -> OFFERED(trip)` in a store (conditional write / Redis Lua) with expiry.
- Trip state machine: REQUESTED, MATCHING, DRIVER_ASSIGNED, ARRIVED, IN_PROGRESS, COMPLETED, CANCELLED. Persist transitions in a durable DB; events published to Kafka.

## Deep dive 3: ETA, pricing, tracking

- **ETA/routing**: road graph with live traffic, precomputed hierarchies (contraction hierarchies); cache popular routes; ML correction.
- **Surge pricing**: compute supply/demand per cell every N seconds (streaming aggregation), multiplier applied per cell; smoothing to prevent oscillation.
- **Live tracking**: rider app subscribes (WebSocket/SSE) to the trip channel; driver locations pushed via pub/sub.
- **Payments**: authorisation at request, capture at end; idempotent, saga-based. See [payment system](16-payment-system.md).

## Failure and scaling

- Shard by city/region so an outage is contained; drivers/riders pinned to region.
- Location shard failure: drivers re-announce within seconds; index rebuilds itself from fresh pings.
- Trip data durable (replicated DB); location data lossy by design.
- Fraud: GPS spoofing detection, speed sanity checks.

## Follow-ups

- Ride pooling / shared rides? (Route insertion optimisation.)
- Handle airport queues and fairness?
- Predict demand to reposition drivers?
