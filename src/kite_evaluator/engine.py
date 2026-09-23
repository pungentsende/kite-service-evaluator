from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re
from typing import Any

ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    level: str = "error"


def evaluate(manifest: dict[str, Any]) -> list[Finding]:
    """Return deterministic findings without contacting a network or wallet."""
    findings: list[Finding] = []
    for key in ("name", "network", "payTo", "routes"):
        if not manifest.get(key):
            findings.append(Finding("missing-field", f"required field is missing: {key}"))
    pay_to = manifest.get("payTo")
    if pay_to and not ADDRESS.fullmatch(str(pay_to)):
        findings.append(Finding("invalid-pay-to", "payTo must be a 20-byte EVM address"))
    routes = manifest.get("routes", [])
    if not isinstance(routes, list):
        findings.append(Finding("invalid-routes", "routes must be an array"))
        return findings
    seen: set[str] = set()
    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            findings.append(Finding("invalid-route", f"route {index} must be an object"))
            continue
        path = route.get("path")
        if not isinstance(path, str) or not path.startswith("/"):
            findings.append(Finding("invalid-path", f"route {index} must use an absolute path"))
        elif path in seen:
            findings.append(Finding("duplicate-path", f"route path is repeated: {path}"))
        else:
            seen.add(path)
        try:
            amount = Decimal(str(route.get("amount", "")))
            if amount <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            findings.append(Finding("invalid-amount", f"route {index} must have a positive amount"))
    if not routes:
        findings.append(Finding("no-routes", "at least one payable route is required"))
    return findings
