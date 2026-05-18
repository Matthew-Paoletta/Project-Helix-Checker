# Project Helix Validation Rules (derived from source PDFs)

Version: 2
Last updated: 2026-05-18

## Scope
These rules validate Helix submissions for:
- Task validity guardrails
- Commit-shape requirements
- .helix environment-setup constraints
- metadata completeness
- test-path integrity

## Decision outcomes
- VALID: all blocking rules pass
- INVALID: one or more blocking rules fail
- NEEDS_HUMAN_REVIEW: deterministic checks pass, but quality/judgment checks remain

## Blocking rules (machine-enforced)

### R-001 Commit prefix format
Each commit message must start with:
- [sol], [f2p], [meta], or [dep]

### R-002 Required commit types
Submission must include at least one:
- [sol], [f2p], [meta]

### R-003 Commit count bounds
Total commits in evaluated range must be:
- min 3, max 4 (optional [dep])

### R-004 Real-logic LOC guardrail
Expected changed lines:
- recommended: 25–500
- hard validator bounds: 25–1000

### R-005 Required metadata file
`.helix/metadata.json` must exist.

### R-006 Required metadata fields non-empty
In `.helix/metadata.json`, required:
- problem_statement
- problem_statement_variant
- hints
- FAIL_TO_PASS
- PASS_TO_PASS

### R-007 Test path plausibility
FAIL_TO_PASS and PASS_TO_PASS should contain plausible test paths.

### R-008 .helix folder strict contents
`.helix/` must contain only:
- Dockerfile.helix
- run-tests-eval.sh
- metadata.json

### R-009 Env-setup PR path scope allowlist
Changed files for env setup must be within:
- .helix/Dockerfile.helix
- .helix/run-tests-eval.sh
- .helix/metadata.json
- .github/workflows/build-push-gar.yml
- .github/workflows/golden-solution-validation.yml
- .github/workflows/helix-validation.yml

### R-010 Dockerfile mandatory deps
`.helix/Dockerfile.helix` must include:
- git
- ca-certificates
(via apt-get/apk patterns)

### R-011 run-tests-eval behavior
`.helix/run-tests-eval.sh` must:
- run all tests with no args
- run provided comma-separated test paths with args
- never invoke docker commands directly

## Human-review rules (non-blocking)

### H-001 Problem statement quality
Clear/model-readable and no PR/git leakage.

### H-002 Variant quality
Same task, less precise, less symbol leakage.

### H-003 Hints quality
Signposts only; no blueprint-style fix instructions.

### H-004 F2P depth quality
Behavioral checks, not trivial symbol existence checks.
