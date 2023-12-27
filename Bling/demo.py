import asyncio
from machine import Pin

from bling import Bling_Display,Bling_Buttons

display=Bling_Display()

async def b0():
	#await display.display('{ArrowL}',scroll=True,justify='R')
	await display.clear()
	#display.row(3,colour=(display.BLUE()))
	
async def b1():
	await display.show('Button {RED}11',colour=display.GREEN(3),justify=('L'))
	
async def b2():
	display.gap=0
	await display.show('{RED}1{GREEN}23{BLUE}45{WHITE}678{RED}90{YELLOW}1{GREEN}23{PURPLE}45',brightness=3)
	display.gap=1
	
async def b3():
	if display.background == display.BLACK(1):
		display.set_background(display.BLUE(1))
	else:
		display.set_background(display.BLACK(1))
	await asyncio.sleep(0.3)

async def main():
	buttons=Bling_Buttons([b0,b1,b2,b3])
	asyncio.create_task(display.show_text())
	asyncio.create_task(display.scroll_text())
	asyncio.create_task(buttons.check())
	await display.show('{RED}Testing {BLUE}1 2 3 {GREEN}4 5 6 ',brightness=3)
	while True:
		await asyncio.sleep(5)
	
asyncio.run(main())
	

			
