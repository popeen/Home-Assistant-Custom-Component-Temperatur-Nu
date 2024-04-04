"""The temperatur_nu integration"""

from __future__ import annotations

from temperaturnu import TemperaturNu

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_API_CLI_ID, CONF_STATION, DOMAIN, SRV_ATTR_HASH, SRV_ATTR_SENSOR

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up temperatur_nu from a config entry."""

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data[CONF_STATION]

    def send_temperature(call):
        """Handle the service call."""
        token = call.data.get(SRV_ATTR_HASH)
        sensor = call.data.get(SRV_ATTR_SENSOR)
        temp = hass.states.get(sensor).state
        tempNu = TemperaturNu(CONF_API_CLI_ID)
        tempNu.set_temp(token, temp)

    hass.services.async_register(DOMAIN, "send_temperature", send_temperature)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
