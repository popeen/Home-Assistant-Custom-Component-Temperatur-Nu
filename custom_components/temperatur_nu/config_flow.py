"""Temperatur.nu"""
from __future__ import annotations
from . import common
from typing import Any
from temperaturnu import TemperaturNu

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

import asyncio
import voluptuous as vol

SCHEMA= vol.Schema(
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
            tempNu = TemperaturNu(common.CONF_API_CLI_ID)
            station = await tempNu.get_name_async(data[common.CONF_STATION])
            isValid = await tempNu.is_valid_id_async(data[common.CONF_STATION])
            if not isValid:
                raise InvalidStationID
    except InvalidStationID:
        common._LOGGER.exception("InvalidStationID exception")
        raise InvalidStationID
    except Exception:
        common._LOGGER.exception("Unexpected exception")
    return station


class ConfigFlow(config_entries.ConfigFlow, domain=common.DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            
            try:
                title = await validate_input(self.hass, user_input)
                if title == common.CONF_REGISTER:
                    title = "Register service"
                return self.async_create_entry(title=title, data=user_input)
            except InvalidStationID:
                common._LOGGER.exception("InvalidStationID exception")
                errors["base"] = "invalid_station_id"

        return self.async_show_form(
            step_id="user", data_schema=SCHEMA, errors=errors
        )

class InvalidStationID(exceptions.HomeAssistantError):
    """Error to indicate the address was invalid."""