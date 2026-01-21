# Phase 2 Trust Upgrade Criteria

## 1. Purpose
To establish a rigorous, evidence-based protocol for elevating system autonomy (Trust Levels) within the EatClub ecosystem. This policy ensures that automation is earned through household-specific verification, never assumed, and remains fully reversible.

## 2. Trust Levels Covered
This policy governs the transition between the following Machine Trust & Responsibility Interface (MTRI) levels:
*   **T1 (Epistemic Humility)**: System Suggests, User Decides. (Default)
*   **T2 (Assisted Execution)**: System Stages, User Confirms. (Upgrade Target 1)
*   **T3 (Supervised Autonomy)**: System Executes, User Reviews. (Upgrade Target 2)

## 3. Preconditions for Upgrade
No upgrade process may initiate unless ALL following conditions are met:
1.  **Household Specificity**: Evidence is derived solely from the local household's interaction history. Global averages are strictly strictly inadmissible.
2.  **Feature Isolation**: Trust is tracked and upgraded per specific capability (e.g., "Email Parsing" is distinct from "Depletion Logic").
3.  **Minimum Viability Period**: The feature must operate at the lower trust level for a minimum of 14 active days.
4.  **Data Integrity**: The local ledger must show zero corruption or unexplained gaps.

## 4. Evidence Required

### 4.1 Upgrade T1 → T2 (Proposals to Drafts)
*Criteria to allow the system to create pre-filled drafts awaiting confirmation.*
*   **Consistency**: Last 20 consecutive T1 suggestions accepted with **Zero** edits to the `ItemIdentity`.
*   **Precision**: Quantity variance on accepted items is < 5% over the same window.
*   **Volume**: Minimum 50 distinct interactions recorded for this feature.
*   **User Action**: Explicit opt-in via "Enable Smart Drafting" settings.

### 4.2 Upgrade T2 → T3 (Drafts to Ledger)
*Criteria to allow the system to commit directly to the ledger within safety bounds.*
*   **Perfect Track Record**: Last 100 consecutive T2 drafts confirmed WITHOUT modification or rejection.
*   **Safety Boundedness**: The feature has defined "Max Value" and "Max Quantity" limits (e.g., < $50, < 2kg) which T3 will never exceed.
*   **Verification Challenge**: User successfully completes a "Spot Check" test, identifying an injected error during a trust audit.
*   **Zero "Truth Failures"**: No user-reported logic errors in the previous 30 days.

## 5. Explicit Non-Qualifiers
The following metrics MUST NOT be used to justify trust upgrades:
*   **ML Confidence Scores**: An internal model confidence of "99.9%" is irrelevant. Only observed outcome correctness matters.
*   **Global Popularity**: "Most users enable this" is not evidence for the current household.
*   **Time Elapsed**: Duration of use without interaction volume counts as zero.
*   **Silence**: Lack of user complaints is not evidence of success; only affirmative confirmations count.

## 6. Downgrade Triggers
Trust is fragile. Any of the following triggers an immediate fallback to the previous level:
*   **Single Blocking Error**: Any draft/action rejected as "Factually Incorrect" (Hallucination).
*   **Edit Spike**: User edits > 10% of generated drafts in any 7-day rolling window.
*   **Manual Revocation**: User toggles "Strict Mode" or manually degrades trust.
*   **System Update**: Major version updates to the logic kernel reset trust to T1 for re-verification.

## 7. Audit & Review Requirements
*   **Immutable Logging**: Every upgrade event must be recorded in the Ledger with a checksum of the evidence used.
*   **Periodic Re-Verification**: T3 status expires every 90 days, requiring a 1-week "Shadow Mode" (T2) period to re-confirm accuracy.
*   **Explainable State**: The system must provide a human-readable "Trust Report" on demand, showing exactly which transactions contributed to the current standing.
