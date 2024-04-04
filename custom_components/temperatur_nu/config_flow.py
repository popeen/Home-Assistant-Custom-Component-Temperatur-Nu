"""Config flow for temperatur_nu integration."""

from __future__ import annotations

import logging
from typing import Any

from temperaturnu import TemperaturNu
import voluptuous as vol

from homeassistant import exceptions
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_API_CLI_ID, CONF_STATION, DOMAIN

_LOGGER = logging.getLogger(__name__)
STEP_USER_DATA_SCHEMA = vol.Schema({vol.Optional(CONF_STATION): str})
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    try:
        tempNu = TemperaturNu(CONF_API_CLI_ID)
        isValid = await tempNu.is_valid_id_async(data[CONF_STATION])
        if not isValid:
            raise InvalidStationID
        station = await tempNu.get_name_async(data[CONF_STATION])
    except InvalidStationID:
        _LOGGER.exception("InvalidStationID exception")
        raise InvalidStationID from NameError
    return station


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for temperatur_nu."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                title = await validate_input(self.hass, user_input)
            except InvalidStationID:
                _LOGGER.exception("InvalidStationID exception")
                errors["base"] = "invalid_station_id"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class InvalidStationID(exceptions.HomeAssistantError):
    """Error to indicate the ID was invalid."""
