from __future__ import annotations
from . import common
from typing import Any

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

import asyncio
import voluptuous as vol


DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(common.CONF_STATION): str,
        vol.Optional(common.CONF_REGISTER): bool
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input."""    
    try:
        if common.CONF_REGISTER in data:
            station = common.CONF_REGISTER
        else:
            #TODO, Add validation
            station = data[common.CONF_STATION]
    except Exception:  # pylint: disable=broad-except
        station = None
    return station


class ConfigFlow(config_entries.ConfigFlow, domain=common.DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                if info == common.CONF_REGISTER:
                    info = "Register services"
                return self.async_create_entry(title=info, data=user_input)
            except Exception:  # pylint: disable=broad-except
                common._LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )