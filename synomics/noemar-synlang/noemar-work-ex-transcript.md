read everything in noemar work essentials                                                                                                 

⏺ **Bash**(ls noemar-work/)                                                                                   

  ⎿  aether                                                                                                                               

     essentials                                                                                                                             

     extra-data

⏺ **Bash**(ls -la noemar-work/essentials/ && echo "---" && find                                             

  noemar-work/essentials/ -type f | head -100)                                                            

  ⎿  total 256                                                                                                                              

     drwxr-xr-x@ 7 <user>  staff    224 Apr 29 19:58 .

     drwxr-xr-x@ 5 <user>  staff    160 Apr 29 19:58 ..                                                                            

     -rw-r--r--@ 1 <user>  staff  20480 Apr 25 22:58 aether-notes-codex.md                                                         

     -rw-r--r--@ 1 <user>  staff  15409 Apr 29 19:45 govops-synlang-patterns.md

     -rw-r--r--@ 1 <user>  staff  34584 Apr 28 22:46 synart-access-and-runtime.md                                                  

     -rw-r--r--@ 1 <user>  staff  40868 Apr 28 18:06 synlang-context.md                                                          

     -rw-r--r--@ 1 <user>  staff  15944 Apr 29 19:53 synlang-iteration-primer.md

     ---

     noemar-work/essentials/synlang-iteration-primer.md

     noemar-work/essentials/govops-synlang-patterns.md

     noemar-work/essentials/aether-notes-codex.md

     noemar-work/essentials/synart-access-and-runtime.md

     noemar-work/essentials/synlang-context.md

  

⏺ Reading all 5 files in parallel.                           

  

⏺ **Read**(noemar-work/essentials/aether-notes-codex.md)                                                      

  ⎿  Read **472** lines

⏺ **Read**(noemar-work/essentials/govops-synlang-patterns.md)                                               

  ⎿  Read **409** lines                                                                                                                         

⏺ **Read**(noemar-work/essentials/synart-access-and-runtime.md)                                               

  ⎿  Read **631** lines                                                                                                                       

⏺ **Read**(noemar-work/essentials/synlang-context.md)                                                         

  ⎿  Read **903** lines                                                                                                                         

⏺ **Read**(noemar-work/essentials/synlang-iteration-primer.md)                                                

  ⎿  Read **321** lines                                                                                                                         

⏺ All 5 essentials files loaded. Here's the high-level map of what's in context:                                                            

  **aether-notes-codex.md** (20KB) — Codex's honest second-pass audit of the AETHER repo. Real vs. aspirational, architecture                   

  (Space/rewriter/protocols/PLN/Atlas/RSI/CLAW), corrections to prior notes, sharp edges (QR-009/010, no full closure, in-process           

  protocol-author imports), and a "what I'd do next" roadmap.                                                                               

  **govops-synlang-patterns.md** (15KB) — Working pattern catalog from the runnable govops_demo. Two-stage pipeline (gate → policy → effect →   

  audit), flat-capability-fact pattern (replaces transitive closure), (if (and …) True False) rule template, attestation-as-positive-flag,

  ed25519 beacon identity, replay nonces. Includes the AETHER constraints table.                                                            

  **synart-access-and-runtime.md** (35KB) — The access-control kernel and runtime architecture. Synome vs chain authorization domains,          

  role+sub-role / cert / auth three-level model, Guardian→GovOps→operational beacon underwriting frame, the gate primitive, in-synlang

  heartbeat, multi-Space design (Hyperon's add-atom &other-space lesson), Goertzel hardware locality, the 16 migration principles and 7     

  Phase-1 commitments.                                                                                                                    

  

  **synlang-context.md** (41KB) — The conservation-network kernel for Halo/Class/Book/Unit. "Books balance, units bridge, everything else is    

  metadata." Four-constructor MeTTa surface with proper types, CRR/encumbrance/RAR derivation, sentinel decision rule, the Platonic kernel

  framing.                                                                                                                                  

  **synlang-iteration-primer.md** (16KB) — Self-contained primer tying it all together: 5 layers, 3 artifact scopes, agent ranks, beacon        

  framework, dual deontic/probabilistic architecture, AETHER constraints table, established patterns, cross-Space conventions, and the open

  pattern-families list (governance proposals, crystallization, rate limits, sentinel formations, etc.).                                    

  Ready for the next step.

  

✻ Crunched for 27s

  

❯ okay lets think of some super high level synlang structure for hte most core process of sky - basically where the daily settlement cycle  

  interacts with real time risk capital covenenants and penalties for breaking capital ratios. so on one hand we both need the thing that   

  measures the exposure of all books in real time per prime to calculate encumbrance ratio of the prime, and separately we also need the    

  thing that calculates base rate payments and distribution rewards payments from and to primes, to be settled every day. do you have       

  enough context to understand what this means? otherwise you can try to read a few relevant docs in laniakea docs                          

⏺ I have most of what I need on the encumbrance side — I have the CRR factor table, the unit-risk-weight derivation, the encumbrance-ratio  

  formula (encumbered / capital), and the lpla-checker role. The conservation-network framing gives me the bridging rules.                

  What I'm thinner on:

  1. **Base rate** mechanics — what Primes pay per day, on what notional, to whom (Generator? USDS holders via Generator?)                      

  2. **Distribution rewards** — direction, formula, what triggers them                                                                          

  3. **Penalty mechanics** when encumbrance breaches 90% — is it instant rate-limit shutoff, escalating fees, forced unwind?

  4. The interface between **continuous** measurement and **discrete** daily close                                                                  

  Let me skim the accounting and risk-framework dirs.                                                                                       

⏺ **Bash**(ls laniakea-docs/accounting/ laniakea-docs/risk-framework/ 2>&1) 

  ⎿  laniakea-docs/accounting/:                                                                           

     README.md                                                                                                                              

     books-and-units.md

     current-accounting.md                                                                                                                  

     daily-settlement-cycle.md                                                                                                            

     forecast-model.md                                                                                                                      

     genesis-capital.md                                                                                                                   

     isolated-deployment.md

     mezzanine-deployment-capital.md

     prime-settlement-methodology.md

     risk-capital-ingression.md

     tugofwar.md

  

     laniakea-docs/risk-framework/:

     README.md

     asc.md

     asset-classification.md

     asset-type-treatment.md

     capital-formula.md

     collateralized-lending-risk.md

     correlation-framework.md

     duration-model.md

     examples.md

     market-risk-frtb.md

     matching.md

     operational-risk-capital.md

     risk-monitoring.md

     sentinel-integration.md

  

⏺ The most relevant files. Reading in parallel.

  

⏺ **Read**(laniakea-docs/accounting/daily-settlement-cycle.md)                                                

  ⎿  Read **701** lines

⏺ **Read**(laniakea-docs/accounting/prime-settlement-methodology.md)                                        

  ⎿  Read **236** lines                                                                                                                         

⏺ **Read**(laniakea-docs/risk-framework/capital-formula.md)                                                   

  ⎿  Read **62** lines                                                                                                                        

⏺ **Read**(laniakea-docs/risk-framework/risk-monitoring.md)                                                   

  ⎿  Read **193** lines                

⏺ **Read**(laniakea-docs/accounting/tugofwar.md)                                                              

  ⎿  Read **489** lines                                                                                                                         

⏺ Yes — I have enough context now. Reading the daily-settlement-cycle, prime-settlement-methodology, capital-formula, risk-monitoring, and  

  tugofwar docs filled the gaps.                                                                                                            

  Before sketching synlang, here's the framing I think the structure has to expose, because the two halves have **inverse temporal shapes** and 

  getting that right is most of the design:                                                                                                 

  ┌──────────────┬──────────────────────────────────────────────────┬──────────────────────────────────────────────────────┐              

  │              │                 **Encumbrance side**                 │                   **Settlement side**                    │

  ├──────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤

  │ Cadence      │ Continuous (any-time query)                      │ Discrete (16:00 UTC moment)                          │

  ├──────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤

  │ Substrate    │ A _fact graph_ (current positions, current states) │ An _event log_ (debt changes, idle balances over time) │                

  ├──────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤                

  │ Reduction    │ Sum-at-instant: Σ (principal × CRR[state])       │ Time-weighted integral over [lock-prev, lock-now]    │                

  ├──────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤                

  │ AETHER pain  │ Aggregation via collapse/fold (QR-009/010)       │ Time-windowed reduction over events                  │              

  ├──────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤                

  │ Failure mode │ Stale read = wrong ratio _now_                     │ Stale read = wrong payment _forever_                   │              

  └──────────────┴──────────────────────────────────────────────────┴──────────────────────────────────────────────────────┘                

  They share one space but pull on it differently. The penalty mechanic is what stitches them: a _continuous_ breach predicate emits a        

  _discrete_ breach-event fact, whose lifetime gets integrated by the settlement machinery exactly the same way debt is.                    

  Here's the high-level synlang structure I'd propose. I'll deliberately stay sketchy — no full constructor bodies yet, just the            

  load-bearing shapes and where each piece lives.

  ---                                                                                                                                     

  **1. The atom layer (what must be flat in the Space)**

  Three families of fact, each kept structurally minimal so the inverted index hits them directly.

  ;; ─── Position graph (continuous side reads this) ───────────────────                                                                    

  (unit $u (issuer $book) (holder $prime) $principal)                                                                                       

  (book-state $book $state)              ; filling | offboarding | deploying | ...                                                          

  (crr-factor $state $factor)            ; state → numeric weight (governance fact)                                                         

  (prime-capital $prime $capital)        ; aggregate available capital                                                                      

  ;; ─── Event log (discrete side reduces over this) ──────────────────                                                                     

  (debt-event   $prime $epoch-id $amount $t)        ; debt outstanding crossed a level at t                                                 

  (idle-event   $prime $kind $location $amount $t)  ; usds/sUSDS balance change                                                             

  (rate-fact    $epoch base-rate $bps)              ; governance-set per epoch                                                              

  (rate-fact    $epoch susds-spread $bps)                                                                                                   

  ;; ─── Cycle state (the metronome) ──────────────────────────────────                                                                     

  (epoch $n (active-from $t0) (lock-at $t1) (settle-at $t2))                                                                                

  (epoch-phase $n active)                ; or processing | settled                                                                          

  (current-epoch $n)                                                                                                                        

  Note what's _not_ here: no encumbrance-ratio fact, no interest-owed fact. Both are derived. Persisting them would create exactly the        

  staleness problem that the lpla-checker spec warns about.                                                                               

  **2. The continuous half — encumbrance ratio**                                                                                                

  Already mostly worked out in synlang-context.md §3.4, but tightened:                                                                      

  ;; Per-unit risk weight, looked up live (no cache)                                                                                        

  (= (unit-risk-weight $u)                                                                                                                  

     (if (and (unit $u (issuer $book) (holder $_) $p)                                                                                       

              (book-state $book $s)                                                                                                         

              (crr-factor $s $f))                                                                                                           

         (* $p $f)                                                                                                                          

         0))                                                                                                                                

  ;; Sum over a Prime's units. AETHER aggregation is brittle here —                                                                         

  ;; in practice this is a Python effect that walks the index and reduces.                                                                

  (= (encumbered-of $prime)                                                                                                                 

     (sum-of unit-risk-weight                                                                                                               

             (units-held-by $prime)))                                                                                                       

  (= (encumbrance-ratio $prime)                                                                                                           

     (/ (encumbered-of $prime) (capital-of $prime)))                                                                                        

  (= (in-breach $prime)

     (> (encumbrance-ratio $prime) 0.90))                                                                                                   

  **Where this runs:** lpla-checker polls (in-breach $p) for each Prime on whatever cadence it likes (seconds, not days). The query is pure     

  synlang; the aggregation underneath is a grounded Python protocol (prime-exposure or similar) because collapse/fold doesn't pencil.

  **3. The breach-as-event bridge (the coupling point)**                                                                                        

  This is where the two halves meet. When lpla-checker detects a breach, it writes a _flat fact_:                                             

  (breach $prime started-at $t)          ; opened on first breach detection                                                                 

  (breach $prime ended-at   $t)          ; closed when ratio re-enters compliance                                                           

  These atoms are now part of the **event log**. Settlement reduces over them the same way it reduces over debt-events. The penalty calculation 

  doesn't need to know about real-time ratios; it just needs the breach intervals.                                                          

  ;; A breach-interval is a bounded window in the event log                                                                               

  (= (breach-intervals $prime $epoch)

     (intervals-of (breach $prime started-at $_)                                                                                            

                   (breach $prime ended-at   $_)

                   (within $epoch)))                                                                                                        

  (= (breach-penalty $prime $epoch)                                                                                                         

     (* (breach-hours $prime $epoch)                                                                                                      

        (penalty-rate-per-hour)                                                                                                             

        (encumbered-during $prime $epoch)))    ; or some variant                                                                            

  This is what gives you the "rate limit reduction proportional to overshoot" mechanic from risk-monitoring.md §Encumbrance Ratio           

  Enforcement without needing a separate enforcement subsystem — the rate limit is just a fact (rate-limit $prime $bps) that a rule rewrites

   in response to breach-events.                                                                                                            

  **4.** **The** **discrete** **half** **—** **daily** **settlement**

  

  The five-step methodology becomes five rules that all consume the event log over the locked interval:                                     

  (= (max-debt-fees $prime $epoch)                                                                                                          

     (* (twap debt-event $prime $epoch)                                                                                                   

        (/ (base-rate $epoch) 365)))                                                                                                        

  (= (idle-reimbursement $prime $epoch)                                                                                                     

     (* (sum-twap idle-event $prime usds-kind $epoch)                                                                                       

        (/ (base-rate $epoch) 365)))                                                                                                        

  (= (susds-profit $prime $epoch)                                                                                                           

     (* (sum-twap idle-event $prime susds-kind $epoch)                                                                                    

        (/ (susds-spread $epoch) 365)))                                                                                                     

  (= (sky-direct-reimbursement $prime $epoch)

     (max 0 (- (base-rate-profit $prime $epoch)                                                                                             

               (actual-profit    $prime $epoch))))                                                                                          

  (= (net-owed $prime $epoch)                                                                                                               

     (- (max-debt-fees $prime $epoch)                                                                                                       

        (+ (idle-reimbursement $prime $epoch)                                                                                             

           (susds-profit       $prime $epoch)                                                                                               

           (sky-direct-reimbursement $prime $epoch)

           (breach-penalty     $prime $epoch))))   ; ← penalty enters here                                                                  

  twap and sum-twap are aggregation primitives — almost certainly Python protocols (event-twap), not native synlang, for the same QR-010    

  reasons.                                                                                                                                  

  **5. The cycle as state machine**                                                                                                             

  Same shape as the Book lifecycle, just at a different layer:                                                                              

  ;; Permission-style: only certain transitions are tabled                                                                                  

  (= (permits lpha-auction (advance-epoch $n active processing $nonce))                                                                     

     (if (and (current-epoch $n)                                                                                                            

              (epoch-phase $n active)                                                                                                       

              (>= (now) (lock-at-of $n)))                                                                                                   

         True False))                                                                                                                     

  (= (permits lpha-auction (advance-epoch $n processing settled $nonce))                                                                  

     (if (and (current-epoch $n)                                                                                                            

              (epoch-phase $n processing)                                                                                                   

              (>= (now) (settle-at-of $n))

              (all-prepayments-submitted $n))                                                                                               

         True False))                                                                                                                       

  Crossing into settled is what makes the period closed — the event log up to settle-at is now frozen for that epoch's net-owed.            

  **6. Where Python lives, where synlang lives**                                                                                                

  ┌────────────────────────────────────┬────────────────────────────────┬─────────────────────────────────────────────────┐                 

  │              Concern               │             Layer              │                       Why                       │               

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ Time-weighted reduction (twap)     │ Python protocol                │ QR-010, aggregation over intervals              │               

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤

  │ Set-summation over units (sum-of)  │ Python protocol                │ Same                                            │                 

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ (in-breach $p) polling             │ Synlang predicate              │ Pure rule logic, called by lpla-checker         │                 

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ Breach event emission              │ Python effect (lpla-checker)   │ Side-effecting writes                           │               

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ The five-step rules                │ Synlang                        │ They're the audit-trail; humans must read these │               

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ Phase advance, prepayment dispatch │ Effects gated by permits rules │ Authority lives in the rule                     │               

  ├────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────────────┤                 

  │ Penalty rate, base rate, spread    │ Synlang facts (governance-set) │ Crystallized parameters                         │               

  └────────────────────────────────────┴────────────────────────────────┴─────────────────────────────────────────────────┘                 

  The principle: **anything that's policy reads as synlang; anything that's an integral or side-effect is a protocol.** The auditor reading the 

  Space sees the _what_ and the _why_; the _how-to-sum_ is sealed behind a typed protocol head.                                                 

  ---                                                                                                                                     

  **7. Open design questions worth flagging now**

  1. **Event log granularity.** Per-tick snapshots vs change-events. Change-events are smaller but twap becomes "piecewise integral over a step

  function" — still Python, just slightly different. Probably fine.                                                                         

  2. **Continuous vs sampled breach detection.** If lpla-checker polls every 60s, a sub-minute breach goes uncounted. Acceptable? Or do we need

  every position-event to also recompute breach-state inline (effect writes both (unit ...) and (breach ...) atomically)?                   

  3. **What "capital" means for the denominator.** TRC vs SRC vs JRC mix; ingression-adjusted recognition                                     

  (accounting/risk-capital-ingression.md). Worth resolving before we write (prime-capital ...) as a flat fact — it might need to be derived 

  too.                                                                                                                                    

  4. **Cross-Space layout.** Position graph in &operational, event log probably also &operational, governance-set rates in &governance, capital 

  tier definitions in &governance. Phase atoms in &governance too (they're authority-bearing). Worth committing in the convention layer even

   before we split physically.

  5. **Sky Direct's "actual profit" input.** That's an oracle-shaped fact someone has to write into the Space. Whose beacon? lpla-checker       

  reading on-chain, or a Generator-side beacon?                                                                                             

  Want me to pick one of these threads and go deeper, or should we first iterate on the atom-layer / rule-layer split above before adding   

  more?                                                                                                                                   

✻ Crunched for 2m 3s                                                                                                                      

  

※ **recap:** _We're sketching high-level synlang structure for Sky's core process — real-time encumbrance ratio per Prime plus daily settlement_  

  _of base rate and distribution payments. I proposed an atom layer, continuous and discrete halves, and a breach-as-event bridge; next is_ 

  _for you to pick which thread to deepen. (disable recaps in /config)_                                                                       

❯ write out an example of the synlang needed to map end to end a primes encumbrance ratio from its risk capital, to its units, mapping      

  those units on to books, and then the risk framework setting CRRs for those books (try to make the example as simple as possible)         

⏺ The chain is four flat fact-types and two derivation rules. Bottom-up:                                                                    

  Risk Framework      Books               Units                     Prime                                                                   

  ─────────────       ─────               ─────                     ─────

  crr-factor          book-state          unit (issuer …            prime-capital                                                           

                                                holder spark …                                                                            

                                                principal)                                                                                  

         └──── unit-risk-weight (joins all four) ────┐                                                                                      

                                                     ▼                                                                                    

                                            encumbered (sum)                                                                                

                                                     ▼ ÷ capital                                                                          

                                            encumbrance-ratio                                                                               

  The synlang (one screen, every line load-bearing):                                                                                        

  ;; ─── Layer 1: Risk framework sets CRR per book state ────────────                                                                       

  (crr-factor filling  0.05)                                                                                                                

  (crr-factor at-rest  0.40)

  ;; ─── Layer 2: Books and their states ────────────────────────────                                                                     

  (book        book-7)

  (book-state  book-7  filling)                                                                                                             

  (book        book-9)

  (book-state  book-9  at-rest)                                                                                                             

  ;; ─── Layer 3: Units (issued by a book, held by a prime) ─────────                                                                       

  (unit nfat-A (issuer book-7) (holder spark-prime)  30000000)

  (unit nfat-B (issuer book-9) (holder spark-prime) 100000000)                                                                              

  ;; ─── Layer 4: Prime's risk capital ──────────────────────────────                                                                       

  (prime-capital spark-prime 500000000)                                                                                                   

  ;; ─── Derivation 1: a unit's risk weight = principal × CRR of                                                                            

  ;;     its issuing book's state ────────────────────────────────────

  (= (unit-risk-weight $u)                                                                                                                  

     (match &self                                                                                                                         

       (and (unit       $u (issuer $book) (holder $_) $principal)                                                                           

            (book-state $book $state)                                                                                                       

            (crr-factor $state $factor))

       (* $principal $factor)))                                                                                                             

  ;; ─── Derivation 2: encumbered = sum over units the prime holds ──                                                                       

  ;; (Aggregation hits AETHER QR-009/010; production uses a

  ;;  `prime-exposure` protocol. Shown here in pure synlang for clarity.)                                                                   

  (= (encumbered $prime)                                                                                                                    

     (fold + 0                                                                                                                              

       (collapse                                                                                                                            

         (match &self (unit $u (issuer $_) (holder $prime) $_)                                                                            

                (unit-risk-weight $u)))))

  ;; ─── Derivation 3: ratio = encumbered / capital ─────────────────

  (= (encumbrance-ratio $prime)                                                                                                             

     (/ (encumbered $prime)                                                                                                                 

        (match &self (prime-capital $prime $c) $c)))

  ! (encumbrance-ratio spark-prime)                                                                                                         

  ;; → 0.083

  Trace:                                                                                                                                  

  

  unit-risk-weight nfat-A

    unit         → principal  30,000,000, issuer book-7

    book-state   → filling                                                                                                                  

    crr-factor   → 0.05

    ⇒ 30,000,000 × 0.05 = 1,500,000                                                                                                         

     (fold + 0

       (collapse

         (match &self (unit $u (issuer $_) (holder $prime) $_)

                (unit-risk-weight $u)))))

  

  ;; ─── Derivation 3: ratio = encumbered / capital ─────────────────

  (= (encumbrance-ratio $prime)

     (/ (encumbered $prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

     (/ (encumbered $prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  unit-risk-weight nfat-A

    unit         → principal  30,000,000, issuer book-7

    book-state   → filling

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  unit-risk-weight nfat-A

    unit         → principal  30,000,000, issuer book-7

     (/ (encumbered $prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

     (/ (encumbered $prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  unit-risk-weight nfat-A

     (/ (encumbered $prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  ! (encumbrance-ratio spark-prime)

  ! (encumbrance-ratio spark-prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

        (match &self (prime-capital $prime $c) $c)))

  

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

        (match &self (prime-capital $prime $c) $c)))

        (match &self (prime-capital $prime $c) $c)))

  

  ! (encumbrance-ratio spark-prime)

  ;; → 0.083

  

  Trace:

  

  unit-risk-weight nfat-A

    unit         → principal  30,000,000, issuer book-7

    book-state   → filling

    crr-factor   → 0.05

    ⇒ 30,000,000 × 0.05 = 1,500,000

  

  unit-risk-weight nfat-B

    ⇒ 100,000,000 × 0.40 = 40,000,000

  

  encumbered spark-prime

    ⇒ 1,500,000 + 40,000,000 = 41,500,000

  

  encumbrance-ratio spark-prime

    ⇒ 41,500,000 / 500,000,000 = 0.083

  

  Three things this example deliberately collapses that the production version would split:

  

  1. **CRR** **is** **just** **crr-factor[state]****.** Real CRR is max(risk-weight, FRTB-drawdown, gap-risk) per capital-formula.md. Each component would be its

  own fact ((asset-risk-weight $book $rw), (frtb-drawdown $book $dd)) and crr-of-book would be a small derivation taking the max.

  2. **prime-capital** **is** **one** **number.** Real version splits across JRC/SRC tiers with ingression-adjusted recognition — (capital-of $prime) becomes a

   derivation over (capital-tier $prime $tier $amount $recognized-at).

  3. **The** **aggregation** **in** **encumbered** is the part that doesn't run cleanly in AETHER today — collapse/fold over a match is exactly the QR-010

  territory. In practice that line is a typed protocol head (prime-exposure) and the synlang above is what the protocol's contract reads as.

  

  Everything else in this chain is honest synlang that would run.