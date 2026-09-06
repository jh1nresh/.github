# Workflow validator regression suite

Protocol: codex-grokbot-v1
Task-ID: jh1nresh/.github:validator-regression-suite-20260907
Execution: ready
Mode: engineering
Packet-Revision: 1
Target-Repo: jh1nresh/.github
Implementation-Base-SHA: 0cb6fd5b730ced897c767d1c9979aba4e49d201d
Executor: Tim
Return-Target: this planning PR

## Outcome

Add fast, offline regression tests for the existing shared workflow validator,
and document how maintainers run validation locally. This is the founder's
explicitly authorized low-risk real engineering trial of the existing native
PR listener → Elon → Tim → 森貝爾 → Elon route. Codex owns this plan; Tim owns
the separate engineering diff. Use one existing Tim/CloudAgent task only.

## Allowed-Paths

- `tests/test_validate_workflows.py` (new)
- `README.md` (only local validation instructions)

## Out-of-Scope

No changes to `.github/workflows/`, `scripts/validate_workflows.py`, action pins,
permissions, dependencies, secrets, products, production, deployment, accounts,
bot profiles or routines. Do not merge this RFD or delete its source branch.
No broad cleanup. Do not implement directly in the RFD branch.

## Must-Read

At the verified implementation base, read `scripts/validate_workflows.py`,
`README.md` and `.github/workflows/self-test.yml`; inspect any repo-local
instructions present in the checkout. Read the current protocol issue body:
https://github.com/jh1nresh/.github/issues/1 .

## Decisions

Use Python stdlib `unittest`, `tempfile`, `unittest.mock` and importlib as needed;
no new packages. Import the existing validator and patch its WORKFLOWS constant
to a temporary fixture directory copied from the checked-in workflow files.
Every mutation is confined to that fixture directory and restored per case.
Preserve existing validator behavior; report discoveries outside this scope.
Tests must be independently runnable from repository root and not modify the
real workflow files. Keep the implementation small and readable.

## Tasks

1. Confirm clean isolated checkout at Implementation-Base-SHA and check existing
   Task-ID ownership. Record baseline validator output before implementation.
2. Add success coverage for the unchanged workflow set and failure coverage for
   a missing workflow, a non-SHA action reference, forbidden pull_request_target,
   missing read-only default permissions, missing job timeout, missing
   workflow_call on a reusable file, and missing cancel-in-progress.
3. Assert SystemExit/error messages for expected failures; the successful case
   should verify the validator succeeds. Use meaningful isolated mutations.
4. Add concise README commands for the validator and unittest suite.
5. Verify, commit only Allowed-Paths on a `codex/` topic branch and open a
   SEPARATE ordinary engineering PR. Link this RFD and Task-ID.
6. Tim sends the ready packet directly to 森貝爾 for independent review;
   Judge returns a verdict and actual test evidence for the current head to
   Elon. Elon performs authorized merge/closeout only when the gates pass.

## Tools

Tim uses the existing `cursor / CloudAgent` integration. Verify its actual
schema in the execution environment. Invoke `action: launch`,
`repo: https://github.com/jh1nresh/.github`,
`starting_ref: 0cb6fd5b730ced897c767d1c9979aba4e49d201d`, with this FULL packet
plus source PR/head and Elon's accepted receipt as the prompt. Retain the
configured model defaults. No new tool integration or credential setup.
In the agent's returned checkout directory (record actual cwd), run all git,
Python and gh commands from repository root. Verify existing GitHub access;
use the existing Elon receipt relay if Tim cannot write GitHub comments.

## Verification

- Baseline and final: `python3 scripts/validate_workflows.py` → exit 0 and
  `validated 4 workflow files; immutable pins and safety policy passed`.
- Final: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v`
  → all eight or more meaningful cases pass, offline, no external dependencies.
- `git diff --check` → exit 0; only Allowed-Paths in engineering PR.
- Compare workflows and validator to Implementation-Base-SHA → unchanged.
- GitHub `Validate Shared Workflows / validate` and all required checks green
  for the engineering head; Judge separately runs the new test suite on that
  same head because existing CI does not yet execute it.

No known baseline validator failure; Codex verified the source and will record
the baseline command output on the RFD. UI/runtime/deployment evidence: N/A,
offline regression tests only.

## Acceptance

- Native `pr-opened` or `pr-pushed` event on THIS RFD causes intake by
  `pr-intake-a-elon-direct`. Return native routine ID, run ID/time, event kind,
  source PR/head and changed lastRunAt. Chat preflight or a manually invoked
  routine must not be represented as native-event proof.
- Elon persists and reads back accepted with Task-ID/source head/revision,
  then closes RFD without merging; saves the full packet for Tim.
- Exactly one Tim CloudAgent writes the separate engineering PR. Repeated
  Task-ID/head/revision delivery is NOOP; no extra successful receipts.
- Tests cover the eight scenarios, README commands are correct, no mutation of
  production files occurs during tests, and engineering scope is exact.
- 森貝爾 independently posts PASS or PASS-with-residual on the current head
  with test evidence. Tip movement invalidates the verdict.
- Founder authorizes Elon to merge THIS engineering PR after current-head
  Judge PASS, required CI green, branch eligibility and no unresolved blocking
  findings. Elon returns PR/head, merge SHA and closeout to this source RFD.
  Only bounded protocol-authorized merged-topic-branch cleanup is included.

## Stop-Conditions

If admission is full (maximum two active implementation/repair/review tasks),
queue this task without duplicating or evicting existing work. Count Tim work
from launch, not only after a PR exists. Block on missing permission, ambiguous
ownership, changed base needing a scope decision, unavailable required tools,
scope expansion, failed verification or unresolved Judge blockers. Route
repairs through Elon to the SAME Tim task. Do not launch a second writer or
alter listener settings to make a failed trial appear successful. If native
intake fails, report the exact blocker; do not silently substitute chat dispatch.

## Deliverable

One separate engineering PR with the tests and README, independent Judge
verdict, green CI, Elon merge and linked closeout; native intake evidence on
this RFD. Configuration/ACK alone must not declare operational default.
