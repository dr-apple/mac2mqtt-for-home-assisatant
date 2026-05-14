# Mac2MQTT HACS Integration

Custom Home Assistant integration for `mac2mqtt` / `mac2mqttd`.

## Features

- `binary_sensor`: Alive, Display
- `sensor`: Battery, Display Changed At
- `switch`: Mute, Display Power
- `number`: Volume (0-100)
- `button`: Sleep, Shutdown, Display Sleep

## MQTT topic mapping

Given:

- `base_topic = mac2mqtt`
- `computer_name = my-macbook`

The integration uses:

- Status subscribe:
  - `mac2mqtt/my-macbook/status/alive`
  - `mac2mqtt/my-macbook/status/battery`
  - `mac2mqtt/my-macbook/status/display`
  - `mac2mqtt/my-macbook/status/display_changed_at`
  - `mac2mqtt/my-macbook/status/volume`
  - `mac2mqtt/my-macbook/status/mute`
- Command publish:
  - `mac2mqtt/my-macbook/command/volume`
  - `mac2mqtt/my-macbook/command/mute`
  - `mac2mqtt/my-macbook/command/sleep`
  - `mac2mqtt/my-macbook/command/shutdown`
  - `mac2mqtt/my-macbook/command/displaysleep`
  - `mac2mqtt/my-macbook/command/display` (`sleep` / `wake`)

## HACS install

1. Push this project to a GitHub repo, e.g. `drapple/mac2mqtt-hacs`.
2. In Home Assistant: HACS -> Integrations -> three dots -> Custom repositories.
3. Add repo URL and select category `Integration`.
4. Install `Mac2MQTT`.
5. Restart Home Assistant.
6. Add integration: Settings -> Devices & Services -> Add Integration -> `Mac2MQTT`.

## Requirements

- Home Assistant MQTT integration configured and connected.
- `mac2mqttd` running on your Mac with same topic base and computer name.
