"""The mac2mqtt integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_BASE_TOPIC, CONF_COMPUTER_NAME, DOMAIN, PLATFORMS
from .coordinator import Mac2MQTTCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up mac2mqtt from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    base_topic = entry.options.get(CONF_BASE_TOPIC, entry.data[CONF_BASE_TOPIC])
    computer_name = entry.options.get(CONF_COMPUTER_NAME, entry.data[CONF_COMPUTER_NAME])

    coordinator = Mac2MQTTCoordinator(hass, base_topic, computer_name)
    await coordinator.async_start()

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
