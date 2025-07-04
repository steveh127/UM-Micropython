import asyncio

from squixl_screen import screen as scr
from squixl_time import SQ_Time
from sq_controls import Button,Select_Button,Radio_Button,Radio_Buttons,Menu
from fonts import *

async def corner():
	print('Corner touched')
	await asyncio.sleep(0.3)

async def display():
	scr.font = sans24I	
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	
	b1 = Button('b1',"PRESS ME",170, 380,BLUE,font=sans32B)
	b1.blue = True
	
	sb = Select_Button('test',"TEST",100, 50,10,GREEN,clicked=BLUE,font=sans32I)
	sb.value = 1
	
	ex = Select_Button('close',"Clear Screen",15, 430,10,RED,clicked=RED,font=sans18I)
	
	r1 = Radio_Button('red',"Red SQUiXL",30, 200,10,RED,clicked=RED,font=serif32I)
	r2 = Radio_Button('blue',"Blue SQUiXL",30, 250,10,BLUE,clicked=BLUE,font=serif32I)
	r3 = Radio_Button('green',"Green SQUiXL",30, 300,10,GREEN,clicked=GREEN,font=serif32I)
	
	rbut = Radio_Buttons((r1,r2,r3)) 
	#rbut = Radio_Buttons((r1,r2,r3),default=2) # default is index to button list
	
	clock = SQ_Time(180,10,GREEN,font=sans32)
	
	menu = Menu('Test',[('cat','Cat'),('mouse','Mouse'),('dog','Dog')],230,200,GREEN,font=sans32,clicked=RED)
	
	scr.add_target((0,0,40,40),corner)
	
	i = 1
	scr.font = serif32B
	scr.write_over(' ' + str(0) + ' ',10, 10, YELLOW,background=RED)
	while True:
		if i % 10 == 0:
			scr.write_over(' ' + str(i//10) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(display())
