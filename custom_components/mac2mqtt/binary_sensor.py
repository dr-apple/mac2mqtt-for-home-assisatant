"""Binary sensors for mac2mqtt."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import Mac2MQTTCoordinator
from .entity import Mac2MQTTEntity

ALIVE_DESCRIPTION = BinarySensorEntityDescription(
    key="alive",
    name="Alive",
    icon="mdi:laptop",
    entity_category=EntityCategory.DIAGNOSTIC,
)

DISPLAY_DESCRIPTION = BinarySensorEntityDescription(
    key="display",
    name="Display",
    icon="mdi:monitor",
)

LOCKED_DESCRIPTION = BinarySensorEntityDescription(
    key="locked",
    name="Locked",
    icon="mdi:lock",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            Mac2MQTTAliveEntity(coordinator),
            Mac2MQTTDisplayEntity(coordinator),
            Mac2MQTTLockedEntity(coordinator),
        ]
    )


class Mac2MQTTAliveEntity(Mac2MQTTEntity, BinarySensorEntity):
    """Alive status entity."""

    entity_description = ALIVE_DESCRIPTION

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "alive", "Alive")

    @property
    def is_on(self) -> bool | None:
        """Return true when daemon is connected to MQTT."""
        value = self.coordinator.data.get("alive")
        return bool(value) if value is not None else None


class Mac2MQTTDisplayEntity(Mac2MQTTEntity, BinarySensorEntity):
    """Display status entity."""

    entity_description = DISPLAY_DESCRIPTION

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "display", "Display")

    @property
    def is_on(self) -> bool | None:
        """Return true when at least one display is active."""
        value = self.coordinator.data.get("display")
        return bool(value) if value is not None else None


class Mac2MQTTLockedEntity(Mac2MQTTEntity, BinarySensorEntity):
    """Session lock status entity."""

    entity_description = LOCKED_DESCRIPTION

    def __init__(self, coordinator: Mac2MQTTCoordinator) -> None:
        super().__init__(coordinator, "locked", "Locked")

    @property
    def is_on(self) -> bool | None:
        """Return true when the user session is locked."""
        value = self.coordinator.data.get("locked")
        return bool(value) if value is not None else None
