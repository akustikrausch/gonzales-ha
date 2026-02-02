# Gonzales - Home Assistant Integration

Custom integration for [Home Assistant](https://www.home-assistant.io/) that monitors your internet speed via a local [Gonzales](https://github.com/akustikrausch/gonzales) instance.

---

## How It Works

This integration is a **read-only sensor plugin** for Home Assistant. It does **not** run speed tests itself and does **not** include its own web interface.

**Architecture:**
```
[Gonzales Server]  <--polls--  [gonzales-ha in HA]  -->  [HA Dashboard / Automations]
  (Raspberry Pi)                 (sensor data)
```

- **Gonzales** runs on a separate machine (e.g., Raspberry Pi) and performs the actual speed tests, stores history, and serves the web dashboard
- **gonzales-ha** (this integration) periodically polls the Gonzales REST API to read the latest measurement, system status, and ISP score
- All data flows one-way: Gonzales -> HA. The integration never triggers tests or modifies config
- Both systems are fully local -- no cloud dependency

You need a running Gonzales instance for this integration to work. Without it, the sensors will show "unavailable".

---

## Features

- **Download Speed** -- Latest download speed in Mbit/s
- **Upload Speed** -- Latest upload speed in Mbit/s
- **Ping Latency** -- Latest ping latency in ms
- **Ping Jitter** -- Latest ping jitter in ms
- **Packet Loss** -- Latest packet loss percentage
- **Last Test Time** -- Timestamp of the most recent speed test
- **ISP Performance Score** -- Composite 0-100 score with grade (A+ to F)
- **Diagnostic Sensors** -- Scheduler status, uptime, total measurements, database size

All sensors support Home Assistant long-term statistics.

---

## Requirements

- Home Assistant 2024.12.0 or newer
- A running Gonzales instance accessible on the local network
- Gonzales API must be reachable from the Home Assistant host

---

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three-dot menu (top right) and select **Custom repositories**
4. Add the repository URL and select **Integration** as the category
5. Click **Add**
6. Search for **Gonzales** in HACS and install it
7. Restart Home Assistant

### Manual

1. Copy the `custom_components/gonzales/` folder into your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

---

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for **Gonzales**
4. Enter the connection details:

| Field | Default | Description |
|-------|---------|-------------|
| Host | `localhost` | Hostname or IP of your Gonzales instance |
| Port | `8000` | Port the Gonzales API is running on |
| Update interval | `60` | How often to poll the API (seconds, 10-3600) |

The integration validates the connection during setup and will show an error if the Gonzales API is not reachable.

---

## Sensors

### Main Sensors

| Entity | Unit | Device Class | Description |
|--------|------|-------------|-------------|
| `sensor.gonzales_download_speed` | Mbit/s | `data_rate` | Latest download speed |
| `sensor.gonzales_upload_speed` | Mbit/s | `data_rate` | Latest upload speed |
| `sensor.gonzales_ping_latency` | ms | `duration` | Latest ping latency |
| `sensor.gonzales_ping_jitter` | ms | `duration` | Latest ping jitter |
| `sensor.gonzales_packet_loss` | % | -- | Latest packet loss |
| `sensor.gonzales_last_test_time` | -- | `timestamp` | Last test timestamp |
| `sensor.gonzales_isp_score` | points | -- | ISP performance score (0-100) |

The ISP score sensor includes extra attributes:
- `grade` -- Letter grade (A+, A, B, C, D, F)
- `speed_score` -- Speed component (0-100)
- `reliability_score` -- Reliability component (0-100)
- `latency_score` -- Latency component (0-100)
- `consistency_score` -- Consistency component (0-100)

The download speed sensor includes extra attributes:
- `server` -- Test server name
- `isp` -- Internet service provider

### Diagnostic Sensors

| Entity | Description |
|--------|-------------|
| `sensor.gonzales_scheduler_running` | Scheduler status (running/stopped) |
| `sensor.gonzales_test_in_progress` | Whether a test is currently running |
| `sensor.gonzales_uptime` | Server uptime in seconds |
| `sensor.gonzales_total_measurements` | Total number of measurements taken |
| `sensor.gonzales_db_size` | Database file size |

---

## Automation Examples

### Notify on slow internet

```yaml
automation:
  - alias: "Notify slow internet"
    trigger:
      - platform: numeric_state
        entity_id: sensor.gonzales_download_speed
        below: 50
    action:
      - service: notify.mobile_app
        data:
          title: "Slow Internet"
          message: >
            Download speed dropped to {{ states('sensor.gonzales_download_speed') }} Mbit/s
```

### Track ISP score changes

```yaml
automation:
  - alias: "ISP score degradation"
    trigger:
      - platform: numeric_state
        entity_id: sensor.gonzales_isp_score
        below: 60
    action:
      - service: notify.mobile_app
        data:
          title: "ISP Performance Alert"
          message: >
            ISP score is {{ states('sensor.gonzales_isp_score') }}
            ({{ state_attr('sensor.gonzales_isp_score', 'grade') }})
```

---

## Troubleshooting

- **Cannot connect**: Verify that the Gonzales API is running and reachable from your HA host. Test with: `curl http://<host>:<port>/api/v1/status`
- **Sensors show "unavailable"**: The Gonzales instance may not have any measurements yet. Run a speed test first.
- **Stale data**: The integration polls at the configured interval. Gonzales runs tests every 30 minutes by default.

---

## License

MIT
