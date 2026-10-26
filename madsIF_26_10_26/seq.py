from note import Note
import numpy as np 
from out import MIDIOUT
class Seqcenser:
	def __init__(self, out):
		self.lastNote = 60
		self.noteTime = [0,0]
		self.fristNote = 60
		self.noteOn = []
		self.notesDown  = []
		self.lengt = 16
		self.count = 0
		self.x = 0
		self.y = 0
		self.div = 6
		self.notesInSeq = []
		self.play = False
		self.Modes = "note", "ratit"
		self.rec= False
		self.canPlay = True
		#self.callback = self.changeLastNote(60)
		for i in range(4):
			self.notesInSeq.append([Note(60), Note(60), Note(60),Note(60)])
		self.midi =out

	def changeLastNote(self, note):
		if note != self.lastNote:
			self.lastNote = note
		if self.rec:
			self.noteTime[0] = int(self.y)
			self.noteTime[1] = int(self.x)
			
			#print(self.lastNote)
	def playNoteOn(self, note):
		if self.play == False:
			self.midi.sendNoteOn(note)
		elif self.rec:
			self.midi.sendNoteOn(note)
	def playNoteOff(self, note):
		self.midi.sendNoteOff(note)
	def stop(self):
		self.play = False
		for note in self.noteOn: 
			self.midi.sendNoteOff(note)
		self.noteOn.clear()
	def changeSeq(self, value, index):
		if(self.notesInSeq[index].value != value):
			self.notesInSeq[index].value = value
	def start(self):
		self.x = 0
		self.y = 0
		if self.notesInSeq[0][0].aktiv == True:
			self.playChord2()
	def calcFristNote(self):
		for i in range(4):
			for t in range(4):
				if self.notesInSeq[i][t].aktiv == True:
					self.fristNote = int(self.notesInSeq[i][t].value)
					return

	def playChord(self):
		if len(self.notesDown) > 0:
			for note in range(len(self.notesDown)):
				noteToPlay = self.fristNote + (self.notesDown[note] - self.fristNote) - (self.fristNote - self.notesInSeq[self.y][self.x].value) 
				self.noteOn.append(noteToPlay)
				self.midi.sendNoteOn(noteToPlay)
	def playChord2(self):
		if len(self.notesDown) > 0 and not self.rec:
			frit_note = self.fristNote
			antal_notes = len(self.notesDown) 
			seq = self.notesInSeq[self.y][self.x]
			if seq.value != 144:
				for note_idx in range(antal_notes):
					noteToPlay = frit_note + (self.notesDown[note_idx] - frit_note) - (frit_note - seq.value) 
					self.noteOn.append(noteToPlay)
					self.midi.sendNoteOn(noteToPlay)
	def clacNestStep(self):
		x = self.x
		y = self.y
		if y > 2 and x > 2:
			return 0, 0
		elif y == 3 and x < 3:
			return y , x +1
		elif x == 3 and y < 3:
			return y +1 , 0 
		else: 
			return y, x + 1
	def stopChord(self):
		y , x = self.clacNestStep()
		if len(self.noteOn) > 0:
			seq = self.notesInSeq[y][x]
			if seq.value != 144 and seq.aktiv or not seq.aktiv : 
				for note in self.noteOn: 
					self.midi.sendNoteOff(note)
				self.noteOn.clear()
	def stopNote(self, note):
		noteToStop = note - (self.fristNote - self.notesInSeq[self.y][self.x].value)
		self.noteOn.remove(noteToStop)
		self.midi.sendNoteOff(noteToStop)
	def go(self):
		self.count = self.count + 1
		if self.count == self.div:
			self.stopChord()
			#self.callback()
			self.canPlay = False
			self.count = 0
			self.x  = self.x + 1
			if self.x == 4:
				self.x = 0
				self.y = self.y + 1
				if self.y == 4:
					self.y = 0
			
			if self.notesInSeq[self.y][self.x].aktiv:
				self.playChord2()
			self.setOnRec()
		
	def setOnRec(self):
		if not self.notesInSeq[self.y][self.x] == int(self.lastNote) and len(self.notesDown) > 0 and self.rec == True:
			if self.noteTime[0] == self.y and  self.noteTime[1] == self.x:
				self.notesInSeq[self.y][self.x].value = int(self.lastNote)
				self.notesInSeq[self.y][self.x].aktiv = True 
			else:
				self.notesInSeq[self.y][self.x].value = 144
				self.notesInSeq[self.y][self.x].aktiv = True 
			

