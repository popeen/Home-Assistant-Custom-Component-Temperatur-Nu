"""Sensor for temperatur_nu integration."""

from datetime import timedelta

from temperaturnu import TemperaturNu
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .const import CONF_API_CLI_ID, CONF_STATION, DOMAIN

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
SCAN_INTERVAL = timedelta(minutes=1)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_STATION): cv.string})


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup entity."""

    station = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([TemperaturNuSensor(station, station)], update_before_add=True)


class TemperaturNuSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, station) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{DOMAIN}_{station}"
        self._attr_attribution = "Data from Temperatur.nu"
        self._name = name
        self._station = station
        self._icon = "mdi:thermometer"
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Icon to use in the frontend."""
        return self._icon

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        tempNu = TemperaturNu(CONF_API_CLI_ID)
        self._state = await tempNu.get_temp_async(self._station)
