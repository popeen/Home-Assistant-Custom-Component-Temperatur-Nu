"""Temperatur.nu"""
import requests

DOMAIN = "temperatur_nu"

ATTR_HASH = "hash"
ATTR_SENSOR = "sensor"
HASS = None

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    HASS = hass

    def send_temperature(call):
        """Handle the service call."""
        token = call.data.get(ATTR_HASH)
        sensor = call.data.get(ATTR_SENSOR)
        temp = HASS.states.get(sensor).state
        requests.get(url="http://www.temperatur.nu/rapportera.php?hash=" + token + "&t=" + str(temp))
        
    hass.services.register(DOMAIN, "send_temperature", send_temperature)
    
    return True