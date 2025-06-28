import asyncio
from machine import Pin,SPI,SDCard

import vfs

from squixl_text import screen as scr
from squixl_time import SQ_Time
from sq_controls import Button,Select_Button,Radio_Button,Radio_Buttons,Menu
from fonts import *

import SQUiXL

def SD_setup():
	SQUiXL.set_iomux(SQUiXL.IOMUX_SD)
	print(SQUiXL.ioex.pin_mode(SQUiXL.SD_DETECT,SQUiXL.INPUT))
	#spi=SPI(1,sck=Pin(45),mosi=Pin(46),miso=Pin(41)) 
	sdcard = SDCard(slot=2,sck=Pin(45),mosi=Pin(42),miso=Pin(46),cs=Pin(41),freq=20000000)
	#vfs = os.VfsFat(sdcard)
	vfs.mount(sdcard,'/sd')



async def display():
	scr.font = sans24I	
	scr.write("SQUiXL !",100,50, PURPLE,font=serif64I)
	scr.write("Peripheral Tests",130,130, PURPLE,font=serif32I)
	
	SD_setup()
	
	clock = SQ_Time(180,10,GREEN,font=sans32)
	ex = Select_Button('close',"Clear Screen",15, 430,10,RED,clicked=RED,font=sans24I)
	
	i = 1
	scr.font = serif32B
	scr.write_over(' ' + str(0) + ' ',10, 10, YELLOW,background=RED)
	while True:
		if i % 10 == 0:
			scr.write_over(' ' + str(i//10) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(display())
