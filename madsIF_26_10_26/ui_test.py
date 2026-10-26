import curses
import threading
import time


class GridUI:
    # Numpad → grid mapping
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

    def __init__(self, seq):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.lock = threading.Lock()
        self.running = False
        self.COLORS = [1, 2, 3]
        self.last_input = ""
        self.heltal = 0
        self.vel = 0
        self.New = False
        self.seq = seq
    # ----------------------------
    # INPUT (fra evdev)
    # ----------------------------
    def handle_input(self, device, key, state):
        self.New = True
        self.last_input = key
        
        if key == "KEY_VOLUMEDOWN":
            self.heltal = self.heltal - 1
        
        if key == "KEY_VOLUMEUP":
            self.heltal = self.heltal + 1
        
        
        if key in self.KEY_MAP:
            y, x = self.KEY_MAP[key]

            with self.lock:
                self.grid[y][x] = state % 3

    # ----------------------------
    # START UI THREAD
    # ----------------------------
    def start(self):
        self.running = True
        curses.wrapper(self._loop)

    def stop(self):
        self.running = False

    # ----------------------------
    # RENDER LOOP
    # ----------------------------
    def _loop(self, stdscr):
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        while self.running:
          #  if self.New:
           #     stdscr.clear()
            #    self.New = False
            with self.lock:
                for y in range(4):
                    for x in range(4):
                        color = self.COLORS[self.grid[y][x]]

                        stdscr.attron(curses.color_pair(color))
                        stdscr.addstr(2 + y * 2, 4 + x * 8, " ■ ")
                        stdscr.addstr(f"{self.seq.lastNote}")
                        stdscr.attroff(curses.color_pair(color))
                #stdscr.addstr(f"{self.last_input}")
                #stdscr.addstr(f"{self.heltal}")
                            
            stdscr.addstr(0, 2, "4x4 Grid UI (evdev + curses)")
            stdscr.refresh()

            time.sleep(0.05)
