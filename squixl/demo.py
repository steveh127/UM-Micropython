import asyncio

from squixl_text import screen as scr
from squixl_time import SQ_Time
from squixl_touch import add_target
from sq_controls import Button,Select_Button
from fonts import *

async def print_hit():
	#scr = get_screen()
	scr.buzz()
	print('Touched')
	await asyncio.sleep(0.5)
	
async def print_h2():
	#scr = get_screen()
	scr.buzz()
	print('Corner Touched')
	await asyncio.sleep(0.5)
	
async def pressed():
	#scr = get_screen()
	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)
	await asyncio.sleep(0.5)
	
async def test():
	#scr = get_screen()
	scr.write("Testing 1 2 3", 200, 200, GREEN,rotation=45)
	await asyncio.sleep(0.5)

async def no_test():
	#scr = get_screen()
	scr.write("Testing 1 2 3", 200, 200, scr.background,rotation=45)
	await asyncio.sleep(0.5)	
	
async def main():
	#scr = get_screen()
	#add_target = get_add_target()
	
	scr.font = sans24I	
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	
	b1 = Button("Micropython is now running SQUiXL",80, 400,WHITE,clicked=RED,font=sans24I,action=pressed)
	rb = Select_Button("TEST",200, 50,10,WHITE,clicked=GREEN,font=sans32B,action=test,off_action=no_test )
	
	clock = SQ_Time(350,10,GREEN,font=sans32)
	i = 1
	
	scr.font = serif32B
	add_target((100,100,100,100),print_hit)
	add_target((0,0,100,100),print_h2)

	scr.write_over(' ' + str(0) + ' ',10, 10, YELLOW,background=RED)
	while True:

		if i % 10 == 0:
			scr.write_over(' ' + str(i//10) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(main())
