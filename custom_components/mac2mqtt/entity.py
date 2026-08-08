"""Entity helpers for mac2mqtt."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import Mac2MQTTCoordinator


class Mac2MQTTEntity(CoordinatorEntity[Mac2MQTTCoordinator]):
    """Base entity for mac2mqtt."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: Mac2MQTTCoordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry_id)},
            name=coordinator.computer_name,
            manufacturer="mac2mqtt",
            model="macOS Host",
        )
