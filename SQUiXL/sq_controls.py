import asyncio

from squixl_screen import screen as scr,SQ_Touch
from actions import actions

class Widget():
	def __init__(self,name,text,x,y,colour,*,font,clicked):
		self.add_target = SQ_Touch()
		self.name = name
		self.text = text
		self.colour = colour
		self.clicked = clicked
		self.font = font
		self.x = x
		self.y = y

class Button(Widget):
	def __init__(self,name,text,x,y,colour,*,font,background=None):
		if background is None:
			clicked = scr.background
		else:
			clicked = background
		Widget.__init__(self,name,text,x,y,colour,font=font,clicked=clicked)
		self.w,self.h = scr.get_size(text,font)
		self.b=int(self.h//4)
		scr.rect(self.x - self.b,self.y-self.b,self.w + (2 * self.b) + 2,self.h + (2 * self.b))
		scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)
		self.add_target((self.x,self.y,self.w,self.h),self.do_action)
	
	async def do_action(self):
		scr.buzz()
		scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.colour)
		await actions(self)
		await asyncio.sleep(0.5)
		scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)

class Select_Button(Widget):
	def __init__(self,name,text,x,y,radius,colour,*,font,clicked):
		super().__init__(name,text,x,y,colour,font=font,clicked=clicked)
		_,self.radius = scr.get_size(text,font)
		self.radius  = int(self.radius / 2)
		scr.circle(x + self.radius ,y  + self.radius,self.radius,colour=colour)
		scr.circle(x + self.radius ,y  + self.radius,self.radius - 2,colour=scr.background,fill=True)
		scr.write(text,x + self.radius * 2 + 7 ,y,colour,font=self.font)
		self.add_target((self.x,self.y,self.radius * 2,self.radius * 2),self.do_action)
		self.on = False
	
	async def do_action(self):		
		scr.buzz()	
		self.on = not self.on
		if not self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 2,colour=scr.background,fill=True)
		if self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 2,colour=self.clicked,fill=True)
		await actions(self)
		await asyncio.sleep(0.5)

class Radio_Button(Widget):
	def __init__(self,name,text,x,y,radius,colour,*,font,clicked):
		super().__init__(name,text,x,y,colour,font=font,clicked=clicked)
		_,self.radius = scr.get_size(text,font)
		self.radius  = int(self.radius / 2)
		scr.circle(x + self.radius ,y  + self.radius,self.radius,colour=colour)
		scr.circle(x + self.radius ,y  + self.radius,self.radius - 2,colour=scr.background,fill=True)
		scr.write(text,x + self.radius * 2 + 7 ,y,colour,font=self.font)
		self.add_target((self.x,self.y,self.radius * 2,self.radius * 2),self.do_action)
		self.on = False
	
	async def do_action(self):
		scr.buzz()
		self.on = not self.on
		if not self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius - 2,colour=scr.background,fill=True)
		if self.on:
			scr.circle(self.x + self.radius ,self.y  + self.radius,self.radius,colour=self.colour)
		await asyncio.sleep(0.5)

class Radio_Buttons():
	def __init__(self,radio_buttons,*,default=None):
		self.buttons = radio_buttons
		if default is None:
			self.picked = -1
			for button in self.buttons:
				button.on = False
				scr.circle(button.x + button.radius ,button.y  + button.radius,button.radius,colour=button.colour)
				scr.circle(button.x + button.radius ,button.y  + button.radius,button.radius - 2,colour=scr.background,fill=True)
		else:
			self.picked = default
		asyncio.create_task(self.check_buttons())
			
	async def update_buttons(self):		
		for i in range(len(self.buttons)):
			if i == self.picked:
				scr.circle(self.buttons[i].x + self.buttons[i].radius ,self.buttons[i].y  + self.buttons[i].radius,self.buttons[i].radius - 2,colour=self.buttons[i].clicked,fill=True)
				self.buttons[i].on = True
				await actions(self.buttons[i])
			else:	
				scr.circle(self.buttons[i].x + self.buttons[i].radius ,self.buttons[i].y  + self.buttons[i].radius,self.buttons[i].radius - 2,colour=scr.background,fill=True)
				self.buttons[i].on = False
				await actions(self.buttons[i])
				
	async def check_buttons(self):
		while True:
			for i in range(len(self.buttons)):
				if self.buttons[i].on and i != self.picked:
					self.picked = i
					await self.update_buttons()
				if not self.buttons[i].on and i == self.picked:
					await self.update_buttons()
			await asyncio.sleep(0.3)

class _Menu_Choice(Widget):
	def __init__(self,name,option,n,x,y,colour,*,font,clicked):
		super().__init__(name,'',x,y,colour,font=font,clicked=clicked)
		self.option = option
		self.width,self.height = scr.get_size(option,self.font)
		self.radius  = int(self.height / 2)
		self.Y = (self.y + (n * (self.height + 2))) 
		scr.circle(self.x + self.radius ,self.Y + self.radius,int(self.radius/2),self.colour,fill=True)
		scr.write_over(option,self.x + self.height + 4,self.Y,self.colour,font=self.font)
		self.add_target((self.x,self.Y,self.height + 4 + self.width,self.height),self.do_action)
		
	async def do_action(self):
		scr.buzz()
		scr.circle(self.x + self.radius ,self.Y + self.radius,int(self.radius/2),self.clicked,fill=True)
		scr.write_over(self.option,self.x + self.height + 4,self.Y,self.clicked,font=self.font)
		await actions(self)
		scr.circle(self.x + self.radius ,self.Y + self.radius,int(self.radius/2),self.colour,fill=True)
		scr.write_over(self.option,self.x + self.height + 4,self.Y,self.colour,font=self.font)
		await asyncio.sleep(0.5)

class Menu(Widget):
	def __init__(self,name,options,x,y,colour,*,font,clicked):
		super().__init__(name,'',x,y,colour,font=font,clicked=clicked)
		n = 0
		for option in options:
			_Menu_Choice(option[0],option[1],n,x,y,colour,font=font,clicked=clicked)
			n += 1					


