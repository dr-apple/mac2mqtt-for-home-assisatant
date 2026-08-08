"""The mac2mqtt integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import CONF_BASE_TOPIC, CONF_COMPUTER_NAME, DOMAIN, PLATFORMS
from .coordinator import Mac2MQTTCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up mac2mqtt from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    base_topic = entry.options.get(CONF_BASE_TOPIC, entry.data[CONF_BASE_TOPIC])
    computer_name = entry.options.get(CONF_COMPUTER_NAME, entry.data[CONF_COMPUTER_NAME])

    coordinator = Mac2MQTTCoordinator(
        hass,
        entry.entry_id,
        base_topic,
        computer_name,
    )
    await coordinator.async_start()
    await _async_migrate_registry_entries(hass, entry)

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: Mac2MQTTCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_stop()
    return unload_ok


async def _async_migrate_registry_entries(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Keep entity IDs stable while scoping registry IDs to the config entry."""
    unique_id_prefix = f"{entry.entry_id}_"
    legacy_prefixes = {
        f"{entry.data[CONF_BASE_TOPIC]}_{entry.data[CONF_COMPUTER_NAME]}_",
        (
            f"{entry.options.get(CONF_BASE_TOPIC, entry.data[CONF_BASE_TOPIC])}_"
            f"{entry.options.get(CONF_COMPUTER_NAME, entry.data[CONF_COMPUTER_NAME])}_"
        ),
    }

    def migrate_entity(entity_entry: er.RegistryEntry) -> dict[str, str] | None:
        if entity_entry.unique_id.startswith(unique_id_prefix):
            return None
        for legacy_prefix in legacy_prefixes:
            if entity_entry.unique_id.startswith(legacy_prefix):
                suffix = entity_entry.unique_id.removeprefix(legacy_prefix)
                return {"new_unique_id": f"{unique_id_prefix}{suffix}"}
        return None

    await er.async_migrate_entries(hass, entry.entry_id, migrate_entity)

    device_registry = dr.async_get(hass)
    for legacy_prefix in legacy_prefixes:
        legacy_identifier = (DOMAIN, legacy_prefix.removesuffix("_"))
        if (
            device_entry := device_registry.async_get_device(identifiers={legacy_identifier})
        ) and device_entry.config_entry_id == entry.entry_id:
            device_registry.async_update_device(
                device_entry.id,
                new_identifiers={(DOMAIN, entry.entry_id)},
            )
            break
