import asyncio

from squixl_touch import get_add_target
from squixl_text import get_screen

class Button():
	def __init__(self,text,x,y,colour,*,font,clicked,action,value=None):
		self.add_target = get_add_target()
		self.value = value
		self.text = text
		self.action = action
		self.colour = colour
		self.clicked = clicked
		self.font = font
		self.x = x
		self.y = y
		self.scr = get_screen()	
		self.w,self.h = self.scr.get_size(text,font)
		self.b=int(self.h//4)
		self.scr.rect(self.x - self.b,self.y-self.b,self.w + (2 * self.b) + 2,self.h + (2 * self.b))
		self.scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)
		self.add_target((self.x,self.y,self.w,self.h),self.do_action)
	
	async def do_action(self):
		self.scr.write_over(self.text,self.x,self.y,self.clicked,font=self.font,background=self.colour)
		self.scr.buzz()
		await self.action()
		await asyncio.sleep(0.5)
		self.scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)
