import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN


class CalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        if info is not None:
            return self.async_create_entry(title=info["name"], data=info)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({vol.Required("name"): str})
        )
