import asyncio
from time import sleep


from squixl_text import screen as scr
from fonts import *

from joke import Get_Joke
joke = Get_Joke()

async def actions(widget):
	if widget.name == 'b1':
		setup,punchline = await joke()
		scr.rect(370,0,100,480,scr.background,True)
		scr.write(setup,380, 460, BLUE,rotation=-90,font=serif24B)
		scr.write(punchline,430, 460, GREEN,rotation=-90,font=serif24B)
		await asyncio.sleep(0.5)
		return
	if widget.name == 'test':
		value = widget.value
		if widget.on:
			scr.write("Testing " + str(value),300, 70, YELLOW,rotation=-30)
			widget.value += 1
		else:
			scr.write("Testing "  + str(value - 1), 300, 70, scr.background,rotation=-30)
		await asyncio.sleep(0.5)
		return
	if widget.name == 'close':
		scr.buzz()
		await asyncio.sleep(0.5)
		scr.deinit()
		return
	if widget.name in ('red','blue','green'):
		if widget.on:
			if widget.name == 'red':
				scr.write("SQUiXL !",100,100, RED,font=serif64I)
			if widget.name == 'blue':
				scr.write("SQUiXL !",100,100, BLUE,font=serif64I)
			if widget.name == 'green':
				scr.write("SQUiXL !",100,100, GREEN,font=serif64I)
		return
	if widget.name in ('cat','mouse','dog'):
		print(widget.name)
		await asyncio.sleep(5)
		return				
	else:
		await asyncio.sleep(0.2)
		
	
	

	
	
