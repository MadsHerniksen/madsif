import curses
import threading
import time
from note import Note
from midiInfo import MidiInfo
class GridUI:
    # Nu-mpad → grid mapping
    KEY_MAP = {
        "KEY_KP7": (0, 0), "KEY_KP8": (0, 1), "KEY_KP9": (0, 2), "KEY_KPPLUS": (1, 3),
        "KEY_KP4": (1, 0), "KEY_KP5": (1, 1), "KEY_KP6": (1, 2), "KEY_KPMINUS": (0, 3),
        "KEY_KP1": (2, 0), "KEY_KP2": (2, 1), "KEY_KP3": (2, 2), "KEY_KPENTER": (3, 3),
        "KEY_KP0": (3, 1), "KEY_KPDOT": (3, 2), "KEY_KPSLASH": (2,3) , "KEY_KPASTERISK": (3,0)
    }

    Knup2 = {
        "KEY_MIN_INTERESTING", "KEY_VOLUMEDOWN", "KEY_VOLUMEUP"
    }
    
    knup1 = {
        "KEY_NUMLOCK", "KEY_SPACEC", "KEY_BACKSPACE"
    }

    def __init__(self, seq, go):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.lock = threading.Lock()
        self.running = False
        self.COLORS = [1, 2, 3, 4]
        self.COLORS2 = [1, 2, 3, 4]
        self.last_input = ""
        self.heltal = 0
        self.vel = 0
        self.New = False
        self.seq = seq
        self.count = -1 
        self.steps = []
        self.stepDown = None
        self.midiInfo = MidiInfo()
        self.step = 0
        self.updateLys = False;
        self.redNote = 0,0
        self.tieToNote = (0,0)
        self.go = go
    # ----------------------------
    # INPUT (fra evdev)
    # ----------------------------
    def handle_input(self, device, key, state):
        self.New = True
        self.last_input = key
        
        if key == "KEY_VOLUMEDOWN":
            self.seq.notesInSeq[self.redNote[0]][self.redNote[1]].value = self.seq.notesInSeq[self.redNote[0]][self.redNote[1]].value  - 1   
            return
        if key == "KEY_VOLUMEUP":
            self.seq.notesInSeq[self.redNote[0]][self.redNote[1]].value = self.seq.notesInSeq[self.redNote[0]][self.redNote[1]].value  + 1  
            return
        if key in self.KEY_MAP:
            y, x = self.KEY_MAP[key]
            with self.lock:
                self.grid[y][x] = state % 3
            return
        if "KEY_MIN_INTERESTIN":
            if  self.seq.rec == False and state == 1:
                self.seq.rec = True
            elif  self.seq.rec == True and state == 1:
                self.seq.rec = False
            return


               # self.updateUI(self, stdscr)
            #self.steps.append(y+x)

    # ----------------------------
    # START UI THREAD
    # ----------------------------
    def updatelys(self):
        self.upadteLys = False
    def start(self):
        self.running = True
        curses.wrapper(self._loop)
    
    def calcTieTo(self):
        fra = self.redNote
        til = self.tieToNote
        x = self.redNote[0]
        y = self.redNote[1]
        tieIforward = False
        for i in range(4,0):
            for t in range(4,0):
                if i == y and t == x:
                    return
                elif i == self.tieNote[0] and t == self.tieNote[1]:
                    tieIforward = True
                    return
                elif tieIforward:
                    self.seq.notesInSeq[i][t].value = 144
    def updateUI(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        
        if self.running == True and self.go:
            with self.lock:
                for y in range(4):
                    for x in range(4):
                        #self.count = self.count + 1
                        color = self.COLORS[self.grid[y][x]]
                        stdscr.attron(curses.color_pair(color))
                        stdscr.addstr(2 + y * 2, 4 + x * 8, " ■ ")
                        if self.grid[y][x] == 1 and len(self.seq.notesDown) != 0:
                            self.seq.notesInSeq[y][x].aktiv = True
                            self.seq.notesInSeq[y][x].value = int(self.seq.lastNote)
                        if self.grid[y][x] == 1 and len(self.seq.notesDown) == 0:
                            self.seq.notesInSeq[y][x].aktiv = False
                        if self.grid[y][x] == 2:
                            self.seq.notesInSeq[y][x].aktiv = True
                            self.seq.calcFristNote()
                            self.redNote = y ,x  
                        if self.seq.notesInSeq[y][x].aktiv == True:
                            stdscr.addstr(f"{self.midiInfo.noteList[self.seq.notesInSeq[y][x].value]}")
                            self.seq.calcFristNote()
                        else:
                            stdscr.addstr(f"   ")
                        #løbelys
                        if self.step != self.seq.count:
                            self.step = self.step + 1
                            if(self.seq.x == x and self.seq.y == y):
                                color2 = self.COLORS2[1]
                                stdscr.attron(curses.color_pair(color2))
                                stdscr.addstr(3 +y * 2, 4 + x * 8, " ■ ")
                            else:
                                color2 = self.COLORS2[3]
                                stdscr.attron(curses.color_pair(color2))
                                stdscr.addstr(3 +y * 2, 4 + x * 8, " ■ ")
                #stdscr.addstr(f"{self.last_input}")
                #stdscr.addstr(f"{self.heltal}")
                self.count = -1
            if self.seq.play and not self.seq.rec:
                color2 = self.COLORS[1]
            elif self.seq.rec:
                color2 = self.COLORS[2]
            else:
                color2 = self.COLORS[0]
            stdscr.attron(curses.color_pair(color2))
            stdscr.addstr(0, 0, f"In:")
            for i in range(8):
                if i < len(self.seq.notesDown):
                    stdscr.addstr(0,  3 +(4 * i), f" {self.midiInfo.noteList[self.seq.notesDown[i]]} ")
                else:
                    stdscr.addstr(0,  3 +(4 * i), f"    ")
            stdscr.refresh()
    def stop(self):
        self.running = False

    # ----------------------------
    # RENDER LOOP
    # ----------------------------
    def _loop(self, stdscr):

        


        while self.running:
            self.updateUI(stdscr)

            time.sleep(0.05)
