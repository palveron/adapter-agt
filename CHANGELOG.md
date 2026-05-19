# Changelog

All notable changes to `palveron-agt` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-05-19

### Changed
- Requires `palveron-sdk>=1.1.0` so callers transparently consume the
  gateway's Sprint-87 HTTP semantics (200/202/403/429 surface as
  governance decisions, not exceptions). The AGT bridge only uses
  `verify()` as a telemetry channel — it logs the returned decision
  and does not gate on it — so no code changes are needed in the
  bridge itself.
- Fixed `__version__` lagging behind `pyproject.toml` (was `"0.1.0"`).

### Known Issues
- `PalveronAGTBridge.fetch_policies()` (formerly named `sync_policies`)
  calls `self._client.listPolicies(...)`, which **does not exist on the
  Python `Palveron` client** — only the TypeScript SDK exposes
  `listPolicies()`. Calling `fetch_policies()` will raise
  `AttributeError`. Pre-existing bug; tracked separately and will be
  resolved by adding `list_policies()` to `palveron-sdk` in a future
  minor release. This bug does not affect `report_decision()`, which
  is the bridge's primary code path.

## [1.0.0] — 2026-05-18

### Added
- Initial public release of `palveron-agt` on PyPI
- Drop-in adapter that wires the Palveron gateway into Microsoft's
  Agent Governance Toolkit (AGT) — gives AutoGen and LangChain
  pipelines the same policy enforcement and audit trail surface as the
  rest of the Palveron platform
- Policy synchronisation from the central Palveron project down to
  the local AGT enforcement layer
- Compatible with the synchronous `Palveron` and the async
  `AsyncPalveron` clients from `palveron-sdk`
- Full type hints (PEP 561 compliant via `py.typed`)
