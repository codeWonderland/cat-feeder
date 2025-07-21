# Microcontroller Relay Controller
# 2023 - codeWonderland

import board
import digitalio
from time import sleep

class LatchingRelay:
    def __init__(self, on_pin, off_pin):
        self.on_pin = digitalio.DigitalInOut(on_pin)
        self.off_pin = digitalio.DigitalInOut(off_pin)
        self.active = False

        self.on_pin.switch_to_output()
        self.off_pin.switch_to_output()

        self.relay_off()


    def toggle_pin(self, pin):
        pin.value = True
        sleep(0.15)
        pin.value = False


    def relay_on(self):
        self.toggle_pin(self.on_pin)
        self.active = True


    def relay_off(self):
        self.toggle_pin(self.off_pin)
        self.active = False
