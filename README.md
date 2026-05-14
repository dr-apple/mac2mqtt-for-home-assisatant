# Mac2MQTT HACS Integration

Custom Home Assistant integration for `mac2mqtt` / `mac2mqttd`.

## Features

- `binary_sensor`: Alive, Display, Locked
- `sensor`: Apps, Battery, Power Source, Display Changed At, Screensaver Selected
- `select`: App
- `switch`: Mute, Display Power
- `number`: Volume (0-100)
- `button`: Sleep, Shutdown, Display Sleep, Display Wake, Start Screensaver
- `text`: Say, Notification, Foreground Notification, Screensaver, Open App

## MQTT topic mapping

Given:

- `base_topic = mac2mqtt`
- `computer_name = my-macbook`

The integration uses:

- Status subscribe:
  - `mac2mqtt/my-macbook/status/alive`
  - `mac2mqtt/my-macbook/status/apps`
  - `mac2mqtt/my-macbook/status/battery`
  - `mac2mqtt/my-macbook/status/power_source`
  - `mac2mqtt/my-macbook/status/display`
  - `mac2mqtt/my-macbook/status/display_changed_at`
  - `mac2mqtt/my-macbook/status/screensaver_selected`
  - `mac2mqtt/my-macbook/status/locked`
  - `mac2mqtt/my-macbook/status/volume`
  - `mac2mqtt/my-macbook/status/mute`
- Command publish:
  - `mac2mqtt/my-macbook/command/volume`
  - `mac2mqtt/my-macbook/command/mute`
  - `mac2mqtt/my-macbook/command/sleep`
  - `mac2mqtt/my-macbook/command/shutdown`
  - `mac2mqtt/my-macbook/command/displaysleep`
  - `mac2mqtt/my-macbook/command/displaywake`
  - `mac2mqtt/my-macbook/command/display` (`sleep` / `wake`)
  - `mac2mqtt/my-macbook/command/say`
  - `mac2mqtt/my-macbook/command/notification` (text or JSON with `title`, `message`, and `foreground`)
  - `mac2mqtt/my-macbook/command/screensaver` (`start` or saver name/path)
  - `mac2mqtt/my-macbook/command/app`

On Macs without an internal battery, `status/battery` and `status/power_source`
are not published and existing retained values are cleared by `mac2mqttd`.
`status/apps` contains a JSON list of installed apps; the integration exposes
the app count as the sensor state and the app objects as attributes. It also
feeds the `App` select entity, which publishes the selected app name to
`command/app`.
The `Foreground Notification` entity sends the notification command as JSON with
`foreground: true`, which opens a frontmost dialog on the Mac.

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
