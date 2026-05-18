---
cssclass: wide-mermaid
cssclasses:
  - wide-mermaid
---

# Sigil Show

Grounded atoms, sigils, workcells, and P1 boot.

Designed for screensharing.



---



## The Old Problem

`grounded atom` is too broad.

It hides three different things:

```text
values
evaluation control
executable powers
```



```mermaid
flowchart TD
  G["grounded atom<br/>(old broad term)"]
  L["literal<br/>grounded value"]
  F["special form<br/>evaluator control"]
  S["sigil<br/>grounded callable"]

  G --> L
  G --> F
  G --> S
```



---



## The New Split

```text
literal
  value

special form
  evaluator control

sigil
  executable power
```



```mermaid
flowchart LR
  L["42<br/>string<br/>true"] --> LV["literal"]
  F["IF<br/>LET<br/>MATCH<br/>QUOTE"] --> FV["special form"]
  S["ADD<br/>SHA256<br/>CHAINREAD"] --> SV["sigil"]
```



---



## Visual Rule

```text
lowercase = meaning
ALL CAPS  = power
$         = variable
&         = Space
numbers   = literals
```



```synlang
$borrower
&entity.halo.spark-term
loan-health
42
ADD
CHAINREAD
```



---



## Atom Classes

```mermaid
flowchart TD
  A["atom"]

  A --> SYM["symbol<br/>borrower<br/>riskbook-attestation"]
  A --> VAR["variable<br/>$borrower"]
  A --> SP["Space ref<br/>&core.settlement"]
  A --> LIT["literal<br/>42<br/>true"]
  A --> EX["expression<br/>(ADD 1 2)"]

  EX --> FORM["special-form expression<br/>(IF $ok pass fail)"]
  EX --> CALL["sigil call<br/>(CHAINREAD ...)"]
```



---



## Literal

Grounded value.

No special marker.



```synlang
42
3.14
"hello"
true
```



Built into Noemar parser and evaluator.

Small fixed set.



---



## Special Form

Evaluator-native control.

Arguments are **not** evaluated by normal call rules.



```synlang
(IF $healthy
    pass
    fail)
```



Only one branch evaluates.

That is why `IF` is not a normal function.



---



## Sigil

Grounded callable.

Arguments evaluate normally.

Then the sigil resolves through a binding.



```synlang
(ADD 1 2)
```



```mermaid
sequenceDiagram
  participant E as Evaluator
  participant B as Binding
  participant I as Implement

  E->>E: evaluate 1
  E->>E: evaluate 2
  E->>B: resolve ADD
  B->>I: call add.v1
  I-->>E: 3
```



---



## Special Form vs Sigil

```text
special forms govern evaluation

sigils compute
```



```mermaid
flowchart LR
  IF["IF"] --> CTRL["controls<br/>which branch evaluates"]
  QUOTE["QUOTE"] --> CTRL2["prevents<br/>evaluation"]
  ADD["ADD"] --> COMPUTE["computes<br/>after args evaluate"]
  CHAINREAD["CHAINREAD"] --> POWER["calls<br/>external read power"]
```



---



## Closed Core, Open Powers

```text
literals
  small fixed language substrate

special forms
  small fixed evaluator substrate

sigils
  open-ended governed capability layer
```



```mermaid
flowchart TD
  N["Noemar core"]
  C["closed core<br/>literals + special forms"]
  O["open governed layer<br/>sigils + bindings"]

  N --> C
  N --> O

  C --> RARE["changes require<br/>runtime/language evolution"]
  O --> GROW["grows with<br/>synome capabilities"]
```



---



## Engineering Rule

```text
Adding a literal type changes the language.

Adding a special form changes the evaluator.

Adding a sigil changes the binding catalog.
```



That is the point of the split.



---



## Sigil Stack

```text
sigil
  synlang name for a power

binding
  governed wiring

implement
  controlled executable adapter

workcell
  externally situated operational setup
```



```mermaid
flowchart LR
  S["sigil<br/>CHAINREAD"]
  B["binding<br/>chainread-eth-mainnet-v1"]
  I["implement method<br/>eth-mainnet-connector.read-slot.v1"]
  H["workcell hub<br/>eth-mainnet-workcell-hub"]
  C["workcell components<br/>full node<br/>archive node<br/>RPC"]

  S --> B --> I --> H --> C
```

!(CHAINREAD 0x12837612847562746237wrerh)
(eth-tx from sfdisajfoiajsd to blabalabal sent 2000 eth)
($match eth-tx from spark-pau to spark-halo sent $_ eth) -> (2000)

CHAINREAD -> bind to -> C:user/path/to/chainread.py

---



## Sigil

The synlang-side callable symbol.



```synlang
(CHAINREAD ethereum
   collateral-account-001
   (balance btc)
   $block-ref)
```



The sigil is **not** the program.

The sigil is the name of the power.



---



## Binding

The governed mapping.



```text
sigil: CHAINREAD
binding-id: chainread-eth-mainnet-v1
implement: C:path/to/eth-mainnet-connector
method: read-slot
version: v1
mode: exo-implement
traits: [read-only, consensus-backed]
determinism: deterministic-at-block
verification: block-ref + proof policy
```



Binding answers:

```text
what code?
what method?
what types?
what authority?
what effects?
what proof / provenance?
```



---



## Implement

The controlled executable adapter.

Usually code.

Often Python in P1.



```text
eth-mainnet-connector.read-slot.v1
```



The implement method is what Noemar can actually call.

It should have a narrow typed interface.



---



## Implement Artifact

The source/package Noemar can materialize.



```text
implement-artifact:
  id: eth-mainnet-connector-v1
  language: python
  source-hash: sha256:...
  entrypoint: eth_mainnet_connector:read_slot
  tests: chainread-conformance-v1
  sandbox: no-network-except-workcell-hub
```



P1 can be simple:

```text
mega .synlang file contains implement source strings or artifact refs

bootstrap writes them to disk

bootstrap verifies hashes

binding points to local materialized paths
```



---



## Workcell

Bounded operational setup.

The real-world backing for implements.



In robotics, a workcell is not just a robot.

It is the whole local operating island:

```text
robot arm
controller
sensors
safety interlocks
fixtures
operator procedures
```



For Ethereum:

```text
full node
archive node
RPC endpoint
signer / HSM
monitoring
operator procedure
```



---



## Workcell Terms

```text
workcell
  bounded operational setup

workcell spec
  human-readable and testable requirements

workcell hub
  strict machine-facing service

workcell component
  concrete operator-provided piece
```



```mermaid
flowchart TD
  W["eth-mainnet-workcell"]
  SPEC["workcell spec<br/>what humans must set up"]
  HUB["workcell hub<br/>machine-facing boundary"]
  C1["component<br/>full node"]
  C2["component<br/>archive node"]
  C3["component<br/>RPC endpoint"]
  C4["component<br/>signer / HSM"]

  W --> SPEC
  W --> HUB
  W --> C1
  W --> C2
  W --> C3
  W --> C4
```



---



## Why Workcell Hub?

Implements should not talk to random infrastructure.

They call the hub.

The hub routes to components.



```mermaid
flowchart LR
  I1["CHAINREAD implement"]
  I2["CHAINLOGS implement"]
  I3["SENDTX implement"]

  HUB["eth-mainnet-workcell-hub"]

  N1["full node"]
  N2["archive node"]
  R["redundant RPC"]
  S["signer / HSM"]

  I1 --> HUB
  I2 --> HUB
  I3 --> HUB

  HUB --> N1
  HUB --> N2
  HUB --> R
  HUB --> S
```



The hub normalizes:

```text
routing
health checks
failover
provenance
credentials
response shape
```



---



## P1 Workcell Boundary

P1 does not make synlang manage the workcell.



```text
humans / installer:
  set up workcell components
  start workcell hubs
  provide paths and endpoints

Noemar / bootstrap:
  reads boot manifest
  registers hub paths
  runs conformance tests
  binds sigils
```



No readiness atoms in P1.

If the human runs boot, they are asserting the setup is ready.



---



## Later Workcell Direction

P1:

```text
human-operated workcells
installer preflight
boot conformance
```



Mature state:

```text
teleonome-operated workcells
embodiment telemetry
continuous conformance
machine-derived readiness
```



Same consumption site.

Better provenance.



```mermaid
flowchart LR
  P1["P1 readiness<br/>human + installer"]
  SAME["same loop requirement<br/>requires eth-mainnet-workcell"]
  FUT["later readiness<br/>teleonome + embodiments"]

  P1 --> SAME --> FUT
```



---



## Loop Requirements

Loops should declare what they need.



```synlang
(loop-requires relay-halo-spark-term
   (sigils [CHAINREAD SHA256 ADD EQ])
   (bindings [chainread-eth-mainnet-v1])
   (workcells [eth-mainnet-workcell])
   (tests [chainread-conformance-v1]))
```



Boot can refuse to start a loop if its requirements are not satisfied.



---



## Runtime Call Path

What happens during normal operation.



```mermaid
sequenceDiagram
  participant L as Synlang loop
  participant E as Noemar evaluator
  participant B as Binding catalog
  participant I as Implement method
  participant H as Workcell hub
  participant C as Workcell components

  L->>E: (CHAINREAD ...)
  E->>B: resolve CHAINREAD
  B-->>E: eth-mainnet-connector.read-slot.v1
  E->>I: call typed method
  I->>H: request read-slot
  H->>C: route to full/archive node
  C-->>H: raw result
  H-->>I: normalized + provenance
  I-->>E: typed atom result
  E-->>L: result
```



---



## Bootstrap Is Different

Normal loops can use bound sigils.

They cannot rewrite the executable substrate.



```text
ordinary loop:
  calls CHAINREAD

bootstrap:
  materializes implement code
  binds CHAINREAD
  registers workcell hub path
```



Bootstrap has birth powers.

Loops have runtime powers.



---



## One-Shot Bootstrap Space

```text
&core.bootstrap
```



Privileged.

Runs once.

Then becomes inert.



```mermaid
flowchart TD
  BOOT["&core.bootstrap<br/>one-shot privileged boot"]
  M["materialize implements"]
  B["bind sigils"]
  W["register workcell hubs"]
  G["allocate genesis Spaces"]
  T["run conformance tests"]
  R["emit boot receipts"]
  I["become inert"]

  BOOT --> M --> B --> W --> G --> T --> R --> I
```



---



## Boot Powers

These are not ordinary loop powers.



```text
MATERIALIZE-IMPLEMENT
  write verified implement artifact to local path

BIND-SIGIL
  bind sigil to implement method path

REGISTER-WORKCELL-HUB
  attach workcell name to local hub endpoint

ENABLE-LOOP
  start loop only after requirements pass
```



Think:

```text
boot-only Noemar-native capabilities
```

Not:

```text
ordinary synlang powers
```



---



## Installer World

The installer is a normal program.

It bridges humans and synome birth.



```mermaid
flowchart TD
  H["human runs installer"]
  C["set up workcell components"]
  WH["start workcell hubs"]
  N["install Noemar"]
  S["load mega .synlang file"]
  BM["write boot manifest"]
  BOOT["invoke &core.bootstrap"]

  H --> C --> WH --> N --> S --> BM --> BOOT
```



---



## Boot Manifest

The installer hands bootstrap the local facts.



```text
boot-manifest:
  noemar-version: ...
  noemar-path: ...

  synome-artifact:
    path: laniakea-p1.synlang
    hash: sha256:...

  implements:
    eth-mainnet-connector-v1:
      materialized-path: /opt/noemar/implements/...
      hash: sha256:...

  workcell-hubs:
    eth-mainnet-workcell:
      endpoint: http://127.0.0.1:8547

  test-forks:
    synome-shadow: enabled
    eth-mainnet-fork: enabled
```



No need for signed readiness atoms in P1.

The manifest is an installer output.



---



## Mega .synlang File

The genesis artifact can contain:

```text
Space definitions
loop bodies
sigil catalog
binding catalog
implement artifact refs or source strings
workcell specs
test definitions
bootstrap recipe
```



```mermaid
flowchart TD
  MEGA["mega .synlang"]
  SP["genesis Spaces"]
  LP["loop bodies"]
  SC["sigil catalog"]
  BC["binding catalog"]
  IA["implement artifacts"]
  WS["workcell specs"]
  TS["test suite"]

  MEGA --> SP
  MEGA --> LP
  MEGA --> SC
  MEGA --> BC
  MEGA --> IA
  MEGA --> WS
  MEGA --> TS
```



---



## Boot Flow

```mermaid
flowchart TD
  INST["installer"]
  MAN["boot manifest"]
  BOOT["&core.bootstrap"]
  MAT["materialized implements"]
  BIND["active bindings"]
  HUBS["registered workcell hubs"]
  GEN["canonical synome frame"]
  LOOPS["enabled loops"]

  INST --> MAN
  MAN --> BOOT
  BOOT --> MAT
  BOOT --> BIND
  BOOT --> HUBS
  BOOT --> GEN
  GEN --> LOOPS
```



---



## Test Setup

After canonical genesis:

```text
fork synome
fork chain
bind shadow to forked workcells
run tests
discard or keep for dev
```



```mermaid
flowchart TD
  CAN["canonical synome frame"]
  PROD["production workcells<br/>eth-mainnet-workcell"]

  SHADOW["shadow/test synome frame"]
  FORK["forked test workcells<br/>eth-mainnet-fork-workcell"]

  CAN --> PROD
  CAN --> SHADOW
  PROD --> FORK
  SHADOW --> FORK

  TEST["run P1 acceptance suite"]
  SHADOW --> TEST
  FORK --> TEST
```



---



## Production vs Shadow Binding

Same sigil.

Different frame.

Different workcell hub.



```text
production frame:
  CHAINREAD -> eth-mainnet-connector.read-slot.v1
            -> eth-mainnet-workcell-hub

shadow frame:
  CHAINREAD -> eth-mainnet-connector.read-slot.v1
            -> eth-mainnet-fork-workcell-hub
```



This lets the same synlang run against production or test reality.



---



## P1 Safety Boundary

```mermaid
flowchart TD
  BOOT["bootstrap<br/>one-shot"]
  RUNTIME["runtime loops<br/>ordinary"]

  BOOT --> BP["birth powers<br/>materialize<br/>bind<br/>register hubs<br/>enable loops"]
  RUNTIME --> RP["runtime powers<br/>call bound sigils<br/>write authorized atoms<br/>derive state"]

  BP -. "not available to" .-> RUNTIME
```



Key rule:

```text
Bootstrap can create and bind the executable substrate.

Ordinary loops can only use already-bound sigils.
```



---



## P1 Example: CHAINREAD

```synlang
(CHAINREAD ethereum
   collateral-account-001
   (balance btc)
   $block-ref)
```



```text
sigil:
  CHAINREAD

binding:
  chainread-eth-mainnet-v1

implement method:
  eth-mainnet-connector.read-slot.v1

workcell hub:
  eth-mainnet-workcell-hub

workcell components:
  full node
  archive node
  RPC endpoint
```



---



## P1 Example: Risk Heartbeat

```mermaid
flowchart LR
  EXO["exobook atoms"]
  CH["CHAINREAD<br/>collateral + debt"]
  MM["market memory"]
  RF["custodial-crypto<br/>risk form"]
  CRR["CRR components"]
  SB["structbook<br/>matching"]
  ER["prime-er"]

  EXO --> RF
  CH --> RF
  MM --> RF
  RF --> CRR --> SB --> ER
```



The risk form does not care how `CHAINREAD` is backed.

It only needs the bound sigil result.



---



## What The Team Builds

```text
Noemar core
  parser
  atom classifier
  evaluator
  special forms
  literal handling

Sigil layer
  sigil catalog
  binding catalog
  implement artifact materialization
  binding resolver

Workcell layer
  workcell specs
  workcell hubs
  component setup docs
  hub conformance tests

Installer / boot
  installer
  boot manifest
  &core.bootstrap
  shadow synome + forked chain setup
```



---



## Final Mental Model

```mermaid
flowchart TD
  LANG["language core<br/>literals + special forms"]
  POW["power layer<br/>sigils + bindings"]
  CODE["code layer<br/>implements"]
  OPS["operation layer<br/>workcells"]
  BOOT["birth layer<br/>installer + &core.bootstrap"]
  LOOP["ordinary loops"]

  BOOT --> LANG
  BOOT --> POW
  BOOT --> CODE
  BOOT --> OPS

  LOOP --> LANG
  LOOP --> POW
  POW --> CODE
  CODE --> OPS
```



One sentence:

```text
Noemar gives synlang a small fixed core and a governed way to call real-world powers.
```



---



## The Important Boundary

```text
The synome can name powers.

Bindings wire those powers to code.

Code calls workcell hubs.

Workcells touch the world.
```



```text
P1:
  humans and installer prepare workcells

later:
  teleonomes and embodiments operate workcells
```



The read path stays stable.

The provenance gets better.
