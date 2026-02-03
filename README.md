# Gonzales - Home Assistant Add-on & Integration

This repository provides two components for running [Gonzales](https://github.com/akustikrausch/gonzales) with [Home Assistant](https://www.home-assistant.io/):

1. **Gonzales Add-on** -- Runs Gonzales entirely inside Home Assistant (recommended)
2. **Gonzales Integration** -- Sensor plugin that connects to an external Gonzales instance

---

## Option A: Home Assistant Add-on (Recommended)

The add-on runs Gonzales as a self-contained Docker container managed by the HA Supervisor. It includes the speed test backend, scheduler, database, and web dashboard -- all accessible through the HA sidebar. Pre-built images for **aarch64** (Raspberry Pi) and **amd64** are available on GHCR for fast installation.

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
| `download_threshold_mbps` | `1000.0` | Expected download speed (your subscribed plan) |
| `upload_threshold_mbps` | `500.0` | Expected upload speed (your subscribed plan) |
| `tolerance_percent` | `15.0` | Acceptable deviation from threshold (15% means 85% of subscribed speed is OK) |
| `preferred_server_id` | `0` | Ookla server ID (0 = auto-select) |
| `log_level` | `INFO` | Log verbosity (DEBUG, INFO, WARNING, ERROR) |

The tolerance setting allows you to define what counts as "acceptable" speed. For example, with a 1000 Mbps plan and 15% tolerance, any measurement above 850 Mbps is considered compliant.

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
| API key | *(empty)* | API key if the instance has `GONZALES_API_KEY` set |
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

## Main Project

This repository contains only the Home Assistant add-on and integration. The Gonzales speed monitor itself (backend, web dashboard, TUI, API) lives in the main repository:

**[github.com/akustikrausch/gonzales](https://github.com/akustikrausch/gonzales)** -- standalone installation, full API documentation, configuration reference, Raspberry Pi setup, and development guide.

---

## Security

- **API key**: The add-on auto-generates a persistent API key and passes it to the integration via Supervisor discovery. For standalone setups, the key can be entered manually during integration setup.
- **AppArmor**: The add-on ships with a restrictive AppArmor profile.
- **No exposed ports**: The web UI is only accessible via HA Ingress.

## Ookla Speedtest CLI

This project uses the [Ookla Speedtest CLI](https://www.speedtest.net/apps/cli), which is proprietary software free for personal, non-commercial use. By using Gonzales, you agree to Ookla's [terms of use](https://www.speedtest.net/about/terms) and [privacy policy](https://www.speedtest.net/about/privacy).

## License

MIT (Gonzales code). The Ookla Speedtest CLI has its own license -- see above.
