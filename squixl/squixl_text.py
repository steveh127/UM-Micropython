import framebuf

import SQUiXL
from fonts import sans32, DARK_BLUE,WHITE

#only access one copy of this class
#using get_screen()
class _SQUiXL_Text():
	def __init__(self,font):
		#setup SQUiXL screen
		buf = SQUiXL.create_display()
		SQUiXL.screen_init_spi_bitbanged()
		self.fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)
		self.background = DARK_BLUE
		self.fill(self.background)
		self.font = font
		self.click = SQUiXL.drv.play
		self.click()
	
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
	
	def get_size(self,text,font=None):
		if font is None:
			font = self.font
		_,height,_ = font.get_ch(text[0])
		width = 0
		for ch in text:
			_,h,w = font.get_ch(ch)
			if h > height:
				height = h
			width += w
		width += 2	
		return width,height
			

#use this to get a copy of active screen created on imported
#SQUiXL_Text must be a singleton
def active_screen():
	screen = _SQUiXL_Text(sans32)
	def get():
		nonlocal screen
		return screen	
	return get
	
get_screen = active_screen()
