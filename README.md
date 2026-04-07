# vexis-agt-adapter

VEXIS ↔ **Microsoft Agent Governance Toolkit** bridge — centralized policies from VEXIS, sub-millisecond local enforcement via AGT, unified audit trails.

[![PyPI](https://img.shields.io/pypi/v/vexis-agt-adapter.svg?style=flat-square)](https://pypi.org/project/vexis-agt-adapter/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)

---

Microsoft AGT gives you local policy enforcement at sub-millisecond speed. VEXIS gives you centralized policy management, blockchain attestation, and cross-platform audit trails. This adapter connects them.

## Installation

```bash
pip install vexis-agt-adapter
```

## Quick Start

```python
from vexis_agt import VexisAGTBridge

bridge = VexisAGTBridge(api_key="gp_live_xxx")

# 1. Fetch policies from VEXIS for local AGT enforcement
policies = bridge.fetch_policies()

# 2. Export as AGT-compatible YAML
yaml_config = bridge.to_agt_yaml(policies)
# Write to AGT config file

# 3. Report local enforcement decisions back to VEXIS
trace_id = bridge.report_decision(
    agent_id="finance-bot",
    tool="database_query",
    decision="ALLOW",
    input_text="SELECT * FROM transactions WHERE amount > 10000",
)
```

## Architecture

```
┌─────────────────┐     Policies      ┌──────────────┐
│  VEXIS Gateway  │ ──────────────────→│  Microsoft   │
│  (Central)      │                    │  AGT (Local) │
│                 │ ←──────────────────│              │
│  Traces + Audit │     Evidence       │  <1ms Enforce│
└─────────────────┘                    └──────────────┘
```

VEXIS is the policy authority. AGT is the enforcement engine. Together they give you the best of both worlds.

## Links

- [Documentation](https://docs.vexis.io/integrations/microsoft-agt)
- [Microsoft AGT](https://github.com/microsoft/agent-governance-toolkit)
- [VEXIS Dashboard](https://app.vexis.io)

## License

[Apache 2.0](./LICENSE)
