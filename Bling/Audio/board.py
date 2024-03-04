from machine import SPI,Pin,I2C
spi=SPI(1,sck=Pin(36),mosi=Pin(35),miso=Pin(37))
CS=21
#I2S
SCK=2
WS=1
SD=4
#buttons
BUTTONS=[11,33,10,34]
