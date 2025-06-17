import asyncio

from squixl_text import *
from squixl_time import SQ_Time
from squixl_touch import SQ_Touch

def print_hit():
	print('Touched')

def print_h2():
	print('Corner Touched')

def print_b():
	scr = get_screen()
	print('Button')
	scr.write('Button',200,10,RED)

async def main():
	scr = get_screen()
	scr.font = sans24I
		
	scr.write("SQUiXL !",100,100, PURPLE,font=serif64I)
	scr.write("Testing 1 2 3", 200, 200, GREEN,rotation=45)
	scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)
	scr.write("Micropython is now running SQUiXL",80, 400, WHITE)

	clock = SQ_Time(350,10,GREEN,font=sans32)
	i = 1
	
	scr.font = serif32B
	t = SQ_Touch()
	t.add_target((100,100,100,100),print_hit)
	t.add_target((0,0,100,100),print_h2)
	scr.rect(200,10,100,30)
	t.add_target((200,10,100,30),print_b)
	
	while True:
		if t.touched:
			t.touched = False
			print(t.point)
		if i % 10 == 0:
			scr.write_over(' ' + str(i) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(1)
		i += 1
	
asyncio.run(main())
