import collections
import io
import logging
from typing import Iterable, List, Set

import evdev
import inotify_simple

from keydope import mods
from keydope.keycodes import KEY_CODES, Action, Key, KeyAction

OUTPUT_DEVICE_NAME = 'keydope-fake-output-device'

logger = logging.getLogger(__name__)


class OutputDevice:

    def __init__(self, uinput_device: evdev.uinput.UInput):
        self.uinput_device = uinput_device
        # Keys that change the state of the downstream keyboard handler (X11 in
        # this case). They must be tracked in order to predictably control the
        # downstream keyboard handler regardless of the previously pressed keys.
        self.pressed_mod_keys = set()
        self.combo_to_released_mod_keys = collections.defaultdict(list)
        self.combo_to_pressed_mod_keys = collections.defaultdict(list)

    def _update_modifier_key_pressed(self, key_action: KeyAction):
        if key_action.key in mods.get_all_modifier_keys():
            if key_action.action.is_pressed():
                self.pressed_mod_keys.add(key_action.key)
            else:
                self.pressed_mod_keys.discard(key_action.key)

    def _send_sync(self) -> None:
        self.uinput_device.syn()

    def send_event(self, event) -> None:
        self.uinput_device.write_event(event)
        self._send_sync()

    def send_key_action(self, key_action: KeyAction) -> None:
        logger.debug('Sending %s', key_action)
        self._update_modifier_key_pressed(key_action)
        # pylint: disable=no-member
        self.uinput_device.write(evdev.ecodes.EV_KEY, key_action.key.value,
                                 key_action.action.value)
        self._send_sync()

    def get_modifier_keys(self) -> Set[Key]:
        return self.pressed_mod_keys

    def set_modifier_keys(self, modifier_keys: Iterable[Key]) -> None:
        modifier_to_key = {}
        for key in modifier_keys:
            mod = mods.key_to_modifier(key)
            if not mod:
                raise ValueError('Not a modifier key: {}'.format(key.name))
            if mod in modifier_to_key:
                logging.info(
                    'Got multiple keys for the same modifier. '
                    'Modifier: %s, Keys: %s, %s', mod, modifier_to_key[mod],
                    key)
                continue
            modifier_to_key[mod] = key
        for modifier in set(mods.Modifier) - modifier_to_key.keys():
            for modifier_key in mods.modifier_to_keys(modifier):
                if modifier_key in self.pressed_mod_keys:
                    self.send_key_action(
                        KeyAction(modifier_key, Action.RELEASE))
        for modifier in modifier_to_key:
            modifier_keys = mods.modifier_to_keys(modifier)
            if any(modifier_key in self.pressed_mod_keys
                   for modifier_key in modifier_keys):
                continue
            modifier_key = modifier_to_key[modifier]
            self.send_key_action(KeyAction(modifier_key, Action.PRESS))


def get_uinput_device():
    return evdev.uinput.UInput(name=OUTPUT_DEVICE_NAME)


def get_devices_list():
    return [
        evdev.InputDevice(device_fn)
        for device_fn in reversed(evdev.list_devices())
    ]


def is_keyboard_device(device: evdev.InputDevice) -> bool:
    '''Guesses if the device is a keyboard'''
    capabilities = device.capabilities(verbose=False)
    key_capabilities = capabilities.get(1)
    if not key_capabilities:
        return False
    supported_keys = set()
    for keycode in key_capabilities:
        if keycode in KEY_CODES:
            supported_keys.add(Key(keycode))
    if Key.SPACE not in supported_keys or \
       Key.A not in supported_keys or \
       Key.Z not in supported_keys:
        # Doesn't support common keys, not keyboard.
        return False
    # Originally, this code was filtering devices with mouse buttons, so I
    # assume some mice may have incorrectly reported keyboard keys, causing a
    # false positive in the keyboard classification.
    # However, keyboards with touchpads, like Logitech K400 Plus and K830, also
    # report mouse keys, and they're valid keyboards, so filtering out devices
    # with mouse will cause a false negative. Therefore the current approach is
    # to use these devices, but log this decision.
    if Key.BTN_MOUSE in supported_keys:
        logger.info(
            'Device %s supports mouse buttons but is classified as a keyboard.',
            device.name)
    return True


def format_device_list(devices: List[evdev.InputDevice]) -> str:
    device_format = '{1.fn:<20} {1.name:<35} {1.phys}'
    device_lines = [device_format.format(n, d) for n, d in enumerate(devices)]
    header_lines = []
    header_lines.append('-' * len(max(device_lines, key=len)))
    header_lines.append('{:<20} {:<35} {}'.format('Device', 'Name', 'Phys'))
    header_lines.append('-' * len(max(device_lines, key=len)))
    result = io.StringIO()
    result.writelines(line + '\n' for line in header_lines)
    result.writelines(line + '\n' for line in device_lines)
    return result.getvalue()


# pylint: disable=too-few-public-methods
class DeviceFilter:

    def __init__(self, devices_to_match: List[str]):
        self.devices_to_match = devices_to_match

    def __call__(self, device: evdev.InputDevice) -> bool:
        # Exclude evdev device, which is used for output emulation.
        if device.name == OUTPUT_DEVICE_NAME:
            return False
        # If devices to match were specified, use them to filter. Otherwise, use
        # any keyboard looking device.
        if self.devices_to_match:
            for device_to_match in self.devices_to_match:
                if device_to_match in (device.fn, device.name):
                    return True
            return False
        # Exclude none keyboard devices.
        if not is_keyboard_device(device):
            return False
        return True


def get_all_input_devices() -> List[evdev.InputDevice]:
    return [
        evdev.InputDevice(device_fn)
        for device_fn in reversed(evdev.list_devices())
    ]


def watch_devices() -> inotify_simple.INotify:
    inotify = inotify_simple.INotify()
    inotify.add_watch('/dev/input', inotify_simple.flags.CREATE)
    logger.info('Watching for keyboard devices plugged in')
    return inotify


def on_device_add(inotify: inotify_simple.INotify, device_filter: DeviceFilter,
                  monitored_devices: List[evdev.InputDevice]) -> None:
    new_devices = []
    for event in inotify.read():
        new_device = evdev.InputDevice('/dev/input/' + event.name)
        if not device_filter(new_device) or any(
                new_device.fn == dev.fn for dev in monitored_devices):
            continue
        try:
            new_device.grab()
            monitored_devices.append(new_device)
            new_devices.append(new_device)
        except IOError:
            # Only log errors on new devices
            logger.error('IOError when grabbing new device: %s',
                         new_device.name)
    if new_devices:
        logger.info('Enabling remapping on the following new device(s):\n%s',
                    format_device_list(new_devices))
