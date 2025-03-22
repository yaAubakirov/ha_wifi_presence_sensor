import logging
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "wifi_presence"
_LOGGER = logging.getLogger(__name__)

# Schema for user input (MAC addresses)
DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required("device_name"): str,
        vol.Required("mac_address"): str,
    }
)

class WifiPresenceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for WiFi Presence."""

    def __init__(self):
        self.devices = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            device_name = user_input["device_name"]
            mac_address = user_input["mac_address"]

            if mac_address in self.devices.values():
                errors["base"] = "duplicate_mac"
            else:
                self.devices[device_name] = mac_address
                return self.async_create_entry(title="WiFi Presence", data={"known_devices": self.devices})

        return self.async_show_form(
            step_id="user",
            data_schema=DEVICE_SCHEMA,
            errors=errors
        )

    async def async_step_options(self, user_input=None):
        """Handle the options flow for modifying known devices."""
        if user_input is not None:
            return self.async_create_entry(title="", data={"known_devices": user_input})

        options_schema = vol.Schema(
            {vol.Optional(name, default=mac): str for name, mac in self.devices.items()}
        )

        return self.async_show_form(
            step_id="options",
            data_schema=options_schema
        )