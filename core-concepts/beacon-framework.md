# Beacon Framework

> Two-tier authority framing for the regulated action apertures through which teleonomes affect the world. Beacons are pure I/O — calculation lives in synart-resolved code.

**Also known as:** beacon taxonomy, two-tier authority

## Definition

A beacon is a synome-registered, enforceable action aperture through which an embodied agent may affect the external world. Beacons are not entities — they are modes of action. A single teleonome may operate many beacons without revealing they are linked.

The load-bearing classification axis is **authority**:

| Tier | What it is |
|---|---|
| **High authority** | Certified by a synomic entity; auth-scoped to specific verbs/targets; operates a Synomic Entity (Prime / Halo / Generator / Guardian). Includes deterministic relayers, executors, and sentinel formations. |
| **Low authority** | No Synomic Entity operation. Either passive observation (reporting, scraping, attesting) OR direct teleonome-to-teleonome interaction (peer-to-peer trading, arbitrage, cooperation). |

Underneath authority, beacons divide by **I/O role** (input vs action — non-prescriptive working cut, not load-bearing). Input beacons (`market-data-beacon` / `attest-data-beacon` / `patch-beacon`) push data atoms into book spaces; endoscraper is no longer a beacon class but a grounded runtime primitive (`(chain-read $contract $slot)`) callable from any rule. Action beacons (relay / sentinel) emit chain transactions based on synart state. Calculation does not live in beacons — it lives in synart-resolved in-space computation that synserv runs against current input atoms.

Power-as-axis has retired. With cognition in synart, embodiment cognitive capability is no longer a load-bearing classification axis for beacons. Light/medium/heavy embodiment levels remain meaningful for hardware-aware cognition but don't classify beacons.

## Key Properties

- Beacons are apertures, not minds — they externalize intent, they don't have it
- All external action must flow through a registered beacon; unregistered action has no synomic legitimacy
- Beacons are registered, scoped (authority envelope), anchored (physical infrastructure), observable, and revocable
- **BEAMs** (Bounded External Access Modules) are on-chain authorized roles that make beacons high-authority in the smart-contract sense: pBEAM (process/execution), cBEAM (configuration), aBEAM (administration). Orthogonal to the beacon taxonomy.
- **Sentinel formations** are an operating setup that pairs three high-authority classes: `baseline-{prime}` (relay; decision/execution), `warden-{prime}-{op}` (relay; independent monitoring/risk enforcement), and `stream-{prime}-{actor}` (sentinel; data ingestion/sensing with call-out density into operator telart). `principal-{owner}` is a separate sentinel variant for owner-operated direct control (no formation).
- Stream-class sentinels carry call-out density and are operationally dominant — they act faster than governance processes; relays execute pre-agreed deterministic rules without call-outs.
- Multi-beacon reality: a teleonome may operate many beacons; aggregation occurs only when necessary (risk thresholds, enforcement)

## Relationships

- **implements:** [binding-mechanics](binding-mechanics.md) — beacons are the verification surface through which binding is enforced
- **defends-against:** [cancer-logic](cancer-logic.md) — beacons are revocable and observable, limiting blast radius of any compromised agent
- **requires:** [atlas-synome-separation](atlas-synome-separation.md) — beacon authority envelopes derive from governance via the Synome
