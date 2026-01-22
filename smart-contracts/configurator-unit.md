# Configurator Unit — Business Requirements

## Executive Summary

The Configurator Unit is a governance layer that controls rate limits and static parameters for Parallelized Allocation Units (PAUs) without modifying deployed ALM Controller contracts. It uses a two-tier access model: **aBEAMs** (admin BEAMs) manage inits and role assignments with timelock protection, while **cBEAMs** (configurator BEAMs) operationally manage specific PAUs within bounded constraints.

---

## Concepts

| Term | Definition |
|------|------------|
| **PAU** | Parallelized Allocation Unit — the standard building block consisting of Controller, ALMProxy, and RateLimits contracts |
| **Configurator Unit** | The governance layer (BEAMTimeLock + BEAMState + Configurator) that manages a set of PAUs |
| **BEAM** | Bounded External Access Module — an authorized role with constrained operational capabilities |
| **aBEAM** | Admin BEAM — Core Council role that manages inits and cBEAM assignments (via timelock) |
| **cBEAM** | Configurator BEAM — a role that exists for each PAU; when granted to a GovOps, that GovOps becomes accordant to the PAU |
| **GovOps** | Governance Operations team — an operational entity that receives cBEAMs from Core Council, making them accordant to specific PAUs |
| **Accordant** | A GovOps is accordant to a PAU when Core Council has granted them the cBEAM for that PAU |
| **Init rate limit** | A pre-approved rate limit configuration (maxAmount, slope) that accordant GovOps can instantiate for their PAUs |
| **Init controller action** | A pre-approved controller function call (e.g., `setMaxSlippage`) that accordant GovOps can execute for their PAUs |
| **Restricted init** | An init that can only be used by a specific PAU (when `pau != address(0)`) |
| **Relayer** | The address that executes operations on the Controller; set by accordant GovOps via `setRelayer` |
| **Freezer** | The address that can remove compromised relayers from a Controller; set by accordant GovOps via `setFreezer` |
| **Second-order rate limit (SORL)** | The constraint on how fast rate limits can be increased (default: 20% per 18 hours) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  aBEAMs                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │Core Council │  │    Mom      │  │   Freezer   │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
└─────────┼────────────────┼────────────────┼─────────────────────┘
          │                │                │
          ▼                ▼                ▼
   ┌─────────────────────────────────────────────────┐
   │           CONFIGURATOR UNIT                     │
   │                                                 │
   │  ┌─────────────┐                                │
   │  │BEAMTimeLock │◄── schedule/execute additions  │
   │  └──────┬──────┘                                │
   │         │                                       │
   │         ▼                                       │
   │  ┌─────────────┐                                │
   │  │ BEAMState   │◄── inits + accordant mappings  │
   │  └──────┬──────┘                                │
   │         │                                       │
   │         ▼                                       │
   │  ┌─────────────┐                                │
   │  │Configurator │◄── cBEAMs operate here         │
   │  └──────┬──────┘                                │
   └─────────┼───────────────────────────────────────┘
             │
┌────────────┼────────────────────────────────────────┐
│  cBEAMs    │  (held by GovOps teams)                │
│  ┌─────────┴───┐  ┌─────────────┐                   │
│  │  GovOps 1   │  │  GovOps 2   │                   │
│  └─────────────┘  └─────────────┘                   │
└─────────────────────────────────────────────────────┘
             │
             ▼
   ┌─────────────────────────────────────────────────┐
   │           PARALLELIZED ALLOCATION UNIT          │
   │                                                 │
   │  ┌─────────────┐                                │
   │  │ RateLimits  │◄── configured by Configurator  │
   │  └──────┬──────┘                                │
   │         │                                       │
   │         ▼                                       │
   │  ┌─────────────┐                                │
   │  │ Controller  │◄── static params set here      │
   │  └──────┬──────┘                                │
   │         │                                       │
   │         ▼                                       │
   │  ┌─────────────┐                                │
   │  │  ALMProxy   │◄── holds custody of funds      │
   │  └─────────────┘                                │
   └─────────────────────────────────────────────────┘
```

---

## Role Capabilities

### aBEAM (Core Council, Mom, Freezer)

| Action | Timelock | Description |
|--------|----------|-------------|
| Register PAU | ✓ | Map a PAU identifier to its Controller and RateLimits contracts |
| Add init rate limit | ✓ | Approve a rate limit that any PAU can use (`pau=0`) |
| Add restricted init rate limit | ✓ | Approve a rate limit for a specific PAU only |
| Add init controller action | ✓ | Approve a controller call (e.g., `setMaxSlippage`) |
| Grant cBEAM to GovOps | ✓ | Make a GovOps accordant to specific PAUs |
| Unregister PAU | ✗ | Instantly remove a PAU registration |
| Delete init rate limit | ✗ | Instantly remove an approved init |
| Revoke cBEAM from GovOps | ✗ | Instantly remove a GovOps's accordant status |
| Pause BEAMTimeLock | ✗ | Emergency halt all pending operations |

### cBEAM (held by GovOps Teams)

| Action | Constraint | Description |
|--------|------------|-------------|
| Set rate limit | Must have init | Convert an init rate limit into an active rate limit for an accordant PAU |
| Increase rate limit | SORL | Max 20% increase per 18h cooldown period |
| Decrease rate limit | None | Always instant |
| Call controller action | Must have init | Execute an approved controller call for an accordant PAU |
| Set relayer | None | Set the relayer address for an accordant PAU |
| Set freezer | None | Set the freezer address for an accordant PAU |
| Remove rate limit | None | Disable a configured rate limit |

---

## Contract Interfaces

### BEAMState

Storage for inits and accordant mappings. No logic—data and access control only.

```solidity
/// Check if an init rate limit exists for this key and PAU (or globally if pau=0)
function getInitRateLimits(bytes32 key, address pau)
    external view returns (DefaultRateLimits memory);

/// Check if a controller action is enabled for this PAU (or globally)
function isControllerActionEnabled(bytes32 key, address pau)
    external view returns (bool);

/// Grant admin authorization
function rely(address usr) external auth;

/// Revoke admin authorization  
function deny(address usr) external auth;

/// Grant cBEAM (GovOps) permission for a PAU
function addGovOps(address pau, address usr) external auth;

/// Revoke cBEAM permission for a PAU
function delGovOps(address pau, address usr) external auth;

/// Add an init rate limit (global if pau=0, restricted if pau specified)
function addInitRateLimits(bytes32 key, address pau, uint256 maxAmount, uint256 slope)
    external auth;

/// Remove an init rate limit
function delInitRateLimits(bytes32 key, address pau) external auth;

/// Enable an init controller action (computes key from calldata)
function addInitControllerActions(bytes calldata data, address pau)
    external auth returns (bytes32 key);

/// Enable an init controller action (precomputed key)
function addInitControllerActions(bytes32 key, address pau) external auth;

/// Disable an init controller action
function delInitControllerActions(bytes32 key, address pau) external auth;
```

### BEAMTimeLock

OpenZeppelin TimelockController with pause capability. All additions flow through here.

```solidity
/// Pause scheduling and execution (emergency use by aBEAMs)
function pause() external;

/// Unpause (admin only)
function unpause() external onlyRole(DEFAULT_ADMIN_ROLE);

/// Schedule an operation with delay
function schedule(
    address target,
    uint256 value,
    bytes calldata data,
    bytes32 predecessor,
    bytes32 salt,
    uint256 delay
) public virtual override whenNotPaused;

/// Schedule a batch of operations
function scheduleBatch(
    address[] calldata targets,
    uint256[] calldata values,
    bytes[] calldata payloads,
    bytes32 predecessor,
    bytes32 salt,
    uint256 delay
) public virtual override whenNotPaused;

/// Execute a scheduled operation after delay
function execute(
    address target,
    uint256 value,
    bytes calldata payload,
    bytes32 predecessor,
    bytes32 salt
) public payable virtual override whenNotPaused;

/// Execute a batch of scheduled operations
function executeBatch(
    address[] calldata targets,
    uint256[] calldata values,
    bytes[] calldata payloads,
    bytes32 predecessor,
    bytes32 salt
) public payable virtual override whenNotPaused;

/// Update the timelock delay (admin only)
function adminUpdateDelay(uint256 newDelay) external onlyRole(DEFAULT_ADMIN_ROLE);
```

### Configurator

Operational interface for cBEAMs. Enforces SORL constraints on rate limit increases.

```solidity
/// Grant admin authorization
function rely(address usr) external auth;

/// Revoke admin authorization
function deny(address usr) external auth;

/// Add address to allowlist
function kiss(address usr) external auth;

/// Remove address from allowlist
function diss(address usr) external auth;

/// Set governance parameters (hop = cooldown period, maxChange = max increase %)
function file(bytes32 what, uint256 data) external auth;

/// Set or modify a rate limit for an accordant PAU
/// - Increases: subject to SORL (must wait `hop` since last increase, max `maxChange` percentage)
/// - Decreases: always allowed immediately
function setRateLimit(address pau, bytes32 key, uint256 maxAmount, uint256 slope)
    external govOps(pau);

/// Execute a whitelisted controller action (e.g., setMaxSlippage)
function callControllerAction(address pau, bytes calldata data)
    external govOps(pau) returns (bytes memory);
```

### BEAMRoleTimeLock

aBEAM interface for additions (routes through BEAMTimeLock).

```solidity
/// Grant cBEAM permission through timelock
function addGovOps(address pau, address usr) external onlySigner;

/// Add init rate limit through timelock
function addInitRateLimits(bytes32 key, address pau, uint256 maxAmount, uint256 slope)
    external onlySigner;

/// Enable init controller action (computes key)
function addInitControllerActions(bytes calldata data, address pau)
    external onlySigner returns (bytes32 key);

/// Enable init controller action (precomputed key)
function addInitControllerActions(bytes32 key, address pau) external onlySigner;
```

### BEAMRoleDirect

aBEAM interface for removals (no timelock required).

```solidity
/// Revoke cBEAM permission instantly
function delGovOps(address pau, address usr) external onlySigner;

/// Remove init rate limit instantly
function delInitRateLimits(bytes32 key, address pau) external onlySigner;

/// Disable init controller action instantly
function delInitControllerActions(bytes32 key, address pau) external onlySigner;
```

---

## Invariants

1. **PAU must be registered**: A PAU cannot be configured unless it has been registered via `setPauContracts`
2. **No configuration without init**: A rate limit cannot be set unless a matching init exists in BEAMState
3. **Accordant check**: A GovOps can only configure PAUs for which they hold the cBEAM (granted by aBEAM)
4. **SORL constraint**: Rate limit increases are bounded to `maxChange` per `hop` period
5. **Instant decreases**: Decreases are never blocked
6. **Timelock on additions**: All PAU registrations, init additions, and cBEAM grants require BEAMTimeLock delay
7. **Instant removals**: PAU unregistrations, init removals, and permission removals are immediate (emergency response)

---

## Default Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Timelock delay | 14 days | Minimum wait before additions take effect |
| `hop` | 18 hours | SORL cooldown between rate limit increases |
| `maxChange` | 20% (2000 bps) | SORL maximum increase per cooldown period |

---

## Deployment Scope

Each Configurator Unit manages PAUs within its scope:

| Configurator Unit | Manages |
|-------------------|---------|
| Generator Config | All Generator PAUs |
| Mainnet Config | All mainnet Prime + Halo PAUs |
| Altchain Config (per chain) | All Foreign Prime + Foreign Halo PAUs on that chain |

---

## Extra Requirements

**Parameter configurability**: The following parameters must be modifiable through the BEAMTimeLock itself (i.e., changes to these values require going through the timelock delay):

- **Timelock delay** — the delay period for BEAMTimeLock operations
- **`hop`** — the SORL cooldown period between rate limit increases
- **`maxChange`** — the SORL maximum percentage increase allowed per cooldown period

This ensures that changes to governance constraints are subject to the same monitoring window as other sensitive operations.

**Relayer management**: A `setRelayer` function must be available that allows an accordant GovOps to set the relayer address for their PAUs. This is controlled via the Configurator (not through BEAMTimeLock). Typically, a GovOps team will set itself as the relayer for its accordant PAUs, giving the GovOps unified control over:
- Relayer operations (executing transactions on the Controller)
- SORL increases (via Configurator)
- Onboarding new allocation targets (using inits via Configurator)

**PAU registration**: The Configurator needs a mapping from PAU identifier to its underlying contracts. A function like `setPauContracts(address pau, address controller, address rateLimits)` must exist so that:
- `setRateLimit(pau, ...)` knows which RateLimits contract to call
- `callControllerAction(pau, ...)` knows which Controller contract to call
- `setRelayer(pau, ...)` knows which Controller to set the relayer on

PAU registration should be an aBEAM function routed through BEAMTimeLock (adding new PAU infrastructure is a significant action). Removal should be instant for emergency response.

**Admin role prerequisites**: Before a PAU can be managed through the Configurator Unit, the deployed PAU contracts (Controller, RateLimits) must grant the Configurator the necessary admin roles (`DEFAULT_ADMIN_ROLE` or equivalent). This is a deployment-time concern, not managed by the Configurator Unit itself.

**Freezer management**: The Controller's FREEZER role (which can remove compromised relayers) should be settable by accordant GovOps via the Configurator, similar to `setRelayer`.

---

## User Stories

### Story 1: Full Prime Onboarding

**Goal**: Core Council onboards a new Prime and a new Halo for it to deploy into, then hands operational control to a GovOps team.

**Prerequisites**: 
- Prime PAU contracts (Controller, ALMProxy, RateLimits) have been deployed
- PAU contracts have granted admin roles to the Configurator

**Flow**:

1. **aBEAM registers the new PAU** (via BEAMTimeLock, 14-day delay):
   ```
   setPauContracts(primeA, primeAController, primeARateLimits)
   ```

2. **aBEAM creates inits for the new Halo** (via BEAMTimeLock, 14-day delay):
   ```
   addInitRateLimits(LIMIT_4626_DEPOSIT + haloVault, pau=0, maxAmount=10M, slope=115k/s)
   addInitRateLimits(LIMIT_4626_WITHDRAW + haloVault, pau=0, maxAmount=MAX, slope=0)
   addInitControllerActions(setMaxSlippage(haloVault, 0.999e18), pau=0)
   ```

3. **aBEAM grants cBEAM to GovOps** (via BEAMTimeLock, 14-day delay):
   ```
   addGovOps(primeA, govOpsAddress)
   ```

4. **After BEAMTimeLock executes** (14 days later), GovOps is now accordant to Prime A

5. **GovOps sets rate limits using inits**:
   ```
   configurator.setRateLimit(primeA, LIMIT_4626_DEPOSIT + haloVault, 10M, 115k/s)
   configurator.setRateLimit(primeA, LIMIT_4626_WITHDRAW + haloVault, MAX, 0)
   ```

6. **GovOps sets maxSlippage using init**:
   ```
   configurator.callControllerAction(primeA, setMaxSlippage(haloVault, 0.999e18))
   ```

7. **GovOps sets itself as relayer**:
   ```
   configurator.setRelayer(primeA, govOpsAddress)
   ```

8. **GovOps starts deploying capital** (as relayer, directly on Controller):
   ```
   primeAController.depositERC4626(haloVault, 5M)
   ```

9. **GovOps increases rate limit via SORL** to deploy more:
   ```
   // 18 hours later
   configurator.setRateLimit(primeA, LIMIT_4626_DEPOSIT + haloVault, 12M, 138k/s)  // +20%
   
   // Another 18 hours later
   configurator.setRateLimit(primeA, LIMIT_4626_DEPOSIT + haloVault, 14.4M, 166k/s)  // +20%
   ```

**Result**: GovOps now has unified control over Prime A — managing relayer operations, rate limit configuration, and SORL increases.

---

### Story 2: Onboarding a New Yield Source to Existing Prime

**Goal**: A GovOps team (accordant to Prime A) wants to deploy capital to a new Morpho vault.

1. **aBEAM creates inits** (via BEAMTimeLock, 14-day delay):
   ```
   addInitRateLimits(LIMIT_4626_DEPOSIT + vault, pau=0, maxAmount=10M, slope=115k/s)
   addInitRateLimits(LIMIT_4626_WITHDRAW + vault, pau=0, maxAmount=MAX, slope=0)  // unlimited
   addInitControllerActions(setMaxSlippage(vault, 0.999e18), pau=0)
   ```

2. **After BEAMTimeLock executes**, inits are active in BEAMState

3. **GovOps (holding cBEAM for Prime A) sets rate limits and calls controller action**:
   ```
   configurator.setRateLimit(primeA, LIMIT_4626_DEPOSIT + vault, 10M, 115k/s)
   configurator.setRateLimit(primeA, LIMIT_4626_WITHDRAW + vault, MAX, 0)
   configurator.callControllerAction(primeA, setMaxSlippage(vault, 0.999e18))
   ```

4. **GovOps can now increase limits** (subject to SORL: 20%/18h):
   - Day 1: 10M → 12M ✓
   - Day 2: 12M → 14.4M ✓
   - Day 7: up to ~35.8M

---

### Story 3: Emergency Response

**Goal**: Vulnerability discovered in a yield source.

1. **GovOps instantly decreases rate limit** (no cooldown):
   ```
   configurator.setRateLimit(primeA, key, 0, 0)
   ```

2. **If broader action needed, aBEAM can**:
   - Remove the init entirely (instant via `delInitRateLimits`)
   - Pause the BEAMTimeLock to halt all pending additions

---

*Document Version: 0.1*