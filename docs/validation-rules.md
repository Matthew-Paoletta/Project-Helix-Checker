# Project Helix Validation Rules (derived from source PDFs)

Version: 1
Last updated: 2026-05-18

## Scope
These rules validate Helix submissions for commit shape, metadata quality signals, and test-path integrity.

## Decision outcomes
- VALID: all blocking rules pass.
- INVALID: one or more blocking rules fail.
- NEEDS_HUMAN_REVIEW: deterministic checks pass, but qualitative checks require reviewer judgment.

## Blocking rules (machine-enforced)

### R-001 Commit prefix format
Each commit message should start with one of:
- [sol]
- [f2p]
- [meta]
- [dep] (optional baseline dependency commit)

### R-002 Required commit types
Submission must include at least one commit with each:
- [sol]
- [f2p]
- [meta]

### R-003 Commit count bounds
Expected total commit count in evaluated range:
- minimum: 3
- maximum: 4 (optional [dep])

### R-004 Metadata file required
`.helix/metadata.json` must exist.

### R-005 Metadata fields required
`.helix/metadata.json` must contain non-empty:
- problem_statement
- problem_statement_variant
- hints
- FAIL_TO_PASS
- PASS_TO_PASS

### R-006 Test path plausibility
FAIL_TO_PASS and PASS_TO_PASS should reference plausible test files
(e.g., contain test/tests, or suffix .spec/.test/_test).

### R-007 Meaningful change-size guardrail
Total changed lines should generally be at least 25 and no more than 1000.

## Human-review rules (non-blocking)

### H-001 Problem statement quality
Must be model-readable, specific, and avoid PR/git leakage.

### H-002 Variant quality
Same task, less precise phrasing, reduced symbol leakage, shorter than main statement.

### H-003 Hints quality
Hints should be signposts (paths/symbols/errors), not implementation blueprint.

### H-004 F2P depth quality
F2P should test behavior, not symbol existence only.
