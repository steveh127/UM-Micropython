import asyncio

from squixl_touch import add_target
from squixl_text import screen

class Widget():
	def __init__(self,text,x,y,colour,*,font,clicked,action,value=None):
		self.add_target = add_target
		self.value = value
		self.text = text
		self.action = action
		self.colour = colour
		self.clicked = clicked
		self.font = font
		self.x = x
		self.y = y
		self.scr = screen
		
	async def do_action(self):
		await asyncio.sleep(0.5)

class Button(Widget):
	def __init__(self,text,x,y,colour,*,font,clicked,action,value=None):
		Widget.__init__(self,text,x,y,colour,font=font,clicked=clicked,action=action,value=value)
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

class Select_Button(Widget):
	def __init__(self,text,x,y,radius,colour,*,font,clicked,action,off_action,value=None):
		Widget.__init__(self,text,x,y,colour,font=font,clicked=clicked,action=action,value=value)
		_,self.radius = self.scr.get_size(text,font)
		self.radius  = int(self.radius / 2)
		self.scr.circle(x + self.radius ,y  + self.radius,self.radius,colour=colour)
		self.scr.circle(x + self.radius ,y  + self.radius,self.radius - 6,colour=clicked,fill=True)
		self.scr.write(text,x + self.radius * 2 + 7 ,y,colour,font=self.font)
		self.colour = colour
		self.clicked = clicked
		self.add_target((self.x,self.y,self.x + self.radius * 2,y + self.radius * 2),self.do_action)
		self.on = False
		self.off_action = off_action
	
	async def do_action(self):
		self.on = not self.on
		if self.on:
			self.scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius,colour=self.clicked)
			self.scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 6,colour=self.colour,fill=True)
			self.scr.buzz()
			await self.action()
		if not self.on:
			self.scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius,colour=self.colour)
			self.scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 6,colour=self.clicked,fill=True)
			await self.off_action()
			self.scr.buzz()
			
		await asyncio.sleep(0.5)
