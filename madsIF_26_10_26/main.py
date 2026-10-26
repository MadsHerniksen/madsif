# Nederst i din fil, efter klassen er defineret:
if __name__ == "__main__":
    # Vi laver en simpel callback-funktion, der bare printer eventet
    def mit_callback(event):
        print(f"Callback modtog: {event}")

    # Start listeneren på bus 0, device 0
    listener = MidiSpiListener(bus=0, device=0, callback=mit_callback)
    listener.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
        print("Program afsluttet.")
