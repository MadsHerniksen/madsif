import spidev
import time
import threading


class MidiSpiListener:
    def __init__(
        self,
        bus=0,
        device=0,
        max_speed_hz=50000,
        spi_mode=0,
        poll_interval=0.0001,
        callback=None,
    ):
        self.bus = bus
        self.device = device
        self.max_speed_hz = max_speed_hz
        self.spi_mode = spi_mode
        self.poll_interval = poll_interval
        self.callback = callback

        self.spi = None
        self.thread = None
        self.running = False


    def start(self):
        if self.running:
            return

        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = self.max_speed_hz
        self.spi.mode = self.spi_mode

        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

        print("MIDI SPI listener startet")

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join()

        if self.spi:
            self.spi.close()

        print("MIDI SPI listener stoppet")

    def _decode_event(self, response):
        if response == 0:
            return None

        elif response == 1:
            return {"type": "start"}

        elif response == 2:
            return {"type": "stop"}

        elif response == 3:
            return {"type": "clock"}

        elif response <= 127:
            return {
                "type": "note_on",
                "pitch": response
            }
        else:
            return {
            "type": "note_off",
            "pitch": response - 128
        }

    def run(self):
        while self.running:
            try:
                response = self.spi.xfer2([0x00])[0]

                event = self._decode_event(response)

                if event:
                    if self.callback:
                        self.callback(event)
                    else:
                        print(event)

                time.sleep(self.poll_interval)

            except Exception as e:
                print(f"SPI fejl: {e}")
                time.sleep(1)