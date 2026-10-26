import threading
import time
from midi_SPI_IN import MidiSpiListener
from seq import Seqcenser
from ui import GridUI
from keyboard import MultiInputListener   # din evdev klasse-
import curses
import time
from findkeypad import findKeypad 
import sys
from out import MIDIOUT
def main():
    # ------------------------
    # 1. UI START
    # ------------------------
    out = MIDIOUT()
    seq = Seqcenser(out)
    Mlistener = MidiSpiListener(bus=0, device=0, seq = seq)
    Mlistener.start()
    ui = GridUI(seq, True)
    ui_thread = threading.Thread(target=ui.start, daemon=True)
    
    ui_thread.start()
    time.sleep(0.2)  # give curses time to boot
   
    # ------------------------
    # 2. INPUT DEVICES
    # ------------------------
    keys = findKeypad() 
    devices = keys.deviceAdress
     #   "/dev/input/event9",
     #   "/dev/input/event4", 
     #   "/dev/input/event5", 
    #    "/dev/input/event7", 
        
   # ]


    # ------------------------
    # 3. INPUT LISTENER
    # ------------------------
    listener = MultiInputListener(devices, ui)

    try:
       # print("System running. Ctrl+C to exit.")
        listener.start()

    except KeyboardInterrupt:
        print("Stopping system...")

    finally:
        ui.stop()
        Mlistener.stop()
        listener.stop() 
       # sys.exit(0)

if __name__ == "__main__":
    main()

