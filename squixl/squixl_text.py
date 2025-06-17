import framebuf

import SQUiXL
from mycrofont import MicroFont

#A range of serif and sans-serif fonts. 

sans18 = MicroFont("Sans:R:18.mfnt",cache_index=True)
sans18B = MicroFont("Sans:B:18.mfnt",cache_index=True)
sans18I = MicroFont("Sans:I:18.mfnt",cache_index=True)

sans24 = MicroFont("Sans:R:24.mfnt",cache_index=True)
sans24B = MicroFont("Sans:B:24.mfnt",cache_index=True)
sans24I = MicroFont("Sans:I:24.mfnt",cache_index=True)

sans32 = MicroFont("Sans:R:32.mfnt",cache_index=True)
sans32B = MicroFont("Sans:B:32.mfnt",cache_index=True)
sans32I = MicroFont("Sans:I:32.mfnt",cache_index=True)

sans64 = MicroFont("Sans:R:64.mfnt",cache_index=True)
sans64B = MicroFont("Sans:B:64.mfnt",cache_index=True)
sans64I = MicroFont("Sans:I:64.mfnt",cache_index=True)

serif18 = MicroFont("LBask:R:18.mfnt",cache_index=True)
serif18B = MicroFont("LBask:B:18.mfnt",cache_index=True)
serif18I = MicroFont("LBask:I:18.mfnt",cache_index=True)

serif24 = MicroFont("LBask:R:24.mfnt",cache_index=True)
serif24B = MicroFont("LBask:B:24.mfnt",cache_index=True)
serif24I = MicroFont("LBask:I:24.mfnt",cache_index=True)

serif32 = MicroFont("LBask:R:32.mfnt",cache_index=True)
serif32B = MicroFont("LBask:B:32.mfnt",cache_index=True)
serif32I = MicroFont("LBask:I:24.mfnt",cache_index=True)

serif64 = MicroFont("LBask:R:64.mfnt",cache_index=True)
serif64B = MicroFont("LBask:B:64.mfnt",cache_index=True)
serif64I = MicroFont("LBask:I:64.mfnt",cache_index=True)


RED = 0xf800
GREEN = 0x07e0
BLUE = 0x001f
DARK_BLUE = 0x000b
YELLOW = GREEN + RED
PURPLE = RED + BLUE
WHITE = 0xffff
BLACK = 0

class SQUiXL_Text():
	def __init__(self,font):
		#setup SQUiXL screen
		buf = SQUiXL.create_display()
		SQUiXL.screen_init_spi_bitbanged()
		self.fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)
		self.background = DARK_BLUE
		self.fill(self.background)
		self.font = font
	
	def fill(self,colour):
		self.fb.fill(colour)
	
	def rect(self,x,y,width,height,colour=WHITE,fill=False):
		self.fb.rect(x,y,width,height,colour,fill)

	def write(self,text,x,y,colour,*,rotation=0,font=None,):
		if font is None:
			font = self.font
		font.write(text,self.fb,framebuf.RGB565, 480, 480, x, y, colour,rot=rotation)
	
	def write_over(self,text,x,y,colour,*,rotation=0,font=None,background = None):
		if background is None:
			back = self.background
		else:
			back = background
		if font is None:
			font = self.font
		font.back = back
		font.write(text,self.fb,framebuf.RGB565, 480, 480, x, y, colour,rot=rotation)
		font.back = -1

#use this to get a copy of active screen created on imported
#SQUiXL_Text must be a singleton
def active_screen():
	screen=SQUiXL_Text(sans32)
	def get():
		nonlocal screen
		return screen	
	return get
	
get_screen = active_screen()
