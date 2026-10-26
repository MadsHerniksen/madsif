class MidiInfo:
	def __init__(self):
		self.noteList = []
		for i in range(12):
			self.noteList.append(f"C{i} ")
			self.noteList.append(f"C#{i}")
			self.noteList.append(f"D{i} ")
			self.noteList.append(f"D#{i}")
			self.noteList.append(f"E{i} ")
			self.noteList.append(f"F{i} ")
			self.noteList.append(f"F#{i}")
			self.noteList.append(f"G{i} ")
			self.noteList.append(f"G#{i} ")
			self.noteList.append(f"A{i} ")
			self.noteList.append(f"A#{i}")
			self.noteList.append(f"B{i} ")
		self.noteList.append("...")
