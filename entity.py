"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, VERSION, MANUFACTURER


class CustomEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry, hass):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.hass = hass

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.config_entry.data.get("name"),
            "model": VERSION,
            "manufacturer": MANUFACTURER,
        }