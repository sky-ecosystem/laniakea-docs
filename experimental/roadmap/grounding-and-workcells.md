# Grounding and Workcells

**Status:** P1 substrate companion.
**Scope:** The grounded execution model Noemar needs for Phase 1: literals, special forms, sigils, bindings, implements, implement code blobs, workcells, installer boot, and `&core.bootstrap`.

This doc does not add an ongoing sigil / binding / workcell registry. P1 has one boot Space, `&core.bootstrap`, that materializes the runtime call surface and then becomes inert. Ordinary loops only use already-bound sigils.

---

## 1. Grounded atom split

The old term `grounded atom` is too broad. For P1, split it into three cases:

| Term | Meaning | Examples |
|---|---|---|
| **literal** | Built-in value atom | `42`, `3.14`, `"hello"`, `true` |
| **special form** | Evaluator-native control form | `IF`, `LET`, `MATCH`, `QUOTE` |
| **sigil** | Grounded callable atom | `ADD`, `SHA256`, `CHAINREAD` |

Rule of thumb:

```text
literals are values
special forms govern evaluation
sigils compute or reach power
```

Syntax convention:

```text
lowercase = ordinary symbolic meaning
ALL CAPS  = special/executable atom
$         = variable
&         = Space
numbers   = literals
```

Examples:

```text
$borrower
&entity.halo.spark-term
loan-health
42
ADD
CHAINREAD
```

Special forms are Noemar evaluator law. A normal callable cannot implement `IF` or `QUOTE` cleanly because those forms change which arguments evaluate.

Sigils are open-ended. Adding a new literal type changes the language; adding a new special form changes the evaluator; adding a new sigil changes the boot/binding surface.

---

## 2. Sigil stack

A sigil is not the program itself. It is the synlang-side callable name. The P1 stack is:

```text
sigil
  -> binding
    -> implement.method
      -> implement code blob
        -> workcell hub
          -> workcell components
```

Definitions:

| Term | Meaning |
|---|---|
| **sigil** | ALL CAPS callable symbol in synlang. |
| **binding** | Versioned wiring from sigil to an implement method, including type, auth, determinism/effect, and verification policy. |
| **implement** | Controlled executable adapter/service Noemar can call. |
| **implement method** | Specific callable method on an implement. |
| **implement code blob** | Concrete source/package/blob that bootstrap materializes and verifies. |
| **workcell hub** | Strict machine-facing service the implement calls. |
| **workcell component** | Concrete operator-provided backing piece: node, signer, API endpoint, model endpoint, robot arm, camera, etc. |

Example:

```text
CHAINREAD
  sigil

chainread-eth-mainnet-v1
  binding

eth-mainnet-connector.read-slot.v1
  implement method

eth-mainnet-connector-v1.py
  implement code blob

eth-mainnet-workcell-hub
  workcell hub

full node / archive node / RPC endpoint
  workcell components
```

Multiple sigils can share one implement and one workcell:

```text
CHAINREAD    -> eth-mainnet-connector.read-slot.v1
CHAINLOGS    -> eth-mainnet-connector.get-logs.v1
CHAINBALANCE -> eth-mainnet-connector.balance-of.v1
```

P1 binding shape:

```text
sigil: CHAINREAD
binding-id: chainread-eth-mainnet-v1
implement: eth-mainnet-connector
method: read-slot
version: v1
mode: exo-implement
traits: [read-only, consensus-backed]
determinism: deterministic-at-block
verification: block-ref + proof/provenance policy
```

---

## 3. Workcells

A **workcell** is a bounded operational setup backing one or more implement methods.

The term comes from robotics/manufacturing: a workcell is not just the robot; it is the whole local operating island: controller, sensors, safety interlocks, tooling, operator procedures, and the robot itself.

P1 uses the same abstraction for grounded execution:

| Workcell term | Meaning |
|---|---|
| **workcell** | Bounded operational setup. |
| **workcell spec** | Human-readable and testable requirements for operating the setup. |
| **workcell hub** | Strict service implements call into. |
| **workcell component** | Concrete piece the operator provides. |

Ethereum example:

```text
eth-mainnet-workcell
  spec:
    archive-capable reads
    explicit block references
    provider redundancy
    health/provenance reports

  hub:
    eth-mainnet-workcell-hub

  components:
    full node
    archive node
    RPC endpoint
    signer/HSM if effectful methods are enabled
```

P1 boundary:

```text
humans / installer:
  set up workcell components
  start workcell hubs
  provide paths/endpoints

Noemar / bootstrap:
  reads boot manifest
  registers hub paths
  runs conformance checks
  binds sigils
```

P1 does not use signed workcell-readiness atoms. Running the installer / boot function is the operator assertion that the workcells are ready.

Later phases can migrate workcell operation from humans to teleonomes and embodiments. The loop requirement surface stays stable; only readiness provenance improves.

---

## 4. `&core.bootstrap`

`&core.bootstrap` is a P1 Space and part of the fixed topology. It is special because it is one-shot boot substrate, not an ordinary operational registry.

It holds:

- bootstrap recipe;
- boot manifest schema;
- sigil catalog needed for P1;
- binding specs needed for P1;
- implement code blob refs / hashes;
- workcell specs and hub registration shapes;
- loop requirement declarations;
- conformance test hooks;
- boot receipts.

It can perform bootstrap-only powers:

```text
MATERIALIZE-IMPLEMENT
  write a verified implement code blob to a local path

BIND-SIGIL
  bind a sigil to a materialized implement method

REGISTER-WORKCELL-HUB
  attach a workcell name to a local hub endpoint

ENABLE-LOOP
  start a loop only after requirements pass
```

These are not ordinary loop powers. After successful boot, `&core.bootstrap` becomes inert. Ordinary loops cannot materialize code blobs, bind sigils, or register workcell hubs; they only call already-bound sigils.

---

## 5. Installer and boot flow

P1 uses a normal installer as the human/operator bridge:

```text
installer
  -> sets up workcell components
  -> starts workcell hubs
  -> installs Noemar
  -> loads mega .synlang file
  -> writes boot manifest
  -> invokes &core.bootstrap
```

Boot manifest shape:

```text
boot-manifest:
  noemar-version: ...
  noemar-path: ...

  synome-artifact:
    path: laniakea-p1.synlang
    hash: sha256:...

  implement-code-blobs:
    eth-mainnet-connector-v1:
      source-hash: sha256:...
      materialized-path: /opt/noemar/implements/...

  workcell-hubs:
    eth-mainnet-workcell:
      endpoint: http://127.0.0.1:8547

  test-forks:
    synome-shadow: enabled
    eth-mainnet-fork: enabled
```

After canonical genesis, bootstrap creates a shadow synome frame and points its bindings at fork/test workcells:

```text
production frame:
  CHAINREAD -> eth-mainnet-workcell-hub

shadow frame:
  CHAINREAD -> eth-mainnet-fork-workcell-hub
```

The same synlang can then run against production reality or forked test reality.

---

## 6. Loop requirements

Loops declare the grounded powers they need:

```text
(loop-requires relay-halo-spark-term
   (sigils [CHAINREAD SHA256 ADD EQ])
   (bindings [chainread-eth-mainnet-v1])
   (workcells [eth-mainnet-workcell])
   (tests [chainread-conformance-v1]))
```

Bootstrap refuses to enable a loop if its requirements are not satisfied. Once enabled, the loop can only call its already-bound sigils through the normal evaluator.

---

## 7. P1 baseline sigils

P1 should keep the sigil set small.

Native deterministic examples:

```text
ADD
SUB
MUL
DIV
MIN
MAX
SUM
EQ
LT
LTE
GT
GTE
SHA256
```

Read-only exo example:

```text
CHAINREAD
```

Explicitly out of ordinary P1 loop scope:

```text
SENDTX
ASKLLM
randomness / stochastic sigils
```

P1 relays can record transaction receipts and lifecycle atoms, but ordinary synlang loops do not directly send transactions through `SENDTX`. Later phases can add effectful and stochastic sigils with explicit auth, determinism, and verification policies.

