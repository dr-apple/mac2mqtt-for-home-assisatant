"""Text entities for mac2mqtt commands."""

from __future__ import annotations

from homeassistant.components.text import TextEntity
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
    """Set up text entities."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            Mac2MQTTCommandText(coordinator, "say", "Say", "mdi:account-voice"),
            Mac2MQTTCommandText(
                coordinator,
                "notification",
                "Notification",
                "mdi:message-alert-outline",
            ),
        ]
    )


class Mac2MQTTCommandText(Mac2MQTTEntity, TextEntity):
    """Text entity that publishes its value as a command payload."""

    _attr_mode = "text"

    def __init__(
        self,
        coordinator: Mac2MQTTCoordinator,
        command: str,
        name: str,
        icon: str,
    ) -> None:
        super().__init__(coordinator, command, name)
        self._command = command
        self._attr_icon = icon
        self._attr_native_value = None

    async def async_set_value(self, value: str) -> None:
        """Publish the entered text."""
        self._attr_native_value = value
        await self.coordinator.async_publish_command(self._command, value)
        self.async_write_ha_state()
