# Pattern: Running Across Multiple Regions

<!-- nav:start -->
🏷️ **Priority:** Medium · **Difficulty:** Advanced

⬅️ Previous: [Preventing Duplicate Processing](10-preventing-duplicate-processing.md) · 🏠 [Interview Patterns](README.md) · ➡️ Next: [Coordinating Transactions Across Services](12-coordinating-transactions-across-services.md)

> 📚 **Credit:** Chapter selection, ordering and question choice follow the [AlgoMaster.io System Design Interviews course](https://algomaster.io/learn/system-design-interviews/course-roadmap). This write-up was created with Claude for personal interview prep. The premium lesson text was **not** accessed or reproduced. See [CREDITS](../CREDITS.md).
<!-- nav:end -->

**Problem:** Serve users worldwide with low latency, survive a regional outage, and meet data-residency
laws, without turning consistency and operations into chaos.

## Why go multi-region (and when not to)

| Goal | Meaning | Needs multi-region? |
|---|---|---|
| Latency | Users far from the region see 150–300 ms RTT | Reads yes; writes maybe |
| Availability / DR | Survive region failure (RTO/RPO targets) | Yes, at least warm standby |
| Compliance | Data must stay in a country/region | Yes for that data |
| Scale | Spread load | Rarely the main reason |

Multi-region multiplies cost and complexity. If one region + multi-AZ meets the SLO, stay there and
add a DR plan.

## Deployment models

| Model | Description | RPO/RTO | Complexity |
|---|---|---|---|
| Backup & restore | Snapshots in another region | Hours | Low |
| Pilot light | Minimal core running in DR region | Minutes–hours | Low-med |
| Warm standby | Scaled-down full stack, async replication | Minutes | Medium |
| **Active-passive** | One region takes writes; others read/standby | Seconds–minutes | Medium |
| **Active-active** | All regions serve writes | Near zero | High |

## Traffic routing

- **Geo DNS / latency-based routing / anycast** to the nearest healthy region.
- **Health checks** and automated failover (mind DNS TTL and resolver caching).
- Global load balancers and CDNs (edge terminates TLS near users).
- Region affinity: pin a user session to a "home" region to avoid cross-region ping-pong.

## Data strategies

### 1. Home region per user/entity (partition by geography)
Each entity has one writable home; other regions read replicas or route writes to the home. No write
conflicts. Failover = promote another region as home (with RPO consideration). Common and pragmatic.

### 2. Single-leader global with regional read replicas
Writes go to the leader region (higher write latency for remote users); reads local. Simple; async
replication lag means stale reads and possible data loss on failover.

### 3. Multi-leader / active-active
Each region accepts writes and replicates asynchronously. Requires **conflict resolution**:
last-write-wins (loses data), application merge, **CRDTs** (counters, sets), or avoiding conflicts by
ownership. Used by DynamoDB global tables, Cassandra multi-DC, CockroachDB/Spanner (consensus-based,
higher write latency).

### 4. Globally consistent (Spanner-style)
Consensus across regions with TrueTime; strong consistency at the cost of cross-region commit latency
(tens to hundreds of ms).

## Consistency choices by data type

| Data | Approach |
|---|---|
| Static/media | CDN + replicated object storage |
| Profiles, catalogue | Async replicated, read locally |
| Sessions | Regional store; sticky home region |
| Counters/likes | CRDT or regional counts merged |
| Money/inventory | Single home/leader or strongly consistent store |
| Config/feature flags | Replicated config service |

## Failure and failover

- Define **RPO/RTO** per data class; test failover regularly (game days).
- Avoid **split brain**: fence the old region (epoch/lease); do not let both accept writes to the same entity.
- **Failback** plan: reconcile data written during the outage.
- Capacity: surviving regions must absorb the failed region's load (N+1 regions).
- Shared-fate dependencies (global DNS, identity, control plane) must themselves be redundant.

## Cross-region costs and pitfalls

- Egress bandwidth is expensive; minimise chatty cross-region calls, especially synchronous ones on the hot path.
- Clock skew between regions; use logical clocks or per-entity versions.
- Replication lag causes read-your-writes bugs: route the writer to their home region briefly, or use session tokens.
- Compliance: replicas and backups also count as data location.
- Deployment: staged rollouts region by region; config drift is a common outage source.

## Worked example: ride-hailing

Each city (region) runs an independent stack: location index, matcher, trip DB. Global services (accounts, payments) are replicated. A regional failure affects only that city; users are pinned by geography.

## Interview questions (with answers)

**Q1. How do you make a user profile service multi-region?** Home region per user for writes, async replication to other regions for reads, session token/versions for read-your-writes, DNS/anycast routing, and a failover procedure that promotes another region.

**Q2. Active-active vs active-passive?** Active-active gives lower latency and near-zero RTO but needs conflict handling and is costlier; active-passive is simpler and avoids conflicts at the price of failover time and idle capacity.

**Q3. How do you avoid split brain during failover?** Quorum/consensus for the leadership decision, leases with expiry, and fencing tokens so the old primary's writes are rejected.

**Q4. Which data should never be multi-master with LWW?** Financial balances, inventory counts, anything where lost updates cause real damage.

## Last-minute revision

Only if needed. Prefer **home-region ownership**; active-active needs conflict resolution (CRDT/merge); test failover; watch replication lag, egress cost and shared-fate dependencies.

Related: [Replication](../03-Concept-Deep-Dives/05-Distributed-Systems/01-replication.md) · [Consistency and CAP](../03-Concept-Deep-Dives/05-Distributed-Systems/03-consistency-and-cap.md) · [Surviving Component Failures](09-surviving-component-failures.md)
