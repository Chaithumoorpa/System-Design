# Security Basics for Design Interviews

You are rarely asked for a deep security design, but strong candidates mention these at the right moment.

## Authentication vs authorisation

- **AuthN**: who are you? Passwords (hashed with bcrypt/argon2, salted), MFA, SSO, OAuth2/OIDC, API keys, mTLS between services.
- **AuthZ**: what may you do? RBAC (roles), ABAC (attributes), ACLs per resource. Enforce server-side on every request.

## Tokens

| | Session cookie | JWT |
|---|---|---|
| State | Server-side store | Self-contained, signed |
| Revocation | Easy (delete session) | Hard until expiry; use short TTL + refresh tokens + denylist |
| Scale | Needs shared store | Stateless verification |

OAuth2 in one line: user grants a client limited access to their resources at a provider, delivered as an access token (short-lived) plus refresh token (long-lived).

## Transport and data protection

- TLS everywhere; HSTS; mTLS for service-to-service.
- Encrypt at rest (disk/DB, envelope encryption with KMS); rotate keys.
- Never log secrets or PII; mask sensitive fields; use a secrets manager.
- Signed pre-signed URLs with short expiry for object access.

## Common attacks and defences

| Threat | Defence |
|---|---|
| SQL injection | Parameterised queries |
| XSS | Output encoding, CSP |
| CSRF | SameSite cookies, CSRF tokens |
| DDoS | CDN/WAF, rate limiting, autoscaling, anycast |
| Credential stuffing | Rate limits, MFA, breached-password checks |
| Insecure direct object reference | Authorise every resource access, do not trust IDs from clients |
| SSRF | Egress allow-lists, validate URLs |
| Replay | Nonces, timestamps, idempotency keys |

## Privacy and compliance

Data minimisation, retention limits, right-to-delete (GDPR) which affects backups, logs and derived data, data residency (regional storage), audit logging, PCI-DSS for card data (use a tokenising provider to keep card numbers out of your systems).

## Where to bring it up

- Payments: tokenisation, idempotency, audit trails.
- File sharing: access control lists, signed URLs, virus scanning.
- Public APIs: auth, rate limits, input validation.
- Multi-tenant systems: tenant isolation in data and cache keys.

## Interview questions

1. How would you revoke a JWT before expiry?
2. How do you store user passwords?
3. How do you securely let a client upload directly to object storage?

---

## 🔗 Used in these case studies

- [Payment System](../14-Payment-and-Financial-Systems/Payment-System/README.md)
- [File Storage and Sync](../10-Media-Streaming-and-Delivery/Google-Drive/README.md)
