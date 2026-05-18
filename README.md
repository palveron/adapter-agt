# palveron-agt

Official Palveron adapter for **Microsoft Agent Governance Toolkit (AGT)** — enforce Palveron policies locally inside AutoGen and LangChain pipelines while keeping the audit trail centralised on the Palveron gateway.

[![PyPI version](https://img.shields.io/pypi/v/palveron-agt.svg?style=flat-square&color=cb3837)](https://pypi.org/project/palveron-agt/)
[![Python versions](https://img.shields.io/pypi/pyversions/palveron-agt.svg?style=flat-square)](https://pypi.org/project/palveron-agt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-palveron.com-5A67D8?style=flat-square)](https://docs.palveron.com/integrations/microsoft-agt)

---

Microsoft AGT gives you local policy enforcement at sub-millisecond speed. Palveron gives you centralised policy management, blockchain-anchored audit trails, and EU-AI-Act-ready compliance fields. This adapter wires them together so policies live in one place and fire everywhere.

- **Pulls policies** from your Palveron project on startup and on every refresh interval
- **Compiles** them into AGT enforcement rules without round-tripping prompts
- **Reports** every enforcement outcome back to the Palveron audit trail
- **Works with AutoGen and LangChain** — the two AGT-first stacks today

## Installation

```bash
pip install palveron-agt
```

## Quick Start

```python
import asyncio
from palveron_agt import PalveronAgtAdapter

async def main():
    adapter = PalveronAgtAdapter(api_key="pv_live_xxx")

    # Pull the project's active policies into AGT.
    await adapter.sync()

    # AGT enforces locally; the adapter reports every decision back
    # to the Palveron gateway for the audit trail.
    decision = await adapter.evaluate(
        prompt="Transfer $50,000",
        agent_id="finance_bot",
    )
    print(decision.allowed, decision.reason, decision.trace_id)

asyncio.run(main())
```

## Features

- **One source of truth** — author policies on the Palveron dashboard, enforce them anywhere
- **Local enforcement** — AGT runs in-process, no network hop on the hot path
- **Audit trail anchored** — every AGT decision flows back into the Palveron audit pipeline (and into Flare attestation when configured)
- **Async + sync** — both `Palveron` and `AsyncPalveron` SDK clients are supported

## Requirements

- **Python 3.10 or newer**
- Microsoft AGT runtime
- A Palveron account (free tier works for evaluation)

## Links

- **Documentation** — [docs.palveron.com/integrations/microsoft-agt](https://docs.palveron.com/integrations/microsoft-agt)
- **Dashboard** — [palveron.com](https://palveron.com)
- **Support** — [hello@palveron.com](mailto:hello@palveron.com)
- **GitHub** — [palveron/adapter-agt](https://github.com/palveron/adapter-agt)
- **Changelog** — [CHANGELOG.md](https://github.com/palveron/adapter-agt/blob/main/CHANGELOG.md)

## License

[MIT](./LICENSE) — Copyright © 2026 Palveron.
