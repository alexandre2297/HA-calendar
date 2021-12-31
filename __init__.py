from datetime import timedelta
import datetime
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.event
from custom_components.custom_calendar.api import CalendarApiClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)
_SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup(hass, config):
    """Not used (use this custom calendar by yaml is not allowed """
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    client = CalendarApiClient(entry.entry_id)

    coordinator = CalendarDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "calendar"))

    return True


class CalendarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: CalendarApiClient) -> None:
        """Initialize."""
        self.api = client
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=_SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.api.async_get_data()
        except Exception as exception:
            raise UpdateFailed() from exception