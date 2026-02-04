"""Button platform for Gonzales."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import GonzalesConfigEntry, GonzalesCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GonzalesConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gonzales button entities."""
    coordinator: GonzalesCoordinator = entry.runtime_data
    async_add_entities([GonzalesSpeedTestButton(coordinator, entry)])


class GonzalesSpeedTestButton(ButtonEntity):
    """Button to trigger a speed test."""

    _attr_has_entity_name = True
    _attr_name = "Run Speed Test"
    _attr_icon = "mdi:speedometer"

    def __init__(
        self,
        coordinator: GonzalesCoordinator,
        entry: GonzalesConfigEntry,
    ) -> None:
        """Initialize the button."""
        self._coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_run_speedtest"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Gonzales",
            "manufacturer": "Gonzales",
            "model": "Internet Speed Monitor",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._coordinator.async_trigger_speedtest()
