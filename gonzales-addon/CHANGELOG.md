# Changelog

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
