from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import STATE_HOME
from homeassistant.helpers.entity_registry import async_get
from homeassistant.helpers.event import async_track_state_change
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "wifi_presence"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the WiFi Presence sensor based on selected device_tracker entities."""
    entity_registry = async_get(hass)

    # Map selected devices to friendly names
    selected_devices = config_entry.options.get("selected_devices", [])
    friendly_names = {
        entity: entity_registry.entities.get(entity).name or entity
        for entity in selected_devices
        if entity in entity_registry.entities
    }

    async_add_entities([WifiPresenceSensor(hass, config_entry, selected_devices, friendly_names)], True)

class WifiPresenceSensor(BinarySensorEntity):
    """WiFi Presence Sensor using selected device_tracker entities."""

    def __init__(self, hass, config_entry, selected_devices, friendly_names):
        self.hass = hass
        self.config_entry = config_entry  # Store config entry for reference
        self._attr_name = "WiFi Presence Sensor"
        self._attr_unique_id = f"wifi_presence_{config_entry.entry_id}"  # Ensure unique ID
        self._attr_device_class = "connectivity"
        self._is_on = False
        self.selected_devices = selected_devices
        self.friendly_names = friendly_names
        self._attr_extra_state_attributes = {"home_devices": []}

        # Track state changes of selected `device_tracker` entities
        async_track_state_change(hass, selected_devices, self.async_update)

    @property
    def is_on(self):
        return self._is_on

    async def async_update(self, entity_id=None, old_state=None, new_state=None):
        """Update sensor state based on selected device_tracker entities."""
        _LOGGER.info("Checking selected device_tracker status...")
        found_devices = [
            self.friendly_names[entity] for entity in self.selected_devices
            if entity in self.hass.states and self.hass.states.get(entity).state == STATE_HOME
        ]

        self._is_on = len(found_devices) > 0
        self._attr_extra_state_attributes["home_devices"] = found_devices  # Update UI attributes
        _LOGGER.info(f"Devices at home: {found_devices}")  # Logs friendly names
        self.async_write_ha_state()