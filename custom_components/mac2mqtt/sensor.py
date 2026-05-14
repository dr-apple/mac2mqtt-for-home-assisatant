"""Sensors for mac2mqtt."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

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
    async_add_entities(
        [
            Mac2MQTTBatteryEntity(coordinator),
            Mac2MQTTDisplayChangedAtEntity(coordinator),
            Mac2MQTTPowerSourceEntity(coordinator),
        ]
    )


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


class Mac2MQTTDisplayChangedAtEntity(Mac2MQTTEntity, SensorEntity):
    """Last display status change timestamp sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-outline"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "display_changed_at", "Display Changed At")

    @property
    def native_value(self) -> datetime | None:
        """Return the timestamp of the last display status change."""
        value = self.coordinator.data.get("display_changed_at")
        if not value:
            return None

        return dt_util.parse_datetime(value)


class Mac2MQTTPowerSourceEntity(Mac2MQTTEntity, SensorEntity):
    """Current Mac power source sensor."""

    _attr_icon = "mdi:power-plug-battery"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "power_source", "Power Source")

    @property
    def native_value(self) -> str | None:
        """Return the current Mac power source."""
        return self.coordinator.data.get("power_source")
