from evdev import InputDevice, categorize, ecodes
import select


class MultiInputListener:
    def __init__(self, device_paths, handler=None):
        """
        device_paths: liste af /dev/input/eventX
        handler: objekt eller funktion der håndterer events
        """
        self.devices = [InputDevice(path) for path in device_paths]
        self.handler = handler
        self.running = False
        ##self.seq = seq
    def set_handler(self, handler):
        """Skift handler under runtime"""
        self.handler = handler

    def start(self):
        """Starter event loop"""
        self.running = True
     #   print("Lytter på:", [d.path for d in self.devices])

        while self.running:
            r, _, _ = select.select(self.devices, [], [])

            for dev in r:
                for event in dev.read():
                    if event.type == ecodes.EV_KEY:
                        key_event = categorize(event)

                        key = key_event.keycode
                        if isinstance(key, list):
                            key = key[0]

                        state = key_event.keystate  # 0=up,1=down,2=hold
                       # if state == 1:
                           # seq.changeSeq()
                        self.handle_event(dev.path, key, state)

    def stop(self):
        self.running = False

    def handle_event(self, device, key, state):
        """Intern dispatcher"""
        if self.handler:
            # hvis handler er en funktion
            if callable(self.handler):
                self.handler(device, key, state)

            # hvis handler er et objekt med metode
            elif hasattr(self.handler, "handle_input"):
                self.handler.handle_input(device, key, state)
