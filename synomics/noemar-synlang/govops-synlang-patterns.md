# GovOps / Halo / Book — Synlang Patterns

Tech-inspiration extract from the working AETHER demo at
`noemar-work/aether/examples/govops_demo/`. Documents the load-bearing
synlang and Python shapes plus the architectural decisions behind them.
Companion to `synart-access-and-runtime.md` and `synlang-context.md`.

---

## Pipeline shape

```
external submission
       │
       ▼
┌────────────────────────────────────────────────┐
│ STAGE 1 — gate                                 │
│  ed25519 verify against (certified-beacon-key) │
│  facts in the Space. Drops spam silently.      │
└──────────────────────┬─────────────────────────┘
                       │ authenticated msg
                       ▼
┌────────────────────────────────────────────────┐
│ STAGE 2 — pipeline                             │
│  1. parse payload as synlang                   │
│  2. head ∈ effect-protocol allowlist           │
│  3. query (permits $beacon $action) → True?   │
│  4. dispatch Python effect                     │
│  5. write audit row                            │
└────────────────────────────────────────────────┘
```

Three independent gates: signature, policy match, effect-protocol
preconditions. Authority lives **only** in step 3. Steps 1, 2, 4 fail
for structural reasons (bad sig, unknown verb, duplicate artifact),
not authorization.

---

## Atom layer — what lives in the Space

```metta
; Authority chain (seed-time)
(prime spark-prime)
(administers phoenix-govops spark-prime)

; Beacon identity (written by registration)
(certified-beacon-key phoenix-govops "ab9c…")
(beacon-status        phoenix-govops active)
(in-class             phoenix-govops LPHA)
(beacon-role          phoenix-govops govops)

; Constructor outputs (written by Python effects)
(halo spark-halo-A)
(halo-prime spark-halo-A spark-prime)
(halo-admin spark-halo-A phoenix-govops)        ; capability fact

(book book-7)
(parent-halo book-7 spark-halo-A)
(book-state  book-7 filling)
(book-admin  book-7 phoenix-govops)             ; capability fact

; Attestations: positive flag + structured record
(has-pre-deployment-attestation book-7)         ; consumed by policy
(attestation book-7 pre-deployment att-001)     ; audit/replay only
```

Every fact is flat — head + 2-3 atom args. No nested expressions inside
a fact. This is the unit the inverted index can hit in O(1).

---

## Permission rule template

```metta
(= (permits $beacon (VERB ARGS… $nonce))
   (if (and (in-class      $beacon LPHA)
            (beacon-role   $beacon govops)
            (beacon-status $beacon active)
            <flat membership checks…>)
       True
       False))
```

Three non-obvious requirements:

1. **`(if … True False)` wrapper.** A bare `(and …)` body rewrites to
   the unevaluated conjunction; the pipeline's `result == True` check
   silently passes. The wrapper forces a definite boolean.
2. **Trailing `$nonce` in LHS.** Driver auto-appends a sequence atom so
   identical-intent retries produce distinct ed25519 sigs. Bodies
   ignore it.
3. **No existentials in the body.** The structural validator rejects
   variables that appear in the RHS but not the LHS, *unless* the RHS
   head is `and`/`or`/`not`. Inside `(if (and …))`, every variable
   must trace to the action LHS.

---

## The flat-capability pattern (key decision)

The original runtime-doc sketch used `(can $caller $verb $target)`
walking the `(accordant …)` graph by transitive closure. That hits
AETHER's QR-009 (closure over bare facts) and forces existentials.

**Rewrite:** every constructor writes a flat 2-arg capability fact;
every downstream rule checks that fact directly.

```
(administers $govops $prime)        ─┐ seed
                                     │
   create-halo writes ────────────►  (halo-admin $halo $govops)
                                     │
   create-book writes ────────────►  (book-admin $book $govops)
                                     │
   transition-book / attest-* check ─┘
```

Both args of every capability fact appear in the action LHS or the
`$beacon` head of `permits`. Zero existentials. No closure. Validator
happy.

The chain is **append-only and one-directional** — you can't write a
rule that bypasses an earlier link without contradicting an existing
fact.

---

## Permission rules (full set)

```metta
; Top of chain — checks the seed (administers …) fact
(= (permits $beacon (create-halo $halo $prime $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (administers $beacon $prime))
       True
       False))

; Middle — checks fact written by create-halo
(= (permits $beacon (create-book $book $halo $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (halo-admin $halo $beacon))
       True
       False))

; Six transition rules — one per allowed (src, dst) pair
(= (permits $beacon (transition-book $book filling offboarding $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (book-state $book filling)
            (book-admin $book $beacon))
       True
       False))

(= (permits $beacon (transition-book $book offboarding deploying $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (book-state $book offboarding)
            (has-pre-deployment-attestation $book)   ; ← gate
            (book-admin $book $beacon))
       True
       False))

(= (permits $beacon (transition-book $book deploying at-rest $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (book-state $book deploying)
            (has-at-rest-attestation $book)          ; ← gate
            (book-admin $book $beacon))
       True
       False))

; … at-rest→unwinding, unwinding→closed (free, same shape)

; Attestation rules — same beacon for the demo; in production split off
(= (permits $beacon (attest-pre-deployment $book $att-id $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (book-state $book offboarding)
            (book-admin $book $beacon))
       True
       False))
```

Default-deny is enforced by absence of a matching rule. An untabled
transition `(transition-book $book closed unwinding $nonce)` returns
no `permits` results → policy denies.

---

## State machine as data

The transition table **is** the set of permission rules. No switch
statement. Each rule binds `$src` and `$dst` as ground atoms in its LHS
pattern:

```metta
(permits $beacon (transition-book $book offboarding deploying $nonce))
                                       ^^^^^^^^^^^ ^^^^^^^^^
                                       atoms in the LHS pattern
```

Adding a new transition = adding one rule. Removing one = removing the
rule (+ no rebuild, no migration).

---

## Attestation as positive flag (not wildcard match)

```python
def attest_pre_deployment(space, action, *, beacon_id, clock):
    book = action.args[0].canonical()
    att_id = action.args[1].canonical()
    if _state_of(space, book) != "offboarding":
        raise EffectError(...)
    space.add(parse(f"(attestation {book} pre-deployment {att_id})")[0])  # audit
    space.add(parse(f"(has-pre-deployment-attestation {book})")[0])       # policy
```

Policy can't reliably consume `(attestation $book pre-deployment $_)`
inside `(and …)` — wildcards in flat facts inside conjunctions hit
QR-010. Workaround: write **two** atoms — a structured record for
replay/forensics and a flat 1-arg presence flag for policy.

---

## Constructor (Python effect) shape

```python
def create_halo(space, action, *, beacon_id, clock):
    # action == (create-halo $halo $prime $nonce)
    if len(action.args) != 3:
        raise EffectError(f"create-halo expects 3 args, got {len(action.args)}")
    halo  = action.args[0].canonical()
    prime = action.args[1].canonical()
    # Idempotency check
    if list(space.query(parse(f"(halo {halo})")[0])):
        raise EffectError(f"halo {halo} already exists")
    # Atomic write: typed atom + relation atoms + capability fact
    space.add(parse(f"(halo {halo})")[0])
    space.add(parse(f"(halo-prime {halo} {prime})")[0])
    space.add(parse(f"(halo-admin {halo} {beacon_id})")[0])             ; ← chain link
    space.add(parse(f"(halo-created-by {halo} {beacon_id} {clock.now()})")[0])
```

Conventions:

- **Trailing nonce arg.** Driver appends; effect discards.
- **Idempotency check first.** Before any `add`. Errors raise
  `EffectError` (becomes a `denied:ProtocolError` audit row).
- **Capability fact writes happen here, not in the policy.** Policy
  reads what the effect already wrote.
- **No authority decisions.** Authority was decided by `permits` before
  the effect was called. The effect only validates structural
  preconditions (state, existence, idempotency).

---

## Beacon identity — real ed25519, not simulated

```python
class FakeBeacon:
    def __init__(self, beacon_id, beacon_class, *, signing_key=None):
        self.beacon_id = beacon_id
        self._signing_key = signing_key or SigningKey.generate()  # ed25519

    def sign(self, payload: str) -> bytes:
        return self._signing_key.sign(payload.encode("utf-8")).signature
```

```python
def register_beacon(self, beacon_id, beacon_class):
    b = FakeBeacon(beacon_id, beacon_class)
    self._beacons[beacon_id] = b
    self.space.add(parse(f'(certified-beacon-key {beacon_id} "{b.public_key_hex}")')[0])
    self.space.add(parse(f"(beacon-status {beacon_id} active)")[0])
    self.space.add(parse(f"(in-class {beacon_id} {beacon_class})")[0])
```

```python
def gate_atom(space, inbox):
    keys = {bid: pk_hex from (certified-beacon-key …) facts in space}
    for msg in inbox.pending():
        pk_hex = keys.get(msg["beacon_id"])
        if pk_hex is None:
            spam["unknown_beacon"] += 1; continue       # silent drop
        try:
            VerifyKey(bytes.fromhex(pk_hex)).verify(
                msg["payload"].encode("utf-8"), msg["signature"])
        except BadSignatureError:
            spam["bad_signature"] += 1; continue        # silent drop
        authed.append(msg)
```

The pubkey **registry is a query against the live Space**. No external
cache. Revoke a beacon by retracting `(certified-beacon-key …)` and
the gate slams shut on the next message.

The `beacon_id` field on a submission is self-claimed; what makes it
real is the signature verifying under the registered pubkey.

---

## Replay protection

```python
def submit(self, beacon_id, payload):
    self._nonce_counter += 1
    nonce = f"sn{self._nonce_counter}"
    wrapped = f"({head} {args} {nonce})"            # rebuild with trailing atom
    sig = self._beacons[beacon_id].sign(wrapped)
    self.inbox.submit(beacon_id, wrapped, sig, ...)
```

Every payload gets a unique trailing atom before signing. Identical
intent → distinct bytes → distinct ed25519 sig. Permission rules pattern
the nonce as `$nonce` and ignore it; effects discard the last arg.
This is the in-process equivalent of beacon-side nonce rotation.

---

## Pipeline (Stage 2) — the policy/effect handoff

```python
# 1. Parse → fail = denied:BadPayload
action = parse(payload)[0]

# 2. Allowlist check
if action.head.canonical() not in EFFECT_PROTOCOLS:
    audit("denied", "UnknownAction"); continue

# 3. Permission query
permits_q = parse(f"(permits {bid} {action.canonical()})")[0]
results = list(space.query(permits_q))
permitted = any(r.canonical() == "True" for r in results)
if not permitted:
    audit("denied", "NotPermitted"); continue

# 4. Dispatch effect
try:
    EFFECT_PROTOCOLS[head](space, action, beacon_id=bid, clock=clock)
except EffectError as e:
    audit("denied", f"ProtocolError:{e}"); continue

# 5. Accept
audit("accepted", None)
```

Notable:

- `space.query` does the rewrite — `(permits …)` is *evaluated*, not
  pattern-matched. The `if/and` returns a definite `True` atom.
- Default-deny: empty results from `query` → `permitted=False`.
- Effect failure ≠ permission failure. Both become "denied" audit rows
  but with distinguishable `reason` fields.

---

## Critical AETHER / synlang constraints encountered

| Constraint | Where it bites | Workaround |
|---|---|---|
| Existentials only allowed under `and`/`or`/`not` heads | `(if (and (foo $x $existential)) …)` raises StructuralValidationError | Pre-bind everything in action LHS via flat capability facts |
| Bare `(and …)` body doesn't boolean-eval | Permission rule silently accepts everything | Wrap in `(if … True False)` |
| Wildcard `$_` in flat fact inside `(and …)` (QR-010) | `(attestation $book pre-deployment $_)` doesn't reduce to True | Write a separate 1-arg presence flag |
| Recursive/transitive closure over bare facts (QR-009) | `(reaches $a $b)` walking accordancy edges | Replace with append-only flat capability chain |
| Identical-intent retries produce identical sigs | Real beacons rotate nonces; in-process loops don't | Driver appends `sn1, sn2, …` per submit |

---

## What's deliberately not here

- **Cross-Space writes.** Demo uses one Space. Multi-Space (`&genesis`,
  `&governance`, `&operational`, `&library`) is the next layer of the
  runtime doc but doesn't change the auth shapes.
- **Telart / embart.** Demo is purely synart-scope. Teleonome-private
  rules and per-embodiment learned patterns live in different Spaces
  with different auth models.
- **Sentinel formations / TTS / rate limits.** None of HPLA/HPHA. The
  whole demo is one LPHA beacon doing govops work.
- **Crystallization.** No probabilistic→deontic promotion. All facts
  are hard.

---

## File map

| File | Role |
|---|---|
| `noemar-work/aether/examples/govops_demo/seed.synlang` | Authority chain seed |
| `noemar-work/aether/examples/govops_demo/policy.synlang` | 9 `(permits …)` rules |
| `noemar-work/aether/examples/govops_demo/effects.py` | `create-halo` + `create-book` Python effects |
| `noemar-work/aether/examples/govops_demo/run_demo.py` | 11-step storyline runner |
| `noemar-work/aether/examples/govops_demo/test_govops_demo.py` | 3 pytest tests |
| `noemar-work/aether/tests/simulation/harness/halo_book_effects.py` | Re-used `transition-book` + attest effects |
| `noemar-work/aether/tests/simulation/harness/gate.py` | Stage 1 — ed25519 verify |
| `noemar-work/aether/tests/simulation/harness/pipeline.py` | Stage 2 — parse + permission + effect + audit |
| `noemar-work/aether/tests/simulation/harness/driver.py` | SimulationDriver façade |

PR: <https://github.com/amatanasov/aether/pull/247>
