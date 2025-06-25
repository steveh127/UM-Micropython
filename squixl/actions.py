import asyncio
from squixl_text import screen as scr
from fonts import *

async def actions(widget):
	if widget.name == 'b1':
		if widget.blue:
			scr.write("Going, going, gone...",10, 350, BLUE,rotation=-90,font=serif32B)
			widget.blue = False
		else:
			scr.write("Going, going, gone...",10, 350, GREEN,rotation=-90,font=serif32B)
			widget.blue = True
		await asyncio.sleep(0.5)
		return
	if widget.name == 'test':
		value = widget.value
		if widget.on:
			scr.write("Testing 1 2 3 " + str(value),100, 200, GREEN,rotation=45)
			widget.value += 1
		else:
			scr.write("Testing 1 2 3 "  + str(value - 1), 100, 200, scr.background,rotation=45)
		await asyncio.sleep(0.5)
		return
	if widget.name in ('red','blue','green'):
		if widget.on:
			print(widget.name + ' ON')
		else:
			print(widget.name + ' OFF')
		return
	if widget.name in ('cat','mouse','dog'):
		print(widget.name)
		return				
	else:
		await asyncio.sleep(0.2)
		

		

	
	
