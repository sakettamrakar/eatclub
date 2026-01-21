# DWBS — Inventory-Aware Cooking App

(Quality-first, production-usable, anti-fantasy plan)

## Phase 1 — Solid v1 (8–10 weeks)

Objective: App works end-to-end for real households without automation crutches.

### D1. Inventory Ledger (Core System of Record)

Outcome: Single source of truth for household food state.

Sub-deliverables

D1.1 Item master (raw, cooked, packaged)

D1.2 Quantity + unit normalization (kg, pcs, ml)

D1.3 Expiry + purchase date tracking

D1.4 State transitions (bought → used → wasted)

D1.5 Manual override + correction history

Acceptance

Any inventory change is auditable

No negative quantities

Expiry logic deterministic

### D2. Recipe Knowledge Base (30–50 Recipes)

Outcome: Recipes usable by a decision engine, not just text.

Sub-deliverables

D2.1 Ingredient → quantity mappings

D2.2 Mandatory vs optional ingredients

D2.3 Category tagging (breakfast/lunch/dinner)

D2.4 Prep time + difficulty

D2.5 Cultural relevance (Indian households)

Acceptance

Recipe feasibility computable from inventory

No free-text dependency in logic layer

### D3. Decision Engine v1

Outcome: Deterministic recommendations, explainable.

Sub-deliverables

D3.1 Feasibility scoring

D3.2 Expiry-weighted prioritization

D3.3 Substitution logic (limited, rule-based)

D3.4 Explanation generator (“why this recipe”)

Acceptance

Same inputs → same outputs

Recommendation rationale visible to user

### D4. Manual + Invoice Ingestion

Outcome: Low-friction inventory entry.

Sub-deliverables

D4.1 Manual add/edit UI

D4.2 Invoice photo upload

D4.3 OCR extraction (SKU, qty, date)

D4.4 User confirmation loop

D4.5 Error correction flow

Acceptance

OCR errors never silently mutate inventory

User always confirms ingestion

### D5. Android App (MVP-Grade)

Outcome: Usable daily, not demo-ware.

Sub-deliverables

D5.1 Inventory screen

D5.2 Today’s cooking suggestions

D5.3 Recipe detail view

D5.4 Add/edit inventory flows

D5.5 Offline-first support

Acceptance

App usable without crashes for 7 consecutive days

Works for non-technical users

### D6. Real Household Validation

Outcome: Proof that it survives real kitchens.

Sub-deliverables

D6.1 5–10 household onboarding

D6.2 Usage telemetry (non-PII)

D6.3 Failure log + fixes

D6.4 v1 stabilization release

Acceptance

Daily active usage ≥ 60%

At least 1 week continuous use per household

## Phase 2 — Trust & Automation (3–4 months)

Objective: Reduce user effort, increase confidence.

### D7. Email & PDF Ingestion Automation

Outcome: Passive inventory capture.

Sub-deliverables

D7.1 Email connector (Gmail first)

D7.2 Invoice classification

D7.3 PDF parser

D7.4 Confidence scoring

D7.5 User approval UI

Acceptance

No auto-write without approval

Confidence score visible

### D8. Smart Depletion Engine

Outcome: Inventory reduces automatically when cooking happens.

Sub-deliverables

D8.1 Recipe-linked depletion

D8.2 Partial consumption logic

D8.3 Missed-meal reconciliation

D8.4 Undo + correction system

Acceptance

Users trust depletion (low correction rate)

Reversible within 24h

### D9. Voice Prompts & Nudges

Outcome: Hands-free awareness.

Sub-deliverables

D9.1 Daily spoken summary

D9.2 Expiry alerts

D9.3 Cooking suggestions

D9.4 Language support (EN + HI)

Acceptance

Voice never triggers destructive actions

Opt-in only

### D10. Family Sharing

Outcome: Multi-actor household realism.

Sub-deliverables

D10.1 Roles (viewer/editor)

D10.2 Conflict resolution

D10.3 Activity timeline

D10.4 Notification rules

Acceptance

Concurrent edits safe

Clear ownership visibility

## Phase 3 — Moat Deepening (6–12 months)

Objective: Make replication expensive, not just difficult.

### D11. Pattern Learning Engine

Outcome: App learns household behavior.

Sub-deliverables

D11.1 Consumption pattern models

D11.2 Seasonality detection

D11.3 Preference inference

D11.4 Confidence decay logic

Acceptance

Model suggestions outperform rule-based baseline

Explainability preserved

### D12. Health-Aware Suggestions

Outcome: Personal relevance beyond inventory.

Sub-deliverables

D12.1 Dietary preferences

D12.2 Macro tagging

D12.3 Restriction enforcement

D12.4 Long-term balance logic

Acceptance

No medical claims

User-controlled constraints

### D13. Expiry Optimization System

Outcome: Waste reduction becomes measurable.

Sub-deliverables

D13.1 Expiry risk scoring

D13.2 Cross-recipe salvage logic

D13.3 Waste analytics

D13.4 Household benchmarks

Acceptance

Measurable waste reduction over baseline

### D14. Household Analytics Dashboard

Outcome: Value visibility → retention.

Sub-deliverables

D14.1 Spend vs waste tracking

D14.2 Cooking frequency

D14.3 Savings estimation

D14.4 Exportable reports

Acceptance

Users can articulate value in ₹ terms
