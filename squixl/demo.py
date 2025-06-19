import asyncio

from squixl_text import get_screen
from squixl_time import SQ_Time
from squixl_touch import SQ_Touch
from fonts import *

async def print_hit():
	print('Touched')
	await asyncio.sleep(0.5)
	
async def print_h2():
	print('Corner Touched')
	await asyncio.sleep(0.5)
	
async def pressed():
	print('Pressed')
	await asyncio.sleep(0.5)
	
async def test():
	print('Test')
	await asyncio.sleep(0.5)
	
class button():
	def __init__(self,text,x,y,colour,*,font,clicked,action=None):
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
		SQ_Touch().add_target((self.x,self.y,self.w,self.h),self.do_action)
	
	async def do_action(self):
		self.scr.write_over(self.text,self.x,self.y,self.clicked,font=self.font,background=self.colour)
		await self.action()
		await asyncio.sleep(0.5)
		self.scr.write_over(self.text,self.x,self.y,self.colour,font=self.font,background=self.clicked)
	
async def main():
	scr = get_screen()
	scr.font = sans24I
	
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	scr.write("Testing 1 2 3", 200, 200, GREEN,rotation=45)
	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)
	
	button("Micropython is now running SQUiXL",80, 400,WHITE,clicked=RED,font=sans24I,action=pressed)
	button("TEST",200, 20,RED,clicked=GREEN,font=sans24B,action=test)
	
	clock = SQ_Time(350,10,GREEN,font=sans32)
	i = 1
	
	scr.font = serif32B
	t = SQ_Touch()
	t.add_target((100,100,100,100),print_hit)
	t.add_target((0,0,100,100),print_h2)

	scr.write_over(' ' + str(0) + ' ',10, 10, YELLOW,background=RED)
	while True:
		# if t.touched:
			# t.touched = False
			# print(t.point)
		if i % 10 == 0:
			scr.write_over(' ' + str(i//10) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(main())
