# DWBS Phase 2 — Trust & Automation

**Objective:** Automation only where trust already exists. Reduce user effort and increase confidence.
*Timeline: 3–4 months*

## D7. Passive Signals Layer
*Outcome: Signals ≠ Truth. Passive inventory capture.*

### Key Sub-deliverables
*   **D7.1 Signal Collectors:** Email connector (Gmail), PDF parser, Invoice classification.
*   **D7.2 Confidence Ladder:** Visual indicator of data source reliability (e.g., Email < OCR < Manual).
*   **D7.3 Suggestion Flow:** Signals create "Suggestions" in the app, never direct inventory entries.
*   **D7.4 User Approval UI:** Tinder-like or list-based fast approval for suggestions.

### Acceptance
*   **No auto-write without approval.**
*   Confidence score is visible to the user.

## D8. Consumption Inference Engine
*Outcome: System learns when food disappears, but verifies intent.*

### Key Sub-deliverables
*   **D8.1 Cooking Intent Verification:** "Start Cooking" != "Consumed" until confirmed.
*   **D8.2 Missed-Meal Detection:** Identify when planned meals weren't cooked (treat as uncertainty, not failure).
*   **D8.3 Partial Consumption Logic:** Handle "used half an onion" scenarios.
*   **D8.4 Undo & Correction:** "I didn't actually cook that" flow (reversible within 24h).

### Acceptance
*   Users trust depletion suggestions (low correction rate).
*   System handles missed meals gracefully without corrupting inventory counts.

## D9. Voice as Read-Only Interface
*Outcome: Hands-free awareness without risk of hallucinated mutations.*

### Key Sub-deliverables
*   **D9.1 Informational Voice:** "What's in the fridge?", "What expires soon?".
*   **D9.2 Daily Spoken Summary:** Audio briefing of kitchen state.
*   **D9.3 Language Support:** English + Hindi (Indian household context).
*   **D9.4 No-Mutation Rule:** Voice commands *cannot* add/remove items (prevents assistant hallucinations).

### Acceptance
*   Voice never triggers destructive actions.
*   Opt-in only.

## D10. Multi-Actor Household Model
*Outcome: Real families, not single-user apps.*

### Key Sub-deliverables
*   **D10.1 Actor Intent Tracking:** Log *who* performed an action (Viewer/Editor roles).
*   **D10.2 Conflict Surfacing:** If two users edit the same item, surface the conflict instead of auto-resolving.
*   **D10.3 Activity Timeline:** Shared view of household activity.

### Acceptance
*   Concurrent edits are safe.
*   Clear ownership visibility for every action.
