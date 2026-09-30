# Load Balancing

A load balancer (LB) spreads requests across backends to improve throughput, availability and latency.

## Types

| Layer | Sees | Examples | Use |
|---|---|---|---|
| L4 | IP, port, TCP/UDP | AWS NLB, IPVS, HAProxy TCP | Very high throughput, non-HTTP protocols |
| L7 | Full HTTP | Nginx, Envoy, ALB | Path/header routing, TLS termination, retries, canaries |

Also: **DNS load balancing** (coarse, TTL-limited), **global server load balancing** (geo routing between regions), **client-side LB** (client picks from a service registry, used in gRPC and service meshes).

## Algorithms

| Algorithm | Idea | Good when |
|---|---|---|
| Round robin | Rotate through servers | Homogeneous servers, uniform requests |
| Weighted round robin | More traffic to bigger servers | Mixed hardware |
| Least connections | Pick server with fewest open connections | Long-lived or uneven requests |
| Least response time | Prefer fastest recent server | Latency-sensitive |
| IP / key hash | Same key goes to same server | Stickiness, cache affinity |
| Consistent hashing | Minimal remapping when servers change | Caches, sharded backends |
| Power of two choices | Pick two at random, choose the less loaded | Large fleets; avoids herding |

## Health checks

- **Active**: LB probes `/health` periodically.
- **Passive**: LB marks a backend unhealthy after observed errors or timeouts.
- Distinguish **liveness** (process up) from **readiness** (ready for traffic, dependencies OK). A bad readiness check that depends on a shared database can take the whole fleet out at once.

## Sticky sessions

Route a user to the same server (cookie or IP hash). Convenient for in-memory sessions but hurts balance and failover. Prefer stateless servers plus shared session store.

## High availability of the LB itself

- Active-passive pair with virtual IP and failover, or active-active behind anycast/DNS.
- Managed cloud LBs are already redundant across zones.

## Related concerns

- **TLS termination**: at the LB to offload crypto; re-encrypt to backends if the internal network is untrusted.
- **Connection draining**: finish in-flight requests before removing a server during deploys.
- **Slow start**: ramp traffic to a new instance so cold caches do not overload it.
- **Retries**: retry only idempotent requests, with budgets, or you create retry storms.
- **Rate limiting and circuit breaking** commonly live in the same proxy layer.

## Interview questions

1. Round robin vs least connections: when does round robin fail?
2. How do you load balance WebSocket connections and later rebalance them?
3. The LB is healthy but one backend is slow, not down. What do you do?
4. How would you do a canary release using the LB?

---

## 🔗 Used in these case studies

- [Chat System](../08-Real-Time-Communication/WhatsApp/README.md)
- [URL Shortener](../07-Basic-Questions/URL-Shortener/README.md)
