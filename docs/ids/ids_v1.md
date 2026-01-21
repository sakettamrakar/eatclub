1. All inventory mutations must be recorded in an append-only ledger.
2. Inventory quantities must never be negative.
3. Automated ingestion must create draft records requiring explicit user confirmation.
4. Decision engine logic must be deterministic and reproducible.
5. Core business logic must not execute Machine Learning or LLM calls.
6. Every system recommendation must include a structured explanation of its rationale.
7. Recipe feasibility must be computable strictly from current inventory state.
8. Recipe logic must not rely on free-text parsing.
9. All data operations must function without an active internet connection.
10. Historical ledger entries must never be modified or deleted.
11. System must not infer inventory state changes without explicit user action.
