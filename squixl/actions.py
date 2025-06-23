import asyncio
from squixl_text import screen as scr
from fonts import *

async def actions(widget):
	if widget.name == 'b1':
		scr.write("Going, going, gone...",100, 300, BLUE,rotation=-30,font=serif32B)
		await asyncio.sleep(0.5)
	if widget.name == 'rb':
		value = widget.values[0]
		if widget.on:
			scr.write("Testing 1 2 3 " + str(value), 200, 200, GREEN,rotation=45)
			widget.values[0] += 1
		else:
			scr.write("Testing 1 2 3 "  + str(value - 1), 200, 200, scr.background,rotation=45)
		await asyncio.sleep(0.5)

	
	
