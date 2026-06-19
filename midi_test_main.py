import time
from modtager import MidiSpiListener
from seq import Seq


seq = Seq()
listener = MidiSpiListener(args=(seq))
listener.start()
try:
    

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    listener.stop()