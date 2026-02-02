"""Config flow for Gonzales integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_API_KEY, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.Coerce(int),
        vol.Optional(CONF_API_KEY, default=""): str,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
    }
)


class GonzalesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gonzales."""

    VERSION = 1

    _hassio_discovery: dict[str, Any] | None = None

    async def async_step_hassio(
        self, discovery_info: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle Supervisor add-on discovery."""
        host = discovery_info["host"]
        port = discovery_info["port"]
        await self.async_set_unique_id(f"hassio_{host}:{port}")
        self._abort_if_unique_id_configured()
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

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

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
