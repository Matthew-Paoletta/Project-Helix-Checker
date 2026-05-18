# Project Helix Validation Rules (derived from source PDFs)

Version: 4
Last updated: 2026-05-18

## Scope
These rules validate Helix submissions for:
- task validity guardrails
- commit-shape requirements
- .helix environment-setup constraints
- metadata completeness
- F2P/P2P quality and branch/PR hygiene signals

## Decision outcomes
- VALID: all blocking rules pass
- INVALID: one or more blocking rules fail
- NEEDS_HUMAN_REVIEW: deterministic checks pass, but qualitative checks remain

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
- recommended 25–500
- hard validator bounds 25–1000

### R-005 Required metadata file
`.helix/metadata.json` must exist.

### R-006 Required metadata fields non-empty
In `.helix/metadata.json`, required:
- problem_statement
- problem_statement_variant
- hints
- FAIL_TO_PASS
- PASS_TO_PASS

### R-007 Metadata placeholder rejection
Reject placeholder-like metadata values:
- "", "TODO", "N/A", "handshake", "placeholder"

### R-008 Test path plausibility
FAIL_TO_PASS and PASS_TO_PASS should contain plausible test paths.

### R-009 .helix folder strict contents
`.helix/` must contain only:
- Dockerfile.helix
- run-tests-eval.sh
- metadata.json

### R-010 Env-setup PR path scope allowlist
Env-setup scope must remain within:
- .helix/Dockerfile.helix
- .helix/run-tests-eval.sh
- .helix/metadata.json
- .github/workflows/build-push-gar.yml
- .github/workflows/golden-solution-validation.yml
- .github/workflows/helix-validation.yml

### R-011 Dockerfile mandatory deps
`.helix/Dockerfile.helix` must include:
- git
- ca-certificates

### R-012 Dockerfile auth hardening line
Dockerfile should include:
`git config --unset-all http.https://github.com/.extraheader || true`

### R-013 run-tests-eval behavior
`.helix/run-tests-eval.sh` must:
- run all tests with no args
- run provided comma-separated test paths with args
- not invoke docker commands directly
- be executable (mode 100755 expectation)

### R-014 Golden-solution Docker immutability
On `golden-solution` work, solution commits must not modify:
- .helix/Dockerfile.helix
- .helix/run-tests-eval.sh

### R-015 [sol] commit scope
`[sol]` commit should contain feature code only (no tests).

### R-016 [f2p] commit scope
`[f2p]` commit should contain test changes only.

### R-017 [meta] commit scope
`[meta]` commit should contain metadata updates only.

### R-018 Commit order
Expected order:
- [dep] optional first
- [sol]
- [f2p]
- [meta]

### R-019 F2P anti-pattern blocking
Reject weak symbol-existence-only test patterns lacking behavioral assertions.

### R-020 Golden PR title policy
Golden-solution PR title should start with:
- [GOLDEN SOLUTION]

### R-021 Docker-seeding PR title policy
Docker-seeding PR title should start with:
- [DOCKER SEEDING]

## Human-review rules (non-blocking)

### H-001 Problem statement quality
Clear/model-readable and no PR/git leakage.

### H-002 Variant quality
Same task, less precise, reduced symbol leakage.

### H-003 Hints quality
Signposts only; no blueprint-style implementation steps.

### H-004 F2P breadth & behavior
F2P should map to prompt behaviors and include meaningful behavioral checks.

### H-005 PR description quality
PR description should cover:
- Problem
- Approach
- Testing strategy

### H-006 CI status discipline
Do not submit/merge while required checks are pending/failed.

### H-007 Troubleshooting triage
When validation fails, use failed job logs to identify exact failing step and remediate before resubmission.
