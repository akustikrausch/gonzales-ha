#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
# shellcheck disable=SC1091,SC2155
set -euo pipefail

# --- Read and validate configuration ---
readonly TEST_INTERVAL=$(bashio::config 'test_interval_minutes')
readonly DL_THRESHOLD=$(bashio::config 'download_threshold_mbps')
readonly UL_THRESHOLD=$(bashio::config 'upload_threshold_mbps')
readonly SERVER_ID=$(bashio::config 'preferred_server_id')
readonly LOG_LEVEL=$(bashio::config 'log_level')

if [[ "${TEST_INTERVAL}" -lt 1 ]] || [[ "${TEST_INTERVAL}" -gt 1440 ]]; then
    bashio::log.error "test_interval_minutes out of range (1-1440): ${TEST_INTERVAL}"
    bashio::exit.nok
fi

# --- API key: generate once, persist in /data ---
readonly API_KEY_FILE="/data/.api_key"
if [[ -f "${API_KEY_FILE}" ]]; then
    GONZALES_API_KEY=$(cat "${API_KEY_FILE}")
else
    GONZALES_API_KEY=$(head -c 32 /dev/urandom | base64 | tr -d '/+=' | head -c 48)
    echo -n "${GONZALES_API_KEY}" > "${API_KEY_FILE}"
    chmod 600 "${API_KEY_FILE}"
    bashio::log.info "Generated new API key"
fi

# --- Accept Ookla EULA once ---
if [[ ! -f "/data/.speedtest_eula_accepted" ]]; then
    bashio::log.info "Accepting Ookla Speedtest CLI license..."
    speedtest --accept-license --accept-gdpr --format=json > /dev/null 2>&1 || true
    touch /data/.speedtest_eula_accepted
fi

# --- Export environment for Gonzales ---
export GONZALES_HOST="0.0.0.0"
export GONZALES_PORT=8099
export GONZALES_DB_PATH="/data/gonzales.db"
export GONZALES_CONFIG_PATH="/data/config.json"
export GONZALES_HA_ADDON=true
export GONZALES_API_KEY="${GONZALES_API_KEY}"
export GONZALES_TEST_INTERVAL_MINUTES="${TEST_INTERVAL}"
export GONZALES_DOWNLOAD_THRESHOLD_MBPS="${DL_THRESHOLD}"
export GONZALES_UPLOAD_THRESHOLD_MBPS="${UL_THRESHOLD}"
export GONZALES_PREFERRED_SERVER_ID="${SERVER_ID}"
export GONZALES_LOG_LEVEL="${LOG_LEVEL}"

# --- Register discovery (with API key) ---
if bashio::supervisor.ping 2>/dev/null; then
    payload="{\"service\":\"gonzales\",\"config\":{\"host\":\"$(hostname)\",\"port\":8099,\"api_key\":\"${GONZALES_API_KEY}\"}}"
    curl -s -X POST \
        -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "${payload}" \
        http://supervisor/discovery || bashio::log.warning "Discovery registration failed"
fi

# --- Print version and start ---
VERSION=$(python3 -c "from gonzales import __version__; print(__version__)" 2>/dev/null || echo "unknown")
bashio::log.info "Starting Gonzales Speed Monitor v${VERSION}"
bashio::log.info "Test interval: ${TEST_INTERVAL}min | Log level: ${LOG_LEVEL}"

exec python3 -m gonzales
