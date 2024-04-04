"""Temperatur.nu"""
from . import common
from datetime import timedelta
from temperaturnu import TemperaturNu
import hashlib
import time
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
SCAN_INTERVAL = timedelta(minutes=1)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(common.CONF_STATION): cv.string
    }
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    session = async_get_clientsession(hass)
    station = hass.data[common.DOMAIN][config_entry.entry_id]
    
    #Don't add any entity if user checked only register service.
    if station != common.CONF_REGISTER:
        async_add_entities([TemperaturNuSensor(station, station)], update_before_add=True)
    else:
        return None

class TemperaturNuSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, station):
        """Initialize the sensor."""        
        self._attr_unique_id = f"{common.DOMAIN}_{station}"
        self._attr_attribution = "Data from Temperatur.nu"
        self._name = name
        self._station = station
        self._icon = "mdi:thermometer"
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        session = async_get_clientsession(self.hass)
        tempNu = TemperaturNu(common.CONF_API_CLI_ID)
        self._state = await tempNu.get_temp_async(self._station)
