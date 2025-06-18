import asyncio

from squixl_text import get_screen
from squixl_time import SQ_Time
from squixl_touch import SQ_Touch
from fonts import *

def print_hit():
	print('Touched')

def print_h2():
	print('Corner Touched')

def pressed():
	print('Pressed')

def test():
	print('Test')

def button(text,x,y,colour,*,font,action=None):
	scr = get_screen()	
	w,h = scr.get_size(text,font)
	b=int(h//6)
	scr.rect(x-b,y-b,w + (2 * b) + 2,h + (2 * b))
	scr.write_over(text,x,y,colour,font=font)
	SQ_Touch().add_target((x,y,w,h),action)


async def main():
	scr = get_screen()
	scr.font = sans24I
	
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	scr.write("Testing 1 2 3", 200, 200, GREEN,rotation=45)
	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)
	
	button("Micropython is now running SQUiXL",80, 400,WHITE,font=sans24I,action=pressed)
	button("TEST",200, 20,RED,font=sans24B,action=test)
	
	clock = SQ_Time(350,10,GREEN,font=sans32)
	i = 1
	
	scr.font = serif32B
	t = SQ_Touch()
	t.add_target((100,100,100,100),print_hit)
	t.add_target((0,0,100,100),print_h2)

	scr.write_over(' ' + str(0) + ' ',10, 10, YELLOW,background=RED)
	while True:
		if t.touched:
			t.touched = False
			print(t.point)
		if i % 10 == 0:
			scr.write_over(' ' + str(i//10) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(main())
