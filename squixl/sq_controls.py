import asyncio

from squixl_touch import add_target
from squixl_text import screen as scr
from actions import actions

class Widget():
	def __init__(self,name,text,x,y,colour,*,font,clicked,values=None):
		self.add_target = add_target
		self.name = name
		if values is None:
			self.values = []
		else:
			self.values = list(values)
		self.text = text
		self.colour = colour
		self.clicked = clicked
		self.font = font
		self.x = x
		self.y = y

class Button(Widget):
	def __init__(self,name,text,x,y,colour,*,font,clicked,values=None):
		Widget.__init__(self,name,text,x,y,colour,font=font,clicked=clicked,values=values)
		self.w,self.h = scr.get_size(text,font)
		self.b=int(self.h//4)
		scr.rect(self.x - self.b,self.y-self.b,self.w + (2 * self.b) + 2,self.h + (2 * self.b))
		scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)
		self.add_target((self.x,self.y,self.w,self.h),self.do_action)
	
	async def do_action(self):
		scr.write_over(self.text,self.x,self.y,self.clicked,font=self.font,background=self.colour)
		scr.buzz()
		await actions(self)
		await asyncio.sleep(0.5)
		scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)

class Select_Button(Widget):
	def __init__(self,name,text,x,y,radius,colour,*,font,clicked,values=None):
		Widget.__init__(self,name,text,x,y,colour,font=font,clicked=clicked,values=values)
		_,self.radius = scr.get_size(text,font)
		self.radius  = int(self.radius / 2)
		scr.circle(x + self.radius ,y  + self.radius,self.radius,colour=colour)
		scr.circle(x + self.radius ,y  + self.radius,self.radius - 6,colour=clicked,fill=True)
		scr.write(text,x + self.radius * 2 + 7 ,y,colour,font=self.font)
		self.colour = colour
		self.clicked = clicked
		self.add_target((self.x,self.y,self.x + self.radius * 2,y + self.radius * 2),self.do_action)
		self.on = False
	
	async def do_action(self):
		self.on = not self.on
		if self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius,colour=self.clicked)
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 6,colour=self.colour,fill=True)
		if not self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius,colour=self.colour)
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 6,colour=self.clicked,fill=True)
		await actions(self)
		scr.buzz()	
		await asyncio.sleep(0.5)
