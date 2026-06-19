class Seq:
    __init__(self):
        self.seqIndex = 0
        self.seqmode = None
        self.clock = 0
        self.times = [6,12,24,48,96]
        self.time = 12
        
    def getClock(self):
        self.clock = self.clock + 1
        if self.clock == self.time:
            self.seqIndex = self.seqIndex + 1
            self.clock = 0