"""The Gonzales integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import GonzalesConfigEntry, GonzalesCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]

SERVICE_RUN_SPEEDTEST = "run_speedtest"
SERVICE_SET_INTERVAL = "set_interval"
ATTR_ENTRY_ID = "entry_id"
ATTR_INTERVAL = "interval"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GonzalesConfigEntry,
) -> bool:
    """Set up Gonzales from a config entry."""
    coordinator = GonzalesCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services (only once, on first entry)
    if not hass.services.has_service(DOMAIN, SERVICE_RUN_SPEEDTEST):
        async def handle_run_speedtest(call: ServiceCall) -> None:
            """Handle the run_speedtest service call."""
            entry_id = call.data.get(ATTR_ENTRY_ID)

            # Get all config entries for this domain
            entries = hass.config_entries.async_entries(DOMAIN)

            if entry_id:
                # Run for specific entry
                for config_entry in entries:
                    if config_entry.entry_id == entry_id:
                        coord: GonzalesCoordinator = config_entry.runtime_data
                        await coord.async_trigger_speedtest()
                        return
            else:
                # Run for all entries
                for config_entry in entries:
                    coord: GonzalesCoordinator = config_entry.runtime_data
                    await coord.async_trigger_speedtest()

        hass.services.async_register(
            DOMAIN,
            SERVICE_RUN_SPEEDTEST,
            handle_run_speedtest,
            schema=vol.Schema({
                vol.Optional(ATTR_ENTRY_ID): cv.string,
            }),
        )

    if not hass.services.has_service(DOMAIN, SERVICE_SET_INTERVAL):
        async def handle_set_interval(call: ServiceCall) -> None:
            """Handle the set_interval service call."""
            entry_id = call.data.get(ATTR_ENTRY_ID)
            interval = call.data[ATTR_INTERVAL]

            # Get all config entries for this domain
            entries = hass.config_entries.async_entries(DOMAIN)

            if entry_id:
                # Set for specific entry
                for config_entry in entries:
                    if config_entry.entry_id == entry_id:
                        coord: GonzalesCoordinator = config_entry.runtime_data
                        await coord.async_set_interval(interval)
                        return
            else:
                # Set for all entries
                for config_entry in entries:
                    coord: GonzalesCoordinator = config_entry.runtime_data
                    await coord.async_set_interval(interval)

        hass.services.async_register(
            DOMAIN,
            SERVICE_SET_INTERVAL,
            handle_set_interval,
            schema=vol.Schema({
                vol.Required(ATTR_INTERVAL): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=1440)
                ),
                vol.Optional(ATTR_ENTRY_ID): cv.string,
            }),
        )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: GonzalesConfigEntry,
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Unregister services if this is the last entry for the domain
    remaining = hass.config_entries.async_entries(DOMAIN)
    if not [e for e in remaining if e.entry_id != entry.entry_id]:
        hass.services.async_remove(DOMAIN, SERVICE_RUN_SPEEDTEST)
        hass.services.async_remove(DOMAIN, SERVICE_SET_INTERVAL)

    return unload_ok
