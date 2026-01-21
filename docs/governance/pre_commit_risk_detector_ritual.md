# Pre-Commit Risk Detector Ritual

## 1. Purpose
This ritual serves to identify and neutralize irreversible risks before they are embedded into the system's history. It acts as a final cognitive barrier to ensure that all changes adhere strictly to system invariants, trust levels, and epistemic boundaries.

## 2. When This Ritual Is Mandatory
Execution of this ritual is required before:
- Committing any AI-generated code.
- Committing any AI-generated documentation.
- Committing any code refactors.
- Applying changes that alter Trust Levels (MTRI).
- Applying any changes that touch system state or schema.
- Merging any branch into the main branch.

## 3. Inputs Required Before Running
The following documents must be available and referenced during the ritual:
- DWBS (Deterministic Work Breakdown System) status.
- IDS (Invariants & Disqualifiers System) rules.
- MTRI (Multi-Tier Trust Index) definitions.
- Drift Detector Checklist.
- Relevant Decision Logs (if applicable).

## 4. Risk Detector Questions

### Scope Risk
1. Does this change implement features outside the currently active Phase (e.g., Phase 2 or 3)?
2. Does this change introduce a new dependency not explicitly authorized by an ADR?
3. Does this change modify the system's core purpose or domain boundaries?

### Trust Risk
1. Does this change grant the AI agent a Trust Level higher than its current MTRI assignment?
2. Does this change bypass the "Execute on Approval" requirement for state mutation?
3. Does this change remove or weaken an existing authorization check?

### Epistemic Risk
1. Does this change introduce logic that relies on probabilistic or non-deterministic outputs?
2. Does this change allow the system to claim knowledge it cannot verify against the Ledger?
3. Does this change contradict a falsifiable system belief defined in the Epistemic Layer?

### Irreversibility Risk
1. Does this change perform a data migration that cannot be cleanly rolled back?
2. Does this change delete data or history in a way that violates the append-only principle?
3. Does this change introduce a public API or contract that commits us to long-term support without review?

### Reality Misalignment Risk
1. Does this change model a physical process (e.g., cooking, storage) in a way that simplifies it to the point of inaccuracy?
2. Does this change assume user behavior that has not been observed or validated?
3. Does this change create a state representation that can permanently diverge from physical reality?

## 5. Stop Conditions
The commit process MUST STOP immediately if:
- Any answer to the Risk Detector Questions is "YES".
- A required input document is missing or outdated.
- The Trust Level required for the change exceeds the operator's or agent's current clearance.
- There is ambiguity regarding whether an Invariant (IDS) is violated.

## 6. Allowed Outcomes
The only permissible outcomes of this ritual are:
- **Proceed with commit:** All questions answered "NO", and all inputs validated.
- **Revise and re-run ritual:** A risk was identified; the change must be modified to eliminate the risk, then the ritual repeats.
- **Block and escalate:** A fundamental conflict with system laws is identified that cannot be resolved by revision.

## 7. Escalation Path
- **Decision Log:** If a "YES" answer reveals a gap in current architecture, a new Decision Record (ADR) must be drafted and approved before proceeding.
- **RADAR BLUE:** If a Reality Misalignment Risk is identified, a RADAR BLUE review must be scheduled to audit the divergence.
- **Trust Level Downgrade:** If an agent attempts to bypass Trust Risk checks, its MTRI level must be immediately downgraded, and its autonomy suspended until recertification.
