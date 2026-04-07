"""
vexis-agt — VEXIS Governance Bridge for Microsoft Agent Governance Toolkit
==========================================================================

Connects Microsoft AGT's local policy enforcement with VEXIS centralized
governance. Two-way bridge:

1. **Policies FROM VEXIS**: AGT fetches policies from VEXIS API instead of local YAML
2. **Evidence TO VEXIS**: AGT enforcement decisions flow back as VEXIS traces

Usage::

    from vexis_agt import VexisAGTBridge

    bridge = VexisAGTBridge(api_key="gp_live_xxx")

    # Fetch policies from VEXIS for local AGT enforcement
    policies = bridge.fetch_policies()

    # Report enforcement decisions back to VEXIS
    bridge.report_decision(
        agent_id="agent_123",
        tool="database_query",
        decision="ALLOW",
        input_text="SELECT * FROM users",
    )
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

from vexis import Vexis, VerifyRequest, VexisError

__version__ = "0.1.0"
__all__ = ["VexisAGTBridge", "AGTPolicy"]

logger = logging.getLogger("vexis_agt")


@dataclass(frozen=True)
class AGTPolicy:
    """A governance policy in AGT-compatible format."""

    name: str
    description: str
    action: str  # ALLOW, DENY, REQUIRE_APPROVAL, LOG_ONLY
    scope: str  # tool pattern or "*"
    content_types: list[str]
    priority: int


class VexisAGTBridge:
    """
    Bridge between Microsoft Agent Governance Toolkit and VEXIS.

    Enables centralized policy management through VEXIS while leveraging
    AGT's local sub-millisecond enforcement. Evidence flows back to VEXIS
    for unified audit trails and blockchain attestation.

    Architecture::

        ┌─────────────────┐     Policies      ┌──────────────┐
        │  VEXIS Gateway  │ ──────────────────→│  Microsoft   │
        │  (Central)      │                    │  AGT (Local) │
        │                 │ ←──────────────────│              │
        │  Traces + Audit │     Evidence       │  <1ms Enforce│
        └─────────────────┘                    └──────────────┘

    Args:
        api_key: VEXIS project API key.
        base_url: Gateway URL (default: https://gateway.vexis.io).
        sync_interval: How often to sync policies in seconds (default: 300).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://gateway.vexis.io",
        sync_interval: int = 300,
        metadata: Optional[dict[str, Any]] = None,
    ):
        self._client = Vexis(api_key=api_key, base_url=base_url)
        self._sync_interval = sync_interval
        self._metadata = metadata or {}
        self._policies_cache: list[AGTPolicy] = []
        self._last_sync: float = 0

    def fetch_policies(self, environment: str = "prod") -> list[AGTPolicy]:
        """
        Fetch active policies from VEXIS and convert to AGT-compatible format.

        AGT can use these to enforce locally at sub-millisecond speed while
        VEXIS remains the central policy authority.

        Returns:
            List of policies in AGT-compatible format.
        """
        try:
            response = self._client.listPolicies(environment)
            policies = []
            for i, p in enumerate(response.policies):
                policies.append(
                    AGTPolicy(
                        name=p.get("name", f"policy_{i}"),
                        description=p.get("prompt", ""),
                        action=_infer_action(p),
                        scope="*",
                        content_types=p.get("contentTypes", ["text"]),
                        priority=i,
                    )
                )
            self._policies_cache = policies
            self._last_sync = time.monotonic()
            logger.info("📋 Synced %d policies from VEXIS", len(policies))
            return policies

        except VexisError as e:
            logger.error("Failed to sync policies from VEXIS: %s", e)
            return self._policies_cache  # Return cached if sync fails

    def report_decision(
        self,
        agent_id: str,
        tool: str,
        decision: str,
        input_text: str,
        *,
        output_text: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Report an AGT enforcement decision back to VEXIS for unified audit trail.

        This creates a trace in VEXIS that links the local AGT decision
        with the centralized governance record.

        Args:
            agent_id: The agent that made the call.
            tool: The tool or action that was governed.
            decision: AGT's local decision (ALLOW, DENY, etc.).
            input_text: The input that was checked.
            output_text: The output (if available).
            metadata: Extra metadata.

        Returns:
            VEXIS trace_id if successful, None on failure.
        """
        merged_meta = {
            **self._metadata,
            "source": "microsoft-agt",
            "agt_decision": decision,
            "agent_id": agent_id,
            "tool": tool,
            **(metadata or {}),
        }

        try:
            result = self._client.verify(
                VerifyRequest(
                    prompt=f"[AGT:{decision}] [Tool: {tool}] {input_text}",
                    metadata=merged_meta,
                )
            )
            logger.debug(
                "📝 AGT decision reported to VEXIS: %s → %s (trace: %s)",
                decision, result.decision.value, result.trace_id,
            )
            return result.trace_id

        except Exception as e:
            logger.warning("Failed to report AGT decision to VEXIS: %s", e)
            return None

    def should_sync(self) -> bool:
        """Check if policies need to be re-synced."""
        return (time.monotonic() - self._last_sync) >= self._sync_interval

    def to_agt_yaml(self, policies: Optional[list[AGTPolicy]] = None) -> str:
        """
        Export policies as AGT-compatible YAML for local enforcement.

        Returns:
            YAML string that can be written to AGT's policy config.
        """
        pol_list = policies or self._policies_cache
        lines = ["# Auto-generated from VEXIS — do not edit manually", "policies:"]
        for p in pol_list:
            lines.extend([
                f"  - name: {p.name}",
                f"    action: {p.action}",
                f"    scope: \"{p.scope}\"",
                f"    description: \"{p.description[:200]}\"",
            ])
        return "\n".join(lines)

    @property
    def cached_policies(self) -> list[AGTPolicy]:
        return list(self._policies_cache)


def _infer_action(policy: dict[str, Any]) -> str:
    """Infer AGT action from VEXIS policy data."""
    prompt = (policy.get("prompt") or "").lower()
    if any(w in prompt for w in ["block", "deny", "prevent", "reject"]):
        return "DENY"
    if any(w in prompt for w in ["approval", "review", "human"]):
        return "REQUIRE_APPROVAL"
    if any(w in prompt for w in ["log", "monitor", "flag", "observe"]):
        return "LOG_ONLY"
    return "ALLOW"
