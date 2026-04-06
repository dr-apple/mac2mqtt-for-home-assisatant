"""Sensors for mac2mqtt."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import Mac2MQTTCoordinator
from .entity import Mac2MQTTEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Mac2MQTTBatteryEntity(coordinator)])


class Mac2MQTTBatteryEntity(Mac2MQTTEntity, SensorEntity):
    """Battery percentage sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:battery"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "battery", "Battery")

    @property
    def native_value(self) -> int | None:
        """Return battery state."""
        value = self.coordinator.data.get("battery")
        return int(value) if value is not None else None
