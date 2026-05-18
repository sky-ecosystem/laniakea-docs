# Grounding and Workcells

**Status:** P1 substrate companion.
**Scope:** The grounded execution model Noemar needs for Phase 1: literals, special forms, sigils, bindings, implements, implement code blobs, workcells, installer boot, and `&core.bootstrap`.

This doc does not add an ongoing sigil / binding / workcell registry. P1 has one boot Space, `&core.bootstrap`, that materializes the runtime call surface and then becomes inert. Ordinary loops only use already-bound sigils. The complete P1 callable/workcell inventory lives in [`sigils-and-workcells.md`](sigils-and-workcells.md).

---

## 1. Grounded callable split

The old term `grounded atom` is too broad. For P1, split callable and evaluator surface into five cases:

| Term | Meaning | Examples |
|---|---|---|
| **literal** | Built-in value atom | `42`, `3.14`, `"hello"`, `true` |
| **special form** | Evaluator-native control form | `if`, `let`, `match`, `quote` |
| **stdlib pure** | Deterministic local function | `+`, `sha256`, `min`, `=` |
| **native stdlib sigil** | Runtime-grounded callable with no workcell | `NOW` |
| **workcell-backed sigil** | Grounded callable that reaches a bounded operational setup | `CHAINREAD`, `SYNGATE-READ` |

Rule of thumb:

```text
literals are values
special forms govern evaluation
stdlib pure functions compute
native sigils read runtime-controlled context
workcell-backed sigils reach bounded external power
```

Syntax convention:

```text
lowercase / symbols = ordinary symbolic meaning and stdlib
ALL CAPS            = native or workcell-backed sigil
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
+
NOW
CHAINREAD
```

Special forms are Noemar evaluator law. A normal callable cannot implement `if` or `quote` cleanly because those forms change which arguments evaluate.

Adding a new literal type changes the language; adding a new special form changes the evaluator; adding a pure stdlib function changes the library; adding a native or workcell-backed sigil changes the boot/binding surface.

---

## 2. Workcell-backed sigil stack

A workcell-backed sigil is not the program itself. It is the synlang-side callable name. The P1 stack is:

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
| **sigil** | Capability-bearing callable symbol in synlang. P1 native/workcell sigils use ALL CAPS. |
| **binding** | Versioned wiring from a workcell-backed sigil to an implement method, including type, auth, determinism/effect, and verification policy. |
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

eth-mainnet-connector.read.v1
  implement method

eth-mainnet-connector-v1.py
  implement code blob

eth-mainnet-read-workcell-hub
  workcell hub

full node / archive node / RPC endpoint
  workcell components
```

P1 uses one broad `CHAINREAD` sigil rather than separate chain-log or balance sigils:

```text
CHAINREAD -> eth-mainnet-connector.read.v1
  query families: balance, contract read/storage, event/log range, transaction receipt
```

P1 binding shape:

```text
sigil: CHAINREAD
binding-id: chainread-eth-mainnet-v1
implement: eth-mainnet-connector
method: read
version: v1
mode: exo-implement
traits: [read-only, consensus-backed]
determinism: deterministic-at-block
verification: block-ref + proof/provenance policy
```

Native stdlib sigils such as `NOW` have no workcell stack. Pure stdlib functions such as `+` and `sha256` have neither binding nor workcell.

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

Ethereum read example:

```text
eth-mainnet-read-workcell
  spec:
    archive-capable reads
    explicit block references
    provider redundancy
    health/provenance reports

  hub:
    eth-mainnet-read-workcell-hub

  components:
    full node
    archive node
    RPC endpoint
    signer/HSM if effectful methods are enabled
```

Syngate intake example:

```text
syngate-intake-workcell
  spec:
    signed envelope queue
    registered-beacon pubkey snapshot
    signature verification
    basic nonce / rate-limit / spam prefiltering
    replayable cursor batches

  hub:
    syngate-intake-workcell-hub
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
    syngate-intake-connector-v1:
      source-hash: sha256:...
      materialized-path: /opt/noemar/implements/...

  workcell-hubs:
    eth-mainnet-read-workcell:
      endpoint: http://127.0.0.1:8547
    syngate-intake-workcell:
      endpoint: unix:/run/noemar/syngate-intake.sock

  test-forks:
    synome-shadow: enabled
    eth-mainnet-fork: enabled
```

After canonical genesis, bootstrap creates a shadow synome frame and points its bindings at fork/test workcells:

```text
production frame:
  CHAINREAD    -> eth-mainnet-read-workcell-hub
  SYNGATE-READ -> syngate-intake-workcell-hub

shadow frame:
  CHAINREAD    -> eth-mainnet-fork-workcell-hub
  SYNGATE-READ -> syngate-test-intake-workcell-hub
```

The same synlang can then run against production reality or forked test reality.

---

## 6. Loop requirements

Loops declare the grounded powers they need:

```text
(loop-requires synserv-canonical
   (stdlib [core-special-forms-v1 core-stdlib-v1])
   (native-sigils [NOW])
   (sigils [SYNGATE-READ CHAINREAD])
   (bindings [syngate-read-v1 chainread-eth-mainnet-v1])
   (workcells [syngate-intake-workcell eth-mainnet-read-workcell])
   (tests [syngate-read-conformance-v1 chainread-conformance-v1]))
```

Bootstrap refuses to enable a loop if its requirements are not satisfied. Once enabled, the loop can only call declared stdlib/native surface and already-bound workcell sigils through the normal evaluator.

---

## 7. P1 callable inventory

P1 keeps the workcell-backed sigil set small. The canonical list is [`sigils-and-workcells.md`](sigils-and-workcells.md).

Pure stdlib:

```text
+ - * /
min max sum
= < <= > >=
sha256
```

Native stdlib sigil:

```text
NOW
```

Workcell-backed sigils:

```text
SYNGATE-READ
CHAINREAD
```

Explicitly out of ordinary P1 loop scope:

```text
SENDTX
ASKLLM
randomness / stochastic sigils
```

P1 relays can record transaction receipts and lifecycle atoms, but ordinary synlang loops do not directly send transactions through `SENDTX`. Later phases can add effectful and stochastic sigils with explicit auth, determinism, and verification policies.
