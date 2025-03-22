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
                return self.async_create_entry(title="WiFi Presence", data=self.devices)

        return self.async_create_entry(
            title="WiFi Presence",
            data={},
            options={"known_devices": self.devices}  # Store known devices in options
        )
    
    async def async_step_options(self, user_input=None):
        """Redirect to options flow."""
        return self.async_create_entry(title="", data=self.config_entry.options)