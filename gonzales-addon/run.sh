#!/usr/bin/with-bashio

export GONZALES_HOST="0.0.0.0"
export GONZALES_PORT=8099
export GONZALES_DB_PATH="/data/gonzales.db"
export GONZALES_CONFIG_PATH="/data/config.json"
export GONZALES_HA_ADDON=true
export GONZALES_TEST_INTERVAL_MINUTES=$(bashio::config 'test_interval_minutes')
export GONZALES_DOWNLOAD_THRESHOLD_MBPS=$(bashio::config 'download_threshold_mbps')
export GONZALES_UPLOAD_THRESHOLD_MBPS=$(bashio::config 'upload_threshold_mbps')
export GONZALES_PREFERRED_SERVER_ID=$(bashio::config 'preferred_server_id')
export GONZALES_LOG_LEVEL=$(bashio::config 'log_level')

# Register discovery so gonzales-ha integration detects the add-on automatically
curl -s -X POST -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"service":"gonzales","config":{"host":"'"$(hostname)"'","port":8099}}' \
  http://supervisor/discovery || true

bashio::log.info "Starting Gonzales Speed Monitor..."
exec python3 -m gonzales
