import board
import digitalio
import storage
import usb_cdc
import usb_midi
import usb_hid

# Modified boot descriptor to enable RP2040 macropad to work with KVM switch
# https://github.com/adafruit/circuitpython/issues/1136#issuecomment-1002833056
BOOT_KEYBOARD_DESCRIPTOR=bytes((
    #  Keyboard
    0x05, 0x01,                      # USAGE_PAGE (Generic Desktop)	  47 */
    0x09, 0x06,                      # USAGE (Keyboard) */
    0xa1, 0x01,                      # COLLECTION (Application) */
    0x05, 0x07,                      #   USAGE_PAGE (Keyboard) */
    # Keyboard Modifiers (shift, alt, ...) */
    0x19, 0xe0,                      #   USAGE_MINIMUM (Keyboard LeftControl) */
    0x29, 0xe7,                      #   USAGE_MAXIMUM (Keyboard Right GUI) */
    0x15, 0x00,                      #   LOGICAL_MINIMUM (0) */
    0x25, 0x01,                      #   LOGICAL_MAXIMUM (1) */
    0x75, 0x01,                      #   REPORT_SIZE (1) */
	0x95, 0x08,                      #   REPORT_COUNT (8) */
    0x81, 0x02,                      #   INPUT (Data,Var,Abs) */
    # Reserved byte, used for consumer reports, only works with linux */
	0x05, 0x0C,             		 #   Usage Page (Consumer) */
    0x95, 0x01,                      #   REPORT_COUNT (1) */
    0x75, 0x08,                      #   REPORT_SIZE (8) */
    0x15, 0x00,                      #   LOGICAL_MINIMUM (0) */
    0x26, 0xFF, 0x00,                #   LOGICAL_MAXIMUM (255) */
    0x19, 0x00,                      #   USAGE_MINIMUM (0) */
    0x29, 0xFF,                      #   USAGE_MAXIMUM (255) */
    0x81, 0x00,                      #   INPUT (Data,Ary,Abs) */
	# 5 LEDs for num lock etc, 3 left for advanced, custom usage */
	0x05, 0x08,						 #   USAGE_PAGE (LEDs) */
	0x19, 0x01,						 #   USAGE_MINIMUM (Num Lock) */
	0x29, 0x08,						 #   USAGE_MAXIMUM (Kana + 3 custom)*/
	0x95, 0x08,						 #   REPORT_COUNT (8) */
	0x75, 0x01,						 #   REPORT_SIZE (1) */
	0x91, 0x02,						 #   OUTPUT (Data,Var,Abs) */
    # 6 Keyboard keys */
    0x05, 0x07,                      #   USAGE_PAGE (Keyboard) */
    0x95, 0x06,                      #   REPORT_COUNT (6) */
    0x75, 0x08,                      #   REPORT_SIZE (8) */
    0x15, 0x00,                      #   LOGICAL_MINIMUM (0) */
    0x26, 0xE7, 0x00,                #   LOGICAL_MAXIMUM (231) */
    0x19, 0x00,                      #   USAGE_MINIMUM (Reserved (no event indicated)) */
    0x29, 0xE7,                      #   USAGE_MAXIMUM (Keyboard Right GUI) */
    0x81, 0x00,                      #   INPUT (Data,Ary,Abs) */
    # End */
    0xc0                            # END_COLLECTION */
))

maintenance_pin = digitalio.DigitalInOut(board.GP2)
maintenance_pin.direction = digitalio.Direction.INPUT
maintenance_pin.pull = digitalio.Pull.UP
maintenance_mode = not maintenance_pin.value # active low

# Keyboard object using modified boot descriptor
kbd = usb_hid.Device(
    report_descriptor=BOOT_KEYBOARD_DESCRIPTOR,
    usage=0x06,
    usage_page=0x01,
    report_ids=(0,),
    in_report_lengths=(8,),
    out_report_lengths=(1,),
)

if maintenance_mode:
    print("Booting in maintenance mode")
    print("All USB devices enabled")
else:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((kbd,), boot_device=1)
