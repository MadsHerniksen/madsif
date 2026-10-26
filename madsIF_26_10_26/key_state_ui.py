class GridUI:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.lock = threading.Lock()

    def handle_input(self, device, key, state):
        if state != 1:
            return

        # numpad mapping
        if key in KEY_MAP:
            y, x = KEY_MAP[key]

            with self.lock:
                self.grid[y][x] = (self.grid[y][x] + 1) % 3