# Run the existing validator regression suite in CI

Protocol: codex-grokbot-v1
Task-ID: jh1nresh/.github:validator-tests-in-ci-20260907
Execution: ready
Mode: engineering
Packet-Revision: 1
Target-Repo: jh1nresh/.github
Implementation-Base-SHA: fd788697077fbf7584429f2c61e68535a999d1de
Executor: Tim
Return-Target: this planning PR

## Authority and scope

The founder explicitly approved starting this small CI PR through Grokbot,
including Tim implementation, independent Judge review, and Elon's gated
merge/closeout. This is a NEW task after merged engineering PR #3, not a replay
or repair of its completed agent. The canonical protocol remains
https://github.com/jh1nresh/.github/issues/1 .

Initial intake is the real native PR-opened event. This RFD is NEVER merged:
Elon persists and reads back accepted, closes it, and then dispatches Tim.
Keep its source branch. Tim creates one separate engineering PR from the exact
implementation base. On FAIL, reuse the SAME agent for bounded repair.
Elon remains the sole merge/closeout owner; only protocol-scoped merged
engineering branch cleanup is included. No deployment or permission changes.

## Outcome / company context

Product boundary: this repository supplies reusable CI workflows; this change
affects only its own self-test job, not downstream caller workflows.
Current state: PR #3 added eight offline stdlib unittest regressions; existing
CI compiles and runs the validator but never executes that regression suite.
Customer-value eval: maintainers receive an automatic failing PR check when a
validator regression test fails. No commercial/product decision is involved.
Failure taxonomy: zero tests executed despite green CI; swallowed test failure;
accidental change to action pins, permissions, events or reusable interfaces.
Resolve the prior Judge residual without broad workflow or test refactoring.

## Allowed-Paths

- `.github/workflows/self-test.yml` only: add one named test step to existing
  `jobs.validate.steps`, after the existing validator steps.

The planning file belongs ONLY to this RFD and must not enter the engineering PR.

## Out-of-Scope / invariants

- Do not change tests, validator, README, reusable workflows or dependencies.
- Preserve existing workflow/job names, push/pull_request events and branches,
  read-only permissions, concurrency, timeout, runner, Python 3.13 and action pins.
- No new jobs, workflow, packages, caches, matrix, secrets, services or subscriptions.
- No continue-on-error, failure swallowing, conditional skip or `|| true`.
- No auth/account/approval policy changes to make unattended proof easier.
- You are not alone: preserve other agents' work; use a distinct checkout/branch
  and do not touch SAV-E or any unrelated task. No parallel writer for this Task-ID.

## Must-Read

At the implementation base, read `.github/workflows/self-test.yml`,
`tests/test_validate_workflows.py`, `scripts/validate_workflows.py`, `README.md`,
and applicable repository instructions (none tracked at the inspected base).
Prior residual and repair context:
https://github.com/jh1nresh/.github/pull/3#issuecomment-5568751737 .

## Decisions / tasks

1. Verify exact starting base and one owner/agent after accepted receipt.
2. Add `Run validator regression tests` after policy validation, running exactly:
   `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v`
   from repository root using the existing Python setup. Preserve exit status.
3. Run focused checks below; create an atomic commit and separate engineering PR.
4. Tim sends the complete exact-head VERIFY READY packet directly to 森貝爾.
5. Judge independently inspects the one-file diff, reruns checks, and inspects
   the engineering head's real Actions log to verify eight tests actually ran.
6. Elon persists the complete same-head verdict before merging, including an
   explicitly attributed Judge relay if Judge's existing GitHub write route
   returns 403. Then merge only with all protocol gates and return closeout here.

## Tools / cwd

Elon uses the existing GitHub connected service and native intake/SendToAgent
tools; verify actual runtime schemas. Tim uses existing `cursor / CloudAgent`
with `action: launch`, `repo: jh1nresh/.github`, `starting_ref` equal to the full
base above, and this entire packet as prompt; preserve configured model defaults.
All shell commands below run from the isolated repository root. Use existing
GitHub/SCM bindings or authenticated `gh` for PR/check log read-back. No new bridge,
poller, credential or model override. Admission remains at most two active tasks;
queue rather than override existing owners if capacity is full.

## Verification

Baseline: validator and eight tests pass locally; self-test CI lacks the test step.

```bash
python3 -m py_compile scripts/validate_workflows.py
python3 scripts/validate_workflows.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

Expected: validator validates four workflows; exactly 8 tests run and report OK;
no tracked fixture mutations. Inspect diff against base: self-test.yml only and
one added named step/command, all other bytes unchanged. CI must run on the exact
engineering head and expose the new step plus `Ran 8 tests` and `OK` in its log.
The RFD's green CI alone is NOT implementation evidence.

## Acceptance / proof receipt

- One-file bounded diff; unchanged existing safety/CI configuration.
- Local validator and all 8 tests pass; exact-head required CI succeeds and log
  proves those tests executed without swallowed failures.
- Complete independent Judge verdict on the current head is persisted before
  Elon merge; no unresolved blocking findings; head move invalidates verdict.
- Closeout records Task-ID/revision/source head, native routine/event/run/request
  IDs and event time, accepted URL, one actual Tim Agent-ID, engineering PR/head,
  Judge URL, CI/log URL, merge SHA, RFD CLOSED/not merged and scoped branch result.
- Report whether any post-event Codex/user continuation or approval was needed;
  native event proof is not a claim of unattended reliability. Do not replace a
  missing native event with manual dispatch and call the experiment unattended.

## Stop-Conditions / deliverable

Stop with exact blocker for missing coverage/permissions/receipt, ownership
conflict, unknown base, out-of-scope repair, CI/test failure or moved review head.
Do not bypass safety gates. Deliver the separate engineering PR and durable
closeout to this RFD; no additional product, policy or documentation work.
