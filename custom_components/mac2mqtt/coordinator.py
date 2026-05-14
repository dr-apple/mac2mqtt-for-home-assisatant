"""Coordinator for mac2mqtt MQTT subscriptions."""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import topic_prefix

_LOGGER = logging.getLogger(__name__)


class Mac2MQTTCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Store current topic states and handle MQTT traffic."""

    def __init__(self, hass: HomeAssistant, base_topic: str, computer_name: str) -> None:
        super().__init__(hass, _LOGGER, name="mac2mqtt")
        self._hass = hass
        self.base_topic = base_topic
        self.computer_name = computer_name
        self.prefix = topic_prefix(base_topic, computer_name)
        self._unsubscribers: list[Callable[[], None]] = []
        self.data = {
            "alive": None,
            "battery": None,
            "display": None,
            "display_changed_at": None,
            "locked": None,
            "volume": None,
            "mute": None,
            "power_source": None,
        }

    async def async_start(self) -> None:
        """Subscribe to status topics."""
        await self._subscribe("alive")
        await self._subscribe("battery")
        await self._subscribe("display")
        await self._subscribe("display_changed_at")
        await self._subscribe("locked")
        await self._subscribe("volume")
        await self._subscribe("mute")
        await self._subscribe("power_source")

    async def async_stop(self) -> None:
        """Unsubscribe from all topics."""
        while self._unsubscribers:
            unsub = self._unsubscribers.pop()
            unsub()

    async def _subscribe(self, metric: str) -> None:
        topic = f"{self.prefix}/status/{metric}"

        @callback
        def _message_received(msg: mqtt.ReceiveMessage) -> None:
            payload = msg.payload
            parsed: Any = payload
            if metric in ("alive", "display", "locked", "mute"):
                parsed = payload.lower() == "true"
            elif metric in ("battery", "volume"):
                try:
                    parsed = int(payload)
                except ValueError:
                    parsed = None
            elif metric in (
                "display_changed_at",
                "power_source",
            ):
                parsed = payload or None

            self.data[metric] = parsed
            self.async_set_updated_data(dict(self.data))

        unsub = await mqtt.async_subscribe(
            self._hass,
            topic,
            _message_received,
            qos=1,
            encoding="utf-8",
        )
        self._unsubscribers.append(unsub)
        _LOGGER.debug("Subscribed to %s", topic)

    async def async_publish_command(self, command: str, payload: str) -> None:
        """Publish command payload."""
        topic = f"{self.prefix}/command/{command}"
        await mqtt.async_publish(self._hass, topic, payload, qos=1, retain=False)
