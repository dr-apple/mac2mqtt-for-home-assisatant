"""Select entities for mac2mqtt."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
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
    """Set up select entities."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            Mac2MQTTCommandSelect(
                coordinator,
                "app_select",
                "App",
                "app",
                "app_options",
                "mdi:application",
            ),
            Mac2MQTTCommandSelect(
                coordinator,
                "screensaver_select",
                "Screensaver",
                "screensaver",
                "screensaver_options",
                "mdi:monitor-screenshot",
            ),
        ]
    )


class Mac2MQTTCommandSelect(Mac2MQTTEntity, SelectEntity):
    """Select an option and publish it as a command payload."""

    def __init__(
        self,
        coordinator: Mac2MQTTCoordinator,
        key: str,
        name: str,
        command: str,
        options_key: str,
        icon: str,
    ) -> None:
        super().__init__(coordinator, key, name)
        self._command = command
        self._options_key = options_key
        self._attr_icon = icon
        self._attr_current_option = None

    @property
    def options(self) -> list[str]:
        """Return options published by the Mac app."""
        options = self.coordinator.data.get(self._options_key)
        return options if isinstance(options, list) else []

    async def async_select_option(self, option: str) -> None:
        """Publish the selected option."""
        self._attr_current_option = option
        await self.coordinator.async_publish_command(self._command, option)
        self.async_write_ha_state()
