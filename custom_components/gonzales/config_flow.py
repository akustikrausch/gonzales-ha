"""Config flow for Gonzales integration."""
from __future__ import annotations

import logging
import os
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_API_KEY, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# Addon slug (must match config.yaml)
ADDON_SLUG = "local_gonzales"
ADDON_PORT = 8099

# Possible hostnames for the addon container (Docker networking)
# Home Assistant addons use hostname format: <slug> or addon_<slug>
ADDON_HOSTNAMES = [
    "local-gonzales",      # slug with dash
    "local_gonzales",      # slug with underscore
    "addon_local_gonzales",  # prefixed
    "gonzales",            # just the name
    "a]_gonzales",        # sometimes HA uses this
]


class GonzalesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gonzales."""

    VERSION = 1

    _hassio_discovery: dict[str, Any] | None = None
    _addon_detected: bool = False
    _addon_host: str | None = None
    _supervisor_available: bool = False

    async def async_step_hassio(
        self, discovery_info: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle Supervisor add-on discovery."""
        _LOGGER.info("Received hassio discovery: %s", discovery_info)
        host = discovery_info["host"]
        port = discovery_info["port"]
        api_key = discovery_info.get("api_key", "")

        await self.async_set_unique_id(f"hassio_{host}:{port}")
        self._abort_if_unique_id_configured()

        # Try to auto-configure if we can connect
        if await self._validate_connection(host, port, api_key):
            return self.async_create_entry(
                title="Gonzales (Add-on)",
                data={
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_API_KEY: api_key,
                    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                },
            )

        # Store discovery info and ask for confirmation
        self._hassio_discovery = discovery_info
        return await self.async_step_hassio_confirm()

    async def async_step_hassio_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm Supervisor add-on discovery."""
        if user_input is not None:
            assert self._hassio_discovery is not None
            host = self._hassio_discovery["host"]
            port = self._hassio_discovery["port"]
            api_key = self._hassio_discovery.get("api_key", "")
            return self.async_create_entry(
                title="Gonzales (Add-on)",
                data={
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_API_KEY: api_key,
                    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                },
            )
        return self.async_show_form(step_id="hassio_confirm")

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Check if running under Supervisor
        self._supervisor_available = os.environ.get("SUPERVISOR") is not None

        # Try to auto-detect addon on first load
        if user_input is None and not self._addon_detected:
            addon_info = await self._detect_addon()
            if addon_info:
                self._addon_detected = True
                self._addon_host = addon_info["host"]
                host = addon_info["host"]
                port = addon_info["port"]
                api_key = addon_info.get("api_key", "")

                await self.async_set_unique_id(f"addon_{host}:{port}")
                self._abort_if_unique_id_configured()

                # Auto-configure
                return self.async_create_entry(
                    title="Gonzales (Add-on)",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_API_KEY: api_key,
                        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                    },
                )

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            api_key = user_input.get(CONF_API_KEY, "")

            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured()

            if await self._validate_connection(host, port, api_key):
                return self.async_create_entry(
                    title=f"Gonzales ({host}:{port})",
                    data=user_input,
                )
            errors["base"] = "cannot_connect"

        # Determine best default host
        default_host = self._addon_host or DEFAULT_HOST

        # Build schema
        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=default_host): str,
                vol.Required(CONF_PORT, default=ADDON_PORT): vol.Coerce(int),
                vol.Optional(CONF_API_KEY, default=""): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def _detect_addon(self) -> dict[str, Any] | None:
        """Try to detect running Gonzales addon via multiple methods."""
        # Method 1: Query Supervisor API (most reliable)
        addon_info = await self._detect_via_supervisor()
        if addon_info:
            return addon_info

        # Method 2: Try known hostnames
        addon_info = await self._detect_via_hostnames()
        if addon_info:
            return addon_info

        return None

    async def _detect_via_supervisor(self) -> dict[str, Any] | None:
        """Detect addon via Home Assistant Supervisor API."""
        supervisor_token = os.environ.get("SUPERVISOR_TOKEN")
        if not supervisor_token:
            _LOGGER.debug("No SUPERVISOR_TOKEN, skipping Supervisor detection")
            return None

        session = async_get_clientsession(self.hass)

        try:
            # Check if gonzales addon is installed and running
            url = "http://supervisor/addons/local_gonzales/info"
            headers = {"Authorization": f"Bearer {supervisor_token}"}

            async with session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    addon_data = data.get("data", {})
                    state = addon_data.get("state")

                    if state == "started":
                        # Get the hostname from addon info
                        hostname = addon_data.get("hostname", "local-gonzales")
                        _LOGGER.info(
                            "Found running Gonzales addon via Supervisor: hostname=%s",
                            hostname
                        )

                        # Verify we can actually connect
                        if await self._validate_connection(hostname, ADDON_PORT, ""):
                            return {"host": hostname, "port": ADDON_PORT, "api_key": ""}

                        # Try with IP from network info
                        ip = addon_data.get("ip_address")
                        if ip and await self._validate_connection(ip, ADDON_PORT, ""):
                            return {"host": ip, "port": ADDON_PORT, "api_key": ""}

                    else:
                        _LOGGER.warning("Gonzales addon found but not running (state=%s)", state)

        except aiohttp.ClientError as err:
            _LOGGER.debug("Supervisor API error: %s", err)
        except Exception as err:
            _LOGGER.debug("Unexpected error querying Supervisor: %s", err)

        return None

    async def _detect_via_hostnames(self) -> dict[str, Any] | None:
        """Try to detect addon by testing known hostnames."""
        session = async_get_clientsession(self.hass)

        for hostname in ADDON_HOSTNAMES:
            try:
                url = f"http://{hostname}:{ADDON_PORT}/api/v1/status"
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=2)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "scheduler" in data:
                            _LOGGER.info("Detected Gonzales addon at %s:%s", hostname, ADDON_PORT)
                            return {"host": hostname, "port": ADDON_PORT, "api_key": ""}
            except (aiohttp.ClientError, TimeoutError):
                continue

        return None

    async def _validate_connection(
        self, host: str, port: int, api_key: str = ""
    ) -> bool:
        """Validate that we can connect to the Gonzales API."""
        url = f"http://{host}:{port}/api/v1/status"
        headers: dict[str, str] = {}
        if api_key:
            headers["X-API-Key"] = api_key
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return "scheduler" in data
                return False
        except (aiohttp.ClientError, TimeoutError):
            return False
