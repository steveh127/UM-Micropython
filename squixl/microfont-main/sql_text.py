
import framebuf
import SQUiXL
from time import sleep

from microfont import MicroFont

RED = 0xf800
GREEN = 0x07e0
BLUE = 0x001f
YELLOW = GREEN + RED
PURPLE = RED + BLUE
WHITE = 0xffff
BLACK = 0

sans18B = MicroFont("Sans:B:18.mfnt",cache_index=True)
sans24 = MicroFont("Sans:R:24.mfnt",cache_index=True)
sans24B = MicroFont("Sans:B:24.mfnt",cache_index=True)
sans24I = MicroFont("Sans:I:24.mfnt",cache_index=True)
sans32I = MicroFont("Sans:I:32.mfnt",cache_index=True)
sans64B = MicroFont("Sans:B:64.mfnt",cache_index=True)
serif24 = MicroFont("LBask:R:24.mfnt",cache_index=True)
serif32B = MicroFont("LBask:B:32.mfnt",cache_index=True)
serif64I = MicroFont("LBask:I:64.mfnt",cache_index=True)

class SQUiXL_Text():
	def __init__(self):
		buf = SQUiXL.create_display()
		SQUiXL.screen_init_spi_bitbanged()
		self.fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)
		
		self.bgrnd = 0x000b
		self.fill(self.bgrnd)
		self.font = serif24
	
	def fill(self,colour):
		self.fb.fill(colour)

	def write(self,text,x,y,colour,*,rotation=0,font=None,):
		if font is None:
			font = self.font
		font.write(text,self.fb,framebuf.RGB565, 480, 480, x, y, colour,rot=rotation)
		
with SQUiXL as SQUiXL:
	scr = SQUiXL_Text()
		
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)

	scr.font = sans24I
	scr.write("Testing 1 2 3", 100, 200, GREEN,rotation=45)


	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)

	scr.write("Tiddley Pom",100, 360, WHITE)

	scr.font = serif32B
	i = 1
	while True:
		scr.write(str(i),10, 10, YELLOW)
		sleep(1)
		scr.write(str(i), 10, 10, scr.bgrnd)
		i += 1
