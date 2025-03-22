# WiFi Presence Sensor

This Home Assistant integration scans the local WiFi network and detects known devices, acting as a presence sensor.

## Features:
- Uses ARP scanning to detect known devices
- Reports presence as a binary sensor (`home` / `not_home`)
- Configurable scan interval