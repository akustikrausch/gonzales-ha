"""Binary sensor platform for Gonzales."""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GonzalesConfigEntry, GonzalesCoordinator


BINARY_SENSOR_DESCRIPTION = BinarySensorEntityDescription(
    key="internet_outage",
    translation_key="internet_outage",
    device_class=BinarySensorDeviceClass.PROBLEM,
    entity_category=None,  # Main sensor, not diagnostic
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GonzalesConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gonzales binary sensors from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([GonzalesOutageSensor(coordinator)])


class GonzalesOutageSensor(CoordinatorEntity[GonzalesCoordinator], BinarySensorEntity):
    """Binary sensor for internet outage detection.

    ON = Outage active (problem detected)
    OFF = Internet working normally
    """

    entity_description = BINARY_SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: GonzalesCoordinator) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_internet_outage"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Gonzales",
            manufacturer="Gonzales",
            model="Internet Speed Monitor",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def is_on(self) -> bool | None:
        """Return True if outage is active (problem detected)."""
        if self.coordinator.data is None:
            return None
        status = self.coordinator.data.get("status")
        if status is None:
            return None
        outage = status.get("outage")
        if outage is None:
            return False
        return outage.get("outage_active", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the outage sensor."""
        if self.coordinator.data is None:
            return None
        status = self.coordinator.data.get("status")
        if status is None:
            return None
        outage = status.get("outage")
        if outage is None:
            return None
        return {
            "consecutive_failures": outage.get("consecutive_failures", 0),
            "outage_started_at": outage.get("outage_started_at"),
            "last_failure_message": outage.get("last_failure_message", ""),
        }
