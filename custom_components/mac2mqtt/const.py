"""Constants for the mac2mqtt integration."""

from homeassistant.const import Platform

DOMAIN = "mac2mqtt"

CONF_BASE_TOPIC = "base_topic"
CONF_COMPUTER_NAME = "computer_name"

DEFAULT_BASE_TOPIC = "mac2mqtt"

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.SELECT,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.BUTTON,
    Platform.TEXT,
]


def topic_prefix(base_topic: str, computer_name: str) -> str:
    """Build MQTT topic prefix."""
    return f"{base_topic}/{computer_name}"
