import evdev

class findKeypad:
	def __init__(self):
		self.deviceName =["SDINNOVATION SIDE-KEYBOARD", "SDINNOVATION SIDE-KEYBOARD Keyboard", "SDINNOVATION SIDE-KEYBOARD Mouse", "SDINNOVATION SIDE-KEYBOARD Wireless Radio Control"]
		self.deviceAdress = []
		for i in range(4):
			self.deviceAdress.append(self.find_keypad_by_name(self.deviceName[i]))
	
	
	def find_keypad_by_name(self, target_name):
		devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
		for device in devices:
			if target_name in device.name:
				#print(f"Fandt enhed: {device.name} på {device.path}")
				return device.path
		return None	
