# gway-network

Standard network observation and topology helpers for GWAY boxes.

The package owns facts about local interfaces and addressing so consumers such as LCD, e-paper, kiosk, diagnostics, and provisioning do not each shell out to `ip` or NetworkManager independently.

Canonical command surface:

```console
gway network ip wlan0
gway network ip eth0
gway network carrier wlan0
gway network carrier eth0
gway network default-interface
gway network default-gateway
```

The interface is an argument to the capability: `ip(interface)` and `carrier(interface)`. Temporary zero-argument aliases such as `wlan0-ip` and `eth0-ip` remain available for current GWAY-backed Sigils until callable arguments are passed through the Sigil provider.
