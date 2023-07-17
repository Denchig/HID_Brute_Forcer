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
    time.sleep(0.05)
    led.value = False
    time.sleep(0.05)

for x in range(0, 10000):
    numeric = '{0:06}'.format(x)
    for y in numeric:
        keyboard.press(getattr(Keycode, numbers[int(y)]))
        keyboard.release(getattr(Keycode, numbers[int(y)]))
        blink()
    keyboard.press(Keycode.RETURN)
    keyboard.release(Keycode.RETURN)
    time.sleep(12)
