"""GWAY command surface for local network telemetry."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def _run(args: list[str], *, timeout: float = 2.0) -> str:
    try:
        result = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip()


def _ipv4(interface: str) -> str:
    output = _run(["ip", "-j", "-4", "addr", "show", "dev", interface])
    if not output:
        return "-"
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return "-"
    for item in payload:
        for address in item.get("addr_info", []):
            if address.get("family") == "inet" and address.get("local"):
                return str(address["local"])
    return "-"


def _carrier(interface: str) -> int:
    try:
        value = Path(f"/sys/class/net/{interface}/carrier").read_text(encoding="utf-8").strip()
    except OSError:
        return 0
    return int(value == "1")


def wlan0_ip() -> str:
    return _ipv4("wlan0")


def eth0_ip() -> str:
    return _ipv4("eth0") if _carrier("eth0") else "-"


def wlan0_carrier() -> int:
    return _carrier("wlan0")


def eth0_carrier() -> int:
    return _carrier("eth0")


def _default_route() -> dict[str, object]:
    output = _run(["ip", "-j", "route", "show", "default"])
    if not output:
        return {}
    try:
        routes = json.loads(output)
    except json.JSONDecodeError:
        return {}
    if not isinstance(routes, list) or not routes:
        return {}
    route = routes[0]
    return route if isinstance(route, dict) else {}


def default_interface() -> str:
    return str(_default_route().get("dev") or "-")


def default_gateway() -> str:
    return str(_default_route().get("gateway") or "-")
