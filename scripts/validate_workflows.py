#!/usr/bin/env python3
"""Validate the small immutable-policy contract for shared workflows."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
REUSABLE = ("node-ci.yml", "web-ci.yml", "docs-ci.yml")
PINNED_USE = re.compile(r"^\s*-?\s*uses:\s*[^\s@]+@([0-9a-f]{40})(?:\s+#.*)?$")


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def main() -> None:
    paths = sorted(WORKFLOWS.glob("*.yml"))
    if {path.name for path in paths} != {*REUSABLE, "self-test.yml"}:
        fail("workflow set must contain exactly three reusable workflows and self-test.yml")

    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "pull_request_target" in text:
            fail(f"{path.name} uses forbidden pull_request_target")
        if "permissions:\n  contents: read" not in text:
            fail(f"{path.name} must default to contents: read")
        if "timeout-minutes:" not in text:
            fail(f"{path.name} must bound job runtime")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "uses:" not in line:
                continue
            if not PINNED_USE.match(line):
                fail(f"{path.name}:{line_number} action is not pinned to a full commit SHA")

    for name in REUSABLE:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        if "workflow_call:" not in text:
            fail(f"{name} is not reusable")
        if "cancel-in-progress: true" not in text:
            fail(f"{name} does not cancel stale runs")

    print(f"validated {len(paths)} workflow files; immutable pins and safety policy passed")


if __name__ == "__main__":
    main()
