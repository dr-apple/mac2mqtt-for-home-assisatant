"""Select entities for mac2mqtt."""

from __future__ import annotations

from typing import Any

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
    async_add_entities([Mac2MQTTAppSelect(coordinator)])


class Mac2MQTTAppSelect(Mac2MQTTEntity, SelectEntity):
    """Select an installed app to launch or activate."""

    _attr_icon = "mdi:application"

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "app_select", "App")
        self._attr_current_option = None

    @property
    def options(self) -> list[str]:
        """Return installed app names."""
        apps = self.coordinator.data.get("apps")
        if not isinstance(apps, list):
            return []

        names: list[str] = []
        seen: set[str] = set()
        for app in apps:
            name = _app_name(app)
            if name is None or name in seen:
                continue
            names.append(name)
            seen.add(name)
        return names

    async def async_select_option(self, option: str) -> None:
        """Launch or activate the selected app."""
        self._attr_current_option = option
        await self.coordinator.async_publish_command("app", option)
        self.async_write_ha_state()


def _app_name(app: Any) -> str | None:
    """Return an app name from the published app object."""
    if not isinstance(app, dict):
        return None

    name = app.get("name")
    return name if isinstance(name, str) and name else None
