"""Switch entities for mac2mqtt."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up switches."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            Mac2MQTTMuteSwitch(coordinator),
            Mac2MQTTDisplayPowerSwitch(coordinator),
        ]
    )


class Mac2MQTTMuteSwitch(Mac2MQTTEntity, SwitchEntity):
    """Mute switch."""

    _attr_icon = "mdi:volume-mute"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "mute", "Mute")

    @property
    def is_on(self) -> bool | None:
        """Return mute state."""
        value = self.coordinator.data.get("mute")
        return bool(value) if value is not None else None

    async def async_turn_on(self, **kwargs: object) -> None:
        """Mute output."""
        await self.coordinator.async_publish_command("mute", "true")

    async def async_turn_off(self, **kwargs: object) -> None:
        """Unmute output."""
        await self.coordinator.async_publish_command("mute", "false")


class Mac2MQTTDisplayPowerSwitch(Mac2MQTTEntity, SwitchEntity):
    """Display power switch."""

    _attr_icon = "mdi:monitor"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "display_power", "Display Power")

    @property
    def is_on(self) -> bool | None:
        """Return true when at least one display is active."""
        value = self.coordinator.data.get("display")
        return bool(value) if value is not None else None

    async def async_turn_on(self, **kwargs: object) -> None:
        """Wake display output."""
        await self.coordinator.async_publish_command("display", "wake")

    async def async_turn_off(self, **kwargs: object) -> None:
        """Sleep display output."""
        await self.coordinator.async_publish_command("display", "sleep")
