"""Config flow for Gonzales integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.components.hassio import HassioServiceInfo
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_API_KEY, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# Default addon port (must match config.yaml)
ADDON_PORT = 8099

# Fallback hostnames if Supervisor API is unavailable
FALLBACK_HOSTNAMES = [
    "local-gonzales",
    "local_gonzales",
    "gonzales",
]


class GonzalesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gonzales."""

    VERSION = 1

    _hassio_discovery: HassioServiceInfo | None = None
    _addon_detected: bool = False
    _addon_host: str | None = None
    _discovered_host: str = DEFAULT_HOST
    _discovered_port: int = DEFAULT_PORT
    _discovered_api_key: str = ""

    async def async_step_hassio(
        self, discovery_info: HassioServiceInfo
    ) -> ConfigFlowResult:
        """Handle Supervisor add-on discovery."""
        _LOGGER.info("Received hassio discovery: slug=%s, config=%s", discovery_info.slug, discovery_info.config)

        # Extract connection info from discovery config
        self._discovered_host = discovery_info.config.get("host", DEFAULT_HOST)
        self._discovered_port = discovery_info.config.get("port", DEFAULT_PORT)
        self._discovered_api_key = discovery_info.config.get("api_key", "")

        # Use addon slug as stable unique ID
        await self.async_set_unique_id(f"hassio_{discovery_info.slug}")
        self._abort_if_unique_id_configured(
            updates={
                CONF_HOST: self._discovered_host,
                CONF_PORT: self._discovered_port,
                CONF_API_KEY: self._discovered_api_key,
            }
        )

        # Store discovery info for confirmation step
        self._hassio_discovery = discovery_info

        # Always show confirmation - never auto-create (best practice)
        return await self.async_step_hassio_confirm()

    async def async_step_hassio_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm Supervisor add-on discovery."""
        if user_input is not None:
            # Validate connection before creating entry
            if not await self._validate_connection(
                self._discovered_host, self._discovered_port, self._discovered_api_key
            ):
                return self.async_show_form(
                    step_id="hassio_confirm",
                    errors={"base": "cannot_connect"},
                    description_placeholders={
                        "host": self._discovered_host,
                        "port": str(self._discovered_port),
                    },
                )

            return self.async_create_entry(
                title="Gonzales (Add-on)",
                data={
                    CONF_HOST: self._discovered_host,
                    CONF_PORT: self._discovered_port,
                    CONF_API_KEY: self._discovered_api_key,
                    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                },
            )

        return self.async_show_form(
            step_id="hassio_confirm",
            description_placeholders={
                "host": self._discovered_host,
                "port": str(self._discovered_port),
            },
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

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
        """Detect addon via Home Assistant Supervisor component.

        Uses the hassio component's addon info if available.
        """
        try:
            # Check if hassio component is loaded
            if "hassio" not in self.hass.config.components:
                _LOGGER.debug("Hassio component not loaded, skipping Supervisor detection")
                return None

            # Get addon info via hassio component
            hassio = self.hass.components.hassio

            # Try to get addons info
            if hasattr(hassio, "async_get_addon_info"):
                # Try common gonzales addon slugs
                for slug in ["local_gonzales", "gonzales"]:
                    try:
                        addon_info = await hassio.async_get_addon_info(self.hass, slug)
                        if addon_info and addon_info.get("state") == "started":
                            hostname = addon_info.get("hostname")
                            ip_address = addon_info.get("ip_address")
                            _LOGGER.info("Found Gonzales addon: hostname=%s, ip=%s", hostname, ip_address)

                            # Try hostname with dashes first
                            if hostname:
                                dns_hostname = hostname.replace("_", "-")
                                if await self._validate_connection(dns_hostname, ADDON_PORT, ""):
                                    return {"host": dns_hostname, "port": ADDON_PORT, "api_key": ""}
                                if await self._validate_connection(hostname, ADDON_PORT, ""):
                                    return {"host": hostname, "port": ADDON_PORT, "api_key": ""}

                            # Fall back to IP
                            if ip_address and await self._validate_connection(ip_address, ADDON_PORT, ""):
                                return {"host": ip_address, "port": ADDON_PORT, "api_key": ""}
                    except Exception:
                        continue

            _LOGGER.debug("Could not detect Gonzales addon via Supervisor")

        except Exception as err:
            _LOGGER.debug("Error during Supervisor detection: %s", err)

        return None

    async def _detect_via_hostnames(self) -> dict[str, Any] | None:
        """Try to detect addon by testing known hostnames (fallback method)."""
        session = async_get_clientsession(self.hass)

        for hostname in FALLBACK_HOSTNAMES:
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
