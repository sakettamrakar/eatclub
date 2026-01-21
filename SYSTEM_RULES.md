# System Rules

This document establishes the authoritative constraints for all AI agents and tools interacting with the `eatclub` system. These rules prioritize system integrity, predictability, and human oversight.

## AI Tool Constraints

1.  **Truth Before Utility**: Never guess. If any parameter, contract, or state is uncertain, stop and ask the user.
2.  **No Silent Mutation**: All changes to project state, configuration, or structural files must be explicit and documented. No "fixing" things silently.
3.  **Contract-First Implementation**: No feature implementation or code modification is permitted without a corresponding technical contract or approved plan.
4.  **ML Isolation**: No Machine Learning or LLM calls are allowed within internal system logic unless explicitly authorized in the skill's formal definition.
5.  **Audit Integrity**: All logs, history files, and decision ledgers are append-only. Deletion or unauthorized modification of historical records is strictly prohibited.
6.  **Least Privilege Execution**: Tools must only operate within their defined scope. Any action outside of established boundaries requires explicit user consent.
