import asyncio

from squixl_text import *
from squixl_time import SQ_Time

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
	while True:
		scr.write_over(' ' + str(i) + ' ',10, 10, YELLOW,background=RED)
		await asyncio.sleep(10)
		i += 1

asyncio.run(main())
