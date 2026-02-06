"""Sensor platform for Gonzales."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    PERCENTAGE,
    UnitOfDataRate,
    UnitOfInformation,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GonzalesConfigEntry, GonzalesCoordinator


@dataclass(frozen=True, kw_only=True)
class GonzalesSensorEntityDescription(SensorEntityDescription):
    """Describe a Gonzales sensor."""

    value_fn: Callable[[dict[str, Any]], float | int | str | None]


def _measurement(data: dict[str, Any], key: str) -> float | None:
    """Extract a value from the measurement data."""
    m = data.get("measurement")
    if m is None:
        return None
    return m.get(key)


def _status(data: dict[str, Any], key: str) -> Any:
    """Extract a value from the status data."""
    s = data.get("status")
    if s is None:
        return None
    return s.get(key)


def _scheduler(data: dict[str, Any], key: str) -> Any:
    """Extract a value from the scheduler data."""
    s = data.get("status")
    if s is None:
        return None
    sched = s.get("scheduler")
    if sched is None:
        return None
    return sched.get(key)


def _smart_scheduler(data: dict[str, Any], key: str) -> Any:
    """Extract a value from the smart scheduler data."""
    ss = data.get("smart_scheduler")
    if ss is None:
        return None
    return ss.get(key)


def _root_cause(data: dict[str, Any], key: str) -> Any:
    """Extract a value from the root cause analysis data."""
    rc = data.get("root_cause")
    if rc is None:
        return None
    return rc.get(key)


def _layer_score(data: dict[str, Any], layer: str) -> float | None:
    """Extract a layer score from root cause analysis."""
    rc = data.get("root_cause")
    if rc is None:
        return None
    scores = rc.get("layer_scores")
    if scores is None:
        return None
    return scores.get(layer)


MAIN_SENSORS: tuple[GonzalesSensorEntityDescription, ...] = (
    GonzalesSensorEntityDescription(
        key="download_speed",
        translation_key="download_speed",
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        suggested_display_precision=1,
        value_fn=lambda data: _measurement(data, "download_mbps"),
    ),
    GonzalesSensorEntityDescription(
        key="upload_speed",
        translation_key="upload_speed",
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        suggested_display_precision=1,
        value_fn=lambda data: _measurement(data, "upload_mbps"),
    ),
    GonzalesSensorEntityDescription(
        key="ping_latency",
        translation_key="ping_latency",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        suggested_display_precision=1,
        value_fn=lambda data: _measurement(data, "ping_latency_ms"),
    ),
    GonzalesSensorEntityDescription(
        key="ping_jitter",
        translation_key="ping_jitter",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        suggested_display_precision=1,
        value_fn=lambda data: _measurement(data, "ping_jitter_ms"),
    ),
    GonzalesSensorEntityDescription(
        key="packet_loss",
        translation_key="packet_loss",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
        value_fn=lambda data: _measurement(data, "packet_loss_pct"),
    ),
    GonzalesSensorEntityDescription(
        key="last_test_time",
        translation_key="last_test_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: _status(data, "last_test_time"),
    ),
    GonzalesSensorEntityDescription(
        key="isp_score",
        translation_key="isp_score",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:speedometer",
        value_fn=lambda data: (
            data["isp_score"]["composite"]
            if data.get("isp_score")
            else None
        ),
    ),
)

DIAGNOSTIC_SENSORS: tuple[GonzalesSensorEntityDescription, ...] = (
    GonzalesSensorEntityDescription(
        key="scheduler_running",
        translation_key="scheduler_running",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:clock-check-outline",
        value_fn=lambda data: (
            "running" if _scheduler(data, "running") else "stopped"
        ),
    ),
    GonzalesSensorEntityDescription(
        key="test_in_progress",
        translation_key="test_in_progress",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:progress-clock",
        value_fn=lambda data: (
            "yes" if _scheduler(data, "test_in_progress") else "no"
        ),
    ),
    GonzalesSensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        device_class=SensorDeviceClass.DURATION,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        suggested_display_precision=0,
        value_fn=lambda data: _status(data, "uptime_seconds"),
    ),
    GonzalesSensorEntityDescription(
        key="total_measurements",
        translation_key="total_measurements",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
        value_fn=lambda data: _status(data, "total_measurements"),
    ),
    GonzalesSensorEntityDescription(
        key="db_size",
        translation_key="db_size",
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_display_precision=0,
        value_fn=lambda data: _status(data, "db_size_bytes"),
    ),
)

# Smart Scheduler sensors (v3.7.0+)
SMART_SCHEDULER_SENSORS: tuple[GonzalesSensorEntityDescription, ...] = (
    GonzalesSensorEntityDescription(
        key="smart_scheduler_phase",
        translation_key="smart_scheduler_phase",
        icon="mdi:auto-fix",
        value_fn=lambda data: _smart_scheduler(data, "phase"),
    ),
    GonzalesSensorEntityDescription(
        key="smart_scheduler_stability",
        translation_key="smart_scheduler_stability",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=0,
        icon="mdi:signal-cellular-3",
        value_fn=lambda data: (
            round(_smart_scheduler(data, "stability_score") * 100)
            if _smart_scheduler(data, "stability_score") is not None
            else None
        ),
    ),
    GonzalesSensorEntityDescription(
        key="smart_scheduler_interval",
        translation_key="smart_scheduler_interval",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        suggested_display_precision=0,
        icon="mdi:timer-outline",
        value_fn=lambda data: _smart_scheduler(data, "current_interval_minutes"),
    ),
    GonzalesSensorEntityDescription(
        key="smart_scheduler_data_used",
        translation_key="smart_scheduler_data_used",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=0,
        icon="mdi:database",
        value_fn=lambda data: (
            round(100 - (_smart_scheduler(data, "data_budget_remaining_pct") or 100))
            if _smart_scheduler(data, "enabled")
            else None
        ),
    ),
)

# Root-Cause Analysis sensors (v3.7.0+)
ROOT_CAUSE_SENSORS: tuple[GonzalesSensorEntityDescription, ...] = (
    GonzalesSensorEntityDescription(
        key="network_health_score",
        translation_key="network_health_score",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:heart-pulse",
        value_fn=lambda data: _root_cause(data, "network_health_score"),
    ),
    GonzalesSensorEntityDescription(
        key="primary_issue",
        translation_key="primary_issue",
        icon="mdi:alert-circle-outline",
        value_fn=lambda data: (
            _root_cause(data, "primary_cause").get("category")
            if _root_cause(data, "primary_cause")
            else "none"
        ),
    ),
    GonzalesSensorEntityDescription(
        key="dns_health",
        translation_key="dns_health",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:dns",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: _layer_score(data, "dns_score"),
    ),
    GonzalesSensorEntityDescription(
        key="local_network_health",
        translation_key="local_network_health",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:lan",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: _layer_score(data, "local_network_score"),
    ),
    GonzalesSensorEntityDescription(
        key="isp_backbone_health",
        translation_key="isp_backbone_health",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:server-network",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: _layer_score(data, "isp_backbone_score"),
    ),
    GonzalesSensorEntityDescription(
        key="isp_lastmile_health",
        translation_key="isp_lastmile_health",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="points",
        suggested_display_precision=0,
        icon="mdi:home-city-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: _layer_score(data, "isp_lastmile_score"),
    ),
)

ALL_SENSORS = MAIN_SENSORS + DIAGNOSTIC_SENSORS + SMART_SCHEDULER_SENSORS + ROOT_CAUSE_SENSORS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GonzalesConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gonzales sensors from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities(
        GonzalesSensor(coordinator, description)
        for description in ALL_SENSORS
    )


class GonzalesSensor(CoordinatorEntity[GonzalesCoordinator], SensorEntity):
    """Representation of a Gonzales sensor."""

    entity_description: GonzalesSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GonzalesCoordinator,
        entity_description: GonzalesSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Gonzales",
            manufacturer="Gonzales",
            model="Internet Speed Monitor",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for measurement sensors."""
        if self.coordinator.data is None:
            return None
        if self.entity_description.key == "isp_score":
            isp = self.coordinator.data.get("isp_score")
            if isp and "breakdown" in isp:
                return {
                    "grade": isp.get("grade"),
                    "speed_score": isp["breakdown"].get("speed_score"),
                    "reliability_score": isp["breakdown"].get(
                        "reliability_score"
                    ),
                    "latency_score": isp["breakdown"].get("latency_score"),
                    "consistency_score": isp["breakdown"].get(
                        "consistency_score"
                    ),
                }
        if self.entity_description.key == "download_speed":
            m = self.coordinator.data.get("measurement")
            if m:
                return {
                    "server": m.get("server_name"),
                    "isp": m.get("isp"),
                }
        if self.entity_description.key == "smart_scheduler_phase":
            ss = self.coordinator.data.get("smart_scheduler")
            if ss:
                return {
                    "enabled": ss.get("enabled"),
                    "base_interval_minutes": ss.get("base_interval_minutes"),
                    "last_decision_reason": ss.get("last_decision_reason"),
                }
        if self.entity_description.key == "network_health_score":
            rc = self.coordinator.data.get("root_cause")
            if rc:
                primary = rc.get("primary_cause")
                return {
                    "primary_issue_category": primary.get("category") if primary else None,
                    "primary_issue_severity": primary.get("severity") if primary else None,
                    "primary_issue_confidence": primary.get("confidence") if primary else None,
                    "issues_count": len(rc.get("secondary_causes", [])) + (1 if primary else 0),
                    "recommendations_count": len(rc.get("recommendations", [])),
                }
        if self.entity_description.key == "primary_issue":
            rc = self.coordinator.data.get("root_cause")
            if rc and rc.get("primary_cause"):
                cause = rc["primary_cause"]
                return {
                    "severity": cause.get("severity"),
                    "confidence": cause.get("confidence"),
                    "description": cause.get("description"),
                    "occurrence_count": cause.get("occurrence_count"),
                }
        return None
