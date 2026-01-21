# Phase-2 Execution Task Graph

## Phase-2 Execution Ledger Enforcement Protocol

**Ledger File Path**: `/docs/execution/phase2_execution_ledger.md`

**Mandatory Requirement**:
Updates to the Phase-2 Execution Ledger are a **HARD REQUIREMENT** for the completion of any task listed below. A task is considered **INCOMPLETE** and **INVALID** if it does not have a corresponding, verified entry in the ledger.

**Timing & Purpose**:
Ledger entries must be written **AFTER** the implementation and validation steps of each task. These entries serve as the primary evidence for:
1.  **Trust Upgrade Decisions**: Moving from T1 to T2/T3.
2.  **Trust Downgrade Triggers**: Responding to user rejections.
3.  **RADAR BLUE Reviews**: Systemic governance audits.

**Strict Liability**:
The implementor bears full liability for ensuring the "Trust Level Exercised" and "Automation Type" are recorded accurately. Omission of these fields constitutes a governance failure.

---

This document defines the granular execution path for DWBS Phase 2 (Trust & Automation).
Total Tasks: 28

## 1. Phase-2 Foundations

### TASK P2-T1: Implement Feature Flag System
DWBS Deliverable: D10.1 Roles (Foundational)
Category: Foundations
Execution Type: Sequential
Dependencies: None
Scope:
- Allowed: /src/core/config, /android/app/src/main/java/com/eatclub/app/core/config
- Forbidden: None
Task Definition:
Implement a configuration system to toggle Phase 2 features (Passive Ingest, Smart Depletion, Voice, Family). Default all to FALSE.
Constraints:
- IDS Reference: 1 (Append-only context)
- MTRI Trust Level: T0
- No silent activation
Acceptance Criteria:
- Flags stored persistently
- Features disabled by default
Validation Method:
- Unit tests for toggle logic
Failure Handling:
- Default to OFF if config is corrupt
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Configuration)
    - Human Confirmation Points (None)
    - State Mutation Summary (Feature Flags Created)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (Yes)
    - Net Trust Impact (Neutral)

### TASK P2-T2: Harden Ledger for Concurrency
DWBS Deliverable: D10.2 Conflict Resolution (Foundational)
Category: Foundations
Execution Type: Sequential
Dependencies: P2-T1
Scope:
- Allowed: /src/core/ledger, /android/app/src/main/java/com/eatclub/app/core/ledger
- Forbidden: None
Task Definition:
Add optimistic locking (versioning) to InventoryState and Ledger to support future multi-user edits.
Constraints:
- IDS Reference: 10 (Historical integrity)
- MTRI Trust Level: T0
- No data loss
Acceptance Criteria:
- Version field added to State
- Concurrent writes detect conflict
Validation Method:
- Concurrency simulation tests
Failure Handling:
- Reject second write with explicit error
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Concurrency Logic)
    - Human Confirmation Points (None)
    - State Mutation Summary (Schema Update)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (Yes)
    - Net Trust Impact (Neutral)

## 2. Passive Signals Layer

### TASK P2-T3: Implement Email Signal Connector
DWBS Deliverable: D7.1 Email connector
Category: Core
Execution Type: Sequential
Dependencies: P2-T1
Scope:
- Allowed: /src/core/ingestion/passive/email
- Forbidden: Sending emails
Task Definition:
Implement a connector to read specific Gmail labels (readonly). Parse basic metadata (Sender, Date, Subject).
Constraints:
- IDS Reference: 3 (Drafts requiring confirmation)
- MTRI Trust Level: T1 (Draft generation)
- Read-only access
Acceptance Criteria:
- Connects to mock/real endpoint
- Extracts metadata correctly
Validation Method:
- Mock connector tests
Failure Handling:
- Log connection failure, do not retry indefinitely
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Passive Read)
    - Human Confirmation Points (Connection Auth)
    - State Mutation Summary (None - Read Only)
    - User Acceptance/Rejection (Auth Token Grant)
    - Rollback Capability (Revoke Token)
    - Net Trust Impact (Increase - Connectivity)

### TASK P2-T4: Implement Invoice Classification Logic
DWBS Deliverable: D7.2 Invoice classification
Category: Core
Execution Type: Sequential
Dependencies: P2-T3
Scope:
- Allowed: /src/core/ingestion/passive/classification
- Forbidden: ML Models
Task Definition:
Implement rule-based keyword classifier to identify "Grocery Invoice" vs "Junk".
Constraints:
- IDS Reference: 5 (No ML)
- MTRI Trust Level: T0
- Deterministic rules
Acceptance Criteria:
- Known vendors classified correctly
- Unknowns marked as Unsure
Validation Method:
- Keyword test suite
Failure Handling:
- Mark as "Unknown" type
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Rule-based Classification)
    - Human Confirmation Points (None)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

### TASK P2-T5: Implement PDF/Text Parser
DWBS Deliverable: D7.3 PDF parser
Category: Core
Execution Type: Parallel
Dependencies: P2-T3
Scope:
- Allowed: /src/core/ingestion/passive/parser
- Forbidden: OCR APIs (Use text extraction only)
Task Definition:
Implement logic to extract line items from text-based PDF content. Map text lines to `DraftItem`.
Constraints:
- IDS Reference: 8 (No free text reliance - strict formatting expected)
- MTRI Trust Level: T1
- No guessing
Acceptance Criteria:
- Extracts SKU/Price/Qty from clean text
Validation Method:
- Parser unit tests with sample PDFs
Failure Handling:
- Return partial/empty list with error flag
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Parsing)
    - Human Confirmation Points (None)
    - State Mutation Summary (Draft Objects Created)
    - User Acceptance/Rejection (N/A - Internal)
    - Rollback Capability (Yes - Drafts ephemeral)
    - Net Trust Impact (Neutral)

### TASK P2-T6: Implement Signal Confidence Scoring
DWBS Deliverable: D7.4 Confidence scoring
Category: Core
Execution Type: Parallel
Dependencies: P2-T4, P2-T5
Scope:
- Allowed: /src/core/ingestion/passive/scoring
- Forbidden: ML
Task Definition:
Assign confidence (0.0-1.0) to Parsed Items. Known Vendor + Clear Format = 0.9. Unknown = 0.3.
Constraints:
- IDS Reference: 1 (Truth before utility)
- MTRI Trust Level: T0
- Heuristics only
Acceptance Criteria:
- Scores reflect source reliability
Validation Method:
- Scoring logic tests
Failure Handling:
- Default to 0.1 (Low)
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Heuristic Scoring)
    - Human Confirmation Points (None)
    - State Mutation Summary (Score Assignment)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

### TASK P2-T7: Implement Passive Approval UI
DWBS Deliverable: D7.5 User approval UI
Category: Core
Execution Type: Sequential
Dependencies: P2-T6
Scope:
- Allowed: /android/app/src/main/java/com/eatclub/app/ui/ingest/passive
- Forbidden: Auto-commit
Task Definition:
UI to list "Pending Invoices". User must tap "Import" -> specific items -> "Confirm".
Constraints:
- IDS Reference: 3 (Explicit confirmation)
- MTRI Trust Level: T2
- No silent import
Acceptance Criteria:
- Drafts visible
- Confirmation moves to Ledger
Validation Method:
- UI Walkthrough
Failure Handling:
- Show error if ledger commit fails
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T2)
    - Automation Type (Assistive Import)
    - Human Confirmation Points (Final "Commit" Tap)
    - State Mutation Summary (Ledger Append)
    - User Acceptance/Rejection (Explicit Acceptance)
    - Rollback Capability (Yes - Correction Event)
    - Net Trust Impact (Increase - If Successful)

### TASK P2-T8: Validate Passive Signal Flow
DWBS Deliverable: D7 Email & PDF Ingestion
Category: Validation
Execution Type: Sequential
Dependencies: P2-T7
Scope:
- Allowed: /tests/passive
- Forbidden: None
Task Definition:
End-to-end test: Mock Email -> Classify -> Parse -> Score -> UI Review -> Ledger.
Constraints:
- IDS Reference: 11 (No inference without action)
- MTRI Trust Level: T1
Acceptance Criteria:
- Flow completes without crashes
- Ledger unchanged until final click
Validation Method:
- Integration test
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Validation Suite)
    - Human Confirmation Points (Test Result Review)
    - State Mutation Summary (None/Mock)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

## 3. Smart Depletion

### TASK P2-T9: Implement Recipe Depletion Logic
DWBS Deliverable: D8.1 Recipe-linked depletion
Category: Core
Execution Type: Sequential
Dependencies: P2-T1
Scope:
- Allowed: /src/core/depletion
- Forbidden: None
Task Definition:
Function `depleteRecipe(Recipe)`: Calculates required ingredients and creates a drafted `ConsumeEvent` set.
Constraints:
- IDS Reference: 7 (Computable from state)
- MTRI Trust Level: T1
- No auto-commit
Acceptance Criteria:
- Correct quantities mapped
- Missing items handled gracefully
Validation Method:
- Logic unit tests
Failure Handling:
- Return failure result if state invalid
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Calculation)
    - Human Confirmation Points (None)
    - State Mutation Summary (Draft Event Created)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (Yes)
    - Net Trust Impact (Neutral)

### TASK P2-T10: Implement Partial Consumption Logic
DWBS Deliverable: D8.2 Partial consumption logic
Category: Core
Execution Type: Sequential
Dependencies: P2-T9
Scope:
- Allowed: /src/core/depletion
- Forbidden: None
Task Definition:
UI/Logic to adjust depletion (e.g., "Used half"). Updates quantity in `ConsumeEvent`.
Constraints:
- IDS Reference: 1 (Append-only, explicit)
- MTRI Trust Level: T2
Acceptance Criteria:
- Slider/Input adjusts final depletion
Validation Method:
- UI Logic test
Failure Handling:
- Reset to 100% on error
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T2)
    - Automation Type (Assistive Adjustment)
    - Human Confirmation Points (Value Selection)
    - State Mutation Summary (Event Payload Mod)
    - User Acceptance/Rejection (Explicit Set)
    - Rollback Capability (Yes)
    - Net Trust Impact (Increase - Control)

### TASK P2-T11: Implement Missed-Meal Reconciliation
DWBS Deliverable: D8.3 Missed-meal reconciliation
Category: Core
Execution Type: Parallel
Dependencies: P2-T9
Scope:
- Allowed: /src/core/depletion/reconcile
- Forbidden: Auto-waste
Task Definition:
Suggest "Did you make X?" if ingredients for planned meal weren't used.
Constraints:
- IDS Reference: 11 (No inference state change)
- MTRI Trust Level: T1 (Suggestion only)
Acceptance Criteria:
- Identifies undeleted planned meals
Validation Method:
- State analysis tests
Failure Handling:
- Do not suggest if unsure
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Suggestion)
    - Human Confirmation Points (Yes/No Response)
    - State Mutation Summary (None unless confirmed)
    - User Acceptance/Rejection (Response Recorded)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - If Useful)

### TASK P2-T12: Implement Depletion Undo System
DWBS Deliverable: D8.4 Undo + correction system
Category: Core
Execution Type: Parallel
Dependencies: P2-T9
Scope:
- Allowed: /src/core/ledger/correction
- Forbidden: Deleting events
Task Definition:
"Undo" button creates `CorrectionAddEvent` to reverse `ConsumeEvent`.
Constraints:
- IDS Reference: 10 (Append-only history)
- MTRI Trust Level: T2
- Reversal, not deletion
Acceptance Criteria:
- Ledger sum returns to previous
- History shows both actions
Validation Method:
- Ledger Replay test
Failure Handling:
- Block undo if stock since modified
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T2)
    - Automation Type (Correction)
    - Human Confirmation Points (Undo Tab)
    - State Mutation Summary (Correction Event)
    - User Acceptance/Rejection (Explicit)
    - Rollback Capability (Redo?)
    - Net Trust Impact (Increase - Safety)

### TASK P2-T13: Validate Depletion Accuracy
DWBS Deliverable: D8 Smart Depletion Engine
Category: Validation
Execution Type: Sequential
Dependencies: P2-T12
Scope:
- Allowed: /tests/depletion
- Forbidden: None
Task Definition:
Verify calculated depletion matches Recipe math exactly. Verify Undo restores exact balance.
Constraints:
- IDS Reference: 4 (Deterministic)
- MTRI Trust Level: T0
Acceptance Criteria:
- Zero variance in math
Validation Method:
- Automated math suite
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Validation)
    - Human Confirmation Points (Test Review)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

## 4. Voice Interface (Read-Only)

### TASK P2-T14: Implement Daily Summary Generator
DWBS Deliverable: D9.1 Daily spoken summary
Category: Core
Execution Type: Sequential
Dependencies: P2-T1
Scope:
- Allowed: /src/core/voice/generation
- Forbidden: Cloud TTS (Use System TTS)
Task Definition:
Generate text script: "You have X items expiring..."
Constraints:
- IDS Reference: 5 (No LLM generation for text)
- MTRI Trust Level: T0
- Read-only
Acceptance Criteria:
- Script is factually correct
Validation Method:
- String matching test
Failure Handling:
- Fallback to generic greeting
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Content Gen)
    - Human Confirmation Points (Listening)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Listen/Skip)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

### TASK P2-T15: Implement Expiry Alert Generator
DWBS Deliverable: D9.2 Expiry alerts
Category: Core
Execution Type: Sequential
Dependencies: P2-T14
Scope:
- Allowed: /src/core/voice/generation
- Forbidden: None
Task Definition:
Generate text for urgent expiry: "Use your [Item] by [Date]."
Constraints:
- IDS Reference: 6 (Explanation required)
- MTRI Trust Level: T0
Acceptance Criteria:
- Only alerts on actual expiring items
Validation Method:
- Logic test
Failure Handling:
- Silence if no expiry
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Alert Gen)
    - Human Confirmation Points (None)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Ack/Ignore)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase)

### TASK P2-T16: Implement Spoken Suggestion Formatter
DWBS Deliverable: D9.3 Cooking suggestions
Category: Core
Execution Type: Parallel
Dependencies: P2-T14
Scope:
- Allowed: /src/core/voice/generation
- Forbidden: None
Task Definition:
Format top 3 recipes for speech. "You could cook A, B, or C."
Constraints:
- IDS Reference: 7 (Feasible)
- MTRI Trust Level: T0
Acceptance Criteria:
- Matches visual suggestions
Validation Method:
- Comparison test
Failure Handling:
- "No suggestions" message
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Suggestion Gen)
    - Human Confirmation Points (Selection)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Cook/Ignore)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

### TASK P2-T17: Implement Language Resource Bundle
DWBS Deliverable: D9.4 Language support (EN + HI)
Category: Supporting
Execution Type: Parallel
Dependencies: P2-T14
Scope:
- Allowed: /src/core/i18n
- Forbidden: Machine Translation
Task Definition:
Create hardcoded string maps for English and Hindi voice outputs.
Constraints:
- IDS Reference: 4 (Deterministic)
- MTRI Trust Level: T0
Acceptance Criteria:
- Correct translations for keys
Validation Method:
- Review
Failure Handling:
- Fallback to English
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Translation)
    - Human Confirmation Points (None)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

### TASK P2-T18: Validate Voice Output Safety
DWBS Deliverable: D9 Voice Prompts
Category: Validation
Execution Type: Sequential
Dependencies: P2-T17
Scope:
- Allowed: /tests/voice
- Forbidden: None
Task Definition:
Verify voice logic ONLY reads state and NEVER mutates it.
Constraints:
- IDS Reference: 6 (Least Privilege)
- MTRI Trust Level: T0
Acceptance Criteria:
- Ledger hash identical before/after
Validation Method:
- State integrity test
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Safety Check)
    - Human Confirmation Points (Test Review)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

## 5. Household / Multi-Actor Model

### TASK P2-T19: Implement Role Logic & Schema
DWBS Deliverable: D10.1 Roles (viewer/editor)
Category: Core
Execution Type: Sequential
Dependencies: P2-T2
Scope:
- Allowed: /src/core/auth
- Forbidden: Cloud Auth (Local simulation)
Task Definition:
Define `UserRole` enum (Viewer, Editor, Admin). Check permission before mutation.
Constraints:
- IDS Reference: 12 (Access Control)
- MTRI Trust Level: T0
Acceptance Criteria:
- Viewers cannot mutate
Validation Method:
- Permission tests
Failure Handling:
- Throw UnauthorizedException
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Auth Logic)
    - Human Confirmation Points (None)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (Yes)
    - Net Trust Impact (Neutral)

### TASK P2-T20: Implement Conflict Resolution Strategy
DWBS Deliverable: D10.2 Conflict Resolution
Category: Core
Execution Type: Sequential
Dependencies: P2-T19
Scope:
- Allowed: /src/core/ledger/sync
- Forbidden: Data loss
Task Definition:
If `version` mismatch, prompt user to "Keep Mine" or "Accept Theirs".
Constraints:
- IDS Reference: 1 (Truth integrity)
- MTRI Trust Level: T2
Acceptance Criteria:
- Mismatches trigger resolution flow
Validation Method:
- Conflict scenario test
Failure Handling:
- Default to "Keep Last" (Safe fallback)
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T2)
    - Automation Type (Conflict Resolution)
    - Human Confirmation Points (Resolution Selection)
    - State Mutation Summary (Ledger Reorg)
    - User Acceptance/Rejection (Explicit Choice)
    - Rollback Capability (Yes)
    - Net Trust Impact (Increase - Integrity)

### TASK P2-T21: Implement Activity Timeline Logger
DWBS Deliverable: D10.3 Activity timeline
Category: Supporting
Execution Type: Parallel
Dependencies: P2-T19
Scope:
- Allowed: /src/core/logging/timeline
- Forbidden: PII
Task Definition:
Aggregated view of `LedgerEvents` showing "Who did what".
Constraints:
- IDS Reference: 10 (Auditable)
- MTRI Trust Level: T0
Acceptance Criteria:
- Shows Actor Name
Validation Method:
- UI check
Failure Handling:
- Hide actor if unknown
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Logging)
    - Human Confirmation Points (None)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Transparencey)

### TASK P2-T22: Implement Notification Logic
DWBS Deliverable: D10.4 Notification rules
Category: Supporting
Execution Type: Parallel
Dependencies: P2-T19
Scope:
- Allowed: /src/core/notifications
- Forbidden: Push APNS/FCM (Local only)
Task Definition:
Generate in-app alert when another user updates inventory.
Constraints:
- IDS Reference: 1 (Awareness)
- MTRI Trust Level: T1
Acceptance Criteria:
- Alert generated on external change
Validation Method:
- Event listener test
Failure Handling:
- Silent failure acceptable
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T1)
    - Automation Type (Notification)
    - Human Confirmation Points (Alert Ack)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Clear/Interact)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Awareness)

### TASK P2-T23: Validate Multi-User Concurrency
DWBS Deliverable: D10 Family Sharing
Category: Validation
Execution Type: Sequential
Dependencies: P2-T20
Scope:
- Allowed: /tests/multiuser
- Forbidden: None
Task Definition:
Simulate 2 users editing same item. Verify locking and resolution.
Constraints:
- IDS Reference: 4 (Deterministic)
- MTRI Trust Level: T0
Acceptance Criteria:
- System remains consistent
Validation Method:
- Simulation suite
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Validation)
    - Human Confirmation Points (Review)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Neutral)

## 6. Trust Hardening

### TASK P2-T24: Implement Audit Logging for Passive Ingest
DWBS Deliverable: D7 Email & PDF Ingestion (Hardening)
Category: Supporting
Execution Type: Sequential
Dependencies: P2-T8
Scope:
- Allowed: /src/core/logging/audit
- Forbidden: None
Task Definition:
Log every "Draft Created" and "Draft Rejected" event with source evidence (e.g. email ID).
Constraints:
- IDS Reference: 1 (Auditability)
- MTRI Trust Level: T0
Acceptance Criteria:
- Logs traceable to source
Validation Method:
- Log inspection
Failure Handling:
- Continue even if log fails
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Audit Log)
    - Human Confirmation Points (None)
    - State Mutation Summary (Access Logs)
    - User Acceptance/Rejection (N/A)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Auditability)

### TASK P2-T25: Implement Role Enforcement Tests
DWBS Deliverable: D10 Family Sharing (Hardening)
Category: Validation
Execution Type: Parallel
Dependencies: P2-T19
Scope:
- Allowed: /tests/security
- Forbidden: None
Task Definition:
Strict tests to ensure `VIEWER` role can NEVER call `applyMutation`.
Constraints:
- IDS Reference: 6 (Least Privilege)
- MTRI Trust Level: T0
Acceptance Criteria:
- 100% rejection of unauthorized acts
Validation Method:
- Security unit tests
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Security Check)
    - Human Confirmation Points (Review)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Hardening)

### TASK P2-T26: Implement Depletion Reversibility Tests
DWBS Deliverable: D8 Smart Depletion Engine (Hardening)
Category: Validation
Execution Type: Parallel
Dependencies: P2-T12
Scope:
- Allowed: /tests/reliability
- Forbidden: None
Task Definition:
Fuzz testing of Undo/Redo to ensure inventory count never drifts.
Constraints:
- IDS Reference: 1 (Integrity)
- MTRI Trust Level: T0
Acceptance Criteria:
- Drift = 0
Validation Method:
- Fuzz test
Failure Handling:
- Fail test
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Reliability Check)
    - Human Confirmation Points (Review)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Pass/Fail)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Hardening)

## 7. Phase-2 Validation

### TASK P2-T27: Phase-2 Full Regression Suite
DWBS Deliverable: D6 Phase-1 Validation (Regression)
Category: Validation
Execution Type: Sequential
Dependencies: All Previous
Scope:
- Allowed: /tests
- Forbidden: None
Task Definition:
Run all Phase 1 + Phase 2 tests. Ensure no regression in Phase 1 features.
Constraints:
- IDS Reference: 10 (No degradation)
- MTRI Trust Level: T0
Acceptance Criteria:
- All Green
Validation Method:
- CI Run
Failure Handling:
- Block release
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T0)
    - Automation Type (Full Regression)
    - Human Confirmation Points (Sign-off)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Go/No-Go)
    - Rollback Capability (N/A)
    - Net Trust Impact (Increase - Confidence)

### TASK P2-T28: Pilot Group Phase-2 Checkoff
DWBS Deliverable: D6.1 Pilot Group (Extension)
Category: Validation
Execution Type: Sequential
Dependencies: P2-T27
Scope:
- Allowed: /docs/pilot
- Forbidden: None
Task Definition:
Manual confirmation from 3 pilot users: "Passive ingest works", "Voice is accurate".
Constraints:
- IDS Reference: 1 (Human Grounding)
- MTRI Trust Level: T2
Acceptance Criteria:
- Signed off
Validation Method:
- Interview
Failure Handling:
- Rollback feature
#### Ledger Update Requirement
- **Task completion is invalid without a ledger entry.**
- **File**: `/docs/execution/phase2_execution_ledger.md`
- **Must Record**:
    - Trust Level Exercised (T2)
    - Automation Type (Human Validation)
    - Human Confirmation Points (Interview)
    - State Mutation Summary (None)
    - User Acceptance/Rejection (Sign-off/Veto)
    - Rollback Capability (Feature Flag Off)
    - Net Trust Impact (Increase/Decrease)
