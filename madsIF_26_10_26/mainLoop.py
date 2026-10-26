import threading
import time
from keyboard import MultiInputListener  # <-- ret navn


class UIHandler:
    def __init__(self):
        self.last_event = None

    def handle_input(self, device, key, state):
        # kun reagér på tryk (ikke hold)
        if state == 1:
            self.last_event = (device, key)
            print(f"[UI] {device} -> {key} down")
        
        if state == 0:
            self.last_event = (device, key)
            print(f"[UI] {device} -> {key} up")
        
        if state == 2:
            self.last_event = (device, key)
            print(f"[UI] {device} -> {key} hold")
        

            # 👉 her kan du opdatere rigtig UI senere


def main():
    ui = UIHandler()

    listener = MultiInputListener(
        ['/dev/input/event0', '/dev/input/event3'],
        handler=ui
    )

    #listener_thread = threading.Thread(target=listener.start)
    #listener_thread.start()

    try:
        # “main loop” – her ville din UI normalt køre
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopper program...")

        listener.stop()
        listener_thread.join()

        print("Lukket pænt ✔️")


if __name__ == "__main__":
    main()
