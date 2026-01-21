# Simulation: Failure to Governance Loop (Dry Run)

**Date:** 2024-05-23
**Simulation ID:** SIM-001
**Status:** COMPLETED

## 1. Failure Scenario Description
**Title:** The Loose Basmati Rice Density Variance

**Context:**
The household sources "Basmati Rice" from a local kirana store in loose bulk format. The system is configured with a global entity `Rice (Basmati)` which has a volumetric conversion property defined as `1 Cup = 200g` (Standard Long Grain).

**Incident:**
Over a period of 45 days, the user logs 20 cooking sessions. In each session, the user logs consumption of "1 Cup" of rice using the standard volumetric scoop. The system, behaving deterministically, deducts `200g` per session.
Total System Deduction: `20 * 200g = 4000g`.

**Reality:**
The specific variety of loose Basmati rice purchased has a lower bulk density than the system standard. The actual mass of rice in the user's "1 Cup" scoop is `180g`.
Total Real Consumption: `20 * 180g = 3600g`.

**Outcome:**
The system ledger shows the rice container is empty (0g remaining).
The physical container actually holds `400g` of rice.
When the user attempts to log the 21st session ("1 Cup"), the system blocks the action citing "Insufficient Inventory", despite the user clearly seeing rice in the jar.

## 2. Assumption Violated
**Assumption:** `A-004-Volumetric-Constancy`
"Volumetric units (cups, tbsp) map to mass-based units (grams) using a single, immutable global constant for a given ingredient type."

**Violation:**
Bulk density is not an immutable constant for loose commodities; it varies by batch, moisture content, and grain size. The system's "Truth First" architecture prioritized its internal constant over the physical reality of variable density.

## 3. FTM Entry (Structured)

| Field | Entry |
| :--- | :--- |
| **Failure ID** | `F-001-DensityVariance` |
| **User Expectation** | The system allows logging consumption when physical inventory exists. |
| **System Belief** | Inventory is `0g`. Consumption is impossible. |
| **Reality Observed** | Inventory is `400g`. Consumption is physically possible. |
| **Broken Assumption** | `A-004-Volumetric-Constancy`: Density is constant across batches. |
| **Design Implication** | Loose commodities cannot rely on global density constants for T3 (Bounded Auto) tracking. |
| **Linked Invariant** | `IDS-007`: Recipe feasibility must be computable strictly from current inventory state. |

## 4. RADAR BLUE Findings (Condensed)

*   **R (Reality):** Validated. Physical audit confirms `400g` surplus vs. Ledger `0g`. System hallucinated higher consumption.
*   **A (Assumptions):** The assumption that `Density` is a static property of the `Ingredient` class is false for `Loose` procurement types.
*   **D (Decisions):** The decision logic `deduct(cups * density)` remains valid but the input parameter `density` must be scoped to the `Batch`, not the `Ingredient`.
*   **A (Authority):** The system does not have the authority (Trust Level) to assume density for loose items without user verification.
*   **R (Records):** The ledger accurately recorded the *system's intent* (deduct 200g) but failed to record *physical truth*. Historical entries are immutable and will not be changed. A correction entry is required.

## 5. ITSMC Mapping

| Strategic Finding (RADAR) | Operational Lever (ITSMC) | Action |
| :--- | :--- | :--- |
| **R**eality Mismatch | **State** | **Mutation:** `CORRECTION_ADD` +400g to reconcile ledger. |
| **A**ssumption Broken | **Trust** | **Adjustment:** Downgrade `Volumetric Inference` for `Loose` items from T2 to T0. |
| **D**ecision Flaw | **Intent** | **Refinement:** System intent shifts from "Infer mass" to "Request mass" for this category. |
| **A**uthority Check | **Consequence** | **Audit:** Log incident F-001. Flag `Rice (Basmati)` as `Low Confidence`. |

## 6. Governance Actions Triggered

1.  **State Correction:**
    *   Execute `CORRECTION_ADD` transaction: `+400g Rice (Basmati)` with reason code `AUDIT_RECONCILIATION`.
2.  **Trust Adjustment (MTRI):**
    *   Change Trust Level for `Rice (Basmati)` volumetric log from **T2 (Execute on Approval)** to **T0 (Read/Analyze)**.
    *   *Effect:* User can no longer just click "1 Cup". System will now ask "Weight?" or require a one-time density check for the new batch.
3.  **Epistemic Update:**
    *   Tag `Ingredient: Rice (Basmati)` with property `variance_risk: high`.
4.  **IDS Stress Test:**
    *   Trigger review of `IDS-007`. No change needed, but the incident reinforces the rule that inventory state must be accurate for feasibility to work.

## 7. Actions Explicitly NOT Taken

*   **Feature Request:** No "Smart Scale Integration" proposed. (Violates Phase 1 Scope).
*   **Code Change:** No modification to the `Ingredient` class structure or density database. (Violates Risk Detector).
*   **Auto-Correction:** The system did NOT automatically update the density constant based on the mismatch. (Violates IDS-11: No inference without user action).
*   **History Rewrite:** The previous 20 entries of `200g` deduction remain as is. We do not retroactive fix history. (Violates IDS-10).

## 8. Final System State After Simulation

*   **Ledger:** Contains 20 entries of `-200g` and 1 entry of `+400g (Correction)`. Balance: `400g`.
*   **Trust:** `Rice (Basmati)` requires explicit weight or batch-specific density confirmation for future logs.
*   **User Experience:** Slightly higher friction (must verify weight) but higher truth accuracy.
*   **Governance:** Incident closed. FTM F-001 recorded.
