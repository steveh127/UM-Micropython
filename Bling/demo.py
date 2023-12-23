import asyncio
from machine import Pin

from bling import Bling_Display,Button

d=Bling_Display()

async def b0():
	await d.display('{ArrowL}',scroll=True,justify='R')
	
async def b1():
	await d.display('Button {RED}11',colour=d.GREEN(3),justify=('L'))
	
async def b2():
	await d.display('{RED}1{GREEN}23{BLUE}45{RED}61',brightness=3)
	
async def b3():
	d.set_background(d.BLUE(1))

async def main():
	#d.background=(d.BLUE(1))
	buttons=(Button(11,b0),Button(10,b1),Button(33,b2),Button(34,b3))
	asyncio.create_task(d.show_text())
	asyncio.create_task(d.scroll_text())
	for button in buttons:
		asyncio.create_task(button())
	await d.display('{RED}Testing {BLUE}1 2 3 {GREEN}4 5 6 ',brightness=3)
	while True:
		await asyncio.sleep(5)
	
asyncio.run(main())
	

			
