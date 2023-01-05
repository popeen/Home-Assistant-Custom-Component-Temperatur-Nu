"""Platform for sensor integration."""
import requests
from datetime import timedelta

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

DOMAIN = "temperatur_nu"

CONF_NAME = "name"
CONF_LOCATION = "location"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_LOCATION): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None) -> None:
    """Set up the Temperatur.nu sensor platform."""
    add_entities([TemperaturNuSensor(config[CONF_NAME], config[CONF_LOCATION])])


class TemperaturNuSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, location):
        """Initialize the sensor."""
        
        self._attr_unique_id = f"{DOMAIN}_{location}"
        self._name = name
        self._location = location
        self._icon = "mdi:thermometer"
        self._state = self.get_temp()
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

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self) -> None:
        """Get the latest data and updates the states."""
        self._state = self.get_temp()

    def get_temp(self):
        return requests.get(url="http://api.temperatur.nu/tnu_1.17.php?p=" + self._location + "&cli=hass").json()['stations'][0]['temp']