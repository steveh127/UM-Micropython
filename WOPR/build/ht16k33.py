version = '1.0'

class HT16K33():
    """
    A simple, generic driver for the I2C-connected Holtek HT16K33 controller chip.
    This release supports MicroPython and CircuitPython

    Version:    3.1.0
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2022
    
    SH Modified:
    Added Buffer here as not subclassing.
    Removed Draw, blink rate, 
    move _render to update
    Generally stripped down
    """

    HT16K33_GENERIC_DISPLAY_ON = 0x81
    HT16K33_GENERIC_DISPLAY_OFF = 0x80
    HT16K33_GENERIC_SYSTEM_ON = 0x21
    HT16K33_GENERIC_SYSTEM_OFF = 0x20
    HT16K33_GENERIC_DISPLAY_ADDRESS = 0x00
    HT16K33_GENERIC_CMD_BRIGHTNESS = 0xE0

    def __init__(self, i2c, i2c_address):
        self.i2c = i2c
        self.address = i2c_address
        self.buffer = bytearray(29) 
        self.power_on()

    def set_brightness(self, brightness=15):
        if brightness < 0 or brightness > 15: 
			brightness = 15
        self.brightness = brightness
        self._write_cmd(self.HT16K33_GENERIC_CMD_BRIGHTNESS | brightness)

	#Write the display buffer out to I2C
    def update(self):
		#cope with missing I2C addresses
		while True:
			try:
				buffer = bytearray(len(self.buffer) + 1)
				buffer[1:] = self.buffer
				buffer[0] = 0x00
				self.i2c.writeto(self.address, bytes(buffer))
				return
			except:
				pass

    def clear(self):
        for i in range(0, len(self.buffer)): 
			self.buffer[i] = 0x00

    def power_on(self):
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_ON)
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_ON)

    def power_off(self):
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_OFF)
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_OFF)

    def _write_cmd(self, byte):
        self.i2c.writeto(self.address, bytes([byte]))
