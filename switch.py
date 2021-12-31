import logging
from custom_components.custom_calendar.entity import CustomEntity
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([CustomSwitch(coordinator, entry)])


class CustomSwitch(CustomEntity, SwitchEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return self.config_entry.data.get("name") + "_" + "switch"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data["title"] == "on"

    async def async_turn_on(self, **kwargs):
        logging.error(self.config_entry.entry_id)
        await self.coordinator.api.set_title("on")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.set_title("off")
        await self.coordinator.async_request_refresh()
