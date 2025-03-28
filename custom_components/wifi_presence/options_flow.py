import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import async_get

DOMAIN = "wifi_presence"

class WifiPresenceOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for WiFi Presence."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Step to select device_tracker entities."""
        return await self.async_step_select_devices()

    async def async_step_select_devices(self, user_input=None):
        """Allow users to pick device_tracker entities with friendly names."""
        errors = {}

        # Get entity registry
        entity_registry = async_get(self.hass)

        # Fetch all device_tracker entities
        device_trackers = {
            entity_id: entity_registry.entities[entity_id].name or entity_id
            for entity_id in entity_registry.entities
            if entity_id.startswith("device_tracker.")
        }

        if not device_trackers:
            errors["base"] = "no_devices_found"

        if user_input is not None:
            return self.async_create_entry(title="", data={"selected_devices": user_input["selected_devices"]})

        return self.async_show_form(
            step_id="select_devices",
            data_schema=vol.Schema({
                vol.Required(
                    "selected_devices", 
                    default=self.config_entry.options.get("selected_devices", []) if self.config_entry.options.get("selected_devices") is not None else []
                ): vol.In(device_trackers),  # Show friendly names
            }),
            errors=errors
        )