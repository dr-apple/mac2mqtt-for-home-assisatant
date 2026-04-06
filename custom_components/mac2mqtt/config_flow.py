"""Config flow for mac2mqtt."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import CONF_BASE_TOPIC, CONF_COMPUTER_NAME, DEFAULT_BASE_TOPIC, DOMAIN


class Mac2MQTTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for mac2mqtt."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        """Handle first step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            computer_name = user_input[CONF_COMPUTER_NAME].strip()
            base_topic = user_input[CONF_BASE_TOPIC].strip()
            if not computer_name or not base_topic:
                errors["base"] = "required"
            else:
                unique_id = f"{base_topic}:{computer_name}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_NAME: user_input[CONF_NAME].strip(),
                        CONF_COMPUTER_NAME: computer_name,
                        CONF_BASE_TOPIC: base_topic,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Mac2MQTT"): str,
                vol.Required(CONF_COMPUTER_NAME): str,
                vol.Required(CONF_BASE_TOPIC, default=DEFAULT_BASE_TOPIC): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return Mac2MQTTOptionsFlow(config_entry)


class Mac2MQTTOptionsFlow(config_entries.OptionsFlow):
    """Handle options for mac2mqtt."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME,
                    default=self._entry.options.get(
                        CONF_NAME, self._entry.data.get(CONF_NAME, "Mac2MQTT")
                    ),
                ): str,
                vol.Required(
                    CONF_COMPUTER_NAME,
                    default=self._entry.options.get(
                        CONF_COMPUTER_NAME, self._entry.data[CONF_COMPUTER_NAME]
                    ),
                ): str,
                vol.Required(
                    CONF_BASE_TOPIC,
                    default=self._entry.options.get(
                        CONF_BASE_TOPIC, self._entry.data[CONF_BASE_TOPIC]
                    ),
                ): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
