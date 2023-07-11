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

led.value = True
time.sleep(2)
led.value = False
time.sleep(1)
for x in range(0, 10000):
    numeric = '{0:06}'.format(x)
    for y in numeric:
        led.value = True
        keyboard.press(getattr(Keycode, numbers[int(y)]))
        #keyboard.send(getattr(Keycode, numbers[int(y)]))
        keyboard.release_all()
        time.sleep(0.1)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()
    led.value = False
    time.sleep(12)
