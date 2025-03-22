from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.discovery import async_load_platform

DOMAIN = "wifi_presence"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WiFi Presence from a config entry."""
    
    # Ensure `nmap_tracker` is loaded
    hass.async_create_task(
        async_load_platform(hass, "device_tracker", "nmap_tracker", {
            "hosts": "192.168.1.0/24",
            "interval_seconds": 30,
            "consider_home": 180,
            "home_interval": 10,
            "new_device_defaults": {"track_new_devices": False}
        }, entry)
    )

    # Setup binary_sensor
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    )

    return True