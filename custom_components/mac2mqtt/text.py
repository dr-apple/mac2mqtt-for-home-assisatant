"""Text entities for mac2mqtt commands."""

from __future__ import annotations

import json

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
            Mac2MQTTCommandText(
                coordinator,
                "notification",
                "Foreground Notification",
                "mdi:message-badge-outline",
                key="notification_foreground",
                foreground_notification=True,
            ),
            Mac2MQTTCommandText(
                coordinator,
                "screensaver",
                "Screensaver",
                "mdi:television-ambient-light",
            ),
            Mac2MQTTCommandText(
                coordinator,
                "app",
                "Open App",
                "mdi:application-import",
            ),
            Mac2MQTTCommandText(
                coordinator,
                "open_app",
                "Open App Alias",
                "mdi:application-import",
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
        key: str | None = None,
        foreground_notification: bool = False,
    ) -> None:
        super().__init__(coordinator, key or command, name)
        self._command = command
        self._attr_icon = icon
        self._attr_native_value = None
        self._foreground_notification = foreground_notification

    async def async_set_value(self, value: str) -> None:
        """Publish the entered text."""
        self._attr_native_value = value
        payload = value
        if self._foreground_notification:
            payload = json.dumps({"message": value, "foreground": True})
        await self.coordinator.async_publish_command(self._command, payload)
        self.async_write_ha_state()
