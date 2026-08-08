"""Home Assistant 2026.8 compatibility tests."""

from unittest.mock import AsyncMock, patch

from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mac2mqtt.const import (
    CONF_BASE_TOPIC,
    CONF_COMPUTER_NAME,
    DOMAIN,
)
from custom_components.mac2mqtt.coordinator import Mac2MQTTCoordinator


def _entry() -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="Office Mac",
        unique_id="mac2mqtt:imac",
        data={
            CONF_NAME: "Office Mac",
            CONF_BASE_TOPIC: "mac2mqtt",
            CONF_COMPUTER_NAME: "imac",
        },
    )


async def test_setup_scopes_entities_and_device_to_entry(
    hass: HomeAssistant,
    enable_custom_integrations: None,
) -> None:
    """All registry identifiers remain stable across MQTT setting changes."""
    entry = _entry()
    entry.add_to_hass(hass)

    with (
        patch.object(Mac2MQTTCoordinator, "async_start", new=AsyncMock()),
        patch.object(Mac2MQTTCoordinator, "async_stop", new=AsyncMock()),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        entities = er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
        assert len(entities) == 23
        assert all(entity.unique_id.startswith(f"{entry.entry_id}_") for entity in entities)

        devices = dr.async_entries_for_config_entry(dr.async_get(hass), entry.entry_id)
        assert len(devices) == 1
        assert devices[0].identifiers == {(DOMAIN, entry.entry_id)}

        assert await hass.config_entries.async_unload(entry.entry_id)


async def test_legacy_registry_ids_migrate_without_entity_id_change(
    hass: HomeAssistant,
    enable_custom_integrations: None,
) -> None:
    """Legacy topic-based IDs are migrated without renaming the entity."""
    entry = _entry()
    entry.add_to_hass(hass)
    entity_registry = er.async_get(hass)
    legacy_entity = entity_registry.async_get_or_create(
        "binary_sensor",
        DOMAIN,
        "mac2mqtt_imac_alive",
        config_entry=entry,
        suggested_object_id="office_mac_alive",
    )
    device_registry = dr.async_get(hass)
    legacy_device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "mac2mqtt_imac")},
        name="iMac",
    )

    with patch.object(Mac2MQTTCoordinator, "async_start", new=AsyncMock()):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    migrated_entity = entity_registry.async_get(legacy_entity.entity_id)
    assert migrated_entity is not None
    assert migrated_entity.entity_id == legacy_entity.entity_id
    assert migrated_entity.unique_id == f"{entry.entry_id}_alive"

    migrated_device = device_registry.async_get(legacy_device.id)
    assert migrated_device is not None
    assert entry.entry_id in migrated_device.config_entries
    assert migrated_device.identifiers == {(DOMAIN, entry.entry_id)}
