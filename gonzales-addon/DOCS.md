# Gonzales Speed Monitor - Add-on Documentation

## Overview

This add-on runs the [Gonzales](https://github.com/akustikrausch/gonzales) internet speed monitor directly inside Home Assistant. It performs automated speed tests using the Ookla Speedtest CLI, stores results in a local database, and provides a web dashboard accessible through the Home Assistant sidebar.

## How It Works

The add-on is a self-contained Docker container that includes:

- **Gonzales backend** (FastAPI + scheduler + SQLite)
- **Ookla Speedtest CLI** for actual speed measurements
- **Web dashboard** served via Home Assistant Ingress

The add-on runs speed tests at a configurable interval, stores all results persistently in `/data/gonzales.db`, and exposes a full web UI through the HA sidebar.

### Architecture

```
Browser --> HA Sidebar --> Ingress --> Gonzales Web UI (port 8099)
                                        |
                            FastAPI + APScheduler + SQLAlchemy
                                        |
                            Ookla Speedtest CLI + SQLite WAL
```

- **Multi-stage Docker build**: Build dependencies (git) are not included in the runtime image
- **jemalloc allocator**: Reduces memory fragmentation on ARM devices (Raspberry Pi)
- **AppArmor profile**: Restricts container access to only what's needed
- **Watchdog**: Supervisor auto-restarts the add-on if the health check fails

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `test_interval_minutes` | `30` | How often to run a speed test (1-1440 minutes) |
| `download_threshold_mbps` | `1000.0` | Expected download speed for scoring |
| `upload_threshold_mbps` | `500.0` | Expected upload speed for scoring |
| `preferred_server_id` | `0` | Ookla server ID to use (0 = auto-select) |
| `log_level` | `INFO` | Log verbosity (DEBUG, INFO, WARNING, ERROR) |

## Security

- **API key**: The add-on generates a random API key on first start and persists it in `/data/.api_key`. The key is passed to the integration via Supervisor discovery, so no manual configuration is needed.
- **AppArmor**: A restrictive profile limits the container to Python, the speedtest binary, `/data/` access, and network operations.
- **No external ports**: The web UI is only accessible via HA Ingress (no ports exposed to the host network).

## Integration with gonzales-ha

If you also have the **Gonzales** Home Assistant integration installed (via HACS), the add-on will be auto-discovered. You'll get a notification in Home Assistant to set up the integration, which creates sensors for:

- Download/Upload speed
- Ping latency and jitter
- Packet loss
- ISP performance score
- Scheduler status and diagnostics

The API key is passed automatically via discovery -- no manual entry required.

## Data Persistence

All data is stored in `/data/` which is persistent across add-on updates and restarts:

- `gonzales.db` -- SQLite database with all speed test results
- `config.json` -- Runtime configuration changes made via the web UI
- `.api_key` -- Auto-generated API key (permissions: 600)
- `.speedtest_eula_accepted` -- Ookla license acceptance sentinel

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

## Ookla Speedtest CLI

This add-on uses the [Ookla Speedtest CLI](https://www.speedtest.net/apps/cli), which is proprietary software free for personal, non-commercial use. The CLI license (EULA + GDPR consent) is automatically accepted on first start. By using this add-on, you agree to Ookla's [terms of use](https://www.speedtest.net/about/terms).

## Troubleshooting

- **Speed test fails**: Check the add-on logs for error messages. The Ookla CLI license is accepted automatically on first run.
- **Web UI not loading**: Try restarting the add-on. Check that Ingress is enabled in the add-on configuration.
- **Slow or unreliable results**: Try setting a specific `preferred_server_id` instead of auto-selection. You can find server IDs in the web dashboard under Settings.
- **Add-on keeps restarting**: Check the logs for startup errors. The watchdog will restart the add-on if the health check fails for 3 consecutive checks.
