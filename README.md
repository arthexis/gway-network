# gway-network

Standard network observation and topology helpers for GWAY boxes.

The package owns facts about local interfaces and addressing so consumers such as LCD, e-paper, kiosk, diagnostics, and provisioning do not each shell out to `ip` or NetworkManager independently.

Initial command surface:

```console
gway network wlan0-ip
gway network eth0-ip
gway network wlan0-carrier
gway network eth0-carrier
gway network default-interface
gway network default-gateway
```

The zero-argument interface aliases are intentionally available now for GWAY-backed Sigils. A generic argument-based `ip <iface>` / `carrier <iface>` surface can be added when callable Sigil arguments are wired through GWAY providers.
