from datetime import timedelta
import datetime
import logging
from typing import Optional
from homeassistant.const import CONF_ALLOWLIST_EXTERNAL_URLS

from homeassistant.helpers import entity_platform
from voluptuous.schema_builder import Required
from custom_components.custom_calendar.entity import CustomEntity
from homeassistant.components.calendar import PLATFORM_SCHEMA, CalendarEventDevice
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

_LOGGER: logging.Logger = logging.getLogger(__name__)

# Optional fields have a string type to allow empty values
SCHEMA_SERVICE_ADD_EVENT = {
    vol.Required("event"): cv.string,
    vol.Required("start"): cv.date,
    vol.Optional("start_time"): cv.string,
    vol.Optional("end"): cv.string,
    vol.Optional("end_time"): cv.string,
}


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        name="add_event",
        schema=SCHEMA_SERVICE_ADD_EVENT,
        func="add_event",
    )
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([CustomCalendar(coordinator, entry, hass)])


class CustomCalendar(CustomEntity, CalendarEventDevice):
    def __init__(self, coordinator, config_entry, hass):
        super().__init__(coordinator, config_entry, hass)
        async_track_time_interval(
            hass=hass, action=self.manage_notifications, interval=timedelta(seconds=10)
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.config_entry.data.get("name")

    @property
    def event(self):
        """Return the next upcoming event."""
        #  not implemented
        return None

    async def manage_notifications(self, calltime: datetime):
        event_data = {"device_id": "calendar." + self.name, "type": "reminder"}
        self.hass.bus.async_fire(DOMAIN + "_event", event_data)
        await self.coordinator.api.get_next_event(self.unique_id)
        # _LOGGER.warning(calltime)

    async def async_get_events(self, hass, start_date, end_date):
        events = self.coordinator.data["events"]
        return events

    async def add_event(self, event, start, start_time="", end="", end_time=""):
        await self.coordinator.api.add_event(
            event, start.strftime("%Y-%m-%d"), start_time, end, end_time
        )
        await self.coordinator.async_request_refresh()
