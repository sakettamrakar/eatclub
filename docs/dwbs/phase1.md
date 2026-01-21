# DWBS Phase 1 — Solid v1 (Foundation & Truth)

**Objective:** Establish an irreversible household food truth layer. The app must work end-to-end for real households without automation crutches.
*Status: Frozen Scope. Do not add features beyond this phase.*

## D0. System Contracts (Mandatory)
*Outcome: Every future feature obeys fixed contracts. No silent mutation.*

### Deliverables
*   **D0.1 Inventory State Contract:** Strictly define what "in stock" means (e.g., physical presence vs. planned).
*   **D0.2 Mutation Rules:** explicitly define who/what can change inventory.
*   **D0.3 Explainability Contract:** Every system suggestion must have a traceable "why" (e.g., "Recommended because Milk expires in 2 days").
*   **D0.4 Failure Rules:** Define behavior when data is missing (fail safe, don't guess).

### Acceptance
*   Any future automation must comply with these contracts.
*   No silent state mutation allowed.
*   This is the "moat seed" (Anti-Blinkit strategy).

## D1. Inventory Ledger (Core System of Record)
*Outcome: Time-aware, human-correctable household ledger. Single source of truth.*

### Key Sub-deliverables
*   **D1.1 Event-Sourcing Lite:** Append-only log of all inventory changes (Bought -> Used -> Wasted).
*   **D1.2 Item Identity Resolution:** Distinguish specific forms (e.g., Tomato vs. Tomato Puree vs. Canned Tomato).
*   **D1.3 Quantity & Unit Normalization:** Handle kg, pcs, ml with uncertainty handling (e.g., "approx 2 onions").
*   **D1.4 Confidence Scores:** Track source reliability (Manual > OCR > Inference).
*   **D1.5 Expiry & Purchase Tracking:** Deterministic expiry logic based on purchase date.
*   **D1.6 Waste as First-Class Event:** Track waste explicitly, not just deletion.

### Acceptance
*   Inventory can be reconstructed for any past date.
*   Users can see *why* the system believes an item exists.
*   No negative quantities.

## D2. Recipe Knowledge Graph
*Outcome: Structured cooking graph usable for reasoning, not just a recipe list.*

### Key Sub-deliverables
*   **D2.1 Structured Ingredient Mappings:** Ingredient → quantity mappings with substitutability graph.
*   **D2.2 Loss Factors:** Account for shrinkage (raw → cooked state).
*   **D2.3 Cultural & Context Tags:** Indian household bias (e.g., "tadka" dependencies), Meal categories (Breakfast/Lunch/Dinner).
*   **D2.4 Operational Metadata:** Prep time, difficulty, and mandatory vs. optional ingredients.

### Acceptance
*   Recipe feasibility is computable directly from inventory.
*   Graph is usable for logic/querying without a UI.
*   No free-text dependency in the logic layer.

## D3. Decision Engine v1 (Truth-Preserving)
*Outcome: Deterministic, auditable decisions. NO ML/Hallucinations.*

### Explicit Non-Goals
*   ❌ No Machine Learning
*   ❌ No Personalization (in this phase)
*   ❌ No "Smart" Guesses

### Key Sub-deliverables
*   **D3.1 Feasibility Scoring:** Binary or score-based calculation of "can I cook this?".
*   **D3.2 Confidence-Aware Scoring:** Suggest recipes based on high-confidence inventory items first.
*   **D3.3 Expiry Prioritization:** Weighted scoring to use expiring items.
*   **D3.4 "Ask User" Branch:** Explicit flow to query user when uncertainty exceeds threshold (instead of guessing).
*   **D3.5 Explanation Generator:** "Why this recipe?" (e.g., "Uses Spinach expiring tomorrow").

### Acceptance
*   System prefers asking over hallucinating.
*   Same inputs → same outputs (Deterministic).
*   Recommendation rationale is visible to the user.

## D4. Assisted Capture (Ingestion)
*Outcome: System assists humans, never replaces them. Low-friction entry.*

### Key Sub-deliverables
*   **D4.1 Draft State Flow:** OCR/Ingestion creates a "Draft" or "Suggestion" — NOT confirmed inventory.
*   **D4.2 User Confirmation Loop:** User must explicitly commit drafts to the ledger.
*   **D4.3 OCR Extraction:** Extract SKU, Qty, Date, but treat as low-confidence until confirmed.
*   **D4.4 Manual Add/Edit UI:** Fallback for all capture flows.

### Acceptance
*   **Zero auto-writes to ledger.**
*   OCR errors never silently mutate inventory.
*   User always confirms ingestion.

## D5. Android App (Truth Console)
*Outcome: An operational console for the household, not just a consumer app.*

### Key Sub-deliverables
*   **D5.1 Inventory Console:** Real-time view of the ledger.
*   **D5.2 Cooking Suggestions:** View of Decision Engine outputs.
*   **D5.3 Recipe Detail View:** Instructions linked to inventory context.
*   **D5.4 Offline-First Support:** Functional without internet (critical for reliability).
*   **D5.5 Add/Edit Flows:** Quick actions for manual correction.

### Acceptance
*   Non-tech family members can explain the app state.
*   App is usable without crashes for 7 consecutive days.
*   Offline correctness > animations.

## D6. Truth Demo Validation
*Outcome: Proof that the system survives reality. "Truth demo, not demo demo".*

### Key Sub-deliverables
*   **D6.1 Pilot Group:** Onboard 5–10 real households.
*   **D6.2 Session Logging:** Log household sessions as evidence of use.
*   **D6.3 Failure Documentation:** Document failures honestly, don't hide them.
*   **D6.4 Stabilization Release:** Fixes based on pilot feedback.

### Acceptance
*   Daily active usage ≥ 60%.
*   Users correct system < 20% of time after week 2.
*   At least one "this caught waste" incident verified per household.
