# Pilot Household Protocol

## 1. Purpose of Pilot
To empirically validate the **Truth before Utility** hypothesis in real-world environments. The pilot is not designed to test "engagement" or "delight", but to measure the system's epistemic integrity (how often it lies) and the user's tolerance for rigid inventory discipline.

## 2. Household Selection Criteria
*   **Sample Size**: 3-5 Households initially.
*   **Composition**: Must include multi-actor homes (2+ adults) to test conflict/synchronization friction.
*   **Behavior**: High cooking frequency (>4 meals/week cooked at home).
*   **Tech Literacy**: Diverse. At least one "low-tech" primary cook.
*   **Exclusion**: No immediate family of the development team (to avoid "politeness bias").

## 3. Onboarding Rules
1.  **Zero-Touch Install**: Users must be able to install the APK (sideload) and initialize the database without physical assistance from the developer.
2.  **No "Golden Manual"**: Do not provide a perfectly pre-populated inventory. Users must enter their first 5 items manually to feel the "cost" of data entry.
3.  **No Incentives**: No payments, gift cards, or promises of future rewards. Participation must be driven solely by intrinsic utility.

## 4. What Households Are Told (Explicitly)
*   **"The System is Dumb"**: Explicitly lower expectations. "It does not know you bought milk unless you tell it."
*   **"Truth is Your Job"**: "If the app says you have eggs and you don't, that is your failure to update, not the app's failure to guess."
*   **"Report Lies"**: "Your most important job is to tell us when the app says something false."

## 5. What Is Observed (Silently)
*   **Trust Failure Rate**: Ratio of `CorrectionEvents` (admitting the system was wrong) to `ConsumeEvents` (system working as intended).
*   **Session Density**: Frequency of interaction. (Is it being used daily or batched weekly?)
*   **Feature Ignorance**: Which features (e.g., Suggestions) are ignored despite being functional.
*   **Trust Level Stability**: Does the household qualify for T2 upgrades, or do they remain stuck in T1?

## 6. Feedback Channels
*   **Primary**: A shared, low-friction messaging group (e.g., Signal/WhatsApp) for "in-the-moment" frustrations.
*   **Secondary**: Weekly "Truth Dump" interview (15 mins) to review valid/invalid states.
*   **Forbidden**: No "Feature Request" polls. We do not build what they ask for; we build what solves the friction they demonstrate.

## 7. Failure Reporting Protocol
If a user reports a "Lie" (System claimed availability of checking-out item):
1.  **Immediate Stop**: Do not explain away the bug.
2.  **FTM Entry**: Create a Failure Taxonomy Map entry (e.g., FTM-00XX).
3.  **Root Cause**: Classify as Software Bug, Hardware Failure, or *Epistemic Overreach* (Assumed too much).
4.  **Mitigation**: If Epistemic Overreach, *downgrade* the specific feature for that household.

## 8. Trust Protection Rules
*   **No Unearned Upgrades**: No household gets "Smart Depletion" or "Passive Ingest" until they survive 14 days of Manual Mode with < 5% correction rate.
*   **Reversibility**: Users must be shown how to "Nuclear Reset" their inventory if it becomes hopelessly desynchronized.
*   **Silence is not Consent**: If a user stops interacting, assume the data is **Rotting (False)**, not "Stable".

## 9. Exit Criteria
*   **Success**: Household maintains > 95% inventory accuracy for 30 consecutive days.
*   **Failure (Churn)**: User stops updating ledger for > 7 days.
*   **Safety Trigger**: System suggests using a recalled or dangerously expired item (Immediate Pilot Halt).
