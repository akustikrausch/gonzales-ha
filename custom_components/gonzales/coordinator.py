"""DataUpdateCoordinator for Gonzales."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, TypeAlias

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import CONF_API_KEY, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

GonzalesConfigEntry: TypeAlias = ConfigEntry


class GonzalesCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from the Gonzales API."""

    config_entry: GonzalesConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: GonzalesConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self._host = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]
        self._base_url = f"http://{self._host}:{self._port}/api/v1"
        api_key = config_entry.data.get(CONF_API_KEY, "")
        self._headers: dict[str, str] = {}
        if api_key:
            self._headers["X-API-Key"] = api_key
        scan_interval = config_entry.data.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Gonzales API.

        Polls three endpoints:
        - /measurements/latest for current speed test data
        - /status for system health and scheduler info
        - /statistics/enhanced for ISP score
        """
        session = async_get_clientsession(self.hass)
        data: dict[str, Any] = {
            "measurement": None,
            "status": None,
            "isp_score": None,
            "smart_scheduler": None,
            "root_cause": None,
        }

        try:
            # Fetch latest measurement
            async with session.get(
                f"{self._base_url}/measurements/latest",
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    if result is not None:
                        data["measurement"] = result

            # Fetch system status
            async with session.get(
                f"{self._base_url}/status",
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data["status"] = await resp.json()

            # Fetch ISP score from enhanced statistics
            async with session.get(
                f"{self._base_url}/statistics/enhanced",
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=20),
            ) as resp:
                if resp.status == 200:
                    stats = await resp.json()
                    if stats and stats.get("isp_score"):
                        data["isp_score"] = stats["isp_score"]

            # Fetch Smart Scheduler status (v3.7.0+)
            try:
                async with session.get(
                    f"{self._base_url}/smart-scheduler/status",
                    headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status == 200:
                        data["smart_scheduler"] = await resp.json()
            except aiohttp.ClientError:
                pass  # Smart scheduler may not be available on older versions

            # Fetch Root-Cause analysis (v3.7.0+)
            try:
                async with session.get(
                    f"{self._base_url}/root-cause/analysis?days=7",
                    headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 200:
                        data["root_cause"] = await resp.json()
            except aiohttp.ClientError:
                pass  # Root cause may not be available on older versions

        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Error communicating with Gonzales API: {err}"
            ) from err
        except TimeoutError as err:
            raise UpdateFailed(
                f"Timeout communicating with Gonzales API: {err}"
            ) from err

        if data["status"] is None and data["measurement"] is None:
            raise UpdateFailed("No data received from Gonzales API")

        return data

    async def async_trigger_speedtest(self) -> dict[str, Any] | None:
        """Trigger a speed test via the Gonzales API."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.post(
                f"{self._base_url}/speedtest/trigger",
                headers=self._headers,
                timeout=aiohttp.ClientTimeout(total=10),  # Short timeout - returns immediately
            ) as resp:
                if resp.status in (200, 202):  # 202 = Accepted (async)
                    result = await resp.json()
                    _LOGGER.info("Speed test triggered: %s", result.get("status", "started"))
                    # Don't refresh immediately - test runs in background
                    # The regular polling will pick up results
                    return result
                elif resp.status == 429:
                    _LOGGER.warning("Speed test rate limited, try again later")
                    return None
                elif resp.status == 503:
                    _LOGGER.warning("Speed test already in progress")
                    return None
                else:
                    _LOGGER.error("Failed to trigger speed test: %s", resp.status)
                    return None
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.error("Error triggering speed test: %s", err)
            return None

    async def async_set_interval(self, interval_minutes: int) -> bool:
        """Set the test interval via the Gonzales API.

        Args:
            interval_minutes: The test interval in minutes (1-1440).

        Returns:
            True if successful, False otherwise.
        """
        session = async_get_clientsession(self.hass)
        try:
            async with session.put(
                f"{self._base_url}/config",
                headers=self._headers,
                json={"test_interval_minutes": interval_minutes},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    _LOGGER.info(
                        "Set Gonzales test interval to %d minutes", interval_minutes
                    )
                    # Refresh data to get new config
                    await self.async_request_refresh()
                    return True
                else:
                    _LOGGER.error(
                        "Failed to set test interval: %s", resp.status
                    )
                    return False
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.error("Error setting test interval: %s", err)
            return False
