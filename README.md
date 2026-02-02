# Gonzales - Home Assistant Add-on & Integration

This repository provides two components for running [Gonzales](https://github.com/akustikrausch/gonzales) with [Home Assistant](https://www.home-assistant.io/):

1. **Gonzales Add-on** -- Runs Gonzales entirely inside Home Assistant (recommended)
2. **Gonzales Integration** -- Sensor plugin that connects to an external Gonzales instance

---

## Option A: Home Assistant Add-on (Recommended)

The add-on runs Gonzales as a self-contained Docker container managed by the HA Supervisor. It includes the speed test backend, scheduler, database, and web dashboard -- all accessible through the HA sidebar.

```
Browser --> HA Sidebar --> Ingress --> Gonzales Web UI
                                        |
                            Speedtest CLI + Scheduler + SQLite
```

### Add-on Installation

1. In Home Assistant, go to **Settings > Add-ons**
2. Click the **Add-on Store** (bottom right)
3. Open the three-dot menu (top right) and select **Repositories**
4. Add: `https://github.com/akustikrausch/gonzales-ha`
5. Find **Gonzales Speed Monitor** in the store and click **Install**
6. Start the add-on -- the web dashboard appears in the HA sidebar

The sensor integration is auto-discovered when the add-on starts. Confirm setup when prompted to get all sensors in HA.

### Add-on Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `test_interval_minutes` | `30` | Minutes between automatic speed tests (1-1440) |
| `download_threshold_mbps` | `1000.0` | Expected download speed for scoring |
| `upload_threshold_mbps` | `500.0` | Expected upload speed for scoring |
| `preferred_server_id` | `0` | Ookla server ID (0 = auto-select) |
| `log_level` | `INFO` | Log verbosity (DEBUG, INFO, WARNING, ERROR) |

Data is persisted in `/data/` across updates and restarts.

For detailed add-on documentation, see [gonzales-addon/DOCS.md](gonzales-addon/DOCS.md).

---

## Option B: Standalone Integration (HACS)

If you run Gonzales on a separate machine (e.g. a Raspberry Pi or server), install the sensor integration to pull data into HA.

```
[Gonzales Server]  <--polls--  [gonzales-ha in HA]  -->  [HA Dashboard / Automations]
  (Raspberry Pi)                 (sensor data)
```

The integration is a **read-only sensor plugin**. It polls the Gonzales REST API to read measurements, status, and ISP score. It never triggers tests or modifies config. Fully local -- no cloud dependency.

### Integration Installation

**HACS (Recommended):**

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three-dot menu (top right) and select **Custom repositories**
4. Add `https://github.com/akustikrausch/gonzales-ha` and select **Integration**
5. Search for **Gonzales** in HACS and install it
6. Restart Home Assistant

**Manual:**

1. Copy the `custom_components/gonzales/` folder into your HA `config/custom_components/` directory
2. Restart Home Assistant

### Integration Configuration

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

## Requirements

- Home Assistant 2024.12.0 or newer
- **Add-on**: No additional requirements (everything runs inside HA)
- **Integration**: A running Gonzales instance accessible on the local network

---

## Sensors (both options)

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

### Add-on

- **Web UI not loading**: Restart the add-on and check logs. Ensure Ingress is enabled.
- **Speed test fails**: Check add-on logs. The Ookla CLI license is accepted automatically on first run.
- **Sensors not appearing**: The add-on registers auto-discovery on startup. Go to **Settings > Devices & Services** and check for a Gonzales discovery notification.

### Integration (standalone)

- **Cannot connect**: Verify that the Gonzales API is running and reachable from your HA host. Test with: `curl http://<host>:<port>/api/v1/status`
- **Sensors show "unavailable"**: The Gonzales instance may not have any measurements yet. Run a speed test first.
- **Stale data**: The integration polls at the configured interval. Gonzales runs tests every 30 minutes by default.

---

## License

MIT
