import asyncio
from machine import Pin

from bling import Bling_Display

class Button():
	def __init__(self,pin,action):
		self.pin=Pin(pin,Pin.IN)
		self.action=action
	
	async def __call__(self,*args):
		while True:
			if self.pin.value():
				await self.action(*args)
				await asyncio.sleep(0.3)
			await asyncio.sleep(0)

d=Bling_Display()

async def b0():
	d.background=d.BLUE(1)
	await d.display('Button 0')
	
async def b1():
	print(d.text)
	await d.display('Button 1',colour=d.GREEN())
	
async def b2():
	d.background=d.GREEN(1)
	await d.display('Button 2',colour=d.RED(1))
	
async def b3():
	d.background=d.BLACK(1)
	await d.display('{ArrowR}Button 3',colour=d.BLUE(1))	

async def main():
	#d.background=(d.BLUE(1))
	buttons=(Button(11,b0),Button(10,b1),Button(33,b2),Button(34,b3))
	asyncio.create_task(d.show_text())
	asyncio.create_task(d.scroll_text())
	for button in buttons:
		asyncio.create_task(button())
	await d.display('Testing 1 3 5  6',colour=d.RED(1))
	while True:
		await asyncio.sleep(5)
		#await d.display('TESTED',colour=d.RED(1))
	# d.colour=d.RED()
	# d.text='123456'
	# await asyncio.sleep(5)
	# d.text='ABCDEFGHIJK'
	# await asyncio.sleep(3)
	# d.power.off()
	# await asyncio.sleep(3)
	# d.power.on()
	# await d.display_text('{box}Testing',colour=d.PURPLE(1),scroll=True)
	# await asyncio.sleep(10)
	# d.power.off()
	
asyncio.run(main())
	

