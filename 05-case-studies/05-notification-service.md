# Design a Notification Service

**Prompt:** Send push, SMS, email and in-app notifications on behalf of many internal services, at scale.

## Requirements

- Functional: multi-channel delivery, templates, user preferences and opt-outs, scheduling, priorities (OTP vs marketing), delivery tracking.
- Non-functional: OTP within seconds, marketing bursts of millions, at-least-once with dedupe, no user spammed, provider failures tolerated.

## Estimates

- 10M users, 5 notifications/day = 50M/day (~600/s avg) but campaigns of 10M in minutes -> 10-50k/s bursts. Queues absorb the burst.

## High-level design

```
Producers (services/campaigns) -> Notification API -> validate, dedupe, prefs check
      -> Kafka topics per channel & priority -> Channel workers -> Providers (APNs/FCM, SMS, Email)
      -> Delivery events (callbacks/webhooks) -> Status store + analytics
```

Components: Template service, Preference/consent service, Device token registry, Scheduler, Rate limiter per user and per provider, Status tracker.

## Flow

1. Caller sends `{user_id, type, template, params, idempotency_key, priority}`.
2. API checks idempotency key, preferences (channel opt-in, quiet hours, frequency caps), resolves channels and device tokens.
3. Enqueue to `push.high`, `sms.high`, `email.bulk` etc. Separate topics stop bulk traffic delaying OTPs.
4. Workers render template, call provider with timeouts, retry with backoff (respect provider rate limits), send to DLQ after N attempts, fall back to a secondary provider.
5. Provider callbacks (delivered, bounced, unsubscribed) update status and suppression lists.

## Deep dives

- **Priority isolation**: dedicated queues and worker pools per priority and channel.
- **Idempotency and dedupe**: key = `(user, type, event_id)`; workers check before send; provider-side idempotency where supported. Accept rare duplicates over losses for non-critical notices.
- **Fan-out for campaigns**: a campaign job pages through the audience in batches and enqueues per-user messages; throttle to provider and infrastructure limits; support pause/cancel.
- **Preferences and compliance**: unsubscribe handling (legal), quiet hours by time zone, frequency capping via Redis counters, suppression lists for bounces.
- **Device tokens**: users have many devices; remove invalid tokens on provider feedback; token refresh.
- **Provider failures**: circuit breaker per provider, failover to backup provider, exponential backoff.
- **Scheduling**: delayed queue or scheduler service using due-time index.
- **Templates and localisation**: versioned, rendered at send time.
- **Tracking**: notification ID stored with state machine (queued, sent, delivered, opened, failed).

## Follow-ups

- Guarantee an OTP arrives in <5 s during a marketing blast? (Isolation, reserved capacity.)
- Avoid sending the same alert on push and email simultaneously? (Channel escalation policy.)
- Millions of tokens per topic? (Provider topics vs per-token fan-out.)
