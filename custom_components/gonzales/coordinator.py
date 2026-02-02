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
