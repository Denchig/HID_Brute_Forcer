import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
numbers = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']

time.sleep(5)
for x in range(0, 1000000):
    numeric = '{0:06}'.format(x)
    for y in numeric:
        kbd.send(getattr(Keycode, numbers[int(y)]))
        #time.sleep(0.1)
    kbd.send(Keycode.ENTER)
    time.sleep(12)
