import time
import digitalio
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
numbers = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']

time.sleep(4)

def blink():
    led.value = True
    time.sleep(0.1)
    led.value = False

for x in range(0, 10000):
    numeric = '{0:06}'.format(x)
    for y in numeric:
        keyboard.send(getattr(Keycode, numbers[int(y)]))
        blink()
    keyboard.send(Keycode.ENTER)
    time.sleep(12)
