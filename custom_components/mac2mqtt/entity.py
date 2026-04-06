"""Entity helpers for mac2mqtt."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import Mac2MQTTCoordinator


class Mac2MQTTEntity(CoordinatorEntity[Mac2MQTTCoordinator]):
    """Base entity for mac2mqtt."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: Mac2MQTTCoordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.base_topic}_{coordinator.computer_name}_{key}"
        self._attr_device_info = {
            "identifiers": {("mac2mqtt", f"{coordinator.base_topic}_{coordinator.computer_name}")},
            "name": coordinator.computer_name,
            "manufacturer": "mac2mqtt",
            "model": "macOS Host",
        }
