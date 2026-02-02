# Gonzales Speed Monitor - Add-on Documentation

## Overview

This add-on runs the [Gonzales](https://github.com/akustikrausch/gonzales) internet speed monitor directly inside Home Assistant. It performs automated speed tests using the Ookla Speedtest CLI, stores results in a local database, and provides a web dashboard accessible through the Home Assistant sidebar.

## How It Works

The add-on is a self-contained Docker container that includes:

- **Gonzales backend** (FastAPI + scheduler + SQLite)
- **Ookla Speedtest CLI** for actual speed measurements
- **Web dashboard** served via Home Assistant Ingress

The add-on runs speed tests at a configurable interval, stores all results persistently in `/data/gonzales.db`, and exposes a full web UI through the HA sidebar.

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `test_interval_minutes` | `30` | How often to run a speed test (1-1440 minutes) |
| `download_threshold_mbps` | `1000.0` | Expected download speed for scoring |
| `upload_threshold_mbps` | `500.0` | Expected upload speed for scoring |
| `preferred_server_id` | `0` | Ookla server ID to use (0 = auto-select) |
| `log_level` | `INFO` | Log verbosity (DEBUG, INFO, WARNING, ERROR) |

## Integration with gonzales-ha

If you also have the **Gonzales** Home Assistant integration installed (via HACS), the add-on will be auto-discovered. You'll get a notification in Home Assistant to set up the integration, which creates sensors for:

- Download/Upload speed
- Ping latency and jitter
- Packet loss
- ISP performance score
- Scheduler status and diagnostics

## Data Persistence

All data is stored in `/data/` which is persistent across add-on updates and restarts:

- `gonzales.db` — SQLite database with all speed test results
- `config.json` — Runtime configuration changes made via the web UI

## Web Dashboard

Access the Gonzales web dashboard directly from the Home Assistant sidebar. The dashboard provides:

- Real-time speed test progress with live visualization
- Historical speed test results with charts
- ISP performance scoring and statistics
- Data export (CSV/PDF)
- Manual speed test triggering

## Network Requirements

- The add-on needs internet access to perform speed tests
- No incoming ports need to be exposed (Ingress handles web UI access)
- The Ookla Speedtest CLI connects to nearby test servers automatically

## Troubleshooting

- **Speed test fails**: Check the add-on logs for error messages. The Ookla CLI may need to accept the license on first run (handled automatically).
- **Web UI not loading**: Try restarting the add-on. Check that Ingress is enabled in the add-on configuration.
- **Slow or unreliable results**: Try setting a specific `preferred_server_id` instead of auto-selection. You can find server IDs in the web dashboard under Settings.
