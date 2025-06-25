import asyncio

from squixl_text import screen as scr
from squixl_time import SQ_Time
from squixl_touch import add_target
from sq_controls import Button,Select_Button,Radio_Button,Radio_Buttons,Menu
from fonts import *

async def print_hit():
	scr.buzz()
	print('Touched')
	await asyncio.sleep(0.5)
	
async def print_h2():
	scr.buzz()
	print('Corner Touched')
	await asyncio.sleep(0.5)
	
async def main():
	
	scr.font = sans24I	
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	
	b1 = Button('b1',"Micropython is now running SQUiXL",80, 400,BLUE,font=sans24I)
	b1.blue = True
	
	sb = Select_Button('test',"TEST",200, 50,10,GREEN,clicked=BLUE,font=sans32I)
	sb.value = 1
	
	r1 = Radio_Button('red',"Red",200, 200,10,RED,clicked=RED,font=serif32I)
	r2 = Radio_Button('blue',"Blue",200, 250,10,BLUE,clicked=BLUE,font=serif32I)
	r3 = Radio_Button('green',"Green",200, 300,10,GREEN,clicked=GREEN,font=serif32I)
	
	rbut = Radio_Buttons((r1,r2,r3)) 
	#rbut = Radio_Buttons((r1,r2,r3),default=2) # default is index to button list
	
	clock = SQ_Time(350,10,GREEN,font=sans32)
	
	menu=Menu('Test',[],100,100,GREEN,font=sans32,clicked=RED)
	
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
