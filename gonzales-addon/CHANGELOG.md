# Changelog

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
