# Mac2MQTT HACS Integration

Custom Home Assistant integration for `mac2mqtt` / `mac2mqttd`.

Version `0.12.0` is compatible with Home Assistant `2026.8` and tested against
`2026.8.1`. Entity IDs remain stable when the MQTT topic or computer name changes.

## Features

- `binary_sensor`: Alive, Display, Locked, Media Playing
- `sensor`: Battery, Power Source, Display Changed At
- `select`: App, Screensaver
- `switch`: Mute, Display Power, Media Playback
- `number`: Volume (0-100)
- `button`: Sleep, Shutdown, Display Sleep, Display Wake, Start Screensaver, Play Pause
- `text`: Say, Notification, Screensaver, Open App

## MQTT topic mapping

Given:

- `base_topic = mac2mqtt`
- `computer_name = my-macbook`

The integration uses:

- Status subscribe:
  - `mac2mqtt/my-macbook/status/alive`
  - `mac2mqtt/my-macbook/status/battery`
  - `mac2mqtt/my-macbook/status/power_source`
  - `mac2mqtt/my-macbook/status/display`
  - `mac2mqtt/my-macbook/status/display_changed_at`
  - `mac2mqtt/my-macbook/status/locked`
  - `mac2mqtt/my-macbook/status/media_playing`
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
  - `mac2mqtt/my-macbook/command/notification` (text or JSON with `title` and `message`)
  - `mac2mqtt/my-macbook/command/screensaver` (saver name/path)
  - `mac2mqtt/my-macbook/command/app`
  - `mac2mqtt/my-macbook/command/media_playback` (`play` / `pause` / `toggle`)
  - `mac2mqtt/my-macbook/command/play_pause`

On Macs without an internal battery, `status/battery` and `status/power_source`
are not published and existing retained values are cleared by `mac2mqttd`.
The integration exposes native Mac2MQTT select entities for `App` and
`Screensaver` that publish to `command/app` and `command/screensaver`. Their
option lists are read from the Mac app's retained MQTT Discovery config when
available.
Notifications are shown as a frontmost dialog on the Mac.
`command/say` pauses active media playback before speaking and resumes it after
speech finishes.

## HACS install

1. Use the repository `https://github.com/dr-apple/mac2mqtt-for-home-assisatant`.
2. In Home Assistant: HACS -> Integrations -> three dots -> Custom repositories.
3. Add repo URL and select category `Integration`.
4. Install `Mac2MQTT`.
5. Restart Home Assistant.
6. Add integration: Settings -> Devices & Services -> Add Integration -> `Mac2MQTT`.

## Requirements

- Home Assistant MQTT integration configured and connected.
- `mac2mqttd` running on your Mac with same topic base and computer name.
