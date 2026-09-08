from pathlib import Path

from gway_network import commands


def test_ip_returns_dash_without_carrier(monkeypatch):
    monkeypatch.setattr(commands, "_carrier", lambda _interface: 0)
    assert commands.ip("eth0") == "-"


def test_ip_returns_primary_ipv4(monkeypatch):
    monkeypatch.setattr(commands, "_carrier", lambda _interface: 1)
    monkeypatch.setattr(commands, "_ipv4", lambda interface: "10.42.0.1" if interface == "wlan0" else "-")
    assert commands.ip("wlan0") == "10.42.0.1"


def test_zero_arg_aliases_delegate_to_canonical_ip(monkeypatch):
    monkeypatch.setattr(commands, "ip", lambda interface: f"ip:{interface}")
    assert commands.wlan0_ip() == "ip:wlan0"
    assert commands.eth0_ip() == "ip:eth0"


def test_carrier_reads_sysfs(monkeypatch, tmp_path: Path):
    carrier_file = tmp_path / "carrier"
    carrier_file.write_text("1\n", encoding="utf-8")
    original = commands.Path
    monkeypatch.setattr(
        commands,
        "Path",
        lambda value: carrier_file if value == "/sys/class/net/eth0/carrier" else original(value),
    )
    assert commands.carrier("eth0") == 1


def test_default_route_fields(monkeypatch):
    monkeypatch.setattr(
        commands,
        "_run",
        lambda *_args, **_kwargs: '[{"dev":"wlan1","gateway":"192.168.1.1"}]',
    )
    assert commands.default_interface() == "wlan1"
    assert commands.default_gateway() == "192.168.1.1"
