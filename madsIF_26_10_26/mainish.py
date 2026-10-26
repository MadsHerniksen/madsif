import threading
import time
from midi_SPI_IN import MidiSpiListener
from seq import Seqcenser
from ui_test import GridUI
from keyboard import MultiInputListener   # din evdev klasse


def main():
    # ------------------------
    # 1. UI START
    # ------------------------
    seq = Seqcenser()
    Mlistener = MidiSpiListener(bus=0, device=0, callback=None, seq = seq)
    Mlistener.start()
    ui = GridUI(seq)
    
    ui_thread = threading.Thread(target=ui.start, daemon=True)
    ui_thread.start()

    time.sleep(0.2)  # give curses time to boot

    # ------------------------
    # 2. INPUT DEVICES
    # ------------------------
    devices = [
        "/dev/input/event6",
        "/dev/input/event4", 
        "/dev/input/event5", 
        "/dev/input/event7", 
        
    ]


    # ------------------------
    # 3. INPUT LISTENER
    # ------------------------
    listener = MultiInputListener(devices, ui)

    try:
        print("System running. Ctrl+C to exit.")
        listener.start()

    except KeyboardInterrupt:
        print("Stopping system...")

    finally:
        ui.stop()


if __name__ == "__main__":
    main()
