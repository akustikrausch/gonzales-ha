"""Diagnostics support for Gonzales integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant

from .const import CONF_API_KEY
from .coordinator import GonzalesConfigEntry

# Keys to redact from diagnostics output
TO_REDACT = {
    CONF_API_KEY,
    "internal_ip",
    "external_ip",
    "mac_address",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: GonzalesConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry.

    Provides diagnostic information useful for troubleshooting
    without exposing sensitive data like API keys or IP addresses.
    """
    coordinator = entry.runtime_data

    # Redact sensitive data from coordinator data
    redacted_data = async_redact_data(coordinator.data, TO_REDACT)

    return {
        "entry": {
            "title": entry.title,
            "entry_id": entry.entry_id,
            "host": entry.data.get(CONF_HOST),
            "port": entry.data.get(CONF_PORT),
            "has_api_key": bool(entry.data.get(CONF_API_KEY)),
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "last_exception": str(coordinator.last_exception)
            if coordinator.last_exception
            else None,
            "update_interval": str(coordinator.update_interval),
        },
        "data": redacted_data,
    }
