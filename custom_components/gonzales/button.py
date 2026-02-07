"""Button platform for Gonzales."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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


class GonzalesSpeedTestButton(CoordinatorEntity[GonzalesCoordinator], ButtonEntity):
    """Button to trigger a speed test."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:speedometer"
    translation_key = "run_speed_test"

    def __init__(
        self,
        coordinator: GonzalesCoordinator,
        entry: GonzalesConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_run_speedtest"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gonzales",
            manufacturer="Gonzales",
            model="Internet Speed Monitor",
            entry_type=DeviceEntryType.SERVICE,
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_trigger_speedtest()
