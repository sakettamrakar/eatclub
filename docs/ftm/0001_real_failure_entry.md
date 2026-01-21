# Failure Taxonomy Map Entry: FTM-0001

**Failure ID:** FTM-0001
**Date:** 2026-01-22
**Household Context:** Household-Alpha (2 adults, 1 child, high cooking frequency)

**User Expectation:**
To proceed with the "Baked Macaroni" recipe suggested by the app, expecting the primary ingredient (Cheddar Cheese) to be available.

**System Belief:**
System held a high-confidence record (Confidence: 1.0) of `Item: Cheddar Block`, `Qty: 500g`, `Status: In Stock`.
Source: Manual Invoice Scan validated 48 hours prior.

**Reality Observed:**
Upon physical inspection during prep, the user found approximately 100g of the Cheddar Block remaining. The package was open and significantly depleted.

**Broken Assumption:**
*Static World Assumption*: "Inventory quantity remains constant between documented purchase and documented consumption events."
The system assumed independent agents (family members) would not deplete stock without interacting with the ledger.

**Impact on Trust:**
Moderate degradation. The user successfully found a substitute recipe but expressed frustration ("Why suggest it if I can't cook it?").
*Trust State Change:* T2 (Assisted) → T1 (User Verification required for high-risk items).

**Related Invariants:**
*   **IDS-11 (No Inference)**: The system correctly did NOT infer depletion without evidence, but this correctness led to a utility failure.
*   **IDS-1 (Ledger Integrity)**: The ledger accurately reflected the *recorded* history, but failed to reflect *reality*.

**Immediate Action Taken:**
User performed a manual `CorrectionRemoveEvent` (-400g) with the reason code `UNLOGGED_CONSUMPTION`.
Recipe feasibility score for "Baked Macaroni" dropped to 0.0 immediately.

**Deferred Action:**
None. The system behaved according to current Phase-1 specifications. No bug was found.
