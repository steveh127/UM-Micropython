import asyncio
import framebuf

import SQUiXL
from fonts import sans32, DARK_BLUE,WHITE

#class to handle screen touches
class SQ_Touch():	
	def __init__(self):	
		self.touch = SQUiXL.touch
		self.point = -1,-1
		asyncio.create_task(self.check())
		self.target=((0,0,0,0),print)
		
	def __call__(self,rectangle,action):
		x,y,width,height = rectangle
		box = x,x+width,y,y+height
		self.target = box,action
	
	async def check(self):
		last_y = last_x = -1
		while True:
			points = self.touch.read_points()[1]
			if (last_y != points[0][0]) and (last_x != points[0][1]):
				point = points[0][1],points[0][0]
				await self.check_target(point)
				last_x = points[0][1]
				last_y = points[0][0]
			await asyncio.sleep(0.3)
	
	async def check_target(self,point):
		x,y = point
		x_min,x_max,y_min,y_max = self.target[0]
		if (x > x_min) and (x < x_max) and (y > y_min) and (y < y_max):
			await self.target[1]()

'''
Only access one copy of this class using import screen
'''
class _SQUiXL_Text():
	def __init__(self,font):
		#setup SQUiXL screen
		buf = SQUiXL.create_display()
		SQUiXL.screen_init_spi_bitbanged()
		self.fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)
		self.background = DARK_BLUE
		self.fill(self.background)
		self.font = font
		self.add_target = SQ_Touch()
		self.buzz = SQUiXL.drv.play
		#increase length of buzz from default
		SQUiXL.drv.sequence[0] = SQUiXL.Effect(14)
		self.buzz()
		self.deinit = SQUiXL.screen_deinit
	
	def fill(self,colour):
		self.fb.fill(colour)
	
	def rect(self,x,y,width,height,colour=WHITE,fill=False):
		self.fb.rect(x,y,width,height,colour,fill)
	
	def circle(self,x,y,radius,colour=WHITE,fill=False):
		self.fb.ellipse(x,y,radius,radius,colour,fill)
	
	def wrap(self,text,font,width):
		if self.get_size(text,font)[0] < width:
			return text
		else:
			wtext = ''
			wtl = 0
			text_words = text.split(' ')
			line = 1
			for word in text_words:
				wl = self.get_size(word,font)[0]
				if len(wtext) > 0:
					wtl = self.get_size(wtext,font)[0]
				if (wtl + wl) > (line * width - 10):
					wtext += '\n' + word + ' '
					line += 1
				else:
					wtext += word + ' '
		return wtext				
		
	def write(self,text,x,y,colour,*,rotation=0,font=None,width=460):
		if font is None:
			font = self.font
		text = self.wrap(text,font,width)
		font.write(text,self.fb,framebuf.RGB565, 480, 480, x, y, colour,rot=rotation)	
	
	def write_over(self,text,x,y,colour,*,rotation=0,font=None,background=None,width=460):
		if background is None:
			back = self.background
		else:
			back = background
		if font is None:
			font = self.font
		#any value for back 0 or greater will fill in character background with that colour.
		font.back = back
		text = self.wrap(text,font,width)
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
			
#create instance - import this to use screen
screen = _SQUiXL_Text(sans32)

