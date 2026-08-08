"""Button entities for mac2mqtt actions."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up button entities."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            Mac2MQTTCommandButton(coordinator, "sleep", "Sleep", "mdi:power-sleep"),
            Mac2MQTTCommandButton(coordinator, "shutdown", "Shutdown", "mdi:power"),
            Mac2MQTTCommandButton(coordinator, "displaysleep", "Display Sleep", "mdi:monitor-off"),
            Mac2MQTTCommandButton(coordinator, "displaywake", "Display Wake", "mdi:monitor"),
            Mac2MQTTCommandButton(
                coordinator,
                "screensaver",
                "Start Screensaver",
                "mdi:television-ambient-light",
                "start",
                "screensaver_start",
            ),
            Mac2MQTTCommandButton(
                coordinator,
                "play_pause",
                "Play Pause",
                "mdi:play-pause",
            ),
        ]
    )


class Mac2MQTTCommandButton(Mac2MQTTEntity, ButtonEntity):
    """Button that publishes one command payload."""

    def __init__(
        self,
        coordinator: Mac2MQTTCoordinator,
        command: str,
        name: str,
        icon: str,
        payload: str | None = None,
        key: str | None = None,
    ) -> None:
        super().__init__(coordinator, key or command, name)
        self._command = command
        self._payload = payload or command
        self._attr_icon = icon

    async def async_press(self) -> None:
        """Publish command."""
        await self.coordinator.async_publish_command(self._command, self._payload)
