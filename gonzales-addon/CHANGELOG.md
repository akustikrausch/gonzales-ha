# Changelog

## 3.7.4

### Bug Fixes

- **Fix startup crash**: Correct import name in speedtest.py

---

## 3.7.3

### Bug Fixes

- **Fix 502 Bad Gateway on speedtest trigger**: Speedtest trigger endpoint now returns immediately (202 Accepted) and runs test in background, preventing Ingress proxy timeout

---

## 3.7.2

### Bug Fixes

- **Fix live test view**: Test progress now displays correctly during backend-initiated tests in Home Assistant Ingress (fixes "Ready" badge showing during active tests)
- **Fix integration install issues**: Complete cleanup of old integration files including `__pycache__` to prevent "Invalid handler specified" errors when upgrading from older versions

---

## 3.7.1

### Bug Fixes

- **Fix startup crash**: Correct import path in root_cause.py (`db.session` → `db.engine`)

---

## 3.7.0

### Improvements

- **Mobile Navigation UX**: Complete overhaul with proper animations and accessibility
  - Smooth slide-up/slide-down animations for bottom sheet
  - Touch targets increased to 44x44px (Apple/Google guidelines)
  - ARIA attributes for screen readers, focus trapping, keyboard navigation

### New Features

**Smart Test Scheduling**
- **Adaptive test intervals**: Automatically adjusts test frequency based on network conditions
- **Three-phase model**: Normal (fixed interval) → Burst (frequent tests on anomaly) → Recovery (gradual return to normal)
- **Stability detection**: Uses coefficient of variation and z-score analysis to detect network instability
- **Safety mechanisms**: Circuit breaker (max tests per window), daily data budget, min/max interval limits
- **Settings UI**: New Smart Scheduler card in Settings page with phase indicator, stability score, and data budget display

**Root-Cause Analysis**
- **New Root-Cause page**: Comprehensive network diagnostics accessible from navigation
- **Network health score**: 0-100 composite score based on all network layers
- **Layer health breakdown**: Individual scores for DNS, Local Network, ISP Backbone, ISP Last-Mile, and Server
- **Problem fingerprinting**: Automatic detection of issues with severity, confidence, and evidence
- **Hop-speed correlation**: Pearson correlation analysis between traceroute hops and download speed (identifies bottlenecks)
- **Time-based pattern detection**: Detects peak-hour degradation and off-peak improvements
- **Connection impact analysis**: Compares performance across WiFi vs Ethernet connections
- **Actionable recommendations**: Prioritized suggestions based on detected issues

### Home Assistant Integration

**New Sensors:**
- `sensor.gonzales_smart_scheduler_phase` - Current scheduler phase (normal/burst/recovery)
- `sensor.gonzales_stability_score` - Network stability score (0-100%)
- `sensor.gonzales_current_interval` - Current test interval in minutes
- `sensor.gonzales_data_used_today` - Data used today in MB
- `sensor.gonzales_network_health` - Root-cause network health score (0-100)
- `sensor.gonzales_primary_issue` - Primary detected network issue (or "Healthy")
- `sensor.gonzales_dns_health` - DNS layer health score
- `sensor.gonzales_local_network_health` - Local network layer health score
- `sensor.gonzales_isp_backbone_health` - ISP backbone layer health score
- `sensor.gonzales_isp_lastmile_health` - ISP last-mile layer health score

**New CLI Commands:**
- `gonzales smart-scheduler status/enable/disable/config/decisions` - Manage smart scheduling
- `gonzales root-cause analyze/fingerprints/recommendations/hops` - Network diagnostics

### API Endpoints

- `GET /api/v1/smart-scheduler/status` - Current scheduler phase, stability score, data budget
- `GET /api/v1/smart-scheduler/config` - Configuration settings
- `PUT /api/v1/smart-scheduler/config` - Update configuration
- `POST /api/v1/smart-scheduler/enable` - Enable smart scheduling
- `POST /api/v1/smart-scheduler/disable` - Disable smart scheduling
- `GET /api/v1/root-cause/analysis` - Full root-cause analysis

## 3.6.1

### Bug Fixes
- **Fix byte formatting**: Large values now properly display as GB/TB instead of showing huge MB numbers (e.g., "52.1 GB" instead of "53346.8 MB")

## 3.6.0

### New Features
- **Scheduler control toggle**: Click the scheduler badge in the header to pause/resume automatic speed tests
- **Scheduler control in Settings**: New "Scheduler Control" card in Settings page with pause/resume button
- **API endpoint for scheduler control**: New `PUT /api/v1/status/scheduler` endpoint to programmatically control the scheduler

### Improvements
- **Interactive header badge**: Scheduler badge now shows clickable states (Active/Paused/Stopped) with color indicators
- **Visual feedback**: Clear visual states for scheduler status with pause icon when paused

## 3.5.3

### Improvements
- **Comprehensive in-app documentation**: Completely rewritten Docs page with detailed guides for all features
- **Home Assistant automation examples**: Multiple ready-to-use YAML snippets for notifications, outage detection, daily reports
- **Dashboard card examples**: Copy-paste YAML for entities, gauges, and history graphs
- **Troubleshooting guide**: Detailed solutions for common problems including manual hostname discovery
- **Speed test education**: Explanation of WiFi vs Ethernet, factors affecting results, QoS requirements
- **Data usage guide**: Table showing test intervals vs. monthly data consumption

## 3.5.2

### Bug Fixes
- **Fix Auto-Discovery**: Integration now automatically detects the Gonzales addon regardless of installation method (local folder, GitHub repository with hash prefix like `546fc077_gonzales`)
- **Improved addon detection**: Queries Supervisor API to find ALL addons with "gonzales" in the name, not just predefined slugs
- **No manual hostname needed**: Users no longer need to manually find and enter the addon hostname

## 3.5.1

### Improvements
- **Scheduler status in header**: The header now displays the next scheduled test time (e.g., "45 min", "1h 30m") with a clock icon when the scheduler is active
- **Read-only indicator**: Scheduler status is displayed for information only and cannot be toggled from the header

## 3.5.0

### New Features - AI Agent Integration

**MCP Server (Model Context Protocol)**
- Native integration with Claude Desktop and other MCP-compatible AI tools
- New `gonzales-mcp` command to start the MCP server
- Available tools: get_latest_speedtest, run_speedtest, get_statistics, get_connection_status, get_outages, get_isp_score, get_summary

**Summary API Endpoint**
- New `GET /api/v1/summary` endpoint designed for AI agents and LLMs
- Returns structured status with alerts and recommendations
- Supports JSON and Markdown output formats
- Human-readable summary text for quick understanding

**AGENTS.md Documentation**
- Machine-readable documentation for AI agents
- Quick reference for common operations
- Integration examples for Python and curl
- Interpretation guide for results

**Improved OpenAPI Documentation**
- Enhanced endpoint descriptions with use cases
- Added examples to response schemas
- Better parameter documentation

### CLI Improvements
- Consistent `--json` output across all CLI commands
- Unified JSON response format with success/data/timestamp

## 3.0.1

### Bug Fixes
- **Fix Statistics page crash**: Resolved React error #310 by correcting hook ordering
- **Remove floating action button (FAB)**: Removed the quick actions FAB for cleaner UI
- **Fix config endpoint**: Added missing data_retention_days and webhook_url fields
- **Fix database migration**: Added migration for connection_type and mac_address columns
- **Fix missing dependency**: Added aiohttp for webhook service

## 3.0.0

### Major Release - Architecture & Accessibility

**Clean Architecture**
- Complete domain layer implementation with Domain-Driven Design principles
- Pure Python entities (Measurement, Outage, SpeedtestServer, Config)
- Immutable value objects (Speed, Duration, Percentage, NetworkMetrics, ThresholdConfig)
- Domain events for decoupled communication
- Repository pattern with protocol-based interfaces
- Application layer with use cases (RunSpeedtest, GetStatistics, ManageConfig, ExportData)

**Security Enhancements**
- **Rate Limiting**: Token bucket algorithm with per-IP limiting (100 requests/minute)
- HTTP 429 response when rate limit exceeded
- Configurable burst capacity and rate

**Accessibility (WCAG 2.1 AA)**
- ARIA landmarks and roles throughout the UI
- Skip-to-content link for keyboard navigation
- Screen reader announcements via live regions
- Full keyboard navigation support
- Focus-visible indicators on all interactive elements
- prefers-reduced-motion support for animations

**UI Improvements**
- Toast notification system with success/error/warning/info variants
- Enhanced glass button component with loading states
- Improved semantic HTML structure

## 2.1.2

### Fixes
- **Fix discovery parsing**: Integration now correctly parses `HassioServiceInfo` from Home Assistant Supervisor discovery messages. Previously the integration crashed because it expected a plain dict instead of the proper `HassioServiceInfo` type.
- **Better discovery UX**: Discovery confirmation dialog now shows the detected hostname and port (e.g., "Addon found at **546fc077-gonzales:8099**")
- **Auto-update existing config**: When discovery is received with new connection info, existing configuration is automatically updated instead of being ignored.
- **Connection validation**: Validates connection before creating config entry, shows error if addon is unreachable.

## 2.1.1

### Fixes
- **Fix discovery hostname**: Convert underscores to dashes in hostname for DNS compatibility (e.g., `546fc077_gonzales` → `546fc077-gonzales`)
- **Better logging**: Log discovery registration status for debugging

## 2.1.0

### New Features
- **Smart Addon Detection**: Automatically discovers the Gonzales addon regardless of installation method (local or repository). Queries Supervisor API to find addon by name pattern, then uses hostname or IP for reliable connection.
- **Data Usage Estimation**: Settings page now displays estimated daily data consumption based on test interval and speed thresholds. Helps users understand bandwidth impact before configuring.
- **Optimized Default Settings**: Test interval now defaults to 60 minutes (was 30) for better balance between monitoring frequency and resource usage.

### Improvements
- **Universal Compatibility**: Works with addons installed via local folder (`local_gonzales`) or GitHub repository URL (hash-based slugs like `a0d7b954_gonzales`)
- **Smarter Connection Logic**: Tries multiple connection methods - DNS hostname with dashes, original hostname, then IP address as fallback

## 2.0.13

### Fixes
- **Fix connection issue**: Changed default host from 'localhost' to 'local-gonzales' (Docker networking)
- **Improved addon detection**: Added Supervisor API detection method
- **Better hostname handling**: Try multiple hostname patterns for addon discovery

## 2.0.12

### Improvements
- **Better setup UI**: Added helpful descriptions for each configuration field
- **German translation**: Integration UI now available in German
- **Clearer error messages**: Improved error text when connection fails

## 2.0.11

### Improvements
- **Add integration icon**: Integration now shows proper icon in HA UI
- **Fix default port**: Changed default port from 8000 to 8099
- **Auto-detect addon**: Integration automatically detects running addon and configures itself
- **Documentation**: Added restart requirement notice after addon installation

## 2.0.10

### Features
- **Auto-install integration**: The addon now automatically installs the Gonzales custom integration to Home Assistant's `custom_components` folder on startup
- Eliminates need for manual HACS installation or file copying
- Integration version is auto-updated when addon updates

## 2.0.9

### Fixes
- **Fix infinite reload loop**: Update FRONTEND_VERSION constant to match backend version

## 2.0.8

### Fixes
- **Fix Docker build error**: Remove invalid `readme = "README.md"` reference from pyproject.toml that caused hatchling metadata generation to fail

## 2.0.7

### Fixes
- **Fix Docker build error**: Add missing build dependencies (gcc, musl-dev, libffi-dev) for Python package compilation

## 2.0.6

### Changes
- Prepare for HACS submission
- Add GitHub Actions workflows for validation and releases
- Add info.md for HACS integration info panel

## 2.0.5

### Improvements
- **Mobile navigation**: Redesigned bottom nav with 4 main items + "More" sheet
- **SEO optimization**: Meta tags, Open Graph, Twitter Cards
- **LLM-friendly docs**: Added llms.txt files

## 2.0.4

### Features
- **In-app documentation**: Built-in Docs page accessible from sidebar
- **Legal compliance**: Added Ookla trademark notices and EULA links

## 2.0.0 - 2.0.3

### Major Release - New Features
- **ISP Contract Validation**: Professional PDF reports with SLA compliance, violations, timestamps
- **Network Topology Analysis**: Traceroute with hop-by-hop latency analysis
- **QoS Tests**: Application-specific quality tests (Netflix 4K, Zoom, Gaming, VPN)
- **Clean Architecture**: Domain/Application/Infrastructure layer separation
- **New pages**: QoS Tests, Network Topology
- **Dashboard**: Quick QoS status display
- **Settings**: Contract details configuration (ISP name, speeds)

## 1.2.6

### Fixes
- **Fix 403 Forbidden**: Web UI now works correctly in Home Assistant - requests through Ingress proxy are trusted when API key is configured

## 1.2.5

### Features
- **Percentage-based tolerance**: Configure acceptable speed as percentage of subscribed speed (e.g., 85% of 1000 Mbps = 850 Mbps minimum)
- **Time-of-day statistics**: New 5-period analysis (Morning, Midday, Afternoon, Evening, Night) with compliance tracking
- **Date range presets**: Quick filter buttons (Today, This Week, This Month, This Year) in History and Statistics pages
- **Delete all measurements**: New action with confirmation modal (type "DELETE" to confirm)
- **Version display**: Version shown in terminal startup log and Settings > System Status
- **Export branding**: Gonzales branding in CSV header and PDF footer

### Fixes
- **Auto-reload on update**: Frontend automatically reloads when version mismatch detected (no manual cache clear needed)
- **Docker cache invalidation**: Assets now update correctly when addon version changes (BUILD_VERSION cache buster)
- **CSP font fix**: Export page fonts now load correctly (`font-src 'self' data:`)

## 1.2.4

- Fix: Blank Ingress page — React Router now detects `/api/hassio_ingress/<token>/` path and sets basename correctly
- Improve: Startup message now says "Access via Home Assistant sidebar" instead of misleading URL hint

## 1.2.3

- Fix: Restore `init: false` (S6-overlay v3 must be PID 1, Docker tini must not be injected)
- Fix: Rewrite AppArmor profile based on official HA template (`file,` blanket rule + deny /proc writes)

## 1.2.2

- Fix: Add AppArmor capabilities (`setuid`, `setgid`, `kill`, `signal`) required by `s6-overlay-suexec`
- Fix: Allow S6-overlay writable paths and broader executable access in AppArmor profile

## 1.2.1

- Fix: Allow S6-overlay init (remove `init: false` that caused `/init` Permission denied)
- Fix: Update AppArmor profile to permit S6-overlay, `/bin/`, `/opt/gonzales/` paths

## 1.2.0

- Fix: Remove pre-built image reference (local build until GHCR is set up)
- Fix: Use `--target` instead of `--prefix` for reliable Python package installation on Alpine

## 1.1.0

- Multi-stage Docker build (git removed from runtime image)
- S6-overlay v3 compatibility (`init: false`, `with-contenv bashio` shebang)
- Auto-generated persistent API key (`/data/.api_key`)
- API key passed to integration via Supervisor discovery
- Ookla EULA auto-acceptance on first start
- Input validation for `test_interval_minutes`
- AppArmor security profile
- Watchdog health check for auto-restart
- jemalloc memory allocator for ARM efficiency
- OCI + HA container labels
- Pre-built multi-arch images on GHCR (aarch64 + amd64)
- `.dockerignore` to reduce build context
- Version display on startup
- CI/CD: GitHub Actions for multi-arch builds + lint

## 1.0.0

- Initial release
- Gonzales backend with automated speed testing
- Web dashboard via Home Assistant Ingress
- Auto-discovery for gonzales-ha integration
- Persistent storage for database and configuration
- Support for aarch64 and amd64 architectures
