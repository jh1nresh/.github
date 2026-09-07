#!/usr/bin/env python3
"""Offline regression tests for the shared workflow validator."""

from __future__ import annotations

import hashlib
import importlib.util
import shutil
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_workflows.py"
SOURCE_WORKFLOWS = REPO_ROOT / ".github" / "workflows"
SUCCESS_MESSAGE = (
    "validated 4 workflow files; immutable pins and safety policy passed"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_workflows", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"unable to load validator from {VALIDATOR_PATH}")
    spec.loader.exec_module(module)
    return module


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ValidateWorkflowsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.production_digests = {
            path.name: file_digest(path)
            for path in sorted(SOURCE_WORKFLOWS.glob("*.yml"))
        }

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture_dir = Path(self._tmp.name)
        for path in SOURCE_WORKFLOWS.glob("*.yml"):
            shutil.copy2(path, self.fixture_dir / path.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()
        current = {
            path.name: file_digest(path)
            for path in sorted(SOURCE_WORKFLOWS.glob("*.yml"))
        }
        self.assertEqual(current, self.production_digests)

    def _replace(self, name: str, old: str, new: str) -> None:
        path = self.fixture_dir / name
        text = path.read_text(encoding="utf-8")
        if old not in text:
            self.fail(f"{name} fixture does not contain expected text: {old!r}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def _run(self) -> None:
        with patch.object(self.validator, "WORKFLOWS", self.fixture_dir):
            self.validator.main()

    def _assert_fails(self, fragment: str) -> None:
        with patch.object(self.validator, "WORKFLOWS", self.fixture_dir):
            with self.assertRaises(SystemExit) as ctx:
                self.validator.main()
        message = str(ctx.exception)
        self.assertIn("error:", message)
        self.assertIn(fragment, message)

    def test_success_unchanged_workflow_set(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            self._run()
        self.assertEqual(stdout.getvalue().strip(), SUCCESS_MESSAGE)

    def test_missing_workflow_file(self) -> None:
        (self.fixture_dir / "docs-ci.yml").unlink()
        self._assert_fails(
            "workflow set must contain exactly three reusable workflows and self-test.yml"
        )

    def test_non_sha_action_reference(self) -> None:
        path = self.fixture_dir / "self-test.yml"
        text = path.read_text(encoding="utf-8")
        pinned_line = None
        sha = None
        for line in text.splitlines():
            match = self.validator.PINNED_USE.match(line)
            if match:
                pinned_line = line
                sha = match.group(1)
                break
        if pinned_line is None or sha is None:
            self.fail("self-test.yml fixture has no SHA-pinned uses: line")
        mutated_line = pinned_line.replace(f"@{sha}", "@v1", 1)
        path.write_text(text.replace(pinned_line, mutated_line, 1), encoding="utf-8")
        self._assert_fails("action is not pinned to a full commit SHA")

    def test_forbidden_pull_request_target(self) -> None:
        self._replace("self-test.yml", "pull_request:", "pull_request_target:")
        self._assert_fails("uses forbidden pull_request_target")

    def test_missing_read_only_default_permissions(self) -> None:
        self._replace(
            "self-test.yml",
            "permissions:\n  contents: read",
            "permissions:\n  contents: write",
        )
        self._assert_fails("must default to contents: read")

    def test_missing_job_timeout(self) -> None:
        self._replace("self-test.yml", "    timeout-minutes: 5\n", "")
        self._assert_fails("must bound job runtime")

    def test_missing_workflow_call_on_reusable(self) -> None:
        self._replace("node-ci.yml", "  workflow_call:", "  workflow_dispatch:")
        self._assert_fails("is not reusable")

    def test_missing_cancel_in_progress(self) -> None:
        self._replace(
            "node-ci.yml",
            "  cancel-in-progress: true",
            "  cancel-in-progress: false",
        )
        self._assert_fails("does not cancel stale runs")


if __name__ == "__main__":
    unittest.main()
