# Microservices and Service Communication

## Monolith vs microservices

| | Monolith | Microservices |
|---|---|---|
| Deploy | One unit | Independent per service |
| Complexity | In the code | In the network and operations |
| Scaling | Whole app | Per service |
| Data | One shared DB | Database per service |
| Team fit | Small teams, early stage | Many teams, clear domain boundaries |

Good answer: start with a **modular monolith**, extract services when team size, scaling profile or release cadence demand it. Microservices add latency, partial failure, distributed transactions, and debugging cost.

## Service boundaries

Split by business capability (domain-driven design bounded contexts), not by technical layer. Each service owns its data; others access it through its API or events, never its tables.

## Communication styles

| Style | Pros | Cons |
|---|---|---|
| Synchronous (REST/gRPC) | Simple, immediate response | Coupling, cascading failures, latency chain |
| Asynchronous (events/queues) | Decoupled, resilient, scalable | Eventual consistency, harder tracing |

Use sync for queries that need an immediate answer; async for workflows and side effects.

## Supporting infrastructure

- **Service discovery**: registry (Consul, Eureka, Kubernetes DNS) so services find instances; client-side or server-side.
- **API gateway**: single entry, auth, routing, rate limiting, aggregation (BFF pattern for per-client backends).
- **Service mesh** (Istio, Linkerd): sidecar proxies handle mTLS, retries, timeouts, telemetry uniformly.
- **Config and secrets management**: central, versioned, rotated.
- **Contract testing and versioning**: backward-compatible changes, consumer-driven contracts.

## Data across services

- No cross-service joins: use API composition, or replicate needed data via events into a local read model (CQRS).
- Distributed transactions: sagas plus outbox. See [patterns](../04-patterns/).
- Shared IDs and events carry all data consumers need to reduce chatty calls.

## Anti-patterns

Distributed monolith (services must deploy together), shared database, chatty fine-grained calls, synchronous chains of five services, no ownership.

## Interview questions

1. When would you not use microservices?
2. Order service needs user info from user service on every request. Options to avoid coupling and latency?
3. How does a saga differ from a distributed transaction?
4. What does a service mesh give you that a library does not?
