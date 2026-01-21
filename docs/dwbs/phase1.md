# DWBS — Inventory-Aware Cooking System

(Aligned with anti-Blinkit + truth-demo philosophy)

## Phase 1 — Solid v1 (8–10 weeks)

Objective: Establish an irreversible household food truth layer.
If Phase 1 is weak, everything else is theatre.

### D0. System Contracts (NEW – Mandatory)

This was missing earlier and is non-negotiable given your other chats.

Outcome: Every future feature obeys fixed contracts.

Deliverables

D0.1 Inventory State Contract (what is “true”)

D0.2 Mutation Rules (who/what can change inventory)

D0.3 Explainability Contract (every suggestion must explain)

D0.4 Failure Rules (what happens when data is missing)

Acceptance

Any future automation must comply

No silent state mutation allowed

👉 This is the moat seed. Blinkit won’t do this.

### D1. Inventory Ledger (Upgraded)

Outcome: Time-aware, human-correctable household ledger.

Changes vs earlier

Added event-sourcing lite (append-only log)

Added confidence score per item (manual > OCR > inference)

Key Sub-deliverables

Item identity resolution (tomato ≠ tomato puree)

Quantity uncertainty handling

Waste as first-class event (not deletion)

Acceptance

Inventory can be reconstructed for any past date

Users can see why system believes something exists

### D2. Recipe Knowledge Graph (Renamed & Strengthened)

Not a “recipe list”.

Outcome: Structured cooking graph usable for reasoning.

Upgrades

Ingredient substitutability graph (manual rules only)

Loss factor (raw → cooked shrinkage)

Indian household bias explicitly encoded

Acceptance

Recipe feasibility is computable

Graph usable without UI

### D3. Decision Engine v1 (Truth-Preserving)

Outcome: Deterministic, auditable decisions.

Explicit Non-Goals (important)

❌ No ML

❌ No personalization

❌ No “smart” guesses

Upgrades

Confidence-aware scoring

“Ask user” branch when uncertainty > threshold

Acceptance

System prefers asking over hallucinating

Same household → same outputs every time

### D4. Ingestion (Reframed as Assisted Capture)

Language aligned with your “no blind automation” stance.

Outcome: System assists humans, never replaces them (yet).

Upgrades

Ingestion does NOT create inventory by default

Draft state → user confirmation → commit

Acceptance

Zero auto-writes to ledger

OCR errors cannot corrupt truth

### D5. Android App (Truth Console, not Consumer App)

Outcome: App = window into household state.

Reframing

Not “UX polish”

It’s an operational console

Acceptance

Non-tech family member can explain app state

Offline correctness > animations

### D6. Truth Demo Validation (Renamed from Real Household Validation)

This aligns with your “truth demo, not demo demo” language.

Outcome: Proof the system survives reality.

Upgrades

Household sessions are logged as evidence

Failures documented, not hidden

Acceptance

Users correct system < 20% of time after week 2

At least one “this caught waste” incident per household
