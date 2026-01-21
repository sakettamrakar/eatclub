# Phase-1 Execution Task Graph

This document defines the granular execution path for DWBS Phase 1.
Total Tasks: 42

## Phase-1 Execution Ledger Protocol

### Purpose
To maintain a chronological, immutable record of execution events for Phase-1, ensuring auditability and creating a source of truth independent of AI memory.

### File Path
`/docs/execution/phase1_execution_ledger.md`

### Protocol Rules
1.  **Mandatory Updates**: The ledger MUST be updated immediately after the successful completion of a task. No task is complete without this step.
2.  **Entry Structure**: Each entry must contain:
    *   **Task ID**: The specific identifier from this graph.
    *   **Date**: ISO 8601 Timestamp.
    *   **Summary**: A factual summary of implemented changes.
    *   **Files**: List of files created or modified.
    *   **Constraints**: Confirmation that invariants were respected.
    *   **Deviations**: Any authorized deviation from the original graph (or "None").
    *   **Outcome**: Result of the validation step.
3.  **Prohibitions**: No opinions, future plans, or speculative text. No code snippets unless necessary for clarity.
4.  **Responsibility**: The entity (AI or Human) completing the task is responsible for writing the entry.

---

## 1. Phase-1 Core Foundations

### TASK 1.1: Project Setup & Repo Structure
DWBS Deliverable: D0. System Contracts
Category: Core
Execution Type: Sequential
Dependencies: None
Scope:
- Allowed: /src, /tests, /docs/architecture
- Forbidden: None
Task Definition:
Establish the standard repository structure for the android app and core logic library. Initialize build systems (Gradle/Bazel) and strictly separate "core logic" (pure Kotlin/Java) from "android view" code.
Constraints:
- Trust Level: T0
- No side effects allowed
Acceptance Criteria:
- Repo structure mirrors architectural layers
- Build passes for empty modules
- Core module has zero Android dependencies
Validation Method:
- Static inspection of build.gradle files
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.1), Timestamp, Implemented Structure Summary, and Validation Results.

### TASK 1.2: Define Inventory State Contracts
DWBS Deliverable: D0.1 Inventory State Contract
Category: Core
Execution Type: Sequential
Dependencies: 1.1
Scope:
- Allowed: /docs/contracts, /src/core/contracts
- Forbidden: Implementation files
Task Definition:
Define the interface and data classes for `InventoryItem`, `Quantity`, and `InventoryState`. Strictly define what "In Stock" means (Quantity > 0 AND NOT expired OR expired within tolerance).
Constraints:
- Trust Level: T0
- Must be pure interface/data definition
Acceptance Criteria:
- Interface prevents negative quantities by type design if possible
- "In Stock" predicate is explicitly defined
Validation Method:
- Code review of contract definitions
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.2), Timestamp, Defined Interfaces, and Confirmation of Invariant Checks.

### TASK 1.3: Define Mutation Rules Contracts
DWBS Deliverable: D0.2 Mutation Rules
Category: Core
Execution Type: Parallel
Dependencies: 1.2
Scope:
- Allowed: /src/core/contracts
- Forbidden: /src/core/impl
Task Definition:
Define the `InventoryMutation` sealed class hierarchy (e.g., `Bought`, `Consumed`, `Wasted`, `Corrected`). Define the `MutationVerifier` interface that rejects invalid transitions.
Constraints:
- Trust Level: T0
- No silent mutation allowed
Acceptance Criteria:
- All allowed mutations are enumerated
- Illegal states are unrepresentable or throw explicit errors
Validation Method:
- Unit tests defining valid/invalid mutation sequences
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.3), Timestamp, Mutation Classes Defined, and Verification Logic Summary.

### TASK 1.4: Define Explainability Contracts
DWBS Deliverable: D0.3 Explainability Contract
Category: Core
Execution Type: Parallel
Dependencies: 1.2
Scope:
- Allowed: /src/core/contracts
- Forbidden: None
Task Definition:
Define the `Explanation` data structure requiring `reason`, `source_fact`, and `confidence`. Every suggestion output must wrap or include this structure.
Constraints:
- Trust Level: T0
- "Why" must be machine-readable
Acceptance Criteria:
- Suggestion interface requires Explanation field
- Explanation cannot be null or empty string
Validation Method:
- Static analysis of API inspection
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.4), Timestamp, Explanation Structure Details, and Compliance Check.

### TASK 1.5: Define Failure Handling Contracts
DWBS Deliverable: D0.4 Failure Rules
Category: Core
Execution Type: Parallel
Dependencies: 1.2
Scope:
- Allowed: /src/core/contracts
- Forbidden: None
Task Definition:
Define `Result<T>` or `Outcome<T>` wrappers for all core operations. Define standard error codes for "Missing Data", "Low Confidence", and "Ambiguous Input".
Constraints:
- Trust Level: T0
- Fail-safe defaults defined
Acceptance Criteria:
- No bare exceptions in public APIs
- Failure modes explicitly enumerated
Validation Method:
- API Signature review
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.5), Timestamp, Defined Result Types, and Error Code Enumeration.

### TASK 1.6: Validate Contracts Enforcement
DWBS Deliverable: D0 System Contracts
Category: Validation
Execution Type: Sequential
Dependencies: 1.2, 1.3, 1.4, 1.5
Scope:
- Allowed: /tests/contracts
- Forbidden: None
Task Definition:
Write a suite of "Contract Tests" that implementers must pass. These tests verify that any implementation of the contracts adheres to the invariants (e.g., negative quantity formatting).
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Test suite fails for mock implementations breaking rules
Validation Method:
- Run tests against a dummy breaking implementation
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (1.6), Timestamp, Test Suite Coverage Summary, and Validation Outcome.

## 2. Inventory Ledger Tasks

### TASK 2.1: Implement Core Event Schema
DWBS Deliverable: D1.1 Event-Sourcing Lite
Category: Core
Execution Type: Sequential
Dependencies: 1.3
Scope:
- Allowed: /src/core/ledger/events
- Forbidden: Database code
Task Definition:
Implement the `LedgerEvent` sealed classes with JSON serialization support. Fields: `eventId`, `timestamp`, `actor`, `mutationType`, `payload`.
Constraints:
- Trust Level: T0
- Events must be immutable
Acceptance Criteria:
- Events serialize/deserialize 1:1
- All D0.2 mutations covered
Validation Method:
- Serialization unit tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.1), Timestamp, Event Schema Implementation, and Serialization Test Results.

### TASK 2.2: Implement In-Memory Ledger Store
DWBS Deliverable: D1.1 Event-Sourcing Lite
Category: Core
Execution Type: Sequential
Dependencies: 2.1
Scope:
- Allowed: /src/core/ledger/store
- Forbidden: Persistence (SQLite for later)
Task Definition:
Implement `LedgerStore` interface. `append(event)`, `getStream()`, `snapshot()`. Should strictly enforce append-only logic.
Constraints:
- Trust Level: T0
- No deletion API allowed
Acceptance Criteria:
- Appending works
- Modification of past events throws error
Validation Method:
- Unit tests verifying immutability
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.2), Timestamp, Ledger Store Implementation, and Immutability Verification.

### TASK 2.3: Implement Item Identity Resolution
DWBS Deliverable: D1.2 Item Identity Resolution
Category: Core
Execution Type: Parallel
Dependencies: 2.1
Scope:
- Allowed: /src/core/identity
- Forbidden: Fuzzy matching libraries
Task Definition:
Implement `ItemIdentity` logic. Distinguish `Tomato (Fresh)` vs `Tomato (Canned)`. Use strict ID equivalence for now, no fuzzy logic yet.
Constraints:
- Trust Level: T0
- Deterministic resolution only
Acceptance Criteria:
- Distinct IDs for distinct forms
- Map implementation for ID lookups
Validation Method:
- Test cases with collision scenarios
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.3), Timestamp, Identity Logic Implementation, and Resolution Test Outcomes.

### TASK 2.4: Implement Unit Normalization Logic
DWBS Deliverable: D1.3 Quantity & Unit Normalization
Category: Core
Execution Type: Parallel
Dependencies: 1.2
Scope:
- Allowed: /src/core/units
- Forbidden: None
Task Definition:
Implement `UnitConverter`. Normalize inputs (e.g., 500g -> 0.5kg). Handle `approx` flag.
Constraints:
- Trust Level: T0
- No floating point errors (use decimal/rational)
Acceptance Criteria:
- Convertible units convert correctly
- Incompatible units return Failure
Validation Method:
- Parameterized unit tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.4), Timestamp, Unit Converter Implementation, and Normalization Test Results.

### TASK 2.5: Implement Confidence Score Logic
DWBS Deliverable: D1.4 Confidence Scores
Category: Core
Execution Type: Parallel
Dependencies: 2.1
Scope:
- Allowed: /src/core/scoring
- Forbidden: ML models
Task Definition:
Implement `Confidence` value class (0.0-1.0). Rules: Manual Entry = 1.0, Verified OCR = 0.9, Unverified OCR = 0.4.
Constraints:
- Trust Level: T0
- Hardcoded heuristics only
Acceptance Criteria:
- Event source dictates confidence score
Validation Method:
- Static logic check
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.5), Timestamp, Confidence Scoring Logic, and heuristic sources.

### TASK 2.6: Implement Expiry Calculation Logic
DWBS Deliverable: D1.5 Expiry & Purchase Tracking
Category: Core
Execution Type: Sequential
Dependencies: 2.1
Scope:
- Allowed: /src/core/expiry
- Forbidden: External API calls
Task Definition:
Implement `ExpiryCalculator`. Function: `predictExpiry(itemType, purchaseDate)`. Uses a static lookup table for common items.
Constraints:
- Trust Level: T0
- Deterministic lookup
Acceptance Criteria:
- Returns conservative estimate
- Defaults to safe minimal duration if unknown
Validation Method:
- Table coverage tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.6), Timestamp, Expiry Logic Implementation, and Table Coverage Verification.

### TASK 2.7: Implement Waste Tracking Events
DWBS Deliverable: D1.6 Waste as First-Class Event
Category: Core
Execution Type: Sequential
Dependencies: 2.1
Scope:
- Allowed: /src/core/ledger/waste
- Forbidden: None
Task Definition:
Implement specific `WasteEvent` payload containing `reason` (Expired, Spilled, Bad Taste). Ensure this subtracts from stock but adds to Waste Stats.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Waste event reduces inventory count
- Waste reason is mandatory
Validation Method:
- State projection tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.7), Timestamp, Waste Event Implementation, and State Projection Test Results.

### TASK 2.8: Validate Ledger Reconstruction
DWBS Deliverable: D1 Inventory Ledger
Category: Validation
Execution Type: Sequential
Dependencies: 2.2, 2.7
Scope:
- Allowed: /tests/ledger
- Forbidden: None
Task Definition:
Create an integration test that replays a sequence of 100 random events (Buy, Cook, Waste) and asserts the final state matches the expected arithmetic sum.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Replay is 100% accurate
- Performance < 100ms for 100 events
Validation Method:
- Automated replay test suite
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (2.8), Timestamp, Replay Test Summary, and Performance Metrics.

## 3. Recipe Knowledge Tasks

### TASK 3.1: Define Ingredient Entity Schema
DWBS Deliverable: D2.1 Structured Ingredient Mappings
Category: Core
Execution Type: Sequential
Dependencies: None
Scope:
- Allowed: /src/core/recipe/domain
- Forbidden: None
Task Definition:
Define `IngredientRef` and `Recipe` data classes. `IngredientRef` links to `ItemIdentity`.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Structure supports list of ingredients
- Recursive composition allowed (Recipe in Recipe)
Validation Method:
- Schema review
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.1), Timestamp, Ingredient Schema Definition, and Structure Review Confirmation.

### TASK 3.2: Implement Ingredient Substitution Graph
DWBS Deliverable: D2.1 Structured Ingredient Mappings
Category: Supporting
Execution Type: Sequential
Dependencies: 3.1
Scope:
- Allowed: /src/core/recipe/graph
- Forbidden: None
Task Definition:
Implement a directed graph where `Edge(A, B)` means "A can replace B". Include `penalty` weight on edge.
Constraints:
- Trust Level: T0
- Hardcoded graph for Phase 1
Acceptance Criteria:
- Graph traversal finds substitutes
- Cycles detection
Validation Method:
- Graph topology tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.2), Timestamp, Substitution Graph Implementation, and Topology Test Outcomes.

### TASK 3.3: Implement Shrinkage/Loss Logic
DWBS Deliverable: D2.2 Loss Factors
Category: Supporting
Execution Type: Parallel
Dependencies: 3.1
Scope:
- Allowed: /src/core/recipe/math
- Forbidden: complex physics simulations
Task Definition:
Implement `YieldCalculator`. `raw_qty * loss_factor = cooked_qty`. Map standard factors (e.g., Spinach = 0.6).
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Returns accurate cooked weight
Validation Method:
- Unit tests with table data
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.3), Timestamp, Yield Calculator Implementation, and Accuracy Verification.

### TASK 3.4: Implement Cultural Context Tagging
DWBS Deliverable: D2.3 Cultural & Context Tags
Category: Supporting
Execution Type: Parallel
Dependencies: 3.1
Scope:
- Allowed: /src/core/recipe/tags
- Forbidden: None
Task Definition:
Implement `RecipeTag` enum (Indian, Breakfast, Tadka-Required). Logic to filter recipes by these tags.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Filtering logic works
Validation Method:
- Unit tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.4), Timestamp, Tagging Logic Implementation, and Filter Test Results.

### TASK 3.5: Implement Operational Metadata Schema
DWBS Deliverable: D2.4 Operational Metadata
Category: Supporting
Execution Type: Parallel
Dependencies: 3.1
Scope:
- Allowed: /src/core/recipe/domain
- Forbidden: None
Task Definition:
Add `prepTime`, `cookTime`, `difficulty` (Enum) to `Recipe` class.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Fields present and nullable
Validation Method:
- JSON Serialization Check
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.5), Timestamp, Metadata Schema Extensions, and Serialization Checks.

### TASK 3.6: Validate Recipe Feasibility Calculation
DWBS Deliverable: D2 Recipe Knowledge Graph
Category: Validation
Execution Type: Sequential
Dependencies: 2.2, 3.1, 3.2
Scope:
- Allowed: /tests/recipe
- Forbidden: None
Task Definition:
Write logic to check `canCook(Recipe, InventoryState)`. Returns `True` if all ingredients are present (including via substitutions).
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Returns True when exact items exist
- Returns True when valid substitutes exist
- Returns False when missing essential item
Validation Method:
- Scenarios test suite
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (3.6), Timestamp, Feasibility Logic Validation, and Test Scenario Results.

## 4. Decision Engine Tasks

### TASK 4.1: Implement Base Feasibility Scorer
DWBS Deliverable: D3.1 Feasibility Scoring
Category: Core
Execution Type: Sequential
Dependencies: 3.6
Scope:
- Allowed: /src/core/decision/scoring
- Forbidden: ML
Task Definition:
Implement `RecipeScorer`. Base score 1.0 if feasible, 0.0 if not.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Binary feasibility reflected in score
Validation Method:
- Unit tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.1), Timestamp, Scorer Implementation, and Feasibility Test Outcomes.

### TASK 4.2: Implement Confidence-Weighted Scoring
DWBS Deliverable: D3.2 Confidence-Aware Scoring
Category: Core
Execution Type: Sequential
Dependencies: 4.1, 2.5
Scope:
- Allowed: /src/core/decision/scoring
- Forbidden: None
Task Definition:
Refine `RecipeScorer`. Multiply score by lowest ingredient confidence.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Low confidence inventory -> Lower recipe score
Validation Method:
- Scoring simulation
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.2), Timestamp, Weighted Scoring Logic, and Simulation Results.

### TASK 4.3: Implement Expiry Prioritization Logic
DWBS Deliverable: D3.3 Expiry Prioritization
Category: Core
Execution Type: Sequential
Dependencies: 4.1, 2.6
Scope:
- Allowed: /src/core/decision/scoring
- Forbidden: None
Task Definition:
Add boost to score if `Ingredient.expiry` < `Today + 2 days`.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Expiring items push recipes to top
Validation Method:
- Sorting validation tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.3), Timestamp, Expiry Boost Logic, and Sort Validation.

### TASK 4.4: Implement Uncertainty Thresholding
DWBS Deliverable: D3.4 "Ask User" Branch
Category: Core
Execution Type: Sequential
Dependencies: 4.2
Scope:
- Allowed: /src/core/decision/logic
- Forbidden: None
Task Definition:
Implement `ActionRecommender`. If top recipe score < 0.6 due to confidence, return `AskUserAction` instead of `SuggestRecipeAction`.
Constraints:
- Trust Level: T1 (Generates question proposal)
Acceptance Criteria:
- System halts and suggests asking user when data is unsure
Validation Method:
- Threshold boundary tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.4), Timestamp, Uncertainty Logic, and Threshold Test Results.

### TASK 4.5: Implement Explanation Generation Engine
DWBS Deliverable: D3.5 Explanation Generator
Category: Core
Execution Type: Sequential
Dependencies: 1.4, 4.3
Scope:
- Allowed: /src/core/decision/explanation
- Forbidden: LLMs
Task Definition:
Implement templates: "Recommended because [Item] expires in [Time]". Fill templates deterministically.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- All scores accompanied by text explanation
- No hallucinations
Validation Method:
- String matching tests
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.5), Timestamp, Template Engine Implementation, and Output Verification.

### TASK 4.6: Validate Decision Determinism
DWBS Deliverable: D3 Decision Engine v1
Category: Validation
Execution Type: Sequential
Dependencies: 4.1, 4.2, 4.3
Scope:
- Allowed: /tests/decision
- Forbidden: None
Task Definition:
Run the engine twice with identical inputs. Assert outputs are bitwise identical.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Zero variance in outputs
Validation Method:
- Repeated execution loop test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (4.6), Timestamp, Determinism Test Summary, and Verification Confirmation.

## 5. Ingestion Tasks

### TASK 5.1: Implement Draft/Staging Schema
DWBS Deliverable: D4.1 Draft State Flow
Category: Core
Execution Type: Sequential
Dependencies: 2.1
Scope:
- Allowed: /src/core/ingestion/draft
- Forbidden: None
Task Definition:
Define `DraftItem` and `DraftSession`. Drafts are NOT LedgerEvents.
Constraints:
- Trust Level: T1
Acceptance Criteria:
- Drafts distinct from Inventory
Validation Method:
- Type check
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (5.1), Timestamp, Draft Schema Definition, and Type Safety Verification.

### TASK 5.2: Implement OCR Data Extraction Service
DWBS Deliverable: D4.3 OCR Extraction
Category: Supporting
Execution Type: Sequential
Dependencies: 5.1
Scope:
- Allowed: /src/core/ingestion/ocr
- Forbidden: Real OCR APIs (Use Mock for Phase 1 Kernel)
Task Definition:
Implement interface `OcrProvider`. returning `List<DraftItem>`. Mark confidence as 0.4 (Unverified).
Constraints:
- Trust Level: T1
- Mock implementation allowed for core logic
Acceptance Criteria:
- Returns structured drafts
Validation Method:
- Mock integration test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (5.2), Timestamp, Mock OCR Implementation, and Data Structure Validation.

### TASK 5.3: Implement Confirmation Workflow Logic
DWBS Deliverable: D4.2 User Confirmation Loop
Category: Core
Execution Type: Sequential
Dependencies: 5.1, 2.2
Scope:
- Allowed: /src/core/ingestion/workflow
- Forbidden: Auto-commit
Task Definition:
Implement `finalizeDraft(List<DraftItem>)`. Converts Drafts -> `LedgerEvent.Bought` -> Ledger.
Constraints:
- Trust Level: T2 (User Action Required)
Acceptance Criteria:
- Drafts never enter ledger without this call
Validation Method:
- Workflow state test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (5.3), Timestamp, Workflow Logic, and State Transition Test Results.

### TASK 5.4: Implement Manual Entry Fallback Service
DWBS Deliverable: D4.4 Manual Add/Edit UI
Category: Core
Execution Type: Parallel
Dependencies: 2.1
Scope:
- Allowed: /src/core/ingestion/manual
- Forbidden: None
Task Definition:
Implement direct `createEntry(Item, Qty)` logic. bypasses draft if user explicitly types it.
Constraints:
- Trust Level: T2
Acceptance Criteria:
- Creates High-Confidence Events (1.0)
Validation Method:
- Confidence check test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (5.4), Timestamp, Manual Entry Service Implementation, and Confidence Verification.

### TASK 5.5: Validate No-Silent-Mutation Policy
DWBS Deliverable: D4 Assisted Capture
Category: Validation
Execution Type: Sequential
Dependencies: 5.3
Scope:
- Allowed: /tests/ingestion
- Forbidden: None
Task Definition:
Verify that calling OCR provider does NOT increase Ledger count.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Ledger size constant during drafting
Validation Method:
- count assertion test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (5.5), Timestamp, Policy Validation Summary, and Ledger Count Check logic.

## 6. Android App Tasks

### TASK 6.1: Initialize Android Project & Offline DB
DWBS Deliverable: D5.4 Offline-First Support
Category: Core
Execution Type: Sequential
Dependencies: 1.1
Scope:
- Allowed: /android/app
- Forbidden: Network libs (Retrofit etc)
Task Definition:
Create Android module. Setup Room Database to persist `LedgerEvents`.
Constraints:
- Trust Level: T2
- Offline capability mandatory
Acceptance Criteria:
- App launches
- Database works offline
Validation Method:
- Emulator run
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.1), Timestamp, Project Init Summary, and Database Capability Verification.

### TASK 6.2: Implement Inventory List UI
DWBS Deliverable: D5.1 Inventory Console
Category: Core
Execution Type: Sequential
Dependencies: 6.1, 2.2
Scope:
- Allowed: /android/features/inventory
- Forbidden: None
Task Definition:
RecyclerView showing current `InventoryState`. Connects to Core Logic `getSnapshot()`.
Constraints:
- Trust Level: T0 (View only)
Acceptance Criteria:
- Displays items correctly
Validation Method:
- Manual verification
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.2), Timestamp, UI Implementation Summary, and Verified Screenshot/State.

### TASK 6.3: Implement Cooking Suggestion Cards
DWBS Deliverable: D5.2 Cooking Suggestions
Category: Core
Execution Type: Sequential
Dependencies: 6.2, 4.1
Scope:
- Allowed: /android/features/suggestions
- Forbidden: None
Task Definition:
UI to show `SuggestedRecipies`. Includes "Why" text.
Constraints:
- Trust Level: T1 (Suggestions)
Acceptance Criteria:
- Shows suggestions sorted by score
Validation Method:
- Manual verification
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.3), Timestamp, Suggestion UI Summary, and Verified Output state.

### TASK 6.4: Implement Recipe Detail Screen
DWBS Deliverable: D5.3 Recipe Detail View
Category: Supporting
Execution Type: Sequential
Dependencies: 6.3
Scope:
- Allowed: /android/features/recipes
- Forbidden: None
Task Definition:
Full screen view of recipe, highlighting which ingredients user HAS vs MISSING.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Correctly highlights missing items
Validation Method:
- Manual verification
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.4), Timestamp, Detail View Implementation, and Missing Item Highlight verification.

### TASK 6.5: Implement Manual Add/Edit Screens
DWBS Deliverable: D5.5 Add/Edit Flows
Category: Core
Execution Type: Sequential
Dependencies: 5.4, 6.1
Scope:
- Allowed: /android/features/ingest
- Forbidden: None
Task Definition:
Form to manually add item. Calls `ManualEntryService`.
Constraints:
- Trust Level: T2
Acceptance Criteria:
- Adds item to updated list
Validation Method:
- Manual test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.5), Timestamp, Form Logic Implementation, and Add-Item Verified Workflow.

### TASK 6.6: Implement User Confirmation Screens
DWBS Deliverable: D5.5 Add/Edit Flows
Category: Core
Execution Type: Sequential
Dependencies: 5.3
Scope:
- Allowed: /android/features/review
- Forbidden: None
Task Definition:
UI to review Draft items (from mock OCR). "Approve" button commits to ledger.
Constraints:
- Trust Level: T2
Acceptance Criteria:
- Drafts editable before confirm
Validation Method:
- Manual test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.6), Timestamp, Confirmation UI Implementation, and Ledger Commit Verification.

### TASK 6.7: Validate Offline Capabilities
DWBS Deliverable: D5 Android App
Category: Validation
Execution Type: Sequential
Dependencies: 6.1
Scope:
- Allowed: /tests/android
- Forbidden: None
Task Definition:
Test app behavior in Airplane mode. Ensure DB read/write works.
Constraints:
- Trust Level: T2
Acceptance Criteria:
- No Crashes
- Data persists restart
Validation Method:
- Monkey test
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (6.7), Timestamp, Offline Test Results, and Persistence Verification.

## 7. Phase-1 Validation & Hardening

### TASK 7.1: Implement User Session Logger
DWBS Deliverable: D6.2 Session Logging
Category: Supporting
Execution Type: Sequential
Dependencies: 6.1
Scope:
- Allowed: /src/core/logging
- Forbidden: None
Task Definition:
Log start/end of sessions and major actions (Ingest, Cook). Store locally in separate file/table.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Logs valid session durations
Validation Method:
- File inspection
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (7.1), Timestamp, Logger Implementation Summary, and Sample Log Verification.

### TASK 7.2: Create Failure Documentation Templates
DWBS Deliverable: D6.3 Failure Documentation
Category: Supporting
Execution Type: Parallel
Dependencies: 1.5
Scope:
- Allowed: /docs/pilot
- Forbidden: None
Task Definition:
Create markdown templates for Pilot users to file "Truth Failures".
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Templates available in repo
Validation Method:
- Review
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (7.2), Timestamp, Template Creation Summary, and Link to Template.

### TASK 7.3: Create Pilot Onboarding Script
DWBS Deliverable: D6.1 Pilot Group
Category: Supporting
Execution Type: Parallel
Dependencies: None
Scope:
- Allowed: /docs/pilot
- Forbidden: None
Task Definition:
Document instructions for sideloading APK and initializing first inventory.
Constraints:
- Trust Level: T0
Acceptance Criteria:
- Instructions tested on fresh phone
Validation Method:
- Walkthrough
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (7.3), Timestamp, Doc Creation Summary, and Walkthrough Confirmation.

### TASK 7.4: Perform End-to-End Truth Validation
DWBS Deliverable: D6 Phase-1 Validation
Category: Validation
Execution Type: Sequential
Dependencies: All Previous
Scope:
- Allowed: /tests/e2e
- Forbidden: None
Task Definition:
Manual or Automated full cycle: Fresh Install -> Manual Add -> View -> Draft Ingest -> Confirm -> Cook Suggestion -> Cook -> Verify Ledger.
Constraints:
- Trust Level: T2
Acceptance Criteria:
- Ledger reflects reality at end of cycle
Validation Method:
- Full walkthrough report
Ledger Update Requirement:
- Status: Mandatory prerequisite for task completion.
- File: `/docs/execution/phase1_execution_ledger.md`
- Content: Append a new entry with Task ID (7.4), Timestamp, Full Cycle Validation Summary, and Confirmation of Truth.
