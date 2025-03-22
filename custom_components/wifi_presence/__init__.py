from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "wifi_presence"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WiFi Presence from a config entry."""
    
    # Store entry in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry

    # Ensure `nmap_tracker` is set up correctly
    await hass.config_entries.async_forward_entry_setup(entry, "device_tracker")

    # Setup binary_sensor
    await hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")

    return True