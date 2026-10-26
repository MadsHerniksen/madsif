import time
import serial
import mido
mido.set_backend('mido.backends.rtmidi')
class MIDIOUT:
# Åbn forbindelsen præcis efter dine specifikationer
	def __init__(self):
		try:
			ser = serial.Serial('/dev/ttyAMA0', baudrate=38400, timeout=1)
			self.midi = ser
		except Exception as e:
			print(f"Fejl: Kunne ikke åbne porten. Tjek om porten er i brug. \n{e}")
			exit()		
		
		
	def sendNoteOn(self, note):
		if note < 127 and note > 0 :
			note_on = mido.Message('note_on', note=note, velocity=64, channel=0)
			self.midi.write(note_on.bytes())

	def sendNoteOff(self, note):
		if note < 127 and note > 0:
			note_off = mido.Message('note_off', note=note, velocity=0, channel=0)		
			self.midi.write(note_off.bytes())
