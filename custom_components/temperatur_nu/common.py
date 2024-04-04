"""Temperatur.nu"""
import urllib.request, hashlib, logging

DOMAIN = "temperatur_nu"

CONF_STATION = "station"
CONF_REGISTER = "register"
CONF_API_CLI_ID = "popeen_hass_custom_component"
_LOGGER = logging.getLogger(__name__)