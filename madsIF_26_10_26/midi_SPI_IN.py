import spidev
import time
import threading
from note import Note
#from seq import Seqcenser
class MidiSpiListener:
    def __init__(
        self,
        bus=0,
        device=0,
        max_speed_hz=50000,
        spi_mode=0,
        poll_interval=0.0001,
     
        seq=None, # Sæt en standardværdi her, da den er placeret til sidst

    ):
        self.bus = bus
        self.device = device
        self.max_speed_hz = max_speed_hz
        self.spi_mode = spi_mode
        self.poll_interval = poll_interval
       

        self.spi = None
        self.thread = None
        self.running = False
        self.seq = seq # Rettet fra 'sef' til 'self'
        

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
        if response <= 127 and response > 3:
            self.seq.playNoteOn(response)
            self.seq.changeLastNote(response)
            self.seq.notesDown.append(response)
            self.seq.setOnRec()
           
            return {
                "type": "note_on",
                "pitch": response
            }
            
        elif response >= 128 and response <= 255:
            if response - 128 in self.seq.notesDown: 
                self.seq.notesDown.remove(response - 128)
            self.seq.playNoteOff(response - 128)
            return {
                "type": "note_off",
                "pitch": response - 128
            }
 
 
 
 
        if response == 0:
            return None

        elif response == 1:
            self.seq.play = True
            self.seq.start()
            self.count = 0
            return {"type": "start"}

        elif response == 2:
            self.seq.stop()
            
            return {"type": "stop"}

        elif response == 3:
            self.seq.go()
            return {"type": "clock"}


            #seq.changeLastNote(response-128)

    def run(self):
        while self.running:
            try:
                response = self.spi.xfer2([0x00])[0]
                event = self._decode_event(response)

                #if event:
                 #   if self.callback:
                  #      self.callback(event)
                  #  else:
                   #     print(f"Modtog event: {event}")
                   
                
                # Undgå at bruge 100% CPU ved at holde en ultrakort pause
                if self.poll_interval > 0:
                    time.sleep(self.poll_interval)
                    
            except Exception as e:
                print(e)
                self.running = False
# Nederst i din fil, efter klassen er defineret:
# Nederst i din fil, efter klassen er defineret:

