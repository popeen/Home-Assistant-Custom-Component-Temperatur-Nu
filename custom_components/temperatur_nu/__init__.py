"""Temperatur.nu"""
from __future__ import annotations
from . import common
from temperaturnu import TemperaturNu

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

PLATFORMS: list[str] = ["sensor"]

ATTR_HASH = "hash"
ATTR_SENSOR = "sensor"
HASS = None

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if common.CONF_REGISTER in entry.data:
        name = common.CONF_REGISTER
    else:
        name = entry.data[common.CONF_STATION]
    hass.data.setdefault(common.DOMAIN, {})[entry.entry_id] = name
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    HASS = hass

    def send_temperature(call):
        """Handle the service call."""
        token = call.data.get(ATTR_HASH)
        sensor = call.data.get(ATTR_SENSOR)
        temp = HASS.states.get(sensor).state
        tempNu = TemperaturNu(common.CONF_API_CLI_ID)
        tempNu.set_temp(token, temp)
    
    hass.services.register(common.DOMAIN, "send_temperature", send_temperature)
    
    return True