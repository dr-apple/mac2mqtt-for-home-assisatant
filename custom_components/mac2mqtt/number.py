"""Number entities for mac2mqtt."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import Mac2MQTTCoordinator
from .entity import Mac2MQTTEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up number entities."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Mac2MQTTVolumeNumber(coordinator)])


class Mac2MQTTVolumeNumber(Mac2MQTTEntity, NumberEntity):
    """Volume control entity."""

    _attr_icon = "mdi:volume-high"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = "slider"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "volume", "Volume")

    @property
    def native_value(self) -> float | None:
        """Return current volume."""
        value = self.coordinator.data.get("volume")
        return float(value) if value is not None else None

    async def async_set_native_value(self, value: float) -> None:
        """Set volume."""
        clamped = max(0, min(100, int(value)))
        await self.coordinator.async_publish_command("volume", str(clamped))
