# Drift Detector Checklist

## 1. Scope Drift
- [ ] Does this change implement features outside the currently active Phase?
- [ ] Does this change introduce a new entity type not defined in the domain model?
- [ ] Does this change require external dependencies not currently in the lockfile?
- [ ] Does this change modify the definition of "Done" for the current task?
- [ ] Does this change solve a problem the user did not explicitly state?

## 2. Authority Drift
- [ ] Does this change allow the system to mutate state without user confirmation?
- [ ] Does this change override a constraint defined in `SYSTEM_RULES.md`?
- [ ] Does this change prioritize system inference over direct user input?
- [ ] Does this change modify the permissions structure (MTRI)?
- [ ] Does this change bypass the decision engine for a core action?

## 3. Intelligence Drift
- [ ] Does this change use probabilistic logic for core business rules?
- [ ] Does this change rely on an LLM for deterministic state transitions?
- [ ] Does this change assume context that is not present in the file system?
- [ ] Does this change hide logic behind an opaque AI call?
- [ ] Does this change attempt to "guess" user intent?

## 4. Trust Drift
- [ ] Does this change exceed the current Trust Level (T2) allowed actions?
- [ ] Does this change fail to log a decision in the audit trail?
- [ ] Does this change obscure the cause of an error from the user?
- [ ] Does this change remove a safeguard against data corruption?
- [ ] Does this change allow a silent failure mode?

## 5. Reality Drift
- [ ] Does this change assume the digital ledger is more accurate than physical reality?
- [ ] Does this change fail to account for data staleness or latency?
- [ ] Does this change assume an external API is infallible?
- [ ] Does this change ignore the possibility of negative inventory logic errors?
- [ ] Does this change remove a check for physical feasibility?
