# Changelog

All notable changes to `palveron-agt` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

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
