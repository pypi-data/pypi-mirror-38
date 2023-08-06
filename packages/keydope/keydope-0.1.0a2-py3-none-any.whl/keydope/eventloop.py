import logging
import queue
import select
import threading
import time
from typing import List, Optional

import evdev

from keydope import devices, util
from keydope.keycodes import Action, Key, KeyAction

logger = logging.getLogger(__name__)

# pylint: disable=broad-except

# pylint: disable=too-many-locals,too-many-branches
def loop(monitored_devices: List[evdev.InputDevice],
         output_device: devices.OutputDevice,
         key_processor,
         watch_device_connections=True,
         device_filter: devices.DeviceFilter = None) -> None:
    for device in monitored_devices:
        try:
            device.grab()
        except IOError as e:
            raise IOError('Error grabbing device {}: {}'.format(device.name, e))

    events_queue = queue.Queue()
    processing_exceptions = queue.Queue()

    def process_events():
        while True:
            input_device, event = events_queue.get()
            try:
                # pylint: disable=no-member
                if event.type != evdev.ecodes.EV_KEY:
                    output_device.send_event(event)
                    continue
                start_time = time.time()
                key_action = KeyAction(Key(event.code), Action(event.value))
                key_processor.on_event(key_action, input_device.name)
                processing_duration = time.time() - start_time
                logger.debug(
                    'Processing duration: {:.5f}'.format(processing_duration))
            except OSError as e:
                logger.warning('Got OS error: %s', e)
                logger.info('Assuming device removed: %s', input_device)
                monitored_devices.remove(input_device)
            # pylint: disable=broad-except
            except Exception as e:
                processing_exceptions.put(e)
                return

    processing_thread = threading.Thread(
        target=process_events, name='keyboard_remapper')
    processing_thread.start()

    if watch_device_connections:
        inotify = devices.watch_devices()
    try:
        while True:
            try:
                raise processing_exceptions.get(block=False)
            except queue.Empty:
                pass
            waitables = monitored_devices[:]
            if watch_device_connections:
                waitables.append(inotify.fd)
            readables, _, _ = select.select(waitables, [], [])
            for readable in readables:
                # If it's not an input device, it must be the inotify watcher,
                # which means there's a new input device.
                if not isinstance(readable, evdev.InputDevice):
                    devices.on_device_add(inotify, device_filter,
                                          monitored_devices)
                    continue
                for event in readable.read():
                    events_queue.put((readable, event))
    finally:
        for device in monitored_devices:
            device.ungrab()
        if watch_device_connections:
            inotify.close()
