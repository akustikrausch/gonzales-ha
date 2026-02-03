# Gonzales Internet Speed Monitor

Automated internet speed monitoring with Home Assistant integration.

## Features

- **Automatic Speed Tests** - Configurable intervals (default: 30 min)
- **Home Assistant Sensors** - Download, upload, ping, jitter, packet loss
- **ISP Performance Score** - A-F grade based on consistency
- **Internet Outage Detection** - Binary sensor with smart retry logic
- **Web Dashboard** - Full UI accessible via HA sidebar (with add-on)
- **QoS Tests** - Netflix 4K, Zoom HD, Cloud Gaming, VPN profiles
- **Network Topology** - Traceroute analysis
- **Export** - PDF/CSV reports for ISP documentation

## Sensors

| Entity | Description |
|--------|-------------|
| `sensor.gonzales_download_speed` | Download speed (Mbit/s) |
| `sensor.gonzales_upload_speed` | Upload speed (Mbit/s) |
| `sensor.gonzales_ping_latency` | Ping latency (ms) |
| `sensor.gonzales_ping_jitter` | Jitter (ms) |
| `sensor.gonzales_packet_loss` | Packet loss (%) |
| `sensor.gonzales_isp_score` | ISP score (0-100) |
| `binary_sensor.gonzales_internet_outage` | Outage detected |

## Installation Options

### Option 1: Add-on (Recommended)
Add this repository to Home Assistant Add-on Store and install "Gonzales Speed Monitor".

### Option 2: HACS Integration
Install this integration via HACS and connect to an existing Gonzales instance.

## Links

- [Documentation](https://github.com/akustikrausch/gonzales-ha)
- [Main Project](https://github.com/akustikrausch/gonzales)
- [Report Issues](https://github.com/akustikrausch/gonzales-ha/issues)
