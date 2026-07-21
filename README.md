# Shared GitHub Workflows

Reusable CI primitives for repositories owned by `jh1nresh`.

These workflows centralize only stable mechanics: immutable action pins,
read-only permissions, dependency installation, stale-run cancellation, and
bounded timeouts. Product-specific tests remain in each caller repository.

## Workflows

- `node-ci.yml`: npm or pnpm service validation through one package script.
- `web-ci.yml`: npm web verification plus a required build-output check.
- `docs-ci.yml`: one Python or shell validator with optional shell syntax checks.

Callers should pin this repository to a full commit SHA. Do not pass secrets,
deployment credentials, or arbitrary production commands into these workflows.

